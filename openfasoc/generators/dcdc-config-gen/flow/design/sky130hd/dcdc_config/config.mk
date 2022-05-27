export DESIGN_NICKNAME = dcdc_config
export DESIGN_NAME = dcdc_config

export PLATFORM    = sky130hd
#export VERILOG_FILES = $(sort $(wildcard ./designs/src/$(DESIGN_NICKNAME)/*.v))

export VERILOG_FILES 		=   $(sort $(wildcard ./design/src/$(DESIGN_NICKNAME)/*.v))
#								$(sort $(wildcard ./design/src/$(DESIGN_NICKNAME)/*.sv)) \
#								../blocks/$(PLATFORM)/*.v

export SDC_FILE    		= ./design/$(PLATFORM)/$(DESIGN_NICKNAME)/constraint.sdc

export DIE_AREA   	 	= 0 0 50 40
export CORE_AREA   		= 1 1 49 39

export PDN_CFG 			= ../blocks/$(PLATFORM)/pdn.cfg

export PLACE_DENSITY    = 0.99

# export ADDITIONAL_LEFS  	= $(wildcard ../blocks/$(PLATFORM)/lef/*.lef)
# export ADDITIONAL_GDS_FILES 	= $(wildcard ../blocks/$(PLATFORM)/gds/*.gds)
# export LIB_FILES = $(wildcard ../blocks/$(PLATFORM)/lib/*.lib)
# export ADDITIONAL_CDL_FILE = ../blocks/$(PLATFORM)/spice/auxcell.cdl

#export ADD_NDR_RULE		= 1
#export NDR_RULE_NETS 		= r_VIN
#export NDR_RULE 		= NDR_2W_2S
