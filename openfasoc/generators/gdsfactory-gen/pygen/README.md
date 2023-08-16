All functions, classes, etc have a help docustring. See python help() for specific questions

- [Pygen](#pygen)
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
		- [Important GDSFactory Notes and Pygen Utilities](#important-gdsfactory-notes-and-pygen-utilities)
		- [Port Naming Best Practices Guide](#port-naming-best-practices-guide)
		- [Snap to 2x grid](#snap-to-2x-grid)
		- [Mimcaps Implementation](#mimcaps-implementation)
		- [DRC](#drc)
		- [LVS, and Labeling Issues](#lvs-and-labeling-issues)
		- [Addressing Complicated Requirments with Default Decorators](#addressing-complicated-requirments-with-default-decorators)


# Pygen
Pygen is a layout automation tool which generates DRC clean circuit layouts across many technologies. Pygen is implemented as an easy-to-install python package. All required Pygen dependencies are available on pypi and are installed automatically from pypi when downloading OpenFASOC. Pygen (being a generic layout automation tool) does not require an installed pdk (just a MappedPDK description—explained below). Pygen is composed of 2 main parts: the generic pdk framework and the circuit generators.  
The generic pdk framework allows for describing any pdk in a standardized format. The “pdk” sub-package within Pygen contains all code for the generic pdk class (known as “MappedPDK”) in addition to sky130 and gf180 MappedPDK objects. Because MappedPDK is a python class, describing a technology with a MappedPDK allows for passing the pdk as a python object.  
The PDK generic circuit generator programs (also known as cells) are python functions which take as arguments a MappedPDK object and a set of optional layout parameters to produce a DRC clean layout. For example, an nMOS circuit generator (also known as nMOS cell), would require the user to specify a MappedPDK and, optionally, the transistor length, width, number of fingers, etc.

## MappedPDK  
There are only two absolute requirements for drawing a layout: a set of drawing layers, and a set of rules governing the geometric dimensions between layers. All CMOS technologies must satisfy these two requirements.  
### Generic Layers
Almost all CMOS technologies have some version of basically the same layers, some of which are: “active/diffusion”, ”metal contact”, “metal 1”, “via1”, …etc. The layer description format of tuple(integer, integer) is standard. The idea of a generic layer is to map the standard layer names to a specific tuple(integer, integer) depending on the technology. For example, a generic layer present in most technologies is “metal 2”. The sky130 version of “metal 2” is the integer tuple (68, 20). The gf180 version of “metal 2” is the integer tuple (34,0). Importantly, the designer does not use or care about the value of the integer tuple. The designer only cares about the layer it represents, which they can always access in python from the generic name.  
MappedPDK provides the designer with all the generic layers necessary, some of which are: “diffusion”, “dnwell”, “nwell”, “pwell”, “p+s/d”, “n+s/d”, “mcon”...etc. MappedPDK guarantees that regardless of which technology is represented ‘under the hood’ and what the value of the tuple(integer, integer), these layers will be accessible by the same names. The designer can access generic layers using the following syntax (for example):  
`MappedPDK.get_glayer(“metal 2”)`  
This “get_glayer” instance method of the MappedPDK takes the generic layer name and returns the tuple(integer, integer) specific to the technology. A MappedPDK object supports mappings for all design layers necessary. The BEOL generic layers support a metal stack met1-met5. Because metal stacks and some layers are technology dependent, the MappedPDK contains the “MappedPDK.verify_glayers()” method for verifying the presence of layers. For example, if a technology BEOL contains met1-met2, but a cell requires met3, it is possible for the cell generator to verify at runtime that the technology contains met3.

**BEOL Example Generic Layer Mappings**
| Generic Layer Name | sky130 | gf180 |
| :-: | :-: | :-: |
|mcon| (66,44) | (33,0) |
|met1| (67,20) | (34,0) |
|via1| (67,44) | (35,0) |
|met2| (68,20) | (36,0) |


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
It is up to the programmer to decide which technology layer should be used for each generic layer. For example, the Skywater 130nm technology provides a layer called “local interconnect” which is a Titanium Nitride layer used for local routing. Local interconnect has similar (on order of magnitude) conductivity to the metal layers. The pygen provided sky130 MappedPDK object maps: the generic “metal 1” to the sky130 local interconnect layer, the generic “metal contact” to the sky130 local interconnect contact layer, and the generic “via 1” to the sky130 metal contact layer. Progressing up the BEOL, the sky130 MappedPDK generic metals are actually 1 metal ahead of the real layers that are being used; for example, the generic “metal 2” is actually the sky130 metal 1 layer.  
Because there are less than 20 generic layers, MappedPDK requires the programmer to manually define the generic layer python map and pass it to the constructor. However, the generic rules are much more numerous. Pygen provides a utility tool to assist in creating the MappedPDK rule deck. There is a spreadsheet to rule representation conversion program which assists with this. 

## PDK Agnostic Layout, Basics
The python layout generators (known as “cell factories”, but sometimes referred to as “cells” or "components" or "component factories") are built on the MappedPDK framework. All cell factories should have the `@cell` decorator which can be imported with  
`from gdsfactory.cell import cell`   
The MappedPDK.get_glayer and MappedPDK.get_grule methods enable the construction of DRC clean layouts programmatically. However, it is the responsibility of the Cell factory programmer to ensure that the proper rules and layer checks are executed. **The quality of the programmer is the quality of the cell.**
### Via Stack Generator
The only stand alone cell (cell factory which does not call other cell factories) in the pygen package is the via stack. Cell factories generally follow a similar programming procedure, so via stack provides a good introduction to the cell factory structure.  
Like all cells, via stack takes as the first argument a MappedPDK object. There are two other required arguments which specify the generic layers to create the via stack between; the order in which these “glayers” (another name for generic layers) are provided does not matter. There are also several optional arguments providing more specific layout control. To explain this cell, the following function call will be assumed:  
`via_stack(GF180_MappedPDK, “active”, “metal 3”)` OR  `via_stack(GF180_MappedPDK, “metal 3”, “active”)`  
Most cells start by running layer error checking. The via stack must verify that the provided MappedPDK contains both glayers provided and both glayers provided can be routed between. For example, it is usually not possible to route from “nwell” without an “n+s/d” implant, so if one of the layers provided is “nwell”, via stack raises an exception. Additionally, via stack must verify that all layers in between the provided glayers are available in the pdk. In this case, the required glayers are: “active”, “metal contact”, “metal 1”, “via 1”, “metal 2”, via 2”, and “metal 3”. For the passed MappedPDK (GF180), all required glayers are present, but in the case that a glayer is not present, via stack raises an exception.  
layer error checking is done with [`pdk.has_required_glayers(glayers_list)`](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/pygen/pdk/mappedpdk.py#L142).  
The via stack then loops through these layers, placing them one at a time. To legally size and place each layer, via stack must consider “min_enclosure” and “width” rules for vias and metals. For example, to lay the “active” layer, the “metal contact” “width” and the “metal contact” to “active” “min_enclosure” rules must be considered. To lay the “metal 1” layer, the “min_enclosure” and “width” rules of both the via above and the via below “metal 1” must be considered. The programmer of the generic cells must consider all relevant rules to produce a legal layout. Rules are accessed in cell code using the `MappedPDK.get_grule` method.
### Routing
Routing utilities are required to create complicated hierarchical designs. At the backend of routing is the gdsfactory “Port” object. Fundamentally, ports describe a polygon edge. Ports include center, width, and orientation of the edge, along with other attributes and utility methods. The pygen routing functions operate to create paths between ports.  
As described with the via stack example above, the checks and sizings necessary for legal layout are executed in the cell generator. Pygen routing functions do not need to understand cell context; for this reason, routing functions are called “dumb routes”. There are three “dumb route” utilities: straight route, L route, and C route. Dumb routes are simple, but contain optional arguments which allow for precise control over created paths. The default path behavior is easy to predict and will generally make the most reasonable decisions if no direction is provided.   
For example, Straight route creates a straight path directly between two ports. If the two provided ports are not collinear or have different orientations, the function will by default route from the first port to the imaginary line stretching perpendicularly from the second port. By default, the route will begin on the same layer as the first port and will lay a via stack if necessary at the second port. If two ports are parallel, Straight route will raise an exception.

**Straight Route Default Behavoir:**
![straight route default behavoir](docs/straight_route_def_beh.png)  

L route and C route also create simple paths. L route creates an L shaped route (two straight paths perpendicular) and C route creates a C shaped route (two parallel paths connected by a straight path).  
### PDK Agnostic Hierarchical Cells
All cells other than the via stack contain hierarchy. Combining hierarchy and careful routing allows for clean layouts while increasing complexity. 
#### Example 1: [via_array](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/pygen/via_gen.py#L180)
The most basic hierarchical cell is the [via_array](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/pygen/via_gen.py#L180). Via array is composed of via stacks and has a similar interface to the via stack generator, but additionally accepts a size argument. The array spacing computation is another example of the programmers role in creating DRC clean layout. After error checking, the via array program creates the via stack single element that will be copied to create the array. Then, the generator loops through each layer and uses the gdsfactory component.extract method to get the dimension of that layer in the via stack; The min spacing for that layer is `pdk.get_grule(layer)["min_separation"] + 2*layer_dim`. After looping through the entire array, The maximum seperation is the correct spacing to use.  
#### Example 2: [tapring](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/pygen/guardring.py)
tapring produces a substrate / well tap rectanglular ring that legally enclose a rectangular shape. `gdsfactory.component.rectangular_ring` is used along with pygen [via_array](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/pygen/via_gen.py#L180). The ring is always of minimum width and legalizing the ring is easy because via_array does most of the work. Special care is taken at the corners to ensure min spacing between adjacent metal layers is not below min_separation. Although not currently implemented, error checking for this ring should check the size is not too small (separation between edges is not legal).  
Generators should be made as generic as possible. In this case, tapring can produce either a p-tap or n-tap ring. Glayers are just strings and they can be passed to functions as arguments. Also, you glayer variables can be passed directly to `pdk.get_grule(glayer_var)`.
#### Example 3: [fet](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/pygen/fet.py)
The most important component factory in pygen is the [multiplier](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/pygen/fet.py#L61) because it handles the difficult task of creating legal transistors. By passing the source/drain layer (either "p+s/d" or "n+s/d") multiplier code is reused to create nmos and pmos transistors. arrays of multipliers can be created to allow for transistors with several multipliers. read the help docustring for all functions in [fet.py](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/pygen/fet.py)

## Advanced Topics
The following topics are only neccessary if you want to code with pygen, but are not neccessary for a basic understanding of pygen.
### Cells and PDK.activate()
All cell factories should be decorated with the `@cell` decorator which can be imported from gdsfactory with `from gdsfactory.cell import cell`. You must also call pdk.activate() for cells to correctly work. This is related to caching, gds/oasis write settings, default decorators, etc.
### Important GDSFactory Notes and Pygen Utilities
The GDSFactory API is extremely versatile and there are many useful features. It takes some experience to learn about all features and identify the most useful tools from GDSFactory. GDSFactory serves as the backend GDS manipulation library and as an object oriented tool kit with several useful classes including: Components, Component References, and Ports. There are also common shapes as Components in GDSFactory such as rectangles, circles, rectangular_rings, etc. To automate common tasks that do not fit into GDSFactory, Pygen includes many utility functions. The most important of these functions are also addressed here.  
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
	- Component.bbox: return bounding box of the component (xmin,ymin),(xmax,ymax). Pygen has an evaluate_bbox function which return the x and y dimensions of the bbox
	- insertion operator: `ref = Component << Component_to_add`
	- Component.add(): add an one of several types to a Component. (more flexible than << operator)
	- Component.ref()/.ref_center(): return a reference to a component

It is not possible to move Components in GDSFactory. GDSFactory has a Component cache, so moving a component may invalidate the cache, but there are situations where you want to move a component; For these situations, use the pygen [move](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/pygen/pdk/util/custom_comp_utils.py#L146), [movex](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/pygen/pdk/util/custom_comp_utils.py#L185), [movey](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/pygen/pdk/util/custom_comp_utils.py#L195) functions.

- Component references are pointers to components. They have many of the same methods as Components with some additions.
	- ComponentReference.parent: the Component which this component reference points to
	- ComponentReference.movex, movey, move: you can move ComponentReferences
	- ComponentReference.get_ports_list(): get a list of ports in the component.
Ports are edge descriptions.

To add a ComponentReference to a Component, you cannot use the insertion operator. Use the Component.add() method.

- A port describes a single edge of a polygon. The most useful port attributes are **width, center tuple(x,y), orientation (degrees), and layer of the edge**. 
    - For example, the rectangle cell factory provided in gdsfactory.components.rectangle returns a Component type with the following port names: e1, e2, e3, e4.
    	- e1=West, e2=North, e3=East, e4=South. The default naming scheme of ports in GDSFactory is not descriptive
    	- use pygen [rename_ports_by_orientation](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/pygen/pdk/util/custom_comp_utils.py#L65), [rename_ports_by_list](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/pygen/pdk/util/custom_comp_utils.py#L89) functions and see below for port naming best practices guide
    	- pygen [get_orientation](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/pygen/pdk/util/custom_comp_utils.py#L205): returns the letter (N,E,S,W) or degrees of orientation of port.  by default returns the one you do not have. see help.
    	- pygen [assert_is_manhattan](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/pygen/pdk/util/custom_comp_utils.py#L240): assert that a port or list or ports have orientation N, E, S, or W
    	- pygen [assert_ports_perpindicular](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/pygen/pdk/util/custom_comp_utils.py#L251): assert two ports are perpindicular
    	- pygen [set_orientation](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/pygen/pdk/util/custom_comp_utils.py#L262): return new port which is copy of old port but with new orientation
    	- pygen [set_port_width](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/pygen/pdk/util/custom_comp_utils.py#L283): return a new port which is a copy of the old one, but with new width

A very important utility is [align_comp_to_port](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/pygen/pdk/util/custom_comp_utils.py#L300): pass a component or componentReference and a port, and align the component to any edge of the port.

### Port Naming Best Practices Guide
As previously pointed out, the default naming of ports in GDSFactory is not descriptive. By default gdsfactory.components.rectangle returns ports e1 (West port), e2 (North port), e3 (East port), e4 (South port). Additionally, complicated hiearchies can result in thousands of ports, so organizing ports is a neccessity. The below best practices guide should be used to organize ports
- Ports use the "\_" syntax. Think of this like a directory tree for files. Each time you introduce a new level of hiearchy, you should add a prefix + "\_" describing the cell. 
	- For example, adding a via_array to the edge of a tapring, you should call
`tapring.add_ports(via_array.get_ports_list(),prefix="topviaarray_")`
	- The port rename functions look for the "\_" syntax. You can NOT use the port rename functions without this syntax.
- The last 2 characters of a port name should "\_" followed by the orientation (N, E, S, or W)
	- you can easily achieve this by calling pygen [`rename_ports_by_orientation`](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/pygen/pdk/util/custom_comp_utils.py#L42) before returning a component (just the names end with "\_" before calling this function)
- **USE PORTS**: be sure to correctly add and label ports to components you make because you do not know when they will be used in other cells. 
### Snap to 2x grid
All rules (when creating a MappedPDK) and all user provided float arguments must be snapped to 2*grid size. This is because it is possible to center a component. Centering a component which has a dimension on grid may result in off grid polygons. You can snap floating point values to grid easily by calling `pdk.snap_to_2x_grid()`
### Mimcaps Implementation
Although many technolgies have 2 or more mimcap options, there is currently only 1 mimcap option supported. When creating a mapped pdk, you specify the cap metal layer as a generic layer, but you specify the metal above and metal below the cap met as part of the DRC rule set for `pdk.get_grule("capmet")`. You can access the metal above capmet with `pdk.get_grule(capmet)["capmettop"]`.
### DRC
If the system has klayout installed and you provide a klayout lydrc script for your MappedPDK, you can run DRC from python by calling pdk.drc(Component or GDS). The return value is a boolean (legal or not legal) and a lyrdb (xml format) file is written describing each DRC error. This file can be opened graphically in klayout with the following syntax `klayout layout.gds -m drc.lyrdb`
### LVS, and Labeling Issues
There are no glayers for labeling or pins, all cells are generated without any labels. You can easily add pins to your component manually after pygen write the gds, or by using ports, you can write a function for adding labels and pins. See [sky130_nist_tapeout example function](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/sky130_nist_tapeout.py#L97). 
### Addressing Complicated Requirments with Default Decorators
A python decorator is a function (the decorator) is a function which is called on another function. It can be used to enhance the features of a function. With GDSFactory Pdk (and MappedPDK objects) you can define a default decorator which runs on any cell factory (cell factories must be decorated with the `@cell` decorator). The default decorator you define runs in addition to the `@cell` decorator. The defined default_decorator should accept as argument a Component and return a Component.  
This should be used when dealing with PDK specfic requirments that do not fit into the MappedPDK framework. For example, sky130 has a NPC (nitride poly cut) layer which **must** be used wherever licon (local interconnect contact) is laid over poly. It does not make sense to modify MappedPDK to add a generic NPC layer AND modify all cell factories; sky130 is unqiue in this requirment, so modifying MappedPDK/all cell factories would make pygen less generic. Instead, we define a default_decorator [`sky130_add_npc(Component) -> Component`](https://github.com/alibillalhammoud/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/pygen/pdk/sky130_mapped/sky130_add_npc.py). This function uses booleans to add npc anywhere licon is laid over poly (it also joins NPC polygons if they are closer than the NPC min separation rule). Layers and rules in this technology specific function are hard coded because this decorator will only run for sky130 is the active pdk (this is one reason why you must be sure that pdk is activated).