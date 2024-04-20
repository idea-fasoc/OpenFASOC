# If we are running headless use offscreen rendering for save_image
ifndef DISPLAY
export QT_QPA_PLATFORM ?= offscreen
endif

SHELL          = /bin/bash
.SHELLFLAGS    = -o pipefail -c

export FLOW_HOME ?= $(shell pwd)
export COMMON_HOME ?= $(FLOW_HOME)/../../../common
export PLATFORM      ?= sky130hd
export DESIGN_HOME   ?= $(FLOW_HOME)/design
export PLATFORM_HOME ?= $(COMMON_HOME)/platforms
export WORK_HOME     ?= $(shell pwd)
export UTILS_DIR     ?= $(FLOW_HOME)/util
export SCRIPTS_DIR   ?= $(FLOW_HOME)/scripts
export TEST_DIR      ?= $(FLOW_HOME)/test

include $(DESIGN_CONFIG)

PUBLIC=nangate45 sky130hd sky130hs asap7

ifneq ($(wildcard $(PLATFORM_HOME)/$(PLATFORM)),)
  export PLATFORM_DIR = $(PLATFORM_HOME)/$(PLATFORM)
else ifneq ($(findstring $(PLATFORM),$(PUBLIC)),)
  export PLATFORM_DIR = ./platforms/$(PLATFORM)
else ifneq ($(wildcard ../../$(PLATFORM)),)
  export PLATFORM_DIR = ../../$(PLATFORM)
else
  $(error [ERROR][FLOW] Platform '$(PLATFORM)' not found.)
endif

$(info [INFO][FLOW] Using platform directory $(PLATFORM_DIR))
include $(PLATFORM_DIR)/config.mk
export DESIGN_NAME = diff_test
export GALLERY_REPORT ?= 0
export VIN_ROUTE_CONNECTION_POINTS = 3
export RESYNTH_AREA_RECOVER ?= 0
export RESYNTH_TIMING_RECOVER ?= 0
export ABC_AREA ?= 0
export SYNTH_ARGS ?= -flatten
export PLACE_PINS_ARGS
export FLOW_VARIANT ?= glayout
export GPL_TIMING_DRIVEN ?= 1
export GPL_ROUTABILITY_DRIVEN ?= 1
export ENABLE_DPO ?= 1
export DPO_MAX_DISPLACEMENT ?= 5 1
export DESIGN_NICKNAME ?= $(DESIGN_NAME)
export DESIGN_DIR  = $(dir $(DESIGN_CONFIG))
export LOG_DIR     = $(WORK_HOME)/logs/$(PLATFORM)/$(FLOW_VARIANT)
export OBJECTS_DIR = $(WORK_HOME)/objects/$(PLATFORM)/$(FLOW_VARIANT)
export REPORTS_DIR = $(WORK_HOME)/reports/$(PLATFORM)/$(FLOW_VARIANT)
export RESULTS_DIR = $(WORK_HOME)/results/$(PLATFORM)/$(FLOW_VARIANT)

ifeq (, $(strip $(NPROC)))
  NPROC := $(shell nproc 2>/dev/null)

  ifeq (, $(strip $(NPROC)))
    NPROC := $(shell grep -c ^processor /proc/cpuinfo 2>/dev/null)
  endif
  ifeq (, $(strip $(NPROC)))
    NPROC := $(shell sysctl -n hw.ncpu 2>/dev/null)
  endif
  ifeq (, $(strip $(NPROC)))
    NPROC := 1
  endif
endif
export NUM_CORES := $(NPROC)

WRAPPED_LEFS = $(foreach lef,$(notdir $(WRAP_LEFS)),$(OBJECTS_DIR)/lef/$(lef:.lef=_mod.lef))
WRAPPED_LIBS = $(foreach lib,$(notdir $(WRAP_LIBS)),$(OBJECTS_DIR)/$(lib:.lib=_mod.lib))
export ADDITIONAL_LEFS += $(WRAPPED_LEFS) $(WRAP_LEFS)
export LIB_FILES += $(WRAP_LIBS) $(WRAPPED_LIBS)
export DONT_USE_LIBS   = $(patsubst %.lib.gz, %.lib, $(addprefix $(OBJECTS_DIR)/lib/, $(notdir $(LIB_FILES))))
export DONT_USE_SC_LIB ?= $(firstword $(DONT_USE_LIBS))
STREAM_SYSTEM ?= GDS
ifneq ($(findstring GDS,$(shell echo $(STREAM_SYSTEM) | tr '[:lower:]' '[:upper:]')),)
	export STREAM_SYSTEM_EXT := gds
	GDSOAS_FILES = $(GDS_FILES)
	ADDITIONAL_GDSOAS = $(ADDITIONAL_GDS)
	SEAL_GDSOAS = $(SEAL_GDS)
else
	export STREAM_SYSTEM_EXT := oas
	GDSOAS_FILES = $(OAS_FILES)
	ADDITIONAL_GDSOAS = $(ADDITIONAL_OAS)
	SEAL_GDSOAS = $(SEAL_OAS)
endif
export WRAPPED_GDSOAS = $(foreach lef,$(notdir $(WRAP_LEFS)),$(OBJECTS_DIR)/$(lef:.lef=_mod.$(STREAM_SYSTEM_EXT)))

build_macros: $(BLOCK_LEFS)
$(foreach block,$(BLOCKS),$(eval ./results/$(PLATFORM)/$(DESIGN_NICKNAME)_$(block)/$(FLOW_VARIANT)/${block}.lef: ./designs/$(PLATFORM)/$(DESIGN_NICKNAME)/${block}/config.mk))
$(foreach block,$(BLOCKS),$(eval ./results/$(PLATFORM)/$(DESIGN_NICKNAME)_$(block)/$(FLOW_VARIANT)/6_final.gds: ./results/$(PLATFORM)/$(DESIGN_NICKNAME)_$(block)/$(FLOW_VARIANT)/${block}.lef))
$(BLOCK_LEFS):
	$(MAKE) DESIGN_CONFIG=$< generate_abstract
export __open_generator_name__=diff_test

WRAP_CFG = $(PLATFORM_DIR)/wrapper.cfg
export COMMON_VERIF_DIR = $(COMMON_HOME)/drc-lvs-check

magic_drc: $(RESULTS_DIR)/6_final.gds
ifeq ($(shell command -v magic),)
	$(error Magic not found in PATH)
endif
	$(COMMON_VERIF_DIR)/run_drc.sh
	# magic -rcfile $(COMMON_VERIF_DIR)/sky130A/sky130A.magicrc -noconsole -dnull $(COMMON_VERIF_DIR)/magic_commands.tcl < /dev/null

netgen_lvs: $(RESULTS_DIR)/6_final.gds $(RESULTS_DIR)/6_final.cdl
ifeq ($(shell command -v netgen),)
	$(error Netgen not found in PATH)
endif
ifeq ($(shell command -v magic),)
	$(error Magic not found in PATH)
endif
	mkdir -p $(OBJECTS_DIR)/netgen_lvs/spice $(OBJECTS_DIR)/netgen_lvs/ext
	python3 $(UTILS_DIR)/openfasoc/cdl_parser.py -i $(RESULTS_DIR)/6_final.cdl -s $(PLATFORM_DIR)/cdl/sky130_fd_sc_hd.spice -o $(OBJECTS_DIR)/netgen_lvs/spice/$(DESIGN_NAME).spice
	$(COMMON_VERIF_DIR)/run_lvspex.sh $(RESULTS_DIR)/6_final.gds $(DESIGN_NAME) $(REPORTS_DIR)/6_final_lvs.rpt

clean_all: 
	rm -rf $(OBJECTS_DIR)/*
	rm -rf $(REPORTS_DIR)/*
	rm -rf $(RESULTS_DIR)/*
