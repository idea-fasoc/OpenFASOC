export DESIGN_NICKNAME = NON_CLK_GEN
export DESIGN_NAME = NON_CLK_GEN

export PLATFORM    = sky130hd

export VERILOG_FILES =  ./designs/$(PLATFORM)/$(DESIGN_NICKNAME)/NON_CLK_GEN.v

export SDC_FILE          = ./designs/$(PLATFORM)/$(DESIGN_NICKNAME)/constraint.sdc

# These values must be multiples of placement site
export DIE_AREA    = 0.0 0.0 35 40
export CORE_AREA   = 2 2 34 39

#ABC settings
export ABC_AREA = 1
export ABC_CLOCK_PERIOD_IN_PS = 200000
export ABC_DRIVER_CELL = sky130_fd_sc_hd__buf_1
export ABC_LOAD_IN_FF = 3

#keep hierachy cell
export PRESERVE_CELLS = DCDC_BUFFER MUX4 inverterchain_4 DCDC_DIGITAL_NOISE_INJECTION NON_CLK_NOISE_LFSR2 NON_CLK_NOISE_LFSR1
# DCDC_NOV_CLKGEN MUX4 inverterchain_4 DCDC_BUFFER
# 						DCDC_DIGITAL_NOISE_INJECTION NON_CLK_NOISE_LFSR2
# 						NON_CLK_NOISE_LFSR1

#export POST_SYNTHESYS_RENAMING = ./designs/$(PLATFORM)/coyote_tc/post_synthesis_rename.tcl

# Use custom power grid with core rings offset from the pads
export PDN_CFG = ./designs/$(PLATFORM)/$(DESIGN_NICKNAME)/pdn.cfg

# Point to the RC file
export SETRC_FILE = $(PLATFORM_DIR)/setRC.tcl

export MIN_ROUTING_LAYER met1
export MAX_ROUTING_LAYER met5

#fastroute.tcl - platform
#export MACRO_EXTENSION=2

#io_placement.tcl
export PLACE_PINS_ARGS= -group_pins {clk1 clk1b clk0 clk0b} \
             -group_pins {clk clk_in} \
             -group_pins {control rst_n}

#cdl.tcl
export CDL_FILE=./platforms/$(PLATFORM)/cdl/sky130_fd_sc_hd.spice

export PLACE_DENSITY    = 0.7

# IR drop estimation supply net name to be analyzed and supply voltage variable
# For multiple nets: PWR_NETS_VOLTAGES  = "VDD1 1.8 VDD2 1.2"
export PWR_NETS_VOLTAGES  = "VDD 1.8"
export GND_NETS_VOLTAGES  = "VSS 0.0"
