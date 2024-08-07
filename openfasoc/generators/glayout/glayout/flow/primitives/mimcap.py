from gdsfactory.cell import cell
from gdsfactory.component import Component
from gdsfactory.components.rectangle import rectangle
from glayout.flow.pdk.mappedpdk import MappedPDK
from typing import Optional
from glayout.flow.primitives.via_gen import via_array
from glayout.flow.pdk.util.comp_utils import prec_array, to_decimal, to_float
from glayout.flow.pdk.util.port_utils import rename_ports_by_orientation, add_ports_perimeter, print_ports
from pydantic import validate_arguments
from glayout.flow.routing.straight_route import straight_route
from decimal import ROUND_UP, Decimal
from glayout.flow.spice import Netlist

@validate_arguments
def __get_mimcap_layerconstruction_info(pdk: MappedPDK) -> tuple[str,str]:
	"""returns the glayer metal below and glayer metal above capmet
	args: pdk
	"""
	capmettop = pdk.layer_to_glayer(pdk.get_grule("capmet")["capmettop"])
	capmetbottom = pdk.layer_to_glayer(pdk.get_grule("capmet")["capmetbottom"])
	pdk.has_required_glayers(["capmet",capmettop,capmetbottom])
	pdk.activate()
	return capmettop, capmetbottom

def __generate_mimcap_netlist(pdk: MappedPDK, size: tuple[float, float]) -> Netlist:
	return Netlist(
		circuit_name="MIMCap",
		nodes = ['V1', 'V2'],
		source_netlist=""".subckt {circuit_name} {nodes} l=1 w=1
X1 V1 V2 {model} l={{l}} w={{w}}
.ends {circuit_name}""",
		instance_format="X{name} {nodes} {circuit_name} l={length} w={width}",
		parameters={
			'model': pdk.models['mimcap'],
			'length': size[0],
			'width': size[1]
		}
	)

def __generate_mimcap_array_netlist(mimcap_netlist: Netlist, num_caps: int) -> Netlist:
	arr_netlist = Netlist(
		circuit_name="MIMCAP_ARR",
		nodes = ['V1', 'V2']
	)

	for _ in range(num_caps):
		arr_netlist.connect_netlist(
			mimcap_netlist,
			[]
		)

	return arr_netlist

#@cell
def mimcap(
    pdk: MappedPDK, size: tuple[float,float]=(5.0, 5.0)
) -> Component:
    """create a mimcap
    args:
    pdk=pdk to use
    size=tuple(float,float) size of cap
    ****Note: size is the size of the capmet layer
    ports:
    top_met_...all edges, this is the metal over the capmet
    bottom_met_...all edges, this is the metal below capmet
    """
    size = pdk.snap_to_2xgrid(size)
    # error checking and
    capmettop, capmetbottom = __get_mimcap_layerconstruction_info(pdk)
    # create top component
    mim_cap = Component()
    mim_cap << rectangle(size=size, layer=pdk.get_glayer("capmet"), centered=True)
    top_met_ref = mim_cap << via_array(
        pdk, capmetbottom, capmettop, size=size, minus1=True, lay_bottom=False
    )
    bottom_met_enclosure = pdk.get_grule(capmetbottom,"capmet")["min_enclosure"]
    mim_cap.add_padding(layers=(pdk.get_glayer(capmetbottom),),default=bottom_met_enclosure)
    # flatten and create ports
    mim_cap = add_ports_perimeter(mim_cap, layer=pdk.get_glayer(capmetbottom), prefix="bottom_met_")
    mim_cap.add_ports(top_met_ref.get_ports_list())

    component = rename_ports_by_orientation(mim_cap).flatten()

    # netlist generation
    component.info['netlist'] = __generate_mimcap_netlist(pdk, size)

    return component

#@cell
def mimcap_array(pdk: MappedPDK, rows: int, columns: int, size: tuple[float,float] = (5.0,5.0), rmult: Optional[int]=1) -> Component:
	"""create mimcap array
	args:
	pdk to use
	size = tuple(float,float) size of a single cap
	****Note: size is the size of the capmet layer
	ports:
	cap_x_y_top_met_...all edges, this is the metal over the capmet in row x, col y
	cap_x_y_bottom_met_...all edges, this is the metal below capmet in row x, col y
	"""
	capmettop, capmetbottom = __get_mimcap_layerconstruction_info(pdk)
	mimcap_arr = Component()
	# create the mimcap array
	mimcap_single = mimcap(pdk, size)
	mimcap_space = pdk.get_grule("capmet")["min_separation"] #+ evaluate_bbox(mimcap_single)[0]
	array_ref = mimcap_arr << prec_array(mimcap_single, rows, columns, spacing=2*[mimcap_space])
	mimcap_arr.add_ports(array_ref.get_ports_list())
	# create a list of ports that should be routed to connect the array
	port_pairs = list()
	for rownum in range(rows):
		for colnum in range(columns):
			bl_mimcap = f"row{rownum}_col{colnum}_"
			right_mimcap = f"row{rownum}_col{colnum+1}_"
			top_mimcap = f"row{rownum+1}_col{colnum}_"
			for level,layer in [("bottom_met_",capmetbottom),("top_met_",capmettop)]:
				bl_east_port = mimcap_arr.ports.get(bl_mimcap+level+"E")
				r_west_port = mimcap_arr.ports.get(right_mimcap+level+"W")
				bl_north_port = mimcap_arr.ports.get(bl_mimcap+level+"N")
				top_south_port = mimcap_arr.ports.get(top_mimcap+level+"S")
				if rownum == rows-1 and colnum == columns-1:
					continue
				elif rownum == rows-1:
					port_pairs.append((bl_east_port,r_west_port,layer))
				elif colnum == columns-1:
					port_pairs.append((bl_north_port,top_south_port,layer))
				else:
					port_pairs.append((bl_east_port,r_west_port,layer))
					port_pairs.append((bl_north_port,top_south_port,layer))
	for port_pair in port_pairs:
		mimcap_arr << straight_route(pdk,port_pair[0],port_pair[1],width=rmult*pdk.get_grule(port_pair[2])["min_width"])

	# add netlist
	mimcap_arr.info['netlist'] = __generate_mimcap_array_netlist(mimcap_single.info['netlist'], rows * columns)

	return mimcap_arr.flatten()


