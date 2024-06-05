from os.path import join, dirname
from typing import Union, Optional
from copy import deepcopy

import re

class Netlist:
	"""Represents a SPICE netlist/subcircuit."""

	circuit_name: str = ""
	"""Name of the subcircuit."""
	nodes: list[str] = []
	"""List of nodes in the subcircuit."""
	global_nodes: list[str] = []
	"""List of the global nodes in the subcircuit."""

	designs_dir: str = join(dirname(__file__), 'designs')
	"""Path to the src/designs/ directory."""

	source_netlist: str = ""
	"""The source SPICE subcircuit (template) for the subcircuit. [Mako](https://makotemplates.org) templating syntax is supported."""
	instance_format: str = "X{name} {nodes} {circuit_name}"
	"""The format for the SPICE instantiation. Uses the Python string formatting syntax. `self.parameters`, `nodes`, `name`, and `circuit_name` are available parameters."""
	spice_netlist: str = ""
	"""The generated SPICE netlist."""

	sub_netlists: list['Netlist']
	"""List of the sub-netlists."""
	netlist_connections: list[list[str]]
	"""2D matrix of interconnections of the sub-netlists.

	The row and column number in the matrix represent the indices of the connected sub-netlists. The value represents the name of the wire connecting the nodes.
	"""

	# Variable to determine how many wires were created
	wire_index: int = 0
	"""The index of the next interconnection wire.

	The wires for interconnecting sub-netlists are named `wire{wire_index}`. This index is incremented each time a sub-netlist connection is made.
	"""

	parameters: dict = {}
	"""Dictionary of the high-level parameters."""

	def __init__(self, source_netlist: str = '', nodes: list[str] = [], circuit_name: Union[str, None] = None, instance_format: Optional[str] = None, parameters: dict = {}, sub_netlists: list['Netlist'] = []):
		"""Initializes a Netlist object.

		Override to load sub-netlists and parameters on initialization.
		"""
		self.parameters = {**self.parameters, **parameters}

		self.sub_netlists = []
		self.netlist_connections = []
		self.source_netlist = source_netlist
		self.nodes = nodes

		if circuit_name != None:
			self.circuit_name = circuit_name
		else:
			self.circuit_name = self.extract_subckt_name(self.source_netlist)

		if instance_format != None:
			self.instance_format = instance_format

		self.add_netlists(sub_netlists)

	def extract_subckt_name(self, netlist: str) -> str:
		"""Extracts the subcircuit name from the source SPICE."""
		for line in netlist.split('\n'):
			if line.count('subckt') != 0:
				return line.split(' ')[1]

		return 'Netlist'

	def generate_instance(self, name: Optional[str] = None, nodes: Optional[list[str]] = None, instance_format: Optional[str] = None) -> str:
		"""Generates an instance of the netlist subcircuit.
		Override to insert parameters in the instance.
		"""
		if name == None:
			name = self.circuit_name

		if instance_format == None:
			instance_format = self.instance_format

		if nodes == None:
			nodes = self.nodes

		params = {
			**self.generate_source_netlist_params(),
			'nodes': ' '.join(nodes),
			'name': name
		}

		return instance_format.format(**params)

	def read_source_netlist(self, netlist_src: str) -> str:
		"""Reads a source SPICE subcircuit template from a SPICE file. [Mako](https://makotemplates.org) templating syntax is supported in the source SPICE netlist."""
		self.source_netlist = open(join(self.designs_dir, netlist_src)).read()
		return self.source_netlist

	def connect_subnets(
		self,
		net1: Union[int, 'Netlist'],
		net2: Union[int, 'Netlist'],
		node_mapping: list[tuple[str, str]]
	):
		"""Adds a connection between two sub-netlists.

		Parameters:
			- `net1`: The netlist to connect. Either a reference to the Netlist object or it's index in the `sub_netlists` list.
			- `net2`: The netlist to connect to. Either a reference to the Netlist object or it's index in the `sub_netlists` list.
			- `node_mapping`: A list of 2-element tuples representing the connections between nodes of the netlists. The first element in the tuple is the name of the node of `net1` and the second value is the name of the node in `net2` to connect to.
		"""
		for mapping in node_mapping:
			node1, node2 = mapping

			net1_index = net1 if type(net1) == int else self.sub_netlists.index(net1)
			net2_index = net2 if type(net2) == int else self.sub_netlists.index(net2)

			netlist1 = self.sub_netlists[net1_index]
			netlist2 = self.sub_netlists[net2_index]

			node1_index = netlist1.nodes.index(node1)
			node2_index = netlist2.nodes.index(node2)

			connection_wire = ""
			# if one of the nodes is already connected, then use that wire instead of creating a new wire
			if re.match("^wire[\d]+$", self.netlist_connections[net1_index][node1_index]):
				connection_wire = self.netlist_connections[net1_index][node1_index]

			elif re.match("^wire[\d]+$", self.netlist_connections[net2_index][node2_index]):
				connection_wire = self.netlist_connections[net2_index][node2_index]

			else:
				connection_wire = f"wire{self.wire_index}"
				self.wire_index += 1

			self.netlist_connections[net1_index][node1_index] = connection_wire
			self.netlist_connections[net2_index][node2_index] = connection_wire


	def connect_node(
		self,
		net: Union[int, 'Netlist'],
		node_mapping: list[tuple[str, str]]
	):
		"""Connects a sub-netlist to a top-level node.

		Parameters:
		- `net`: The sub-netlist to connect. Either a reference to the Netlist object or it's index in the `sub_netlists` list.
		- `node_mapping`: A list of 2-element tuples representing the connections between the netlist nodes and the top-level nodes. The first element in the tuple is the name of the node of `net` and the second value is the name of the top-level to connect to.
		"""
		net_index = net if type(net) == int else self.sub_netlists.index(net)

		for mapping in node_mapping:
			net_node, top_level_node = mapping

			net = self.sub_netlists[net_index]
			node_index = net.nodes.index(net_node)

			self.netlist_connections[net_index][node_index] = top_level_node

	def add_netlists(self, netlists: list['Netlist']):
		"""Adds sub-netlists.

		Parameters:
		- `netlists`: A list of Netlist objects to add.
		"""
		for netlist in netlists:
			self.sub_netlists.append(netlist)
			self.netlist_connections.append(netlist.nodes.copy())

	def connect_netlist(self, netlist: 'Netlist', node_mapping: list[tuple[str, str]]) -> int:
		"""Adds a sub-netlist and connects it to top-level nodes.

		Parameters:
		- `netlist`: The netlist object to add.
		- `node_mapping`: A list of 2-element tuples representing the connections between the netlist nodes and the top-level nodes. The first element in the tuple is the name of the node of `netlist` and the second value is the name of the top-level to connect to.
		"""
		self.add_netlists([deepcopy(netlist)])
		netlist_index = len(self.sub_netlists) - 1

		self.connect_node(net=netlist_index, node_mapping=node_mapping)

		return netlist_index

	def generate_source_netlist_params(self, circuit_name: Optional[str] = None) -> dict:
		"""Generates the parameters to be inserted in the source SPICE netlist. Uses the Python template string format."""
		return {
			'circuit_name': circuit_name if circuit_name != None else self.circuit_name,
			'nodes': ' '.join(self.nodes),
			**self.parameters
		}

	def __generate_self_subcircuit(self, prefix: str = '', suffix: str = '', with_pins: bool = True) -> str:
		"""Generates the top-level SPICE subcircuit directive.
		The name of the subcircuit is set by `self.circuit_name`.
		"""
		generated_circuit_name = f"{prefix}{self.circuit_name}{suffix}"

		if self.source_netlist != "":
			return self.source_netlist.format(**self.generate_source_netlist_params(generated_circuit_name))

		elif len(self.sub_netlists) > 0:
			if with_pins:
				main_circuit = f".subckt {generated_circuit_name} {' '.join(self.nodes)}\n"
			else:
				main_circuit = f".subckt {generated_circuit_name}\n"
    
			for i, netlist in enumerate(self.sub_netlists):
				main_circuit += netlist.generate_instance(str(i), self.netlist_connections[i]) + "\n"

			main_circuit += f".ends {generated_circuit_name}"

			return main_circuit

		else:
			return ""

	def get_subcircuits_netlist_map(self, sub_netlists_only = False) -> dict[str, list['Netlist']]:
		"""Generates a list of all the unique SPICE subcircuits directives used in the netlist."""
		subcircuits = dict()

		# Get sub netlists' subcircuits
		for netlist in self.sub_netlists:
			subnetlist_subcircuits = netlist.get_subcircuits_netlist_map()

			# For each subnetlists' subcircuit
			for subckt in subnetlist_subcircuits:
				subckt_netlists = subnetlist_subcircuits[subckt]

				if subckt not in subcircuits:
					# If it is unique, create an entry in the dict
					subcircuits[subckt] = [*subckt_netlists]
				else:
					# If it is not unique, append the netlists to the dict
					subcircuits[subckt] += subckt_netlists


		if not sub_netlists_only:
			self_subckt = self.__generate_self_subcircuit()
			if self_subckt not in subcircuits:
				subcircuits[self_subckt] = [self]

		return subcircuits

	def get_global_nodes_list(self) -> set[str]:
		"""Generates a list of unique global nodes used in the netlist."""
		global_nodes = set()

		for netlist in self.sub_netlists:
			global_nodes.update(netlist.global_nodes)

		global_nodes.update(set(self.global_nodes))

		return global_nodes

	def generate_netlist(self, only_subcircuits: bool = False, with_pins: bool = True) -> str:
		"""Generates the final SPICE netlist for the design.

		The final netlist is a set of SPICE subcircuit directives and global directives. The top-level subcircuit is set by `self.circuit_name`.

		Parameters:
		- `only_subcircuits`: Only generates the subcircuit directives if set to `True`. (Default: `False`)
		"""

		# GENERATE UNIQUE SUBCIRCUIT DiRECTIVES
		subcircuits_netlist_map = self.get_subcircuits_netlist_map(sub_netlists_only=True)

		subcircuit_suffixes = dict()
		# Get the unique netlists' list and set their suffixes
		for subckt in subcircuits_netlist_map:
			netlists = subcircuits_netlist_map[subckt]
			# All of these subcircuits will have the same name, so use any one
			subckt_name = netlists[0].circuit_name

			if subckt_name in subcircuit_suffixes:
				# If a suffix exists, use it and increment it
				for netlist in netlists: netlist.circuit_name = f"{netlist.circuit_name}_{subcircuit_suffixes[subckt_name]}"
				subcircuit_suffixes[subckt_name] += 1
			else:
				# If a suffix doesn't exist, create it.
				subcircuit_suffixes[subckt_name] = 1

		unique_subcircuits_list = []
		# Generate all the unique subcircuits (generation is done again since suffixes were updated)
		for subckt in subcircuits_netlist_map:
			unique_subcircuits_list.append(
				# Use any one since all will be equal
				subcircuits_netlist_map[subckt][0].__generate_self_subcircuit()
			)
		# /GENERATE UNIQUE SUBCIRCUIT DiRECTIVES

		# GENERATE THE FINAL NETLIST
		subcircuits = '\n\n'.join(unique_subcircuits_list)
		main_circuit = self.__generate_self_subcircuit(with_pins=with_pins)
		global_nodes = ' '.join(self.get_global_nodes_list())

		self.spice_netlist = "" 

		if len(global_nodes) > 0 and not only_subcircuits: self.spice_netlist += f".global {global_nodes}\n\n"

		self.spice_netlist += subcircuits + "\n\n"
		self.spice_netlist += main_circuit
		# /GENERATE THE FINAL NETLIST

		return self.spice_netlist
