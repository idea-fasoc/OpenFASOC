"""
usage: from mappedpdk import MappedPDK
"""

import gdsfactory as gf
from pydantic import validator, StrictStr, ValidationError
from typing import ClassVar, Optional
from pathlib import Path
import tempfile
import subprocess


class MappedPDK(gf.pdk.Pdk):
    """Inherits everything from the PDK class but also requires mapping to glayers
    glayers are generic layers which can be returned with get_glayer(name: str)
    validate_glayers(list[str]) is used to verify all required generic layers are
    present"""

    valid_glayers: ClassVar[list[str]] = [
        "dnwell",
        "pwell",
        "nwell",
        "p+s/d",
        "n+s/d",
        "active",
        "poly",
        "mcon",
        "met1",
        "via1",
        "met2",
        "via2",
        "met3",
        "via3",
        "met4",
    ]

    glayers: dict[StrictStr, StrictStr]

    klayout_lydrc_file_path: Optional[Path] = None

    # force people to pick glayers from a finite set of string layers that you define
    # if someone tries to pass a glayers dict that has a bad key, throw an error
    @validator("glayers")
    def glayers_check_keys(cls, glayers_obj: dict[StrictStr, StrictStr]):
        """checks glayers to ensure valid keys,type. Glayers must be passed as dict[str,str]"""
        for glayer, mapped_layer in glayers_obj.items():
            if (not isinstance(glayer, str)) or (not isinstance(mapped_layer, str)):
                raise TypeError("glayers should be passed as dict[str, str]")
            if glayer not in cls.valid_glayers:
                raise ValueError(
                    "glayers keys must be one of generic layers listed in class variable valid_glayers"
                )
        return glayers_obj

    @validator("klayout_lydrc_file_path")
    def lydrc_file_exists(cls, lydrc_file_path):
        """Check that lydrc_file_path exists if not none"""
        if lydrc_file_path != None and not lydrc_file_path.is_file():
            raise ValueError(".lydrc script: the path given is not a file")

    def drc(
        self,
        layout: gf.typings.Component | gf.typings.PathType,
        output_dir_or_file: Optional[gf.typings.PathType] = None,
    ):
        """Returns true if the layout is DRC clean and false if not
        Also saves detailed results to output_dir_or_file location as lyrdb
        layout can be passed as a file path or gdsfactory component"""
        if not self.klayout_lydrc_file_path:
            raise NotImplementedError("no drc script for this PDK")
        # find layout gds file path
        if isinstance(layout, gf.typings.Component):
            tempdir = tempfile.TemporaryDirectory()
            layout_path = Path(layout.write_gds(tempdir)).resolve()
        elif isinstance(layout, gf.typings.PathType):
            layout_path = Path(layout).resolve()
        else:
            raise TypeError("layout should be a Component, Path, or string")
        if not layout_path.is_file():
            raise ValueError("layout must exist, the path given is not a file")
        # find report file path, if None the use current directory
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
            str(self.klayout_lydrc_file_path),
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

    # similar to the validate_layers function in gdsfactory default PDK class
    def has_required_glayers(self, layers_required: list[str]):
        """Raises ValueError if any of the generic layers in layers_required: list[str]
        are not mapped to anything in the pdk.glayers dictionary"""
        for layer in layers_required:
            if layer not in self.glayers:
                raise ValueError(
                    f"{layer!r} not in Pdk.glayers {list(self.glayers.keys())}"
                )

    # TODO: implement LayerSpec type
    def get_glayer(self, layer: str) -> gf.typings.Layer:
        """Returns the PDK layer from the generic layer name"""
        return self.get_layer(self.glayers[layer])

    @classmethod
    def from_gf_pdk(cls, gfpdk: gf.pdk.Pdk, glayers: dict[str, str]):
        """Construct a mapped pdk from an existing pdk and a generic layers mapping"""
        # input type validation
        if not isinstance(gfpdk, gf.pdk.Pdk):
            raise TypeError("from_gf_pdk: gfpdk arg only accepts GDSFactory PDK type")
        # convert gfpdk to dictionary
        parent_dict = gfpdk.dict()
        # print(parent_dict)
        # remove all none keys to pass pydantic validation
        keys_to_remove = list()
        for key in parent_dict:
            if parent_dict[key] is None:
                keys_to_remove.append(key)
        for key in keys_to_remove:
            parent_dict.pop(key)
        # add glayers mapping
        parent_dict["glayers"] = glayers
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
