# Create r_VIN net
source $::env(SCRIPTS_DIR)/openfasoc/create_routable_power_net.tcl
create_routable_power_net "VIN" $::env(VIN_ROUTE_CONNECTION_POINTS)

# Custom connections
source $::env(SCRIPTS_DIR)/openfasoc/create_custom_connections.tcl
if {[info exist ::env(CUSTOM_CONNECTION)]} {
  create_custom_connections $::env(CUSTOM_CONNECTION)
}
