# reduces the routing resources of all routing layers by 30%
set_global_routing_layer_adjustment * 0.3

set_routing_layers -signal $::env(MIN_ROUTING_LAYER)-$::env(MAX_ROUTING_LAYER)

if {[info exist env(MACRO_EXTENSION)]} {
  set_macro_extension $::env(MACRO_EXTENSION)
}
