export DESIGN_NICKNAME = cryo
export DESIGN_NAME = cryoInst

export PLATFORM    = sky130hs
#export VERILOG_FILES = $(sort $(wildcard ./designs/src/$(DESIGN_NICKNAME)/*.v))

export VERILOG_FILES 		= $(sort $(wildcard ./design/src/$(DESIGN_NICKNAME)/*.v))

export SDC_FILE    		= ./design/$(PLATFORM)/$(DESIGN_NICKNAME)/constraint.sdc

export DIE_AREA   	 	= 0 0 96 34
export CORE_AREA   		= 2.32 2.32 93.68 31.68

export PDN_CFG 			= ../blocks/$(PLATFORM)/pdn.cfg

# export ADDITIONAL_LEFS  	= ../blocks/$(PLATFORM)/lef/HEADER.lef \
#                         	  ../blocks/$(PLATFORM)/lef/SLC.lef

# export ADDITIONAL_GDS_FILES 	= ../blocks/$(PLATFORM)/gds/HEADER.gds \
# 			      	  ../blocks/$(PLATFORM)/gds/SLC.gds

# export DOMAIN_INSTS_LIST 	= ../blocks/$(PLATFORM)/$(DESIGN_NAME)_domain_insts.txt

# export CUSTOM_CONNECTION 	= ../blocks/$(PLATFORM)/$(DESIGN_NAME)_custom_net.txt

#export ADD_NDR_RULE		= 1
#export NDR_RULE_NETS 		= r_VIN
#export NDR_RULE 		= NDR_2W_2S


# RO inverter placement config

# this is the floorplan dimension for the RO, <W,H>, this should be sufficiently large to allow padding between cells
export RO_CORE_DIM = 48,30
# this is the array dimension for RO inverters, <W,H>, values should be Even, the total number of inverters is W*H
export RO_ARRAY_DIM = 18,8
# this is the cell dimension, <W,H>, use the Site's dimension
export RO_CELL_DIM = 0.48,3.33
# this is the offset from lower left corner of core to the rirst RO placement, <W,H>, W and H values should be >=1 multiples of RO_CELL_DIM respectfullly
export RO_OFFSET = 2.88,3.33
