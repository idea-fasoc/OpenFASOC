All functions, classes, etc have a help docustring. See python help() for specific questions

- [Installation](#installation)
- [Glayout](#glayout)
  - [MappedPDK](#mappedpdk)
    - [Generic Layers](#generic-layers)
    - [Generic Rule Guide](#generic-rule-guide)
    - [Creating a MappedPDK](#creating-a-mappedpdk)
  - [PDK Agnostic Layout, Basics](#pdk-agnostic-layout-basics)
    - [Via Stack Generator](#via-stack-generator)
    - [Routing](#routing)
    - [PDK Agnostic Hierarchical Cells](#pdk-agnostic-hierarchical-cells)
      - [Example 1: via\_array](#example-1-via_array)
      - [Example 2: tapring](#example-2-tapring)
      - [Example 3: fet](#example-3-fet)
  - [Advanced Topics](#advanced-topics)
    - [Cells and PDK.activate()](#cells-and-pdkactivate)
    - [Important GDSFactory Notes and Glayout Utilities](#important-gdsfactory-notes-and-glayout-utilities)
    - [Port Naming Best Practices Guide](#port-naming-best-practices-guide)
      - [PortTree](#porttree)
    - [Snap to 2x grid](#snap-to-2x-grid)
    - [Mimcaps Implementation](#mimcaps-implementation)
    - [DRC](#drc)
    - [LVS, and Labeling Issues](#lvs-and-labeling-issues)
    - [Addressing Complicated Requirments with Default Decorators](#addressing-complicated-requirments-with-default-decorators)
  - [API overview](#api-overview)
- [Natural Language Processing](#natural-language-processing)
  - [Standard Components](#standard-components)
    - [NMOS](#nmos)
    - [PMOS](#pmos)
    - [MIMCAP](#mimcap)
    - [MIMCAP Array](#mimcap-array)
    - [Differential Pair](#differential-pair)
  - [Strict Syntax Commands](#strict-syntax-commands)
    - [Import Command](#import-command)
    - [Create Parameters Command](#create-parameters-command)
    - [Place Command](#place-command)
    - [Move Command](#move-command)
    - [Route Command](#route-command)
  - [Non-Standard Components Which can be Imported](#non-standard-components-which-can-be-imported)
    - [CrossCoupledInverters](#crosscoupledinverters)
  - [StrictSyntax Style Guide](#strictsyntax-style-guide)

# Installation
You must be running python3.10 or later.
- To install the core dependencies, run `python3 -m pip install -r requirements.txt` in the `glayout` directory.
- To install the ML dependencies, run `python3 -m pip install -r requirements.ml.txt`.
- For [Klayout integration](https://gdsfactory.github.io/gdsfactory/notebooks/_2_klayout.html):
  - Open Klayout
  - Go to Tools -> Manage Packages
  - Under "Install New Packages" search for "klive"
  - Install klive and when promoted, select "run macros"

# Glayout
Glayout is a layout automation tool which generates DRC clean circuit layouts for any technology implementing the Glayout framework. Glayout is implemented as an easy-to-install python package. All required Glayout dependencies are available on pypi and are installed automatically from pypi when downloading OpenFASOC. Glayout (being a generic layout automation tool) does not require an installed pdk (just a MappedPDK description, explained below). Glayout is composed of 2 main parts: the generic pdk framework and the circuit generators.
The generic pdk framework allows for describing any pdk in a standardized format. The “pdk” sub-package within Glayout contains all code for the generic pdk class (known as “MappedPDK”) in addition to sky130 and gf180 MappedPDK objects. Because MappedPDK is a python class, describing a technology with a MappedPDK allows for passing the pdk as a python object.
The PDK generic circuit generator programs (also known as cells) are python functions which take as arguments a MappedPDK object and a set of optional layout parameters to produce a DRC clean layout. For example, an nMOS circuit generator (also known as nMOS cell), would require the user to specify a MappedPDK and, optionally, the transistor length, width, number of fingers, etc.

## MappedPDK
There are only two absolute requirements for drawing a layout: a set of drawing layers, and a set of rules governing the geometric dimensions between layers. All CMOS technologies must satisfy these two requirements.
### Generic Layers
Almost all CMOS technologies have some version of basically the same layers, some of which are: “active/diffusion”, ”metal contact”, “metal 1”, “via1”, …etc. The layer description format of tuple(integer, integer) is standard. The idea of a generic layer is to map the standard layer names to a specific tuple(integer, integer) depending on the technology. For example, a generic layer present in most technologies is “metal 2”. The sky130 version of “metal 2” is the integer tuple (68, 20). The gf180 version of “metal 2” is the integer tuple (34,0). Importantly, the designer does not use or care about the value of the integer tuple. The designer only cares about the layer it represents, which they can always access in python from the generic name.
MappedPDK provides the designer with all the generic layers necessary, some of which are: “diffusion”, “dnwell”, “nwell”, “pwell”, “p+s/d”, “n+s/d”, “mcon”...etc. MappedPDK guarantees that regardless of which technology is represented ‘under the hood’ and what the value of the tuple(integer, integer), these layers will be accessible by the same names. The designer can access generic layers using the following syntax (for example):
`MappedPDK.get_glayer(“metal 2”)`
This “get_glayer” instance method of the MappedPDK takes the generic layer name and returns the tuple(integer, integer) specific to the technology. A MappedPDK object supports mappings for all design layers necessary. The BEOL generic layers support a metal stack met1-met5. Because metal stacks and some layers are technology dependent, the MappedPDK contains the “MappedPDK.verify_glayers()” method for verifying the presence of layers. For example, if a technology BEOL contains met1-met2, but a cell requires met3, it is possible for the cell generator to verify at runtime that the technology contains met3.

**BEOL Example Generic Layer Mappings**
| Generic Layer Name | sky130  | gf180  |
| :----------------: | :-----: | :----: |
|        mcon        | (66,44) | (33,0) |
|        met1        | (67,20) | (34,0) |
|        via1        | (67,44) | (35,0) |
|        met2        | (68,20) | (36,0) |


### Generic Rule Guide
Almost all CMOS technologies have some version of basically the same three rules: “min_separation”, “min_enclosure”, and “min_width” (or “width” for via layers). Hundreds of rules arise by prescribing one of these three rules between combinations of layers. For example, there may be a rule which requires a “min_enclosure” between “via1” and “metal 2”. There can also be “self rules” or rules describing a requirement between a layer and itself; most “min_width” rules are self rules. An example of a “self rule” between “metal 2” and “metal 2” would be the “min_width” rule.
The description of CMOS rules provided in the above paragraph fits very well within a mathematical graph. Layers can be thought of as vertices in the graph. Rules describe relationships between layers; rules can be thought of as edges in the graph. A “self rule” can be thought of as a “self edge” in the graph (an edge connecting a vertex to itself). This graph can be described mathematically as an undirected graph.
**figure here of example rule graph**
To greatly simplify the rule graph, context dependent rules (sometimes referred to as lambda rules) are eliminated by taking the worst case value for each rule. This allows the designer to lookup rules without providing any additional context of surrounding layer geometry (usually required for dependent rules).
Rule lookups are performed using the following syntax (for example, rules between metal2 and via1):
`MappedPDK.get_grule(“metal 2”, “via 1”)`
The MappedPDK.get_grule method returns a python dictionary containing all rules between the two layers provided (all edges between the two vertices). The keys are one of the three rule names “min_enclosure”, “min_separation”, or “min_width” / “width” (depending on the context). Furthermore, as an undirected graph, an equivalent lookup for this dictionary is the following syntax:
`MappedPDK.get_grule(“via 1”, “metal 2”)`
For self edges, the following simplified syntax is available:
`MappedPDK.get_grule(“metal 2”, “metal 2”)` or `MappedPDK.get_grule(“metal 2”)`
### Creating a MappedPDK
To create a MappedPDK for an arbitrary technology, the generic layer mapping and the rule deck must be provided. MappedPDK stores generic layers as a python dictionary; the keys are generic layer names and the values are tuple(int, int) layers. Keys must be one of the generic layers listed in the class variable MappedPDK.valid_glayers; this class variable is an attribute which belongs to the MappedPDK type rather than an individual instance of MappedPDK so it should not be modified.
It is up to the programmer to decide which technology layer should be used for each generic layer. For example, the Skywater 130nm technology provides a layer called “local interconnect” which is a Titanium Nitride layer used for local routing. Local interconnect has similar (on order of magnitude) conductivity to the metal layers. The glayout provided sky130 MappedPDK object maps: the generic “metal 1” to the sky130 local interconnect layer, the generic “metal contact” to the sky130 local interconnect contact layer, and the generic “via 1” to the sky130 metal contact layer. Progressing up the BEOL, the sky130 MappedPDK generic metals are actually 1 metal ahead of the real layers that are being used; for example, the generic “metal 2” is actually the sky130 metal 1 layer.
Because there are less than 20 generic layers, MappedPDK requires the programmer to manually define the generic layer python map and pass it to the constructor. However, the generic rules are much more numerous. Glayout provides a utility tool to assist in creating the MappedPDK rule deck. There is a spreadsheet to rule representation conversion program which assists with this.

## PDK Agnostic Layout, Basics
The python layout generators (known as “cell factories”, but sometimes referred to as “cells” or "components" or "component factories") are built on the MappedPDK framework. All cell factories should have the `@cell` decorator which can be imported with
`from gdsfactory.cell import cell`
The MappedPDK.get_glayer and MappedPDK.get_grule methods enable the construction of DRC clean layouts programmatically. However, it is the responsibility of the Cell factory programmer to ensure that the proper rules and layer checks are executed. **The quality of the programmer is the quality of the cell.**
### Via Stack Generator
The only stand alone cell (cell factory which does not call other cell factories) in the glayout package is the via stack. Cell factories generally follow a similar programming procedure, so via stack provides a good introduction to the cell factory structure.
Like all cells, via stack takes as the first argument a MappedPDK object. There are two other required arguments which specify the generic layers to create the via stack between; the order in which these “glayers” (another name for generic layers) are provided does not matter. There are also several optional arguments providing more specific layout control. To explain this cell, the following function call will be assumed:
`via_stack(GF180_MappedPDK, “active”, “metal 3”)` OR  `via_stack(GF180_MappedPDK, “metal 3”, “active”)`
Most cells start by running layer error checking. The via stack must verify that the provided MappedPDK contains both glayers provided and both glayers provided can be routed between. For example, it is usually not possible to route from “nwell” without an “n+s/d” implant, so if one of the layers provided is “nwell”, via stack raises an exception. Additionally, via stack must verify that all layers in between the provided glayers are available in the pdk. In this case, the required glayers are: “active”, “metal contact”, “metal 1”, “via 1”, “metal 2”, via 2”, and “metal 3”. For the passed MappedPDK (GF180), all required glayers are present, but in the case that a glayer is not present, via stack raises an exception.
layer error checking is done with [`pdk.has_required_glayers(glayers_list)`](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/glayout/flow//pdk/mappedpdk.py#L142).
The via stack then loops through these layers, placing them one at a time. To legally size and place each layer, via stack must consider “min_enclosure” and “width” rules for vias and metals. For example, to lay the “active” layer, the “metal contact” “width” and the “metal contact” to “active” “min_enclosure” rules must be considered. To lay the “metal 1” layer, the “min_enclosure” and “width” rules of both the via above and the via below “metal 1” must be considered. The programmer of the generic cells must consider all relevant rules to produce a legal layout. Rules are accessed in cell code using the `MappedPDK.get_grule` method.
### Routing
Routing utilities are required to create complicated hierarchical designs. At the backend of routing is the gdsfactory “Port” object. Fundamentally, ports describe a polygon edge. Ports include center, width, and orientation of the edge, along with other attributes and utility methods. The glayout routing functions operate to create paths between ports.
As described with the via stack example above, the checks and sizings necessary for legal layout are executed in the cell generator. Glayout routing functions do not need to understand cell context; for this reason, routing functions are called “dumb routes”. There are three “dumb route” utilities: straight route, L route, and C route. Dumb routes are simple, but contain optional arguments which allow for precise control over created paths. The default path behavior is easy to predict and will generally make the most reasonable decisions if no direction is provided.
For example, Straight route creates a straight path directly between two ports. If the two provided ports are not collinear or have different orientations, the function will by default route from the first port to the imaginary line stretching perpendicularly from the second port. By default, the route will begin on the same layer as the first port and will lay a via stack if necessary at the second port. If two ports are parallel, Straight route will raise an exception.

**Straight Route Default Behavoir:**
![straight route default behavoir](docs/straight_route_def_beh.png)

L route and C route also create simple paths. L route creates an L shaped route (two straight paths perpendicular) and C route creates a C shaped route (two parallel paths connected by a straight path).
### PDK Agnostic Hierarchical Cells
All cells other than the via stack contain hierarchy. Combining hierarchy and careful routing allows for clean layouts while increasing complexity.
#### Example 1: [via_array](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/glayout/flow/primitives/via_gen.py#L180)
The most basic hierarchical cell is the [via_array](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/glayout/flow/primitives/via_gen.py#L180). Via array is composed of via stacks and has a similar interface to the via stack generator, but additionally accepts a size argument. The array spacing computation is another example of the programmers role in creating DRC clean layout. After error checking, the via array program creates the via stack single element that will be copied to create the array. Then, the generator loops through each layer and uses the gdsfactory component.extract method to get the dimension of that layer in the via stack; The min spacing for that layer is `pdk.get_grule(layer)["min_separation"] + 2*layer_dim`. After looping through the entire array, The maximum seperation is the correct spacing to use.
#### Example 2: [tapring](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/glayout/flow/primitives/guardring.py)
tapring produces a substrate / well tap rectanglular ring that legally enclose a rectangular shape. `gdsfactory.component.rectangular_ring` is used along with glayout [via_array](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/glayout/flow/primitives/via_gen.py#L180). The ring is always of minimum width and legalizing the ring is easy because via_array does most of the work. Special care is taken at the corners to ensure min spacing between adjacent metal layers is not below min_separation. Although not currently implemented, error checking for this ring should check the size is not too small (separation between edges is not legal).
Generators should be made as generic as possible. In this case, tapring can produce either a p-tap or n-tap ring. Glayers are just strings and they can be passed to functions as arguments. Also, you glayer variables can be passed directly to `pdk.get_grule(glayer_var)`.
#### Example 3: [fet](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/glayout/flow/primitives/fet.py)
The most important component factory in glayout is the [multiplier](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/glayout/flow/primitives/fet.py#L61) because it handles the difficult task of creating legal transistors. By passing the source/drain layer (either "p+s/d" or "n+s/d") multiplier code is reused to create nmos and pmos transistors. arrays of multipliers can be created to allow for transistors with several multipliers. read the help docustring for all functions in [fet.py](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/glayout/flow/primitives/fet.py)

## Advanced Topics
The following topics are only neccessary if you want to code with glayout, but are not neccessary for a basic understanding of glayout.
### Cells and PDK.activate()
All cell factories should be decorated with the `@cell` decorator which can be imported from gdsfactory with `from gdsfactory.cell import cell`. You must also call pdk.activate() for cells to correctly work. This is related to caching, gds/oasis write settings, default decorators, etc.
### Important GDSFactory Notes and Glayout Utilities
The GDSFactory API is extremely versatile and there are many useful features. It takes some experience to learn about all features and identify the most useful tools from GDSFactory. GDSFactory serves as the backend GDS manipulation library and as an object oriented tool kit with several useful classes including: Components, Component References, and Ports. There are also common shapes as Components in GDSFactory such as rectangles, circles, rectangular_rings, etc. To automate common tasks that do not fit into GDSFactory, Glayout includes many utility functions. The most important of these functions are also addressed here.
- Components are the GDSFactory implementation of GDS cells. Components contain references to other components (Component Reference). Important methods are included below.
	- Component.name: get or set the name of a Component
	- Component.flatten(): flattens all references in the components
	- Component.remove_layers(): removes some layers from the component and return the modified component
	- Component.extract(): extract some layers from a component and return the modified component
	- Component.ports: dictionary of ports in the component
	- Component.add_ports(): add ports to the component
	- Component.add_padding(): add a layer surrounding the component
	- Component booleans: see the gdsfactory documentation for how to run boolean operations of components.
	- Component.write_gds(): write the gds to disk
	- Component.bbox: return bounding box of the component (xmin,ymin),(xmax,ymax). Glayout has an evaluate_bbox function which return the x and y dimensions of the bbox
	- insertion operator: `ref = Component << Component_to_add`
	- Component.add(): add an one of several types to a Component. (more flexible than << operator)
	- Component.ref()/.ref_center(): return a reference to a component

It is not possible to move Components in GDSFactory. GDSFactory has a Component cache, so moving a component may invalidate the cache, but there are situations where you want to move a component; For these situations, use the glayout [move](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/glayout/flow/pdk/util/comp_utils.py#L24), [movex](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/glayout/flow/pdk/util/comp_utils.py#L63), [movey](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/glayout/flow/pdk/util/comp_utils.py#L73) functions.

- Component references are pointers to components. They have many of the same methods as Components with some additions.
	- ComponentReference.parent: the Component which this component reference points to
	- ComponentReference.movex, movey, move: you can move ComponentReferences
	- ComponentReference.get_ports_list(): get a list of ports in the component.
Ports are edge descriptions.

To add a ComponentReference to a Component, you cannot use the insertion operator. Use the Component.add() method.

- A port describes a single edge of a polygon. The most useful port attributes are **width, center tuple(x,y), orientation (degrees), and layer of the edge**.
    - For example, the rectangle cell factory provided in gdsfactory.components.rectangle returns a Component type with the following port names: e1, e2, e3, e4.
    	- e1=West, e2=North, e3=East, e4=South. The default naming scheme of ports in GDSFactory is not descriptive
    	- use glayout [rename_ports_by_orientation](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/glayout/flow/pdk/util/port_utils.py#L67), [rename_ports_by_list](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/glayout/flow/pdk/util/port_utils.py#L91) functions and see below for port naming best practices guide
    	- glayout [get_orientation](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/glayout/flow/pdk/util/port_utils.py#L124): returns the letter (N,E,S,W) or degrees of orientation of port.  by default returns the one you do not have. see help.
    	- glayout [assert_port_manhattan](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/glayout/flow/pdk/util/port_utils.py#L159): assert that a port or list or ports have orientation N, E, S, or W
    	- glayout [assert_ports_perpindicular](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/glayout/flow/pdk/util/port_utils.py#L181): assert two ports are perpindicular
    	- glayout [set_port_orientation](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/glayout/flow/pdk/util/port_utils.py#L181): return new port which is copy of old port but with new orientation
    	- glayout [set_port_width](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/glayout/flow/pdk/util/port_utils.py#L202): return a new port which is a copy of the old one, but with new width

A very important utility is [align_comp_to_port](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/glayout/flow/pdk/util/comp_utils.py#L83): pass a component or componentReference and a port, and align the component to any edge of the port.

### Port Naming Best Practices Guide
As previously pointed out, the default naming of ports in GDSFactory is not descriptive. By default gdsfactory.components.rectangle returns ports e1 (West port), e2 (North port), e3 (East port), e4 (South port). Additionally, complicated hiearchies can result in thousands of ports, so organizing ports is a neccessity. The below best practices guide should be used to organize ports
- Ports use the "\_" syntax. Think of this like a directory tree for files. Each time you introduce a new level of hiearchy, you should add a prefix + "\_" describing the cell.
	- For example, adding a via_array to the edge of a tapring, you should call
`tapring.add_ports(via_array.get_ports_list(),prefix="topviaarray_")`
	- The port rename functions look for the "\_" syntax. You can NOT use the port rename functions without this syntax.
- The last 2 characters of a port name should "\_" followed by the orientation (N, E, S, or W)
	- you can easily achieve this by calling glayout [`rename_ports_by_orientation`](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/glayout/flow/pdk/util/port_utils.py#L67) before returning a component (just the names end with "\_" before calling this function)
- **USE PORTS**: be sure to correctly add and label ports to components you make because you do not know when they will be used in other cells.

#### PortTree
The [PortTree](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/glayout/flow/pdk/util/port_utils.py#L232) class is designed to assist in finding ports and understanding port structure. Initialize a PortTree by calling [`PortTree(Component or ComponentReference)`](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/glayout/flow/pdk/util/port_utils.py#L245). The PortTree will internally construct a directory tree structure from the Component's ports. You can use [`PortTree.print()`](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/glayout/flow/pdk/util/port_utils.py#L304) to print this whole structure for a nice figure explaining a Component's ports. See the example print output from a via_stack component below:

**PortTree of a via_stack:**
![PortTree example](docs/PortTreeExample.png)

### Snap to 2x grid
All rules (when creating a MappedPDK) and all user provided float arguments must be snapped to 2*grid size. This is because it is possible to center a component. Centering a component which has a dimension on grid may result in off grid polygons. You can snap floating point values to grid easily by calling `pdk.snap_to_2x_grid()`. You should also take care to snap to 2xgrid whenever you see it is neccessary while writing generator code. For example, most generators which take a size(xdim: float, ydim: float) argument should snap to 2xgrid.
The `gf180_mapped` and `sky130_mapped` PDK modules initialize their `grid_size`
to `1e-3` and, when imported, update `gdsfactory.config.CONF.grid_size`

accordingly. If this attribute does not exist, it is created. This ensures a
consistent snap-to-grid behavior across layouts.
### Mimcaps Implementation
Although many technolgies have 2 or more mimcap options, there is currently only 1 mimcap option supported. When creating a mapped pdk, you specify the cap metal layer as a generic layer, but you specify the metal above and metal below the cap met as part of the DRC rule set for `pdk.get_grule("capmet")`. You can access the metal above capmet with `pdk.get_grule(capmet)["capmettop"]`.
### DRC
If the system has klayout installed and you provide a klayout lydrc script for your MappedPDK, you can run DRC from python by calling pdk.drc(Component or GDS). The return value is a boolean (legal or not legal) and a lyrdb (xml format) file is written describing each DRC error. This file can be opened graphically in klayout with the following syntax `klayout layout.gds -m drc.lyrdb`
### LVS, and Labeling Issues
There are no glayers for labeling or pins, all cells are generated without any labels. You can easily add pins to your component manually after glayout write the gds, or by using ports, you can write a function for adding labels and pins. See [sky130_nist_tapeout example function](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/tapeout_and_RL/sky130_nist_tapeout.py#L97).
### Addressing Complicated Requirments with Default Decorators
A python decorator is a function (the decorator) is a function which is called on another function. It can be used to enhance the features of a function. With GDSFactory Pdk (and MappedPDK objects) you can define a default decorator which runs on any cell factory (cell factories must be decorated with the `@cell` decorator). The default decorator you define runs in addition to the `@cell` decorator. The defined default_decorator should accept as argument a Component and return a Component.
This should be used when dealing with PDK specfic requirments that do not fit into the MappedPDK framework. For example, sky130 has a NPC (nitride poly cut) layer which **must** be used wherever licon (local interconnect contact) is laid over poly. It does not make sense to modify MappedPDK to add a generic NPC layer AND modify all cell factories; sky130 is unqiue in this requirment, so modifying MappedPDK/all cell factories would make glayout less generic. Instead, we define a default_decorator [`sky130_add_npc(Component) -> Component`](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/glayout/flow/pdk/sky130_mapped/sky130_add_npc.py). This function uses booleans to add npc anywhere licon is laid over poly (it also joins NPC polygons if they are closer than the NPC min separation rule). Layers and rules in this technology specific function are hard coded because this decorator will only run for sky130 is the active pdk (this is one reason why you must be sure that pdk is activated).

## API overview
This section provides a high-level overview of all functions in glayout. See **docs** (TODO) printed docustrings of all files.


- glayout:
  - generators
    - via_gen.py
      - via_stack: via between any two 'routable' layers
      - via_array: array of via stacks. specify area or num vias desired
    - guardring.py: create a tapring around an enclosed area
    - fet.py
      - multiplier: the basic building block for both n/pfets
      - pfet
      - nfet
    - diff_pair.py: create a common centroid ab ba place diff pair (either n or pfet)
    - opamp.py: create an opamp (TODO: see docs for netlist and general layout plan)
    - mimcap.py
      - mimcap
      - mimcap_array
    - common
      - two_transistor_place.py: two_transistor_place, place two devices in any configuration specified by a string (e.g. aba bab aba)
      - two_transistor_interdigitized.py
        - two_transistor_interdigitized: place two transistor interdigitized
        - two_nfet_interdigitized: a specialization of two_transistor_interdigitized to place specifically nfet
    - routing
      - straight_route: route in a straight line
      - L_route: route in an L shape
      - c_route: rout in a C shape
    - pdk
      - mappedpdk.py: MappedPDK class
      - sky130_mapped_pdk: MappedPDK object for sky130
        - `from glayout.pdk.sky130_mapped import sky130_mapped_pdk`
      - gf180_mapped_pdk: MappedPDK object for gf180
        - `from glayout.pdk.gf180_mapped import gf180_mapped_pdk`
      - util
        - comp_utils.py
          - evaluate_bbox: returns [width, hieght] of a component
          - move: move Component, compref, or Port
          - movex: movex Component, compref, or Port
          - movey: movey Component, compref, or Port
          - align_comp_to_port: move a compref or Component such that it is aligned to a port (also specify how you want to align with `alignment` option).
          - prec_array: create an array of components
          - prec_center: return the amount of x,y translation required to center a component
          - prec_ref_center: return a centered ref of a component
          - get_padding_points_cc: get points of a rectangle which pads (with some extra space optionally) a component. (e.g. lay p+s/d over diffusion with padding=0.2um)
          - to_decimal: convert a float or list of float (or decimal) to python decimal
          - to_float: convert decimal or list of decimal (or float) to python float
        - port_utils.py
        - print_rules.py
        - snap_to_grid.py
        - component_array_create.py
# Natural Language Processing
In addition to python code, there is also natural language capabilities within Glayout. Glayout strictsyntax is a command language for producing analog circuit layout. Component placement in Analog layout is drawing the geometric shapes representing various Components. Routing is the process of connecting these Components by drawing metal lines between them. Glayout strictsyntax allows the designer to place, move, and connect circuit Components without needing to draw them, rather with strictsyntax the designer can describe them in simple words and with simple commands. The Glayout runtime interprets these commands and will automatically place, move, and route the final layout.

To get started with the glayout runtime, you can create a basic run.py script using the following:
```
import argparse
from glayout.syntaxer.dynamic_load import run_session
from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage, interact, and run conversation sessions.")
    parser.add_argument(
        "-l",
        "--load_conversation",
        type=Path,
        help="Specify the file path to load a previous conversation",
    )
    parser.add_argument(
        "-r",
        "--restore_and_exit",
        action='store_true',
        help="Restore the conversation state and exit",
    )
    args = parser.parse_args()
    run_session(args.load_conversation, args.restore_and_exit)
```
By entering `python run.py` with no arguments to the above script you can begin creating layout with the strictsyntax.

Components are predesigned circuits which can be used as building blocks to create larger circuits. Components are highly modular and have many parameters which can be configured when they are placed. Placing a Component is also known as instantiating the Component. Instances must be given a name. The instance name is called the ComponentRef. Components are also hierarchical, meaning that a Component can be made up of many sub-Components. Also, after making a circuit with Glayout, it can be used in the future as a Component in a larger circuit.

Components can be connected together through a process called routing. Components include several Ports. Ports serve as nodes on Components. Ports are used to create connections (also known as routes) between different Components in a circuit. Ports represent the input or output nodes for Components in the layout and act like an interface to the Component. In the geometry of the layout, Ports correspond to edges of nodes.
Ports are accessed through an organized naming syntax. The names correspond to the function of the Port. For example, MOS Field-Effect Transistors (MOSFETs) have three main nodes: drain, gate, and source. Remember, each Port corresponds to an edge in layout, so they always end with a direction indicator. Direction indicators are North (N), East (E), South (S), or West (W). Indicators N, E, S, W are for specifying which edge of the node we are referring to. For example, if we want to refer to the west edge of the drain node, we would use the port name “ComponentRef_drain_W”, replacing ComponentRef with the name of the Component instance.

## Standard Components
There are several existing components which are part of the Glayout runtime. These components are described below and do not require any imports. Note that it is also possible to import other Components.

### NMOS
Nmos is an n-type mosfet transistor. It is also referred to as nmos, n-type, or nfet. It has the following parameters which are configurable when you place the component:
length: a float parameter specifying the transistor length
width: a float parameter specifying the width of a single transistor
fingers: an integer parameter which multiplies the width. For example, if fingers is 3, then the size will be 3 times the width.
multipliers: An integer parameter specifying how many rows of fingers to place. Each row is equivalent to width*fingers in size, so that the total size is multipliers*width*fingers. Default is 1.
with_tie: True or False, specifies if a bulk tie is required. Set this true unless the designer specifies otherwise.
with_substrate_tap: True or False. If True, then add a substrate tap on the very outside perimeter of nmos. Set this to False unless the designer specifies otherwise.
with_dummy: When True, specifies dummy devices should be added to the edges of the transistor. You should set this to True unless the designer specifies otherwise.
with_dnwell: boolean parameter specifying to use deep nwell if True. You should usually set this to False unless the designer specifies otherwise.
rmult: make metal connections within the nmos component wider. Specify this as 1 unless the designer asks to make routing wider or use wider metals.

The main nmos ports correspond to source, gate, and drain nodes. Each underscore in a port name represents a level of hierarchy. For example, we start with the ComponentRef which is the name of the nmos Component instance. Then we specify one of the nodes from drain, gate, or source. Lastly we specify a direction indicator from N, E, S, W. The following are just some examples of the valid nmos ports:
ComponentRef_source_N
ComponentRef_drain_W
ComponentRef_source_E
ComponentRef_gate_S

### PMOS
Pmos is a p-type mosfet transistor. It is also referred to as pmos, pfet or p-type. It has the following parameters which are configurable when you place the component:
length: a float parameter specifying the transistor length
width: a float parameter specifying the width of a single transistor
fingers: an integer parameter which multiplies the width. For example, if fingers is 3, then the size will be 3 times the width.
multipliers: An integer parameter specifying how many rows of fingers to place. Each row is equivalent to width*fingers in size, so that the total size is multipliers*width*fingers. Default is 1.
with_tie: True or False, specifies if a bulk tie is required. Set this true unless the designer specifies otherwise.
with_substrate_tap: True or False. If True, then add a substrate tap on the very outside perimeter of nmos. Set this to False unless the designer specifies otherwise.
with_dummy: When True, specifies dummy devices should be added to the edges of the transistor. You should set this to True unless the designer specifies otherwise.
dnwell: Note that this is different from the nmos “width_dnwell” argument, but it serves a similar purpose. When dnwell is set to True it adds a deep nwell to the pmos transistor. You should set this to False unless the designer specifies otherwise. The designer may say they want triple well isolation, in which case you should set this as True.
rmult: make metal connections within the pmos component wider. Specify this as 1 unless the designer asks to make routing wider or use wider metals.

Here are just some examples of the valid pmos ports:
ComponentRef_gate_S
ComponentRef_source_E
ComponentRef_drain_W

### MIMCAP
The mimcap is a capacitor. The mimcap takes only one argument which can be configured when the component is placed:
size: a tuple of floating point numbers like (2.1, 3.7) denoting the x and y dimension of the capacitor. The default size is (5.0, 5.0)

The mimcap has the following 4 ports:
ComponentRef_top_met_N
ComponentRef_top_met_E
ComponentRef_top_met_S
ComponentRef_top_met_W

### MIMCAP Array
There is also a mimcap_array (also written as mimcap array) which automatically places and routes several mimcaps together. The mimcap_array takes the following parameters:
size: a tuple of floating point numbers denoting the x and y dimension of the capacitor.
columns: the number of columns in the array
rows: the number of rows in the array


### Differential Pair
A differential pair is available, which is referred to as diff_pair or diff pair. The diff_pair is a differential pair Component which is created using 2 nfet Components. The nfet Components are referred to as “A” and “B” respectively. The diff pair has the following configurable parameters:
length: a float parameter specifying the length of all transistor Components part of the diff pair.
width: a float parameter specifying the width of all transistor Components part of the diff pair.
fingers: an integer parameter which modifies the number of fingers in all transistor Components which are part of the diff pair.

The following are just some examples of the valid ports for diff_pair:
ComponentRef_A_source_S
ComponentRef_A_drain_N
ComponentRef_B_source_S
ComponentRef_A_gate_E
ComponentRef_B_drain_W
ComponentRef_B_gate_E

## Strict Syntax Commands
Strict syntax supports the commands listed below. Note I have left square brackets [] around places where specific command calls should fill in information.
### Import Command
Sometimes you want to use Components which are not included in the Glayout runtime. You do this using the import command. The import command automatically searches for the Component path, so you do not need to specify a path. All you need is to specify the Component you want. The general syntax for importing a Component is:
import [Component]
For example, to import a CrossCoupledInvereters, the user could do the following:
import CrossCoupledInverters
### Create Parameters Command
You generally want to make the Components as parameterized as possible so that they are highly modular and customizable. To do this you need to create parameters. You can create parameters with the following general command syntax:
create a [Type] parameter called [ParameterName]
Here are some examples using the create parameter command:
create a float parameter called device_width
create a int parameter called device_fingers
### Place Command
The general syntax for the place command is below. I have left square brackets around names of Components or ComponentRefs or parameters that should be inserted when using the command. When you insert parameters, you can specify them as a comma separated list.
place a [Component] called [ComponentRef] with [parameters]
An example of using the place command is as follows:
place a nmos called m1 with width 1.0, length 2.0, fingers 2, rmult 1, multipliers 3, with_substrate_tap False, with_tie True, with_dummy True, with_dnwell False
The parameter list also supports passing existing parameter names instead of values.
### Move Command
By default all placed Components are centered at the origin. Obviously, if we place more than one ComponentRef we need to move some of them so that they are not overlapping. To emphasize, if more than one ComponentRef is placed, at least one ComponentRef must be moved to avoid overlapping. To do this, use the move command. The move command allows you to specify relative movements relative to other placed ComponentRefs.
The general relative move syntax is as follows:
move [ComponentRef we are moving] [relative direction] [relative to ComponentRef]
Directions include above, below, right, or left.
Here is an example of using relative move (say we have a ComponentRef called m1 and another called m2):
move m1 below m2
### Route Command
Routes are connections between 2 Ports. There are 4 types of routes: straight_route, c_route, L_route, and smart_route. Unless you are very confident, always use smart_route. Only under special circumstances you can specifcy a different route type, but in almost all cases smart_route is the best option. smart_route can almost always optimally route between two ports. There are also some rules you can use to determine the Port orientations. If you are routing between ComponentRefs which are left or right of each other, then select Ports which are on the adjacent sides. If you are routing between ComponentRefs above or below each other, then select Ports that are both on the East side or both on the West side. The general route syntax is as follows:
route between [Port1] and [Port2] using [route_type]
For example, if we have a nmos ComponentRef called m1 which is to the west of a pmos ComponentRef called m2, an example route command to connect the sources of both would be as follows:
route between m1_source_E and m2_source_W using smart_route
Note that the first part of the portname is the ComponentRef name. Also, notice why the E and W ports were chosen. The nmos ComponentRef called m1 is to the left of the pmos ComponentRef called m2, so the sides adjacent to each other are the east side of m1 and west side of m2. If m1 was above m2, then I could have selected both East Ports or both West Ports as follows:
route between m1_source_E and m2_source_E using smart_route
or
route between m1_source_W and m2_source_W using smart_route

## Non-Standard Components Which can be Imported
### CrossCoupledInverters
CrossCoupledInverters is available to use and can be imported with:
import CrossCoupledInverters
The cell is made up of 4 transistor Components. The top two transistors are pfets and the bottom two transistors are nfets.
This cell implements the following prepackage circuit for easy import:
CrossCoupledInverters includes two inverters. Inverters are composed of an nfet and pfet with their gates shorted with each other (the input of an inverter) and their drains shorted with each other (the output of an inverter). The inputs of the inverters are also shorted, with the sources of the nfets shorted with each other and the drains of the pfets shorted with each other. Importing the cell allows for it to be placed without any extra work. The CrossCoupledInverters has the following parameters:
pfet_width: A float parameter specifying the width of the pmos Components
nfet_width: A float parameter specifying the width of the nmos Components
length: A float parameter specifying the length of all transistor Components
numfingers: An int parameter specifying the number of fingers in all transistor Components

The west (or left) inverter generally has the following port naming conventions:
ComponentRef_top,bottom_A_source,drain,gate_N,E,S,W
The west (or right) inverter generally has the following port naming conventions:
ComponentRef_top,bottom_B_source,drain,gate_N,E,S,W
Where top refers to the inverter’s pmos Component and bottom refers to the inverters nmos Component. A or B refers to the inverter, with A representing the west inverter and B representing the east inverter.

## StrictSyntax Style Guide
You should always follow this order of commands when creating a Component with strictsyntax: Start by importing any required Components, then create any required parameters, then place all required ComponentRefs with their respective parameters, then move all ComponentRefs to their final positions relative to one another, and lastly route between ComponentRefs.


