Scripts not in OpenROAD-flow-scripts, created for use within the OpenROAD flow in OpenFASOC.

### Scripts part of the flow:

- `add_ndr_rules.tcl`: adds NDR rules before global route
- `create_custom_connections.tcl`: connects instances to specified net before global route
- `pre_global_route.tcl`: script called before global route in OpenROAD (PRE_GLOBAL_ROUTE env var)
- `read_domain_instances.tcl`: adds instances to voltage domain after floorplan
- `create_routable_power_net.tcl`: creates the r_VIN net in the design, allowing for multi-voltage domain routes

### Custom scripts:

-`custom_place.tcl`: procedures for placing cells arbitrarily
