export DESIGN_NICKNAME = cryo
export DESIGN_NAME = cryoInst

export PLATFORM    = sky130osu15Tls
#export VERILOG_FILES = $(sort $(wildcard ./designs/src/$(DESIGN_NICKNAME)/*.v))

export VERILOG_FILES 		= $(sort $(wildcard ./design/src/$(DESIGN_NICKNAME)/*.v))

export SDC_FILE    		= ./design/$(PLATFORM)/$(DESIGN_NICKNAME)/constraint.sdc

export DIE_AREA   	 	= 0 0 100 30
export CORE_AREA   		= 4 1 96 29

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
export RO_CORE_DIM = 58,30
# this is the array dimension for RO inverters, <W,H>, values should be Even, the total number of inverters is W*H
export RO_ARRAY_DIM = 36,4
# this is the cell dimension, <W,H>, use the Site's dimension
export RO_CELL_DIM = 0.11,5.55
# this is the offset from lower left corner of core to the rirst RO placement, <W,H>, W and H values should be >=1 multiples of RO_CELL_DIM respectfullly
export RO_OFFSET = 3.63,5.55
