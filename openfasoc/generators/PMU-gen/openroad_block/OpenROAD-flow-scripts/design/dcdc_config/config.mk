export DESIGN_NICKNAME = dcdc_config
export DESIGN_NAME = dcdc_config

export PLATFORM    = sky130hd

export VERILOG_FILES =  ./designs/$(PLATFORM)/$(DESIGN_NICKNAME)/*.v

export SDC_FILE          = ./designs/$(PLATFORM)/$(DESIGN_NICKNAME)/constraint.sdc

#export ABC_AREA = 1
# These values must be multiples of placement site
export DIE_AREA    = 0.0 0.0 30 40
export CORE_AREA   = 1 1 29 39

export ABC_AREA = 1
export ABC_CLOCK_PERIOD_IN_PS = 10000
export ABC_DRIVER_CELL = sky130_fd_sc_hd__buf_1
export ABC_LOAD_IN_FF = 3


#export POST_SYNTHESYS_RENAMING = ./designs/$(PLATFORM)/coyote_tc/post_synthesis_rename.tcl

# Use custom power grid with core rings offset from the pads
export PDN_CFG = ./designs/$(PLATFORM)/$(DESIGN_NICKNAME)/pdn.cfg

# Point to the RC file
export SETRC_FILE = $(PLATFORM_DIR)/setRC.tcl

export MIN_ROUTING_LAYER met1
export MAX_ROUTING_LAYER met5

#fastroute.tcl - platform
export MACRO_EXTENSION=2

export PLACE_PINS_ARGS= -group_pins {a[0] a[1] a[2] a[3] a[4] a[5]} \
            -group_pins {s[0] s[1] s[2] s[3] s[4] s[5] s[6] s[7] s[8] s[9] s[10] s[11]}
#cdl.tcl
export CDL_FILE=./platforms/$(PLATFORM)/cdl/sky130_fd_sc_hd.spice

export PLACE_DENSITY    = 0.7

# IR drop estimation supply net name to be analyzed and supply voltage variable
# For multiple nets: PWR_NETS_VOLTAGES  = "VDD1 1.8 VDD2 1.2"
export PWR_NETS_VOLTAGES  = "VDD 1.8"
export GND_NETS_VOLTAGES  = "VSS 0.0"
