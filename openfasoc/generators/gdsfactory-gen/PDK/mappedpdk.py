"""
usage: from mappedpdk import MappedPDK
"""

from gdsfactory.pdk import Pdk
from gdsfactory.typings import Component, PathType, Layer
from pydantic import validator, StrictStr, ValidationError
from typing import ClassVar, Optional
from pathlib import Path
import tempfile
import subprocess


class MappedPDK(Pdk):
    """Inherits everything from the PDK class but also requires mapping to glayers
    glayers are generic layers which can be returned with get_glayer(name: str)
    has_required_glayers(list[str]) is used to verify all required generic layers are
    present"""

    # of all the cap* layers, capmet is the only real layer
    # the other cap layers get initialized to copies of the respective layers
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
        # copied layers
        "capbottommet",
        "captopmet",
        "capvia",
    )

    glayers: dict[StrictStr, StrictStr]
    # friendly way to implement a graph
    grules: dict[StrictStr, dict[StrictStr, Optional[dict]]]
    klayout_lydrc_file: Optional[Path] = None

    @validator("glayers")
    def glayers_check_keys(cls, glayers_obj: dict[StrictStr, StrictStr]):
        """force people to pick glayers from a finite set of string layers that you define
        checks glayers to ensure valid keys,type. Glayers must be passed as dict[str,str]
        if someone tries to pass a glayers dict that has a bad key, throw an error"""
        for glayer, mapped_layer in glayers_obj.items():
            if (not isinstance(glayer, str)) or (not isinstance(mapped_layer, str)):
                raise TypeError("glayers should be passed as dict[str, str]")
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

    def drc(
        self,
        layout: Component | PathType,
        output_dir_or_file: Optional[PathType] = None,
    ):
        """Returns true if the layout is DRC clean and false if not
        Also saves detailed results to output_dir_or_file location as lyrdb
        layout can be passed as a file path or gdsfactory component"""
        if not self.klayout_lydrc_file:
            raise NotImplementedError("no drc script for this PDK")
        # find layout gds file path
        tempdir = None
        if isinstance(layout, Component):
            tempdir = tempfile.TemporaryDirectory()
            layout_path = Path(layout.write_gds(tempdir)).resolve()
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
        # return True or False

    def has_required_glayers(self, layers_required: list[str]):
        """Raises ValueError if any of the generic layers in layers_required: list[str]
        are not mapped to anything in the pdk.glayers dictionary
        also checks that the values in the glayers dictionary map to real Pdk layers"""
        for layer in layers_required:
            if layer not in self.glayers:
                raise ValueError(
                    f"{layer!r} not in self.glayers {list(self.glayers.keys())}"
                )
            self.validate_layers([self.glayers[layer]])

    # TODO: implement LayerSpec type
    def get_glayer(self, layer: str) -> Layer:
        """Returns the PDK layer from the generic layer name"""
        return self.get_layer(self.glayers[layer])

    def get_grule(
        self, glayer1: str, glayer2: Optional[str] = None
    ) -> dict[StrictStr, float]:
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
        # return and error check
        if rules_dict is None or rules_dict == {}:
            raise NotImplementedError(
                "no rules found between " + str(glayer1) + " and " + str(glayer2)
            )
        return rules_dict

    @classmethod
    def is_routable_glayer(cls, glayer: StrictStr):
        return any(hint in glayer for hint in ["met", "active", "poly"])

    @classmethod
    def from_gf_pdk(
        cls,
        gfpdk: Pdk,
        glayers: dict[str, str],
        grules: dict[StrictStr, dict[StrictStr, Optional[dict]]],
        klayout_lydrc_file: Optional[PathType] = None,
    ):
        """Construct a mapped pdk from an existing pdk and the extra parts of MappedPDK"""
        # input type and value validation
        if not isinstance(gfpdk, Pdk):
            raise TypeError("from_gf_pdk: gfpdk arg only accepts GDSFactory PDK type")
        # convert gfpdk to dictionary
        parent_dict = gfpdk.dict()
        # add glayers mapping and lydrc file
        parent_dict["glayers"] = glayers
        parent_dict["klayout_lydrc_file"] = Path(klayout_lydrc_file).resolve()
        parent_dict["grules"] = grules
        # get mapped value and try to resolve validation issues
        try:
            rtrval = cls.parse_obj(parent_dict)
        except ValidationError as valerr:
            errorobj_list = valerr.errors()
            for errorobj in errorobj_list:
                problem_field = errorobj["loc"][0]
                if problem_field in parent_dict:
                    parent_dict.pop(problem_field)
            rtrval = cls.parse_obj(parent_dict)
        return rtrval
