##for HSPICE netlist
import function

# import os


def gen_cryo_netlist(ninv, aux1, aux2, srcDir) -> None:
    r_netlist = open(srcDir + "/cryo_ro.v", "r")
    lines = list(r_netlist.readlines())
    w_netlist = open(srcDir + "/cryo_ro.nl.v", "w")
    port = "X"

    netmap1 = function.netmap()  # modify here
    netmap1.get_net("nn", None, 1, int(ninv), 1)
    netmap1.get_net("n0", None, int(ninv), int(ninv), 1)
    netmap1.get_net("na", aux1, 1, 1, 1)
    netmap1.get_net("nb", aux2, 0, int(ninv) - 2, 1)
    netmap1.get_net("ni", None, 0, int(ninv) - 2, 1)
    netmap1.get_net("n1", None, 1, int(ninv) - 1, 1)
    netmap1.get_net("n2", None, 2, int(ninv), 1)
    netmap1.get_net("ng", aux2, 1, 1, 1)

    for line in lines:
        # line = line.replace("nbout", port)
        netmap1.printline(line, w_netlist)

    return
