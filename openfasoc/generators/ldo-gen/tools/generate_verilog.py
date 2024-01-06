import math

INCLUDE_2_PMOS_ARRSIZE = int(40)

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

        ldo_domain_insts.write("cmp1\npmos_1\n")
        # The below code is commented since pmos_2 is commented in the Verilog
        # if arrSize > INCLUDE_2_PMOS_ARRSIZE:
        #     ldo_domain_insts.write("pmos_2\n")

        # write arrSize pt cells
        for i in range(arrSize):
            ldo_domain_insts.write("{pt_array_unit\[" + str(i) + "\]}\n")

def update_ldo_place_insts(blocksDir, arrSize):
    """Writes arrSize pt unit cell instances to ldo_domain_insts.txt."""
    with open(blocksDir + "/ldo_place.txt", "w") as ldo_place_insts:
        # write arrSize pt cells
        for i in range(arrSize):
            ldo_place_insts.write(
                "{pt_array_unit\\\["
                + str(i)
                + "\\\]} {pt_array_unit\["
                + str(i)
                + "\]}\n"
            )


def update_custom_nets(blocksDir, arrSize):
    """Creates custom routes in ldo_custom_net.txt."""
    with open(blocksDir + "/ldo_custom_net.txt", "w") as ldo_domain_insts:
        # Always write comparator and pmos connections
        ldo_domain_insts.write("r_VREG\ncmp1 VREG\npmos_1 VREG\n")

        # The below code is commented since pmos_2 is commented in the Verilog
        # if arrSize > INCLUDE_2_PMOS_ARRSIZE:
        #     ldo_domain_insts.write("pmos_2 VREG\n")

        # write arrSize pt cells
        for i in range(arrSize):
            ldo_domain_insts.write("{pt_array_unit\[" + str(i) + "\]} VREG\n")


def get_ctrl_wd_rst(arrSize):
    """Returns the value of the ctrlWdRst parameter used in the Verilog source."""
    # Get ctrl word initialization in hex
    ctrlWordHexCntF = int(math.floor(arrSize / 4.0))
    ctrlWordHexCntR = int(arrSize % 4.0)
    ctrlWordHex = ["h"]
    ctrlWordHex.append(str(hex(pow(2, ctrlWordHexCntR) - 1)[2:]))
    for i in range(ctrlWordHexCntF):
        ctrlWordHex.append("f")
    ctrlWdRst = str(arrSize) + "'" + "".join(ctrlWordHex)

    return ctrlWdRst


def update_area_and_place_density(flowDir, arrSize):
    """Increases place density for designs with large power transistor arrays."""
    with open(flowDir + "design/sky130hvl/ldo/config_template.mk", "r") as config:
        config_template = config.read()
    die_length = die_width = 275 + 20 * int(arrSize / 50)
    core_length = core_width = 260 + 20 * int(arrSize / 50)
    vreg_width = die_width - 39

    place_density = round(0.3 + 0.1 * math.ceil((arrSize%50)/10),1)

    config_template = config_template.replace("@PARAM_DIE_WIDTH", str(die_width), 1)
    config_template = config_template.replace("@PARAM_DIE_LENGTH", str(die_length), 1)
    config_template = config_template.replace("@PARAM_CORE_WIDTH", str(core_width), 1)
    config_template = config_template.replace("@PARAM_CORE_LENGTH", str(core_length), 1)
    config_template = config_template.replace("@PARAM_VREG_WIDTH", str(vreg_width), 2)

    config_template = config_template.replace(
        "@PARAM_PLACE_DENSITY", str(place_density), 1
    )
    with open(flowDir + "design/sky130hvl/ldo/config.mk", "w") as config:
        config.write(config_template)
