#not a real clk
set sdc_version 2.1
set_units -time ns -resistance kOhm -capacitance pF -voltage V -current mA
create_clock [get_ports clk] -name "CLK" -period 0
set_operating_conditions tt_025C_1v80 -library sky130_fd_sc_hd__tt_025C_1v80
set_driving_cell -lib_cell sky130_fd_sc_hd__buf_2 [get_ports clk_in]
set_driving_cell -lib_cell sky130_fd_sc_hd__buf_2 [get_ports clk]
set_driving_cell -lib_cell sky130_fd_sc_hd__buf_2 [get_ports rst_n]
set_driving_cell -lib_cell sky130_fd_sc_hd__buf_2 [get_ports control]
# set_max_fanout 50 [current_design]
set_load -pin_load 9.667 [get_ports clk0]
set_load -pin_load 9.667 [get_ports clk0b]
set_load -pin_load 9.667 [get_ports clk1]
set_load -pin_load 9.667 [get_ports clk1b]
# group_path -name output_grp1  -to [list [get_ports clk0] [get_ports clk0b]]
# group_path -name output_grp2  -to [list [get_ports clk1] [get_ports clk1b]]
