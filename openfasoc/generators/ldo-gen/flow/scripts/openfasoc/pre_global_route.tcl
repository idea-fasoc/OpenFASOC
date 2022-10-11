#Create custom net
source $::env(SCRIPTS_DIR)/openfasoc/create_rVREG.tcl

# NDR rules
source $::env(SCRIPTS_DIR)/openfasoc/add_ndr_rules.tcl

# Custom connections
source $::env(SCRIPTS_DIR)/openfasoc/create_custom_connections.tcl
if {[info exist ::env(CUSTOM_CONNECTION)]} {
  create_custom_connections $::env(CUSTOM_CONNECTION)
}
