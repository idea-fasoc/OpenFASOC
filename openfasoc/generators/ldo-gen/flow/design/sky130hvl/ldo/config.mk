export DESIGN_NICKNAME = ldo
export DESIGN_NAME = ldoInst
#export DESIGN_NAME = tempsenseInst_error
export PLATFORM    = sky130hvl
#export VERILOG_FILES = $(sort $(wildcard ./designs/src/$(DESIGN_NICKNAME)/*.v))

# export VERILOG_FILES 		= ./designs/src/$(DESIGN_NICKNAME)/tempsenseInst.v \
#   			  			  ./platforms/$(PLATFORM)/tempsense/tempsenseInst.blackbox.v
export VERILOG_FILES 		= $(sort $(wildcard ./designs/src/$(DESIGN_NICKNAME)/*.v)) \
				  ../blocks/$(PLATFORM)/ldoInst.blackbox.v

export SDC_FILE    		= ./designs/$(PLATFORM)/$(DESIGN_NICKNAME)/constraint.sdc

export DIE_AREA   	 	= 0 0 280 330
export CORE_AREA   		= 15 15 265 315

export VREG_AREA                = 55 40 230 170

# PDN
export PDN_TCL 			= ../blocks/$(PLATFORM)/pdn.tcl

#Placement options
export PLACE_DENSITY = 0.30

# Macro options
export MACRO_PLACE_HALO         = 1 1
export MACRO_PLACE_CHANNEL      = 20 20
export MACRO_PLACEMENT          = ../blocks/$(PLATFORM)/manual_macro.tcl

# keep with gf
export CELL_PAD_IN_SITES_GLOBAL_PLACEMENT = 1
export CELL_PAD_IN_SITES_DETAIL_PLACEMENT = 0

# Additional files
export ADDITIONAL_LEFS  	= ../blocks/$(PLATFORM)/lef/capacitor_test_nf.lef \
                        	  ../blocks/$(PLATFORM)/lef/LDO_COMPARATOR_LATCH.lef \
				  ../blocks/$(PLATFORM)/lef/PMOS.lef \
			   	  ../blocks/$(PLATFORM)/lef/PT_UNIT_CELL.lef \
				  ../blocks/$(PLATFORM)/lef/vref_gen_nmos_with_trim.lef


export ADDITIONAL_GDS  	        = ../blocks/$(PLATFORM)/gds/capacitor_test_nf.gds \
                        	  ../blocks/$(PLATFORM)/gds/LDO_COMPARATOR_LATCH.gds \
				  ../blocks/$(PLATFORM)/gds/PMOS.gds \
			   	  ../blocks/$(PLATFORM)/gds/PT_UNIT_CELL.gds \
				  ../blocks/$(PLATFORM)/gds/vref_gen_nmos_with_trim.gds

#export ADDITIONAL_LIBS		= ../blocks/$(PLATFORM)/lib/capacitor_test_nf.lib \
                                  ../blocks/$(PLATFORM)/lib/LDO_COMPARATOR_LATCH.lib \
                                  ../blocks/$(PLATFORM)/lib/PMOS.lib \
                                  ../blocks/$(PLATFORM)/lib/PT_UNIT_CELL.lib \
                                  ../blocks/$(PLATFORM)/lib/vref_gen_nmos_with_trim.lib

export DOMAIN_INSTS_LIST 	= ../blocks/$(PLATFORM)/ldo_domain_insts.txt

#export CUSTOM_CONNECTION 	= ../blocks/$(PLATFORM)/tempsenseInst_custom_net.txt

export ADD_NDR_RULE		= 1
export NDR_RULE_NETS 		= r_VIN
export NDR_RULE 		= NDR_2W_2S
