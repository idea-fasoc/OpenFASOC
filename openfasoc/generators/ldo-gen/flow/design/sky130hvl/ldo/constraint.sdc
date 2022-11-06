
set clk_name  core_clock
set clk_port_name clk
set clk_period $::env(CLK_PERIOD_IN_NS)

set clk_port [get_ports $clk_port_name]

create_clock -name $clk_name -period $clk_period $clk_port

# set_dont_touch  [get_cells {temp_analog_0, temp_analog_1}]
