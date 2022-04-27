export DESIGN_NICKNAME = dcdc
export DESIGN_NAME = dcdcInst

export PLATFORM    = sky130hs
#export VERILOG_FILES = $(sort $(wildcard ./designs/src/$(DESIGN_NICKNAME)/*.v))

export VERILOG_FILES 		=   $(sort $(wildcard ./design/src/$(DESIGN_NICKNAME)/*.v)) \
								$(sort $(wildcard ./design/src/$(DESIGN_NICKNAME)/*.sv)) \
								../blocks/$(PLATFORM)/dcdcInst.blackbox.v

export SDC_FILE    		= ./design/$(PLATFORM)/$(DESIGN_NICKNAME)/constraint.sdc

export DIE_AREA   	 	= 0 0 1400 1400
export CORE_AREA   		= 10 10 1390 1390

export PDN_CFG 			= ../blocks/$(PLATFORM)/pdn.cfg

export ADDITIONAL_LEFS  	= $(wildcard ../blocks/$(PLATFORM)/lef/*.lef)
export ADDITIONAL_GDS_FILES 	= $(wildcard ../blocks/$(PLATFORM)/gds/*.gds)
export LIB_FILES = $(wildcard ../blocks/$(PLATFORM)/lib/*.lib)

#export ADD_NDR_RULE		= 1
#export NDR_RULE_NETS 		= r_VIN
#export NDR_RULE 		= NDR_2W_2S
