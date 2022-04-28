import re
import subprocess as sp


def run_cryo_sim(simDir, lib_path, dut_path, sc_path) -> None:
    # process 6-stage conv verilog
    with open(simDir + "templates/cryoInst_ngspice.sp", "r") as file:
        filedata = file.read()
        filedata = re.sub(r"@@PATH_TO_LIB", lib_path, filedata)
        filedata = re.sub(r"@@PATH_TO_DUT_SP", dut_path, filedata)
        filedata = re.sub(r"@@PATH_TO_SC_SP", sc_path, filedata)

    with open(simDir + "/cryoInst_ngspice.sp", "w") as file:
        file.write(filedata)

    print("Starting simulation")

    p = sp.Popen(
        [
            "/shared/bin/ngspice",
            "-b",
            "-n",
            "-a",
            "-r",
            "cryoInst.out",
            "cryoInst_ngspice.sp",
        ],
        cwd=simDir,
    )
    p.wait()
