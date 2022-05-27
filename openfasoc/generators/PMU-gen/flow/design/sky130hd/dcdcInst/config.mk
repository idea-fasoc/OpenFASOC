export DESIGN_NICKNAME = dcdcInst
export DESIGN_NAME = dcdcInst

export PLATFORM    = sky130hd
#export VERILOG_FILES = $(sort $(wildcard ./designs/src/$(DESIGN_NICKNAME)/*.v))

export VERILOG_FILES 		=   $(sort $(wildcard ./design/src/$(DESIGN_NICKNAME)/*.v)) \
								../blocks/$(PLATFORM)/dcdcInst.blackbox.v

export SDC_FILE    		= ./design/$(PLATFORM)/$(DESIGN_NICKNAME)/constraint.sdc

export DIE_AREA   	 	= 0 0 470 310
export CORE_AREA   		= 1 1 469 309

export PDN_CFG 			= ../blocks/$(PLATFORM)/pdn.cfg

export ADDITIONAL_LEFS  	= $(wildcard ../blocks/$(PLATFORM)/lef/*.lef)
export ADDITIONAL_GDS_FILES 	= $(wildcard ../blocks/$(PLATFORM)/gds/*.gds)
export LIB_FILES = $(wildcard ../blocks/$(PLATFORM)/lib/*.lib)
#export ADDITIONAL_CDL_FILE = ../blocks/$(PLATFORM)/spice/auxcell.cdl

#export ADD_NDR_RULE		= 1
#export NDR_RULE_NETS 		= r_VIN
#export NDR_RULE 		= NDR_2W_2S

export MACRO_PLACEMENT = ./design/$(PLATFORM)/$(DESIGN_NICKNAME)/PMU.macro_placement.cfg
export MACRO_EXTENSION = 1
