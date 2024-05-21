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
import pathlib, shutil, os, sys

class SetupPDKFiles:
    """Class to setup the PDK files required for DRC and LVS checks.
    """
    def __init__(
        self, 
        pdk_root: Optional[PathType] = None, 
        klayout_drc_file: Optional[PathType] = None, 
        magic_commands_file: Optional[PathType] = None, 
        lvs_schematic_ref_file: Optional[PathType] = None,
        lvs_setup_tcl_file: Optional[PathType] = None, 
        magic_drc_file: Optional[PathType] = None,
        temp_dir: Optional[PathType] = None,
        pdk: Optional[str] = 'sky130'
    ):
        """Initializes the class with the required PDK files for DRC and LVS checks."""
        self.pdk = pdk
        
        if pdk_root is None: 
            # condition for pdk_root not being provided
            if klayout_drc_file is None: 
                self.klayout_drc_valid = 0
            else:
                if not isinstance(klayout_drc_file, PathType):
                    raise ValueError("The file must be provided as a Path object or string")
                else:
                    self.klayout_drc_file = klayout_drc_file
                    self.klayout_drc_valid = 1
            if magic_commands_file is None or magic_drc_file is None:
                self.magic_drc_valid = 0
            else:
                if not isinstance(magic_commands_file, PathType) or not isinstance(magic_drc_file, PathType):
                    raise ValueError("The files must be provided as Path objects or strings")
                else:
                    self.magic_commands_file = magic_commands_file
                    self.magic_drc_file = magic_drc_file
                    self.magic_drc_valid = 1
            if lvs_schematic_ref_file is None or lvs_setup_tcl_file is None or magic_drc_file is None:
                self.lvs_valid = 0
            else:
                if not isinstance(lvs_schematic_ref_file, PathType) or not isinstance(lvs_setup_tcl_file, PathType):
                    raise ValueError("The files must be provided as Path objects or strings")
                else:
                    self.lvs_schematic_ref_file = lvs_schematic_ref_file
                    self.lvs_setup_tcl_file = lvs_setup_tcl_file
                    self.magic_drc_file = magic_drc_file
                    self.lvs_valid = 1
        else:
            if not isinstance(pdk_root, PathType):
            # condition for pdk_root not being a Path object
                raise ValueError("pdk_root must be a Path object or string")
            # condition for pdk_root being provided
            self.pdk_root = pdk_root
            if klayout_drc_file is None:
                # condition for klayout_drc_file not being provided with pdk_root provided
                if pdk == 'sky130':
                    if isinstance(pdk_root, Path):
                        self.klayout_drc_file = pdk_root / "sky130A" / "libs.tech" / "klayout" / "drc" / "sky130.lydrc"
                    else: 
                        self.klayout_drc_file = Path(pdk_root) / "sky130A" / "libs.tech" / "klayout" / "drc" / "sky130.lydrc"
                elif pdk == 'gf180':
                    raise NotImplementedError("Klayout lvs is not supported for gf180 PDK")
                else:
                    raise ValueError("pdk must be either 'sky130' or 'gf180', others not supported!")
                
            if magic_commands_file is None:
                # condition for magic_commands_file not being provided with pdk_root provided
                
                # print("magic_commands.tcl not provided, trying in openfasoc/common/drc-lvs-check")
                # magic_commands_file_path = Path(__file__).parent.parent.parent.parent.parent.parent / "common" / "drc-lvs-check" / "magic_commands.tcl"
                # if magic_commands_file_path.is_file():
                #     self.magic_commands_file = magic_commands_file_path.resolve()
                # else:
                
                print("Defaulting to stale magic_commands.tcl")
                magic_commands_file_str = f"""
gds flatglob *$$*
gds flatglob *VIA*
gds flatglob *CDNS*
gds flatglob *capacitor_test_nf*

gds read $::env(RESULTS_DIR)/$::env(DESIGN_NAME).gds

proc custom_drc_save_report {{{{cellname ""}} {{outfile ""}}}} {{

if {{$outfile == ""}} {{set outfile "drc.out"}}

set fout [open $outfile w]
set oscale [cif scale out]
if {{$cellname == ""}} {{
    select top cell
    set cellname [cellname list self]
    set origname ""
}} else {{
    set origname [cellname list self]
    puts stdout "\[INFO\]: Loading $cellname\n"
    flush stdout

    load $cellname
    select top cell
}}

drc check
set count [drc list count]

puts $fout "$cellname count: $count"
puts $fout "----------------------------------------"
set drcresult [drc listall why]
foreach {{errtype coordlist}} $drcresult {{
    puts $fout $errtype
    puts $fout "----------------------------------------"
    foreach coord $coordlist {{
        set bllx [expr {{$oscale * [lindex $coord 0]}}]
        set blly [expr {{$oscale * [lindex $coord 1]}}]
        set burx [expr {{$oscale * [lindex $coord 2]}}]
        set bury [expr {{$oscale * [lindex $coord 3]}}]
        set coords [format " %.3fum %.3fum %.3fum %.3fum" $bllx $blly $burx $bury]
        puts $fout "$coords"
    }}
puts $fout "----------------------------------------"
}}
puts $fout ""

if {{$origname != ""}} {{
    load $origname
}}

close $fout
puts "\[INFO\]: DONE with $outfile\n"
}}

custom_drc_save_report $::env(DESIGN_NAME) $::env(REPORTS_DIR)/$::env(DESIGN_NAME).rpt
"""
            
                new_path = temp_dir / "magic_commands.tcl"
                with open(str(new_path.resolve()), 'w') as f:
                    f.write(magic_commands_file_str)
                    
                self.magic_commands_file = new_path.resolve()
                    # need to delete after execution
            else:
                self.magic_commands_file = magic_commands_file
                
            if lvs_schematic_ref_file is None:
                if pdk == 'gf180':
                    raise NotImplementedError("LVS is not supported for gf180 PDK")
                if isinstance(pdk_root, Path):
                    lvs_spice_file = pdk_root / "sky130A" / "libs.ref" / "sky130_fd_sc_hd" / "spice" / "sky130_fd_sc_hd.spice"
                else:
                    lvs_spice_file = Path(pdk_root) / "sky130A" / "libs.ref" / "sky130_fd_sc_hd" / "spice" / "sky130_fd_sc_hd.spice"
                output_lvs_spice_file = temp_dir / "sky130_fd_sc_hd.spice"
                self.write_custom_spice_to_file(lvs_spice_file, output_lvs_spice_file)
                self.lvs_schematic_ref_file = output_lvs_spice_file
            else: 
                self.lvs_schematic_ref_file = lvs_schematic_ref_file 
                
            if lvs_setup_tcl_file is None:
                if pdk == 'gf180':
                    raise NotImplementedError("LVS is not supported for gf180 PDK")
                dest_lvs_setup_tcl = temp_dir / "sky130A_setup.tcl"
                lvs_setup_tcl_file = self.magic_netgen_file_exists(dest_lvs_setup_tcl, pdk_root)
                self.lvs_setup_tcl_file = lvs_setup_tcl_file
            else: 
                self.lvs_setup_tcl_file = lvs_setup_tcl_file
                
            if magic_drc_file is None:
                if pdk == "sky130":
                    dest_magic_drc = temp_dir / f"{pdk}A.magicrc"     
                elif pdk == "gf180": 
                    dest_magic_drc = temp_dir / f"{pdk}mcuC.magicrc"
                    
                magic_drc_file = self.magic_netgen_file_exists(dest_magic_drc, pdk_root)
                self.magic_drc_file = magic_drc_file
            else: 
                self.magic_drc_file = magic_drc_file
            
            self.klayout_drc_valid = 0 if klayout_drc_file is None else 1
            
            if self.magic_commands_file is None or self.magic_drc_file is None:
                self.magic_drc_valid = 0
            else: 
                self.magic_drc_valid = 1
            
            if self.lvs_schematic_ref_file is None or self.lvs_setup_tcl_file is None or self.magic_drc_file is None:
                self.lvs_valid = 0 
            else:
                self.lvs_valid = 1        
    
    def write_custom_spice_to_file(
        self, 
        input_spice: str, 
        output_spice: str
    ):
        """Writes a custom spice file to the output_spice file path."""
        custom_spice_string = f"""
* HEADER and SLC cells
* Proxy pins that may or may not be generated by magic sky130_fd_sc_hd__tap_1_0/VPB sky130_fd_sc_hd__tap_1_1/VPB

.subckt HEADER VGND VIN VNB VPWR
xMN0 VPWR VGND net7 VNB sky130_fd_pr__nfet_03v3_nvt ad=0p pd=0u as=0p ps=0u w=700000u l=500000u
xMN1 net7 VGND VPWR VNB sky130_fd_pr__nfet_03v3_nvt ad=1.1445e+12p pd=1.167e+07u as=3.92e+11p ps=3.92e+06u w=700000u l=500000u
xMN2 VPWR VGND net7 VNB sky130_fd_pr__nfet_03v3_nvt ad=0p pd=0u as=0p ps=0u w=700000u l=500000u
xMN3 net7 VGND VPWR VNB sky130_fd_pr__nfet_03v3_nvt ad=0p pd=0u as=0p ps=0u w=700000u l=500000u
xMN4 net7 VGND VIN VNB sky130_fd_pr__nfet_03v3_nvt ad=0p pd=0u as=0p ps=0u w=700000u l=500000u
xMN5 VIN VGND net7 VNB sky130_fd_pr__nfet_03v3_nvt ad=3.92e+11p pd=3.92e+06u as=0p ps=0u w=700000u l=500000u
xMN6 net7 VGND VIN VNB sky130_fd_pr__nfet_03v3_nvt ad=0p pd=0u as=0p ps=0u w=700000u l=500000u
xMN7 VIN VGND net7 VNB sky130_fd_pr__nfet_03v3_nvt ad=0p pd=0u as=0p ps=0u w=700000u l=500000u
.ends

.subckt SLC IN INB VOUT VGND VNB VPWR VPB
xMP0 net02 net07 VPWR VPB sky130_fd_pr__pfet_01v8_hvt m=1 mult=1 w=360000u l=150000u sa=265e-3 sb=265e-3 sd=280e-3
xMP1 net03 net03 net02 VPB sky130_fd_pr__pfet_01v8_hvt mult=1 w=360000u l=150000u sa=265e-3 sb=265e-3 sd=280e-3
xMP3 net06 net03 VPWR VPB sky130_fd_pr__pfet_01v8_hvt m=1 mult=1 w=360000u l=150000u sa=265e-3 sb=265e-3 sd=280e-3
xMP4 net07 net07 net06 VPB sky130_fd_pr__pfet_01v8_hvt m=1 mult=1 w=360000u l=150000u sa=265e-3 sb=265e-3 sd=280e-3
xMP6 VOUT net06 VPWR VPB sky130_fd_pr__pfet_01v8_hvt m=2 mult=1 w=0.5 l=150000u sa=265e-3 sb=265e-3 sd=280e-3
xMN4 VOUT net07 VGND VNB sky130_fd_pr__nfet_01v8 m=1 mult=1 w=0.65 l=150000u sa=265e-3 sb=265e-3 sd=280e-3
xMN0 net03 INB VGND VNB sky130_fd_pr__nfet_01v8_lvt m=10 mult=1 w=0.5 l=150000u sa=265e-3 sb=265e-3 sd=280e-3
xMN8 net07 IN VGND VNB sky130_fd_pr__nfet_01v8_lvt m=10 mult=1 w=500000u l=150000u sa=265e-3 sb=265e-3 sd=280e-3
.ends

******* EOF

* Modified subthreshold inverter cell

.subckt dinv1 Yb Y Ab A Apb Ap VGND VPWR
X1    t1    Apb    VPWR    VPWR   sky130_fd_pr__pfet_01v8_hvt m=1 mult=1 w=360000u l=150000u sa=265e-3 sb=265e-3 sd=280e-3
X2    Y    Yb    t1    t1   sky130_fd_pr__pfet_01v8_hvt m=1 mult=1 w=360000u l=150000u sa=265e-3 sb=265e-3 sd=280e-3
X3    t2    Ap    VPWR    VPWR  sky130_fd_pr__pfet_01v8_hvt m=1 mult=1 w=360000u l=150000u sa=265e-3 sb=265e-3 sd=280e-3 
X4    Yb    Y    t2    t2   sky130_fd_pr__pfet_01v8_hvt m=1 mult=1 w=360000u l=150000u sa=265e-3 sb=265e-3 sd=280e-3
X5    Y    Ab    t3    t3   sky130_fd_pr__nfet_01v8 m=1 mult=1 w=180000u l=150000u sa=265e-3 sb=265e-3 sd=280e-3
X6    t3    Ab    VGND   VGND  sky130_fd_pr__nfet_01v8 m=1 mult=1 w=180000u l=150000u sa=265e-3 sb=265e-3 sd=280e-3
X7    Yb    A    t4    t4  sky130_fd_pr__nfet_01v8 m=1 mult=1 w=180000u l=150000u sa=265e-3 sb=265e-3 sd=280e-3
X8    t4    A    VGND    VGND  sky130_fd_pr__nfet_01v8 m=1 mult=1 w=180000u l=150000u sa=265e-3 sb=265e-3 sd=280e-3
.ends 

******** EOF
"""
        with open(input_spice, 'r') as rf:
            lines = rf.readlines()
            with open(output_spice, 'w') as wf:
                for line in lines:
                    wf.write(line)
                wf.write(custom_spice_string)
                
    def magic_netgen_file_exists(
        self, 
        magic_file, 
        pdk_root
    ):
            """Check that magic_file exists if not none, and copy it to the required pdk directory if it doesn't exist"""
            def copy_if_not_exists(src, dest):
                if not os.path.exists(dest):
                    print(f'copying file from required pdk dir: {src}')
                    shutil.copy(src, dest)
                else:
                    print(f'Either file not found: {src}, or already copied to: {dest}')
                    
            def return_pdk_full_name(self):
                """Returns the full name of the pdk based on the class name"""
                if self.pdk == 'sky130':
                    return f"{self.pdk}A"
                elif self.pdk == 'gf180':
                    return f"{self.pdk}mcuC"
            
            # Check if the magic_file exists, if not, copy it to the required pdk directory
            if magic_file != None and not magic_file.is_file():
                # Check if the pdk_root is a directory, if not raise an error
                if pdk_root != None and Path(pdk_root).resolve().is_dir():
                    pdk_name = return_pdk_full_name(self)
                    if ".magicrc" in str(magic_file):
                        magic_file_source = Path(pdk_root) / f"{pdk_name}" / "libs.tech" / "magic" / f"{pdk_name}.magicrc"
                    elif "_setup.tcl" in str(magic_file):
                        magic_file_source = Path(pdk_root) / f"{pdk_name}" / "libs.tech" / "netgen" / f"{pdk_name}_setup.tcl"
                    copy_if_not_exists(magic_file_source, magic_file)
                    return magic_file
                elif pdk_root != None and not pdk_root.is_dir():
                    raise ValueError("pdk_root must be a directory")
                raise ValueError("magic/netgen script: the path given is not a file")
            return magic_file
        

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
    # magic_commands_file: Optional[Path] = None
    # lvs_schematic_ref_file: Optional[Path] = None

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
    def drc_magic(
        self, 
        layout: Component | str, 
        design_name: str, 
        pdk_root: Optional[PathType] = "/usr/bin/miniconda3/share/pdk/", 
        magic_commands_file: Optional[PathType] = None,
        magic_drc_file: Optional[PathType] = None
    ):
        """Runs DRC using magic on the either the component or the gds file path provided. Requires the design name and the pdk_root to be specified, handles importing the required magicrc and other setup files, if not specified. Accepts overriden magic_commands_file and magic_drc_file.

        Args:
            - layout (Component | str):
                - Either the Component or the gds file path to run DRC on
            - design_name (str):
                - The designated name of the design
            - pdk_root (Optional[PathType], optional):
                - The directory where the pdk files are located. 
                - e.g. - "/usr/bin/miniconda3/share/pdk/". Defaults to "/usr/bin/miniconda3/share/pdk/".
            - magic_commands_file (Optional[PathType], optional):
                - A file containing magic commands to be executed for DRC (magic_commands.tcl). 
                - Defaults to None.
            - magic_drc_file (Optional[PathType], optional):
                - The .magicrc file for your PDK of choice. 
                - Defaults to None.

        Raises:
            - ValueError: 
                - If the magic DRC cannot be run! 
                - Please either provide a PDK root or the following files: 
                    - a file containing magic commands to be executed for DRC (magic_commands.tcl) 
                    - the .magicrc file for your PDK of choice

        Returns:
            str: A string indicating whether the DRC passed or failed, and if there are any errors in the DRC report
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = pathlib.Path(temp_dir).resolve()
    
            pdkfiles = SetupPDKFiles(
                pdk_root=pdk_root, 
                pdk=self.name, 
                magic_commands_file=magic_commands_file, magic_drc_file=magic_drc_file, 
                temp_dir=temp_dir_path
            )
            
            if not pdkfiles.magic_drc_valid:
                raise ValueError("magic DRC cannot be run! Please either provide a PDK root or the following files: a file containing magic commands to be executed for DRC (magic_commands.tcl) and the .magicrc file for your PDK of choice")
            
            # check if default pdk_root is being used
            if pdk_root == "/usr/bin/miniconda3/share/pdk/":
                print("Using default pdk_root: /usr/bin/miniconda3/share/pdk/")
            env_vars = {
                'PDK_ROOT': pdk_root,
                'DESIGN_NAME': design_name,
                'REPORTS_DIR': str(temp_dir_path),
                'RESULTS_DIR': str(temp_dir_path)
            }

            os.environ.update(env_vars)
                    
            gds_path = str(temp_dir_path / f"{design_name}.gds")
            if isinstance(layout, Component):
                layout.write_gds(gds_path)
            elif isinstance(layout, PathType):            
                shutil.copy(layout, gds_path)
            
            cmd = f'bash -c "magic -rcfile {pdkfiles.magic_drc_file} -noconsole -dnull {pdkfiles.magic_commands_file} < /dev/null"'
            
            subp = subprocess.Popen(
                cmd, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            
            subp.wait()
            print(subp.stdout.read().decode('utf-8'))
            
            subproc_code = subp.returncode
            result_str = "magic drc script passed" if subproc_code == 0 else "magic drc script failed"
            # print errors
            
            errors = subp.stderr.read().decode('utf-8')
            if errors:
                print(f"Soft errors: \n{errors}")
                
            with open(f'{str(temp_dir_path)}/{design_name}.rpt', 'r') as f:
                num_lines = len(f.readlines())
                if num_lines > 3:
                    result_str = result_str + "\nErrors found in DRC report"
                    f.seek(0)
                    print(f.read())
                else:
                    result_str = result_str + "\nNo errors found in DRC report"

        return result_str

    @validate_arguments
    def lvs_netgen(
        self,
        layout: Component | PathType, 
        design_name: str, 
        pdk_root: Optional[PathType] = None,
        lvs_setup_tcl_file: Optional[PathType] = None,
        lvs_schematic_ref_file: Optional[PathType] = None,
        magic_drc_file: Optional[PathType] = None, 
        cdl_path: Optional[PathType] = None,
        report_handling: Optional[tuple[Optional[bool], Optional[str]]] = (False, None)
    ):
        """Runs LVS using netgen on the either the component or the gds file path provided. Requires the design name and the pdk_root to be specified, handles importing the required setup files, if not specified. Accepts overriden lvs_setup_tcl_file, lvs_schematic_ref_file, and magic_drc_file.

        Args:
            - layout (Component | PathType): 
                - Either the Component or the gds file path to run LVS on
            design_name (str): 
                - The designated name of the design
            pdk_root (Optional[PathType], optional): 
                - The directory where the pdk files are located. 
                - e.g. - "/usr/bin/miniconda3/share/pdk/". Defaults to None.
            - lvs_setup_tcl_file (Optional[PathType], optional): 
                - A file containing netgen setup commands to be executed for LVS (sky130A_setup.tcl). 
                - Defaults to None. 
                - (Found in libs.tech/netgen/ of the pdk directory)
            - lvs_schematic_ref_file (Optional[PathType], optional): 
                - A spice file containing subckt definitions for the PDK. 
                - Defaults to None. 
                - (Found in libs.ref/sky130_fd_sc_hd/spice of the pdk directory)
            - magic_drc_file (Optional[PathType], optional): 
                - The .magicrc file for your PDK of choice. 
                - Defaults to None.
            - cdl_path (Optional[PathType], optional): 
                - The path to the CDL file (netlist) for the design. 
                - Defaults to None.
            - report_handling (Optional[tuple[Optional[bool], Optional[str]]], optional): 
                - A tuple containing a boolean value and a string. 
                - The boolean value indicates whether to handle the report or not, and the string indicates the path to the report. 
                - Defaults to (False, None).

        Raises:
            - NotImplementedError: 
                - If LVS is not supported for gf180 PDK
            - RuntimeError:
                - If Netgen or Magic is not found in the system
            - ValueError:
                - If LVS cannot be run! 
                - Please provide either a PDK root or the following files: a setup.tcl file for the PDK, a .magicrc file, and a spice file containing subckt definitions for the PDK.

        """
        if self.name == 'gf180':
            raise NotImplementedError("LVS is not supported for gf180 PDK")
        def extract_design_name_from_netlist(file_path: str):
            """ Extracts the design name from the netlist file (found after the final .ends statement in the netlist file)"""
            with open(file_path, 'r') as file:
                lines = file.readlines()
            last_ends_line = None
            for line in lines:
                if line.strip().startswith(".ends"):
                    last_ends_line = line.strip()

            if last_ends_line:
                parts = last_ends_line.split()
                if len(parts) > 1:
                    return parts[1]
                else:
                    return None
                
        def check_command_exists(command: str):
            """ Check if a command exists in the system """
            result = subprocess.run(f"command -v {command}", shell=True, capture_output=True, text=True)
            return result.returncode == 0
        
        def modify_design_name_in_cdl(cdl_path, design_name):
            design_name_from_cdl = extract_design_name_from_netlist(cdl_path)
            if design_name_from_cdl is not None and design_name_from_cdl == design_name:
                print(f"Design name from CDL file: {design_name_from_cdl} matches the design name: {design_name}")
            else:
                # replace all occurences of design_name_from_cdl with design_name in the cdl file
                with open(cdl_path, 'r') as file:
                    filedata = file.read()
                newdata = filedata.replace(design_name_from_cdl, design_name)
                with open(cdl_path, 'w') as file:
                    file.write(newdata)
        
        def write_spice(input_cdl, output_spice, lvs_schematic_ref_file):
        # create {design_name}.spice
            with open(input_cdl, 'r') as file:
                lines = file.readlines()
                with open(output_spice, 'w') as file2:
                    sky130_spice_path = Path(lvs_schematic_ref_file).resolve()
                    file2.write(f".include {sky130_spice_path}\n")
                    # write the rest of the lines
                    for line in lines:
                        file2.write(line)
        
        if not check_command_exists("netgen"):
            raise RuntimeError("Netgen not found in the system")
        if not check_command_exists("magic"):
            raise RuntimeError("Magic not found in the system")
        os.environ['DESIGN_NAME'] = design_name
        # results go to a tempdirectory 
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir).resolve()
            
            pdkfiles = SetupPDKFiles(
                pdk_root=pdk_root, 
                pdk=self.name, 
                temp_dir=temp_dir_path, 
                lvs_schematic_ref_file=lvs_schematic_ref_file, lvs_setup_tcl_file=lvs_setup_tcl_file, 
                magic_drc_file=magic_drc_file
            )
            if not pdkfiles.lvs_valid:
                raise ValueError("LVS cannot be run! Please provide either a PDK root or the following files: a setup.tcl file for the PDK, a .magicrc file, and a spice file containing subckt definitions for the PDK.")
            
            lvsmag_path = temp_dir_path / f"{design_name}_lvsmag.spice"
            pex_path = temp_dir_path / f"{design_name}_pex.spice"
            sim_path = temp_dir_path / f"{design_name}_sim.spice"
            spice_path = temp_dir_path / f"{design_name}.spice"
            cdl_path_from_comp = temp_dir_path / f"{design_name}.cdl"
            gds_path = temp_dir_path / f"{design_name}.gds"
            report_path = temp_dir_path / f"{design_name}_lvs.rpt"
            
            if isinstance(layout, Component):
                layout.write_gds(str(gds_path))
                netlist = layout.info['netlist'].generate_netlist()
                with open(str(cdl_path_from_comp), 'w') as f:
                    f.write(netlist)
            elif isinstance(layout, PathType):            
                shutil.copy(layout, str(gds_path))
                if cdl_path is None:
                    raise ValueError("Path to cdl (netlist) must be provided if only gds file is provided! Provide Component alternatively!")
                else:
                    shutil.copy(cdl_path, str(cdl_path_from_comp))
                    
            modify_design_name_in_cdl(str(cdl_path_from_comp), design_name)
            
            write_spice(str(cdl_path_from_comp), str(spice_path), pdkfiles.lvs_schematic_ref_file)
            
            magic_script_content = f"""
gds flatglob *\\$\\$*
gds read {gds_path}
load {design_name}

select top cell
extract all
ext2spice lvs
ext2spice -o {str(lvsmag_path)}
load {design_name}
extract all
ext2spice lvs
ext2spice rthresh 0
ext2spice cthresh 0
ext2spice -o {str(pex_path)}
load {design_name}
extract all
ext2spice cthresh 0
ext2spice -o {str(sim_path)}
exit
"""

            with tempfile.NamedTemporaryFile(mode='w', delete=False) as magic_script_file:
                magic_script_file.write(magic_script_content)
                magic_script_path = magic_script_file.name
            
            try:
                # dest_magicrc = temp_dir_path / f"{self.name}A.magicrc"
                # dest_netgen_tcl = temp_dir_path / f"{self.name}A_setup.tcl"
                # magic_rc_file = self.magic_netgen_file_exists((dest_magicrc), pdk_root)
                
                magic_cmd = f"bash -c 'magic -rcfile {pdkfiles.magic_drc_file} -noconsole -dnull < {magic_script_path}'",
                magic_subproc = subprocess.run(
                    magic_cmd, 
                    shell=True,
                    check=True,
                    capture_output=True
                )
                
                magic_subproc_code = magic_subproc.returncode
                magic_subproc_out = magic_subproc.stdout.decode('utf-8')
                print(magic_subproc_out)
                
                # netgen_setup_tcl_file = self.magic_netgen_file_exists(dest_netgen_tcl, pdk_root)
                netgen_command = f'netgen -batch lvs "{str(lvsmag_path)} {design_name}" "{str(spice_path)} {design_name}" {pdkfiles.lvs_setup_tcl_file} {str(report_path)}'
                
                netgen_subproc = subprocess.run(
                    netgen_command,
                    shell=True,
                    check=True, 
                    capture_output=True
                )
                netgen_subproc_code = netgen_subproc.returncode
                netgen_subproc_out = netgen_subproc.stdout.decode('utf-8')
                print(netgen_subproc_out)
            
            finally: 
                os.remove(magic_script_path)
                if os.path.exists(f'{design_name}.ext'):
                    os.remove(f'{design_name}.ext')
                # copy the report from the temp directory to the specified location
                if report_handling[0]:
                    shutil.copy(report_path, report_handling[1])
                    
    
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

