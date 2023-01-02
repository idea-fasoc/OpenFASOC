import json
import math
import re


# model file contains polynomial coeficients
# for a polynomial which represents max current "x" vs number of transistors in array "f(x)"
def polynomial_output_at_point_from_coefficients(model_coefficients, polynomial_input):
    """Treats model_coefficients as hashtable of polynomial coeficients.
    Produces the output of the polynomial defined by model_coefficients for polynomial_input."""
    N = 0
    coefLength = len(model_coefficients)
    for i in range(coefLength):
        nth_degree_term = coefLength - i - 1
        z = model_coefficients[i]
        N = N + (float(z) * pow(polynomial_input, nth_degree_term))
    polynomial_output = N
    return polynomial_output


def update_ldo_domain_insts(blocksDir, arrSize):
    """Writes arrSize pt unit cell instances to ldo_domain_insts.txt."""
    with open(blocksDir + "/ldo_domain_insts.txt", "w") as ldo_domain_insts:
        # Always write comparator and pmos instances
        ldo_domain_insts.write("cmp1\npmos_1\npmos_2\n")
        # write arrSize pt cells
        for i in range(arrSize):
            ldo_domain_insts.write("{pt_array_unit\[" + str(i) + "\]}\n")


def update_custom_nets(blocksDir, arrSize):
    """Creates custom routes in ldo_custom_net.txt."""
    with open(blocksDir + "/ldo_custom_net.txt", "w") as ldo_domain_insts:
        # Always write comparator and pmos connections
        ldo_domain_insts.write("r_VREG\ncmp1 VREG\npmos_1 VREG\npmos_2 VREG\n")
        # write arrSize pt cells
        for i in range(arrSize):
            ldo_domain_insts.write("{pt_array_unit\[" + str(i) + "\]} VREG\n")


def generate_LDO_verilog(directories, outputDir, designName, arrSize):
    """Writes specialized behavioral verilog to output dir and flow dir."""
    with open(directories["verilogDir"] + "/LDO_TEMPLATE.v", "r") as verilog_template:
        filedata = verilog_template.read()
    filedata = re.sub(
        r"parameter integer ARRSZ = \d+;",
        r"parameter integer ARRSZ = " + str(arrSize) + ";",
        filedata,
    )
    filedata = re.sub(r"module \S+", r"module " + designName + "(", filedata)
    # write verilog src files to output dir and flow dir
    with open(outputDir + "/" + designName + ".v", "w") as verilog_template:
        verilog_template.write(filedata)
    with open(
        directories["flowDir"] + "/design/src/ldo/" + designName + ".v", "w"
    ) as verilog_template:
        verilog_template.write(filedata)


def generate_controller_verilog(directories, outputDir, arrSize):
    """Writes specialized behavioral verilog to output dir and flow dir."""
    # Get ctrl word initialization in hex
    ctrlWordHexCntF = int(math.floor(arrSize / 4.0))
    ctrlWordHexCntR = int(arrSize % 4.0)
    ctrlWordHex = ["h"]
    ctrlWordHex.append(str(hex(pow(2, ctrlWordHexCntR) - 1)[2:]))
    for i in range(ctrlWordHexCntF):
        ctrlWordHex.append("f")
    ctrlWdRst = str(arrSize) + "'" + "".join(ctrlWordHex)

    with open(directories["verilogDir"] + "/LDO_CONTROLLER_TEMPLATE.v", "r") as file:
        filedata = file.read()
    filedata = re.sub(
        r"parameter integer ARRSZ = \d+;",
        r"parameter integer ARRSZ = " + str(arrSize) + ";",
        filedata,
    )
    filedata = re.sub(
        r"wire \[ARRSZ-1:0\] ctrl_rst = \S+",
        r"wire " + "[ARRSZ-1:0] ctrl_rst = " + ctrlWdRst + ";",
        filedata,
    )
    with open(outputDir + "/LDO_CONTROLLER.v", "w") as file:
        file.write(filedata)
    with open(directories["flowDir"] + "/design/src/ldo/LDO_CONTROLLER.v", "w") as file:
        file.write(filedata)


def update_area_and_place_density(flowDir, arrSize):
    """Increases place density for designs with large power transistor arrays."""
    with open(flowDir + "design/sky130hvl/ldo/config.mk", "r") as config_read:
        lines = config_read.readlines()
    # adjust config based on arrSize
    if arrSize in range(1, 51):
        lines[18] = "export DIE_AREA                 = 0 0 270 270\n"
        lines[19] = "export CORE_AREA                = 15 15 255 255\n"
        lines[20] = "export VREG_AREA                = 40 40 230 60\n"
        if arrSize in range(1, 11):
            lines[25] = "export PLACE_DENSITY = 0.30\n"
        elif arrSize in range(11, 21):
            lines[25] = "export PLACE_DENSITY = 0.40\n"
        elif arrSize in range(21, 31):
            lines[25] = "export PLACE_DENSITY = 0.50\n"
        elif arrSize in range(31, 41):
            lines[25] = "export PLACE_DENSITY = 0.60\n"
        elif arrSize in range(41, 51):
            lines[25] = "export PLACE_DENSITY = 0.70\n"
    elif arrSize in range(51, 101):
        lines[18] = "export DIE_AREA                 = 0 0 290 290\n"
        lines[19] = "export CORE_AREA                = 15 15 275 275\n"
        lines[20] = "export VREG_AREA                = 40 40 250 60\n"
        if arrSize in range(51, 61):
            lines[25] = "export PLACE_DENSITY = 0.30\n"
        elif arrSize in range(61, 71):
            lines[25] = "export PLACE_DENSITY = 0.40\n"
        elif arrSize in range(71, 81):
            lines[25] = "export PLACE_DENSITY = 0.50\n"
        elif arrSize in range(81, 91):
            lines[25] = "export PLACE_DENSITY = 0.60\n"
        else:
            lines[25] = "export PLACE_DENSITY = 0.70\n"
    elif arrSize in range(101, 151):
        lines[18] = "export DIE_AREA                 = 0 0 310 310\n"
        lines[19] = "export CORE_AREA                = 15 15 295 295\n"
        lines[20] = "export VREG_AREA                = 40 40 270 60\n"
        if arrSize in range(101, 111):
            lines[25] = "export PLACE_DENSITY = 0.30\n"
        elif arrSize in range(111, 121):
            lines[26] = "export PLACE_DENSITY = 0.40\n"
        elif arrSize in range(121, 131):
            lines[25] = "export PLACE_DENSITY = 0.50\n"
        elif arrSize in range(131, 141):
            lines[25] = "export PLACE_DENSITY = 0.60\n"
        else:
            lines[25] = "export PLACE_DENSITY = 0.70\n"
    elif arrSize in range(151, 201):
        lines[18] = "export DIE_AREA                 = 0 0 330 330\n"
        lines[19] = "export CORE_AREA                = 15 15 315 315\n"
        lines[20] = "export VREG_AREA                = 40 40 290 60\n"
        if arrSize in range(151, 161):
            lines[25] = "export PLACE_DENSITY = 0.30\n"
        elif arrSize in range(161, 171):
            lines[25] = "export PLACE_DENSITY = 0.40\n"
        elif arrSize in range(171, 181):
            lines[25] = "export PLACE_DENSITY = 0.50\n"
        elif arrSize in range(181, 191):
            lines[25] = "export PLACE_DENSITY = 0.60\n"
        else:
            lines[25] = "export PLACE_DENSITY = 0.70\n"
    else:
        lines[18] = "export DIE_AREA                 = 0 0 345 345\n"
        lines[19] = "export CORE_AREA                = 15 15 330 330\n"
        lines[20] = "export VREG_AREA                = 40 40 305 60\n"
        if arrSize in range(201, 211):
            lines[25] = "export PLACE_DENSITY = 0.30\n"
        elif arrSize in range(211, 221):
            lines[25] = "export PLACE_DENSITY = 0.40\n"
        elif arrSize in range(221, 231):
            lines[25] = "export PLACE_DENSITY = 0.50\n"
        elif arrSize in range(231, 241):
            lines[25] = "export PLACE_DENSITY = 0.60\n"
        else:
            lines[25] = "export PLACE_DENSITY = 0.70\n"
    with open(flowDir + "design/sky130hvl/ldo/config.mk", "w") as config_spec:
        config_spec.writelines(lines)
