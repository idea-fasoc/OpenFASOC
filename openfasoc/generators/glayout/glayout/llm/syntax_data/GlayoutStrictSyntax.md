# What is Glayout strict syntax
Glayout strictsyntax is a command language for producing analog circuit layout. Analog circuit layout is the process of drawing the geometry and shapes of the final masks which will be sent to a fabrication factory for production. Component placement in Analog layout is drawing the geometric shapes representing various Components. Routing is the process of connecting these Components by drawing metal lines between them. Glayout strictsyntax allows the designer to place, move, and connect circuit Components without needing to draw them, rather with strictsyntax the designer can describe them in simple words and with simple commands. The Glayout runtime interprets these commands and will automatically place, move, and route the final layout.

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
