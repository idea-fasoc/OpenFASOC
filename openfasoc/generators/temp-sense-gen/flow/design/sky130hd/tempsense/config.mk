export DESIGN_NICKNAME = tempsense
export DESIGN_NAME = tempsenseInst_error
#export DESIGN_NAME = tempsenseInst_error
export PLATFORM    = sky130hd
#export VERILOG_FILES = $(sort $(wildcard ./designs/src/$(DESIGN_NICKNAME)/*.v))

# export VERILOG_FILES 		= ./designs/src/$(DESIGN_NICKNAME)/tempsenseInst.v \
#   			  			  ./platforms/$(PLATFORM)/tempsense/tempsenseInst.blackbox.v
export VERILOG_FILES 		= $(sort $(wildcard ./design/src/$(DESIGN_NICKNAME)/*.v)) \
			  	  ../blocks/$(PLATFORM)/tempsenseInst.blackbox.v
export SDC_FILE    		= ./design/$(PLATFORM)/$(DESIGN_NICKNAME)/constraint.sdc

export DIE_AREA   	 	= 0 0 155.48 146.88
export CORE_AREA   		= 18.4 16.32 137.08 130.56

export VD1_AREA                 = 33.58 32.64 64.86 62.56

export PDN_CFG 			= ../blocks/$(PLATFORM)/pdn.cfg

export ADDITIONAL_LEFS  	= ../blocks/$(PLATFORM)/lef/HEADER.lef \
                        	  ../blocks/$(PLATFORM)/lef/SLC.lef

export ADDITIONAL_GDS_FILES 	= ../blocks/$(PLATFORM)/gds/HEADER.gds \
			      	  ../blocks/$(PLATFORM)/gds/SLC.gds

export DOMAIN_INSTS_LIST 	= ../blocks/$(PLATFORM)/tempsenseInst_domain_insts.txt

export CUSTOM_CONNECTION 	= ../blocks/$(PLATFORM)/tempsenseInst_custom_net.txt

export ADD_NDR_RULE		= 1
export NDR_RULE_NETS 		= r_VIN
export NDR_RULE 		= NDR_2W_2S
