"""
usage: from mappedpdk import MappedPDK
"""

from gdsfactory.pdk import Pdk
from gdsfactory.typings import Component, PathType, Layer
from pydantic import validator, StrictStr, ValidationError
from typing import ClassVar, Optional, Any, Union, Literal, Iterable, TypedDict
from pathlib import Path
from decimal import Decimal, ROUND_UP
import tempfile
import subprocess
from decimal import Decimal
from pydantic import validate_arguments
import xml.etree.ElementTree as ET

class MappedPDK(Pdk):
    """Inherits everything from the pdk class but also requires mapping to glayers
    glayers are generic layers which can be returned with get_glayer(name: str)
    has_required_glayers(list[str]) is used to verify all required generic layers are
    present"""

    valid_glayers: ClassVar[tuple[str]] = (
        "dnwell",
        "pwell",
        "nwell",
        "p+s/d",
        "n+s/d",
        "active_diff",
        "active_tap",
        "poly",
        "mcon",
        "met1",
        "via1",
        "met2",
        "via2",
        "met3",
        "via3",
        "met4",
        "via4",
        "met5",
        "capmet",
    )

    models: dict = {
        "nfet": "",
        "pfet": "",
        "mimcap": ""
    }

    glayers: dict[StrictStr, Union[StrictStr, tuple[int,int]]]
    # friendly way to implement a graph
    grules: dict[StrictStr, dict[StrictStr, Optional[dict[StrictStr, Any]]]]
    klayout_lydrc_file: Optional[Path] = None

    @validator("models")
    def models_check(cls, models_obj: dict[StrictStr, StrictStr]):
        for model in models_obj.keys():
            if not model in ["nfet","pfet","mimcap"]:
                raise ValueError(f"specify nfet, pfet, or mimcap models only")
        return models_obj

    @validator("glayers")
    def glayers_check_keys(cls, glayers_obj: dict[StrictStr, Union[StrictStr, tuple[int,int]]]):
        """force people to pick glayers from a finite set of string layers that you define
        checks glayers to ensure valid keys,type. Glayers must be passed as dict[str,str]
        if someone tries to pass a glayers dict that has a bad key, throw an error"""
        for glayer, mapped_layer in glayers_obj.items():
            if (not isinstance(glayer, str)) or (not isinstance(mapped_layer, Union[str, tuple])):
                raise TypeError("glayers should be passed as dict[str, Union[StrictStr, tuple[int,int]]]")
            if glayer not in cls.valid_glayers:
                raise ValueError(
                    "glayers keys must be one of generic layers listed in class variable valid_glayers"
                )
        return glayers_obj

    @validator("klayout_lydrc_file")
    def lydrc_file_exists(cls, lydrc_file_path):
        """Check that lydrc_file_path exists if not none"""
        if lydrc_file_path != None and not lydrc_file_path.is_file():
            raise ValueError(".lydrc script: the path given is not a file")
        return lydrc_file_path

    @validate_arguments
    def drc(
        self,
        layout: Component | PathType,
        output_dir_or_file: Optional[PathType] = None,
    ):
        """Returns true if the layout is DRC clean and false if not
        Also saves detailed results to output_dir_or_file location as lyrdb
        layout can be passed as a file path or gdsfactory component"""
        if not self.klayout_lydrc_file:
            raise NotImplementedError("no drc script for this pdk")
        # find layout gds file path
        tempdir = None
        if isinstance(layout, Component):
            tempdir = tempfile.TemporaryDirectory()
            layout_path = Path(layout.write_gds(gdsdir=tempdir.name)).resolve()
        elif isinstance(layout, PathType):
            layout_path = Path(layout).resolve()
        else:
            raise TypeError("layout should be a Component, Path, or string")
        if not layout_path.is_file():
            raise ValueError("layout must exist, the path given is not a file")
        # find report file path, if None then use current directory
        report_path = (
            Path(output_dir_or_file).resolve()
            if output_dir_or_file
            else Path.cwd().resolve()
        )
        if report_path.is_dir():
            report_path = Path(
                report_path
                / str(
                    self.name
                    + layout_path.name.replace(layout_path.suffix, "")
                    + "_drcreport.lyrdb"
                )
            )
        elif not report_path.is_file():
            raise ValueError("report_path must be file or dir")
        # run klayout drc
        drc_args = [
            "klayout",
            "-b",
            "-r",
            str(self.klayout_lydrc_file),
            "-rd",
            "input=" + str(layout_path),
            "-rd",
            "report=" + str(report_path),
        ]
        rtr_code = subprocess.Popen(drc_args).wait()
        if rtr_code:
            raise RuntimeError("error running klayout DRC")
        # clean up and return
        if tempdir:
            tempdir.cleanup()
        # there is a drc parsing open-source at:
        # https://github.com/google/globalfoundries-pdk-libs-gf180mcu_fd_pr/blob/main/rules/klayout/drc
        # eventually I can return more info on the drc run, but for now just void and view the lyrdb in klayout

        # Open DRC output XML file
        drc_tree = ET.parse(report_path.resolve())
        drc_root = drc_tree.getroot()
        if drc_root.tag != "report-database":
            raise TypeError("DRC report file is not a valid report-database")
        # Check if DRC passed
        drc_error_count = len(drc_root[7])
        return (drc_error_count == 0)

    @validate_arguments
    def has_required_glayers(self, layers_required: list[str]):
        """Raises ValueError if any of the generic layers in layers_required: list[str]
        are not mapped to anything in the pdk.glayers dictionary
        also checks that the values in the glayers dictionary map to real Pdk layers"""
        for layer in layers_required:
            if layer not in self.glayers:
                raise ValueError(
                    f"{layer!r} not in self.glayers {list(self.glayers.keys())}"
                )
            if isinstance(self.glayers[layer], str):
                self.validate_layers([self.glayers[layer]])
            elif not isinstance(self.glayers[layer], tuple):
                raise TypeError("glayer mapped value should be str or tuple[int,int]")


    @validate_arguments
    def layer_to_glayer(self, layer: tuple[int, int]) -> str:
        """if layer provided corresponds to a glayer, will return a glayer
        else will raise an exception
        takes layer as a tuple(int,int)"""
        # lambda for finding last matching key in dict from val
        find_last = lambda val, d: [x for x, y in d.items() if y == val].pop()
        if layer in self.glayers.values():
            return find_last(layer, self.glayers)
        elif self.layers is not None:
            # find glayer verfying presence along the way
            pdk_real_layers = self.layers.values()
            if layer in pdk_real_layers:
                layer_name = find_last(layer, self.layers)
                if layer_name in self.glayers.values():
                    glayer_name = find_last(layer_name, self.glayers)
                else:
                    raise ValueError("layer does not correspond to a glayer")
            else:
                raise ValueError("layer is not a layer present in the pdk")
            return glayer_name
        else:
            raise ValueError("layer might not be a layer present in the pdk")

    # TODO: implement LayerSpec type
    @validate_arguments
    def get_glayer(self, layer: str) -> Layer:
        """Returns the pdk layer from the generic layer name"""
        direct_mapping = self.glayers[layer]
        if isinstance(direct_mapping, tuple):
            return direct_mapping
        else:
            return self.get_layer(direct_mapping)

    @validate_arguments
    def get_grule(
        self, glayer1: str, glayer2: Optional[str] = None, return_decimal = False
    ) -> dict[StrictStr, Union[float,Decimal]]:
        """Returns a dictionary describing the relationship between two layers
        If one layer is specified, returns a dictionary with all intra layer rules"""
        if glayer1 not in MappedPDK.valid_glayers:
            raise ValueError("get_grule, " + str(glayer1) + " not valid glayer")
        # decide if two or one inputs and set rules_dict accordingly
        rules_dict = None
        if glayer2 is not None:
            if glayer2 not in MappedPDK.valid_glayers:
                raise ValueError("get_grule, " + str(glayer2) + " not valid glayer")
            rules_dict = self.grules.get(glayer1, dict()).get(glayer2)
            if rules_dict is None or rules_dict == {}:
                rules_dict = self.grules.get(glayer2, dict()).get(glayer1)
        else:
            glayer2 = glayer1
            rules_dict = self.grules.get(glayer1, dict()).get(glayer1)
        # error check, convert type, and return
        if rules_dict is None or rules_dict == {}:
            raise NotImplementedError(
                "no rules found between " + str(glayer1) + " and " + str(glayer2)
            )
        for rule in rules_dict:
            if type(rule) == float and return_decimal:
                rules_dict[rule] = Decimal(str(rule))
        return rules_dict

    @classmethod
    def is_routable_glayer(cls, glayer: StrictStr):
        return any(hint in glayer for hint in ["met", "active", "poly"])

    # TODO: implement
    @classmethod
    def from_gf_pdk(
        cls,
        gfpdk: Pdk,
        **kwargs
    ):
        """Construct a mapped pdk from an existing pdk and the extra parts of MappedPDK
        grid is the grid size in nm"""
        # input type and value validation
        if not isinstance(gfpdk, Pdk):
            raise TypeError("from_gf_pdk: gfpdk arg only accepts GDSFactory pdk type")
        # create argument dictionary
        passargs = dict()
        # pdk args
        passargs["name"]=gfpdk.name
        #passargs["cross_sections"]=gfpdk.cross_sections
        #passargs["cells"]=gfpdk.cells
        #passargs["symbols"]=gfpdk.symbols
        #passargs["default_symbol_factory"]=gfpdk.default_symbol_factory
        #passargs["containers"]=gfpdk.containers
        #passargs["base_pdk"]=gfpdk.base_pdk
        #passargs["default_decorator"]=gfpdk.default_decorator
        passargs["layers"]=gfpdk.layers
        #passargs["layer_stack"]=gfpdk.layer_stack
        #passargs["layer_views"]=gfpdk.layer_views#??? layer view broken???
#        passargs["layer_transitions"]=gfpdk.layer_transitions
#        passargs["sparameters_path"]=gfpdk.sparameters_path
#        passargs["modes_path"]=gfpdk.modes_path
#        passargs["interconnect_cml_path"]=gfpdk.interconnect_cml_path
#        passargs["warn_off_grid_ports"]=gfpdk.warn_off_grid_ports
#        passargs["constants"]=gfpdk.constants
#        passargs["materials_index"]=gfpdk.materials_index
#        passargs["routing_strategies"]=gfpdk.routing_strategies
#        passargs["circuit_yaml_parser"]=gfpdk.circuit_yaml_parser
#        passargs["gds_write_settings"]=gfpdk.gds_write_settings
#        passargs["oasis_settings"]=gfpdk.oasis_settings
#        passargs["cell_decorator_settings"]=gfpdk.cell_decorator_settings
#        passargs["bend_points_distance"]=gfpdk.bend_points_distance
        # MappedPDK args override existing args
        passargs.update(kwargs)
        # create and return MappedPDK
        mappedpdk = MappedPDK(**passargs)
        return mappedpdk

    # util methods
    @validate_arguments
    def util_max_metal_seperation(self, metal_levels: Union[list[int],list[str], str, int] = range(1,6)) -> float:
        """returns the maximum of the min_seperation rule for all layers specfied
        although the name of this function is util_max_metal_seperation, layers do not have to be metals
        you can specify non metals by using metal_levels=list of glayers
        if metal_levels is list of int, integers are converted to metal levels
        if a single int is provided, all metals below and including that int level are considerd
        by default this function returns the maximum metal seperation of metals1-5
        """
        if type(metal_levels)==int:
            metal_levels = range(1,metal_levels+1)
        metal_levels = metal_levels if isinstance(metal_levels,Iterable) else [metal_levels]
        if len(metal_levels)<1:
            raise ValueError("metal levels cannot be empty list")
        if type(metal_levels[0])==int:
            metal_levels = [f"met{i}" for i in metal_levels]
        sep_rules = list()
        for met in metal_levels:
            sep_rules.append(self.get_grule(met)["min_separation"])
        return self.snap_to_2xgrid(max(sep_rules))

    @validate_arguments
    def snap_to_2xgrid(self, dims: Union[list[Union[float,Decimal]], Union[float,Decimal]], return_type: Literal["decimal","float","same"]="float", snap4: bool=False) -> Union[list[Union[float,Decimal]], Union[float,Decimal]]:
        """snap all numbers in dims to double the grid size.
        This is useful when a generator accepts a size or dimension argument
        because there is a chance the cell may be centered (resulting in off grid components)
        args:
        dims = a list OR single number specifying the dimensions to snap to grid
        return_type = return a decimal, float, or the same type that was passed to the function
        snap4: snap to 4xgrid (Defualt false)
        """
        dims = dims if isinstance(dims, Iterable) else [dims]
        dimtype_in = type(dims[0])
        dims = [Decimal(str(dim)) for dim in dims] # process in decimals
        grid = 2 * Decimal(str(self.grid_size))
        grid = grid if grid else Decimal('0.001')
        grid = 2*grid if snap4 else grid
        # snap dims to grid
        snapped_dims = list()
        for dim in dims:
            snapped_dim = grid * (dim / grid).quantize(1, rounding=ROUND_UP)
            snapped_dims.append(snapped_dim)
        # convert to correct type
        if return_type=="float" or (return_type=="same" and dimtype_in==float):
            snapped_dims = [float(snapped_dim) for snapped_dim in snapped_dims]
        # correctly return list or single element
        return snapped_dims[0] if len(snapped_dims)==1 else snapped_dims

