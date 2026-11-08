"""Write the standard-cell library that the netgen LVS schematic netlist includes.

The layout side of LVS is extracted by magic with the PDK's own tech file, so the schematic side must use the
same PDK's standard-cell netlists (libs.ref/<lib>/spice). The platform cdl in common/platforms is an older copy
of those netlists (no sky130_fd_pr__special_nfet_01v8 / special_pfet_01v8_hvt devices in the flip-flops and
latches) plus the generator's own aux cells (HEADER, SLC, dinv1, ...). This keeps every PDK cell from the PDK and
adds only the platform cells that the PDK does not have.
"""

import argparse
import re

parser = argparse.ArgumentParser(description="PDK standard cells + platform-only aux cells for netgen LVS")
parser.add_argument("--pdk", required=True, help="PDK standard-cell spice (libs.ref/<lib>/spice/<lib>.spice)")
parser.add_argument("--platform", required=True, help="platform cdl/spice that also holds the aux cells")
parser.add_argument("--output", "-o", required=True, help="merged spice to write")
args = parser.parse_args()

subckt_re = re.compile(r"^\s*\.subckt\s+(\S+)", re.IGNORECASE)
ends_re = re.compile(r"^\s*\.ends\b", re.IGNORECASE)


def subckts(path):
    cells, order, name = {}, [], None
    with open(path) as f:
        for line in f:
            m = subckt_re.match(line)
            if m:
                name = m.group(1)
                order.append(name)
                cells[name] = [line]
            elif name is not None:
                cells[name].append(line)
                if ends_re.match(line):
                    name = None
    return cells, order


pdk_cells, _ = subckts(args.pdk)
platform_cells, platform_order = subckts(args.platform)
aux = [n for n in platform_order if n not in pdk_cells]

with open(args.pdk) as f:
    pdk_text = f.read()
with open(args.output, "w") as wf:
    wf.write(pdk_text)
    if not pdk_text.endswith("\n"):
        wf.write("\n")
    for n in aux:
        wf.write("\n")
        wf.writelines(platform_cells[n])

print("lvs_std_cells: %d PDK cells from %s, %d platform-only cells (%s) from %s"
      % (len(pdk_cells), args.pdk, len(aux), " ".join(aux), args.platform))
