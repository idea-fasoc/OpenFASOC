set_global_routing_layer_adjustment $::env(MIN_ROUTING_LAYER)-$::env(MAX_ROUTING_LAYER) 0.5

set_global_routing_layer_pitch 2 0.37
set_global_routing_layer_pitch 3 0.48
set_global_routing_layer_pitch 4 0.74
set_global_routing_layer_pitch 5 0.96
set_global_routing_layer_pitch 6 3.33

global_route -guide_file $::env(RESULTS_DIR)/route.guide \
          -layers $::env(MIN_ROUTING_LAYER)-$::env(MAX_ROUTING_LAYER) \
          -unidirectional_routing \
          -overflow_iterations 100 \
	      -verbose 2 \
