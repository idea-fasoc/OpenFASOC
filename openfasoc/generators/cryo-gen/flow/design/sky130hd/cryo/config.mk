export DESIGN_NICKNAME = cryo
export DESIGN_NAME = cryoInst

export PLATFORM    = sky130hd
#export VERILOG_FILES = $(sort $(wildcard ./designs/src/$(DESIGN_NICKNAME)/*.v))

export VERILOG_FILES 		= $(sort $(wildcard ./design/src/$(DESIGN_NICKNAME)/*.v))

export SDC_FILE    		= ./design/$(PLATFORM)/$(DESIGN_NICKNAME)/constraint.sdc

export DIE_AREA   	 	= 0 0 80 40
export CORE_AREA   		= 2.32 2.32 77.68 37.68

export PDN_TCL                  = ../blocks/$(PLATFORM)/pdn.tcl
# RO inverter placement config

# this is the floorplan dimension for the RO, <W,H>, this should be sufficiently large to allow padding between cells
export RO_CORE_DIM = 40,40
# this is the array dimension for RO inverters, <W,H>, values should be Even, the total number of inverters is W*H
export RO_ARRAY_DIM = 12,12
# this is the cell dimension, <W,H>, use the Site's dimension
export RO_CELL_DIM = 0.46,2.72
# this is the offset from lower left corner of core to the rirst RO placement, <W,H>, W and H values should be >=1 multiples of RO_CELL_DIM respectfullly
export RO_OFFSET = 3.68,2.72
# pin arguments (work in progress)
export PLACE_PINS_ARGS = -random
