export DESIGN_NICKNAME = dcdcInst
export DESIGN_NAME     = dcdcInst
export PLATFORM        = sky130hd

# export VERILOG_FILES_BLACKBOX =
export VERILOG_FILES = ./designs/src/$(DESIGN_NICKNAME)/$(DESIGN_NICKNAME).v \
                       ./designs/src/$(DESIGN_NICKNAME)/$(DESIGN_NICKNAME).blackbox.v

export SDC_FILE          = ./designs/$(PLATFORM)/$(DESIGN_NICKNAME)/constraint.sdc
#export BLOCKS = DCDC_COMP dcdc_config DCDC_DAC NON_CLK_GEN six_stage_conv
export PDN_CFG = ./designs/$(PLATFORM)/$(DESIGN_NICKNAME)/pdn.cfg
# export TAPCELL_TCL =

export ABC_AREA = 1
export ABC_CLOCK_PERIOD_IN_PS = 10000
export ABC_DRIVER_CELL = sky130_fd_sc_hd__buf_1
export ABC_LOAD_IN_FF = 3

export SDC_FILE      = ./designs/$(PLATFORM)/$(DESIGN_NICKNAME)/constraint.sdc

export DIE_AREA   = 0 0 1380 1800
export CORE_AREA  = 1 1 1379 1799

export dcdcInst_DIR = ./designs/$(PLATFORM)/$(DESIGN_NICKNAME)

export ADDITIONAL_GDS_FILES  = $(dcdcInst_DIR)/gds/DCDC_COMP.gds \
                               $(dcdcInst_DIR)/gds/dcdc_config.gds \
                               $(dcdcInst_DIR)/gds/DCDC_DAC.gds \
                               $(dcdcInst_DIR)/gds/NON_CLK_GEN.gds \
                               $(dcdcInst_DIR)/gds/six_stage_conv.gds \
                               $(dcdcInst_DIR)/gds/DCDC_CLKGATE.gds \
                               $(dcdcInst_DIR)/gds/DCDC_FF.gds \
                               $(dcdcInst_DIR)/gds/DCDC_INVERTER.gds

export ADDITIONAL_LEFS  = $(dcdcInst_DIR)/lef/DCDC_COMP.lef \
                          $(dcdcInst_DIR)/lef/dcdc_config.lef \
                          $(dcdcInst_DIR)/lef/DCDC_DAC.lef \
                          $(dcdcInst_DIR)/lef/NON_CLK_GEN.lef \
                          $(dcdcInst_DIR)/lef/six_stage_conv.lef \
                          $(dcdcInst_DIR)/lef/NOISE_INJECTION.lef \
                          $(dcdcInst_DIR)/lef/DCDC_CLKGATE.lef \
                          $(dcdcInst_DIR)/lef/DCDC_FF.lef \
                          $(dcdcInst_DIR)/lef/DCDC_INVERTER.lef

export MACRO_PLACEMENT = $(dcdcInst_DIR)/dcdcInst.macro_placment.cfg
export MACRO_EXTENSION = 1
export MIN_ROUTING_LAYER met1
export MAX_ROUTING_LAYER met5

export PLACE_PINS_ARGS= -group_pins {D[0] D[1] D[2] D[3] D[4] D[5]} \
                        -group_pins {noise_D[0] noise_D[1] noise_D[2] noise_D[3]} \
                        -group_pins {config_in[0] config_in[1] config_in[2] config_in[3] config_in[4] config_in[5]} \
                        -group_pins {non_clk_rst_n non_clk_control} \
                        -group_pins {Noise_in DAC_RST} \
                        -group_pins {clk clk_noise} \
                        -group_pins {VREF_in VREF_out} \
                        -group_pins {VOUT}

#pdn rail
# export FP_PDN_RAIL_WIDTH = 0.48
# export FP_PDN_RAIL_OFFSET = 0
export PLACE_DENSITY    = 0.5

#cdl.tcl
# export CDL_FILE=./platforms/$(PLATFORM)/cdl/sky130_fd_sc_hd.spice
# IR drop estimation supply net name to be analyzed and supply voltage variable
# For multiple nets: PWR_NETS_VOLTAGES  = "VDD1 1.8 VDD2 1.2"
export PWR_NETS_VOLTAGES  = "VDD 1.8"
export GND_NETS_VOLTAGES  = "VSS 0.0"

# export MIN_ROUTING_LAYER met1
# export MAX_ROUTING_LAYER met5
