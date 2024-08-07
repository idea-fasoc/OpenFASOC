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
        lvs_schematic_ref_file: Optional[PathType] = None,
        lvs_setup_tcl_file: Optional[PathType] = None, 
        magic_drc_file: Optional[PathType] = None,
        temp_dir: Optional[PathType] = None,
        pdk: Optional[str] = 'sky130'
    ):
        """Initializes the class with the required PDK files for DRC and LVS checks."""
        self.pdk = pdk
        self.temp_dir = temp_dir
        
        if pdk_root is None: 
            # condition for pdk_root not being provided
            if klayout_drc_file is None: 
                raise ValueError("Please provide a Klayout DRC file if not providing PDK root!")
            else:
                if not isinstance(klayout_drc_file, PathType):
                    raise ValueError("The file must be provided as a Path object or string")
                else:
                    self.klayout_drc_file = klayout_drc_file
            if magic_drc_file is None:
                raise ValueError("Please provide a magic DRC file")
            else:
                if not isinstance(magic_drc_file, PathType):
                    raise ValueError("The files must be provided as Path objects or strings")
                else:
                    self.magic_drc_file = magic_drc_file
            if lvs_schematic_ref_file is None or lvs_setup_tcl_file is None or magic_drc_file is None:
                raise ValueError(f"""Please provide the following files:
                      - a spice file with subckt references(lvs_schematic_ref_file)
                      - a tcl file with setup commands(lvs_setup_tcl_file)
                      - a magic DRC file(magic_drc_file)""")
            else:
                if not isinstance(lvs_schematic_ref_file, PathType) or not isinstance(lvs_setup_tcl_file, PathType):
                    raise ValueError("The files must be provided as Path objects or strings")
                else:
                    self.lvs_schematic_ref_file = lvs_schematic_ref_file
                    self.lvs_setup_tcl_file = lvs_setup_tcl_file
                    self.magic_drc_file = magic_drc_file
        else:
            if not isinstance(pdk_root, PathType):
            # condition for pdk_root not being a Path object
                raise ValueError("pdk_root must be a Path object or string")
            # condition for pdk_root being provided
            self.pdk_root = pdk_root
            if klayout_drc_file is None:
                # condition for klayout_drc_file not being provided with pdk_root provided
                if pdk == 'sky130':
                    klayout_drc_file = Path(pdk_root) / "sky130A" / "libs.tech" / "klayout" / "drc" / "sky130.lydrc"
                elif pdk == 'gf180':
                    raise NotImplementedError("Klayout lvs is not supported for gf180 PDK")
                else:
                    raise ValueError("pdk must be either 'sky130' or 'gf180', others not supported!")
            
                
            if lvs_schematic_ref_file is None:
                if pdk == 'gf180':
                    raise NotImplementedError("LVS is not supported for gf180 PDK")
                
                lvs_spice_file = Path(pdk_root) / "sky130A" / "libs.ref" / "sky130_fd_sc_hd" / "spice" / "sky130_fd_sc_hd.spice"
                lvs_schematic_ref_file = temp_dir / "sky130_fd_sc_hd.spice"
                self.write_custom_spice_to_file(lvs_spice_file, lvs_schematic_ref_file)
            
            if lvs_setup_tcl_file is None:
                if pdk == 'gf180':
                    raise NotImplementedError("LVS is not supported for gf180 PDK")
                dest_lvs_setup_tcl = temp_dir / "sky130A_setup.tcl"
                lvs_setup_tcl_file = self.magic_netgen_file_exists(dest_lvs_setup_tcl, pdk_root)
                
            if magic_drc_file is None:
                if pdk == "sky130":
                    dest_magic_drc = temp_dir / f"{pdk}A.magicrc"     
                elif pdk == "gf180": 
                    dest_magic_drc = temp_dir / f"{pdk}mcuC.magicrc"
                    
                magic_drc_file = self.magic_netgen_file_exists(dest_magic_drc, pdk_root)
                
            self.klayout_drc_file = klayout_drc_file
            self.lvs_schematic_ref_file = lvs_schematic_ref_file
            self.lvs_setup_tcl_file = lvs_setup_tcl_file
            self.magic_drc_file = magic_drc_file
            
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
        
    def return_dict_of_files(
        self
    ):
        pdk_files = {
            'pdk_root': self.pdk_root,
            'klayout_drc_file': self.klayout_drc_file,
            'lvs_schematic_ref_file': self.lvs_schematic_ref_file,
            'lvs_setup_tcl_file': self.lvs_setup_tcl_file,
            'magic_drc_file': self.magic_drc_file,
            'temp_dir': self.temp_dir,
            'pdk': self.pdk
        }
        return pdk_files
        

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
    pdk_files: dict[StrictStr, Union[PathType, None]]

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

    @validate_arguments
    def drc(
        self,
        layout: Component | PathType,
        output_dir_or_file: Optional[PathType] = None,
    ):
        """Returns true if the layout is DRC clean and false if not
        Also saves detailed results to output_dir_or_file location as lyrdb
        layout can be passed as a file path or gdsfactory component"""
        if not self.pdk_files['klayout_drc_file']:
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
            str(self.pdk_files['klayout_drc_file']),
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
        layout: Component | PathType, 
        design_name: str, 
        pdk_root: Optional[PathType] = None, 
        magic_drc_file: Optional[PathType] = None, 
        output_file: Optional[PathType] = None 
    ) -> dict:
        """Runs DRC using magic on the either the component or the gds file path provided. Requires the design name and the pdk_root to be specified, handles importing the required magicrc and other setup files, if not specified. Accepts overriden magic_commands_file and magic_drc_file.

        Args:
            - layout (Component | str):
                - Either the Component or the gds file path to run DRC on
            - design_name (str):
                - The designated name of the design
            - pdk_root (Optional[PathType], optional):
                - The directory where the pdk files are located. 
                - e.g. - "/usr/bin/miniconda3/share/pdk/". Defaults to "/usr/bin/miniconda3/share/pdk/".
            - magic_drc_file (Optional[PathType], optional):
                - The .magicrc file for your PDK of choice. 
                - Defaults to None.
            - output_file (Optional[PathType], optional):
                - The .rpt file to save the DRC report.
                - The report will written to regression/drc/{design_name}/{file_name}
                - Defaults to None.

        Raises:
            - ValueError: 
                - If the magic DRC cannot be run! 
                - Please either provide a PDK root or the following files: 
                    - a file containing magic commands to be executed for DRC (magic_commands.tcl) 
                    - the .magicrc file for your PDK of choice
        """
        
        def create_magic_commands_file(temp_dir):
            # magic commands file creation
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
                
            return new_path.resolve()
    
        self.pdk_files['pdk'] = self.name
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = pathlib.Path(temp_dir).resolve()
            self.pdk_files['temp_dir'] = temp_dir_path
            
            if pdk_root is None:
                print("using default pdk_root: /usr/bin/miniconda3/share/pdk/")
            else: 
                print('using provided pdk_root')
                self.pdk_files['pdk_root'] = pdk_root
                
            env_vars = {
                    'PDK_ROOT': str(self.pdk_files['pdk_root']),
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
            
            magicrc_file = self.pdk_files['magic_drc_file'] if magic_drc_file is None else magic_drc_file
            magic_cmd_file = create_magic_commands_file(temp_dir_path)
            cmd = f'bash -c "magic -rcfile {magicrc_file} -noconsole -dnull {magic_cmd_file} < /dev/null"'
            
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
            
            report_path = f'{str(temp_dir_path)}/{design_name}.rpt'
            
            if Path(report_path).is_file():
                with open(report_path, 'r') as f:
                    num_lines = len(f.readlines())
                    if num_lines > 3:
                        result_str = result_str + "\nErrors found in DRC report"
                        f.seek(0)
                        for line in f.readlines():
                            print(line)    
                    else:
                        result_str = result_str + "\nNo errors found in DRC report"
            else: 
                raise ValueError("DRC report file not found")
                    
            ret_dict = {"result_str": result_str, "subproc_code": subproc_code}
            if ret_dict is None:
                raise ValueError('Something weird happened')
            
            if output_file is not None:
                path_to_regression_drc = Path(__file__).resolve().parents[1] / "regression" / "drc"
                dir_name = design_name
                path_to_dir = path_to_regression_drc / dir_name
                if not path_to_dir.exists():
                    path_to_dir.mkdir(parents=True, exist_ok=False)
                new_output_file_path = path_to_dir / output_file
                if not new_output_file_path.exists():
                    shutil.copy(report_path, path_to_dir / output_file)
                else: 
                    raise ValueError("Output file already exists")

        return ret_dict

    @validate_arguments
    def lvs_netgen(
        self,
        layout: Component | PathType, 
        design_name: str, 
        pdk_root: Optional[PathType] = None,
        lvs_setup_tcl_file: Optional[PathType] = None,
        lvs_schematic_ref_file: Optional[PathType] = None,
        magic_drc_file: Optional[PathType] = None, 
        netlist: Optional[PathType] = None,
        output_file_path: Optional[PathType] = None, 
        copy_intermediate_files: Optional[bool] = False
    ) -> dict:
        """ Runs LVS using netgen on the either the component or the gds file path provided. Requires the design name and the pdk_root to be specified, handles importing the required magicrc and other setup files, if not specified. Accepts overriden lvs_setup_tcl_file, lvs_schematic_ref_file, and magic_drc_file.

        Args:
            - layout (Component | PathType):
                - Either the Component or the gds file path to run LVS on
            - design_name (str): 
                - The designated name of the design
            - pdk_root (Optional[PathType], optional): 
                - The directory where the pdk files are located. 
                - e.g. - "/usr/bin/miniconda3/share/pdk/". Defaults to None.
            - lvs_setup_tcl_file (Optional[PathType], optional): 
                - The .tcl file with setup commands for LVS.
                - Defaults to None.
            - lvs_schematic_ref_file (Optional[PathType], optional):
                - The .spice file with subckt references for LVS.
                - Defaults to None.
            - magic_drc_file (Optional[PathType], optional):
                - The .magicrc file for your PDK of choice.
                - Defaults to None.
            - netlist (Optional[PathType], optional): 
                - The .cdl or .spice file for the netlist.
                - Defaults to None.
            - output_file_path (Optional[PathType], optional): 
                - The path to the report file
                - Will write the report to regression/lvs/{design_name}/{output_file_path}
                - Defaults to None.
            - copy_intermediate_files (Optional[bool], optional): 
                - If True, copies intermediate files to the currenty working directory (lvsmag, pex spice, prepex spice).
                - Defaults to False.

        Raises:
            - NotImplementedError:
                - If the LVS cannot be run! 
            - ValueError:
                - If the netlist file is not provided! 
            - RuntimeError:
                - If the netgen command is not found in the system! 
                - If the magic command is not found in the system! 
            - RuntimeError: 
                - If the magic DRC file is not found in the system!
            - ValueError: 
                - If the path to the netlist file is not a file!

        Returns:
            dict: a dictionary containing the result string and the subprocess code
        """
        if not self.name == 'sky130':
            raise NotImplementedError("LVS only supported for sky130 PDK")
        def check_if_path_or_net_string(netlist: PathType):
            cdl_suffix = ".cdl"
            spice_suffix = ".spice"
            if netlist is None:
                raise ValueError("Path to cdl (netlist) must be provided!")
            check_suffix = str(netlist).endswith(cdl_suffix) or str(netlist).endswith(spice_suffix)
            return check_suffix # True for cdl and spice, False if net passed
        
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
        
        def modify_design_name_in_cdl(netlist, design_name):
            design_name_from_cdl = extract_design_name_from_netlist(netlist)
            if design_name_from_cdl is not None:
                if design_name_from_cdl == design_name:
                    print(f"Design name from CDL file: {design_name_from_cdl} matches the design name: {design_name}")
                else:
                    # replace all occurences of design_name_from_cdl with design_name in the cdl file
                    with open(netlist, 'r') as file:
                        filedata = file.read()
                    newdata = filedata.replace(design_name_from_cdl, design_name)
                    with open(netlist, 'w') as file:
                        file.write(newdata)
            else:
                print("Warning: Design name not found in the netlist file")
        
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
            self.pdk_files['temp_dir'] = temp_dir_path
            print("using user specified pdk_root, will search for required files in the specified directory")
            self.pdk_files['pdk_root'] = pdk_root 
            
            lvsmag_path = temp_dir_path / f"{design_name}_lvsmag.spice"
            pex_path = temp_dir_path / f"{design_name}_pex.spice"
            sim_path = temp_dir_path / f"{design_name}_sim.spice"
            spice_path = temp_dir_path / f"{design_name}.spice"
            netlist_from_comp = temp_dir_path / f"{design_name}.cdl"
            gds_path = temp_dir_path / f"{design_name}.gds"
            report_path = temp_dir_path / f"{design_name}_lvs.rpt"
            
            if isinstance(layout, Component):
                layout.write_gds(str(gds_path))
                if netlist is None:
                    netlist = layout.info['netlist'].generate_netlist()
                    with open(str(netlist_from_comp), 'w') as f:
                        f.write(netlist)
                else: 
                    if check_if_path_or_net_string(netlist):
                        shutil.copy(netlist, str(netlist_from_comp))
                    else: 
                        with open(str(netlist_from_comp), 'w') as f:
                            f.write(netlist)
            elif isinstance(layout, PathType):            
                shutil.copy(layout, str(gds_path))
                if netlist is None:
                    raise ValueError("Path to cdl (netlist) must be provided if only gds file is provided! Provide Component alternatively!")
                else:
                    if check_if_path_or_net_string(netlist):
                        shutil.copy(netlist, str(netlist_from_comp))
                    else: 
                        with open(str(netlist_from_comp), 'w') as f:
                            f.write(netlist)
                    
            modify_design_name_in_cdl(str(netlist_from_comp), design_name)
            
            lvsschemref_file = self.pdk_files['lvs_schematic_ref_file'] if lvs_schematic_ref_file is None else lvs_schematic_ref_file
        
            
            write_spice(str(netlist_from_comp), str(spice_path), lvsschemref_file)
            
            magic_script_content = f"""
gds flatglob *\\$\\$*
gds read {gds_path}
load {design_name}

select top cell
ext2resist all
extract all
ext2spice lvs
ext2spice extresist on 
ext2spice -o {str(lvsmag_path)}
load {design_name}
ext2sim cthresh 0
ext2sim -o {str(sim_path)}
exit
"""

            with tempfile.NamedTemporaryFile(mode='w', delete=False) as magic_script_file:
                magic_script_file.write(magic_script_content)
                magic_script_path = magic_script_file.name
            
            try:
                
                magicrc_file = self.pdk_files['magic_drc_file'] if magic_drc_file is None else magic_drc_file
                magic_cmd = f"bash -c 'magic -rcfile {magicrc_file} -noconsole -dnull < {magic_script_path}'",
                magic_subproc = subprocess.run(
                    magic_cmd, 
                    shell=True,
                    check=True,
                    capture_output=True
                )
                
                magic_subproc_code = magic_subproc.returncode
                magic_subproc_out = magic_subproc.stdout.decode('utf-8')
                print(magic_subproc_out)
                
                lvssetup_file = self.pdk_files['lvs_setup_tcl_file'] if lvs_setup_tcl_file is None else lvs_setup_tcl_file 
                netgen_command = f'netgen -batch lvs "{str(lvsmag_path)} {design_name}" "{str(spice_path)} {design_name}" {lvssetup_file} {str(report_path)}'
                
                netgen_subproc = subprocess.run(
                    netgen_command,
                    shell=True,
                    check=True, 
                    capture_output=True
                )
                netgen_subproc_code = netgen_subproc.returncode
                netgen_subproc_out = netgen_subproc.stdout.decode('utf-8')
                print(netgen_subproc_out)
                
                result_str = "LVS run succeeded" if netgen_subproc_code == 0 and magic_subproc_code == 0 else "LVS run failed"

                if report_path.is_file():
                    with open(report_path, 'r') as f:
                        num_lines = len(f.readlines())
                        if num_lines > 3:
                            result_str += f"\nErrors found in LVS report: {report_path}"
                            f.seek(0)
                            print(f.read())
                        else:
                            result_str += f"\nNo errors found in LVS report: {report_path}"
                else: 
                    raise ValueError("LVS report not found!")
                # if netgen_subproc_code == 0 and magic_subproc_code == 0:
                #     print("LVS run succeeded, writing report...")
                # else:
                #     raise ValueError("LVS run failed")
            
            finally: 
                os.remove(magic_script_path)
                if os.path.exists(f'{design_name}.ext'):
                    os.remove(f'{design_name}.ext')
                # remove all files with suffix .ext
                for file in os.listdir(temp_dir_path):
                    if file.endswith(".ext"):
                        os.remove(file)
                # copy the report from the temp directory to the specified location
                if output_file_path is not None:
                    dir_name = design_name
                    path_to_dir = Path(__file__).resolve().parents[1]  / "regression" / "lvs" / dir_name
                    if not path_to_dir.exists():
                        path_to_dir.mkdir(parents=True, exist_ok=False)
                    new_output_file_path = path_to_dir / output_file_path
                    if not new_output_file_path.exists():
                        shutil.copy(report_path, path_to_dir / output_file_path)
                    else: 
                        raise ValueError("Output file already exists!")
                    
                if copy_intermediate_files:
                    shutil.copy(lvsmag_path, str(Path.cwd() / f"{design_name}_lvsmag.spice"))  
                    shutil.copy(sim_path, str(Path.cwd() / f"{design_name}_sim.spice"))
                    
        return {'magic_subproc_code': magic_subproc_code, 'netgen_subproc_code': netgen_subproc_code, 'result_str': result_str}
                    
    
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

