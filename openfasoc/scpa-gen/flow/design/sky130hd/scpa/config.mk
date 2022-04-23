export DESIGN_NICKNAME = scpa
export DESIGN_NAME = scpa
export PLATFORM    = sky130hd
export VERILOG_FILES 		= $(sort $(wildcard ./design/src/$(DESIGN_NICKNAME)/*.v)) \
			  	  ../blocks/$(PLATFORM)/scpa.blackbox.v
export SDC_FILE    		= ./design/$(PLATFORM)/$(DESIGN_NICKNAME)/constraint.sdc

#export PLACE_DENSITY            := 0.7
#export DENSITY_PENALTY            = 0.000001
#export DENSITY_PENALTY            = 0
#export DIE_AREA   	 	= 0 0 155.48 146.88
#export CORE_AREA   		= 18.4 16.32 137.08 130.56

#export VD1_AREA                 = 33.58 32.64 64.86 62.56

#export DIE_AREA   	 	= 0 0 10000 10000
#export CORE_AREA   		= 50 50 8000 8000

#export VD1_AREA                 = 80 80 3500 3500

export DIE_AREA   	 	= 0 0 30 30
export CORE_AREA   		= 5 5 20 20

export VD1_AREA                 = 10 10 15 15

#export PDN_CFG 			= ../blocks/$(PLATFORM)/pdn.cfg

export ADDITIONAL_LEFS  	= ../blocks/$(PLATFORM)/lef/mimcaptut.lef

export ADDITIONAL_GDS_FILES 	= ../blocks/$(PLATFORM)/gds/mimcaptut.gds

#export DOMAIN_INSTS_LIST 	= ../blocks/$(PLATFORM)/tempsenseInst_domain_insts.txt

#export CUSTOM_CONNECTION 	= ../blocks/$(PLATFORM)/tempsenseInst_custom_net.txt

export ADD_NDR_RULE		= 1
export NDR_RULE_NETS 		= r_VIN
export NDR_RULE 		= NDR_2W_2S
