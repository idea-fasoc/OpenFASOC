export DESIGN_NICKNAME = ldo
export DESIGN_NAME = ldoInst
#export DESIGN_NAME = tempsenseInst_error
export PLATFORM    = sky130hvl
#export VERILOG_FILES = $(sort $(wildcard ./designs/src/$(DESIGN_NICKNAME)/*.v))

# export VERILOG_FILES 		= ./designs/src/$(DESIGN_NICKNAME)/tempsenseInst.v \
#   			  			  ./platforms/$(PLATFORM)/tempsense/tempsenseInst.blackbox.v
export VERILOG_FILES 		= $(sort $(wildcard ./design/src/$(DESIGN_NICKNAME)/*.v)) \
				  ../blocks/$(PLATFORM)/ldoInst.blackbox.v

export SDC_FILE    		= ./design/$(PLATFORM)/$(DESIGN_NICKNAME)/constraint.sdc

export DIE_AREA   	 	= 0 0 320 320
export CORE_AREA   		= 10 10 310 310

#export VD1_AREA                 = 33.58 32.64 64.86 62.56

export PDN_CFG 			= ../blocks/$(PLATFORM)/pdn.cfg

export ADDITIONAL_LEFS  	= ../blocks/$(PLATFORM)/lef/capacitor_test_nf.lef \
                        	  ../blocks/$(PLATFORM)/lef/LDO_COMPARATOR_LATCH.lef \
				  ../blocks/$(PLATFORM)/lef/PMOS.lef \
			   	  ../blocks/$(PLATFORM)/lef/PT_UNIT_CELL.lef \
				  ../blocks/$(PLATFORM)/lef/vref_gen_nmos_with_trim.lef


export ADDITIONAL_GDS_FILES  	= ../blocks/$(PLATFORM)/gds/capacitor_test_nf.gds \
                        	  ../blocks/$(PLATFORM)/gds/LDO_COMPARATOR_LATCH.gds \
				  ../blocks/$(PLATFORM)/gds/PMOS.gds \
			   	  ../blocks/$(PLATFORM)/gds/PT_UNIT_CELL.gds \
				  ../blocks/$(PLATFORM)/gds/vref_gen_nmos_with_trim.gds

#export ADDITIONAL_LIBS		= ../blocks/$(PLATFORM)/lib/capacitor_test_nf.lib \
                                  ../blocks/$(PLATFORM)/lib/LDO_COMPARATOR_LATCH.lib \
                                  ../blocks/$(PLATFORM)/lib/PMOS.lib \
                                  ../blocks/$(PLATFORM)/lib/PT_UNIT_CELL.lib \
                                  ../blocks/$(PLATFORM)/lib/vref_gen_nmos_with_trim.lib

export DOMAIN_INSTS_LIST 	= ../blocks/$(PLATFORM)/tempsenseInst_domain_insts.txt

export CUSTOM_CONNECTION 	= ../blocks/$(PLATFORM)/tempsenseInst_custom_net.txt

export ADD_NDR_RULE		= 1
export NDR_RULE_NETS 		= r_VIN
export NDR_RULE 		= NDR_2W_2S
