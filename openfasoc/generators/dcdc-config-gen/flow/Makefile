# ==============================================================================
# Uncomment or add the design to run
# ==============================================================================
default: finish

# ==============================================================================
#  ____  _____ _____ _   _ ____
# / ___|| ____|_   _| | | |  _ \
# \___ \|  _|   | | | | | | |_) |
#  ___) | |___  | | | |_| |  __/
# |____/|_____| |_|  \___/|_|
#
# ==============================================================================

# Include design and platform configuration

DESIGN_CONFIG = ./design/sky130hd/dcdc_config/config.mk

include $(DESIGN_CONFIG)

PUBLIC=sky130hd sky130hs sky130hvl

ifneq ($(findstring $(PLATFORM),$(PUBLIC)),)
  export PLATFORM_DIR = ../../../common/platforms/$(PLATFORM)
else ifneq ($(wildcard ../../$(PLATFORM)),)
  export PLATFORM_DIR = ../../../$(PLATFORM)
else
  $(error [ERROR][FLOW] Platform '$(PLATFORM)' not found)
endif

$(info [INFO][FLOW] Using platform directory $(PLATFORM_DIR))
include $(PLATFORM_DIR)/config.mk

# Setup working directories
export DESIGN_NICKNAME ?= $(DESIGN_NAME)

export LOG_DIR     = ./logs/$(PLATFORM)/$(DESIGN_NICKNAME)
export OBJECTS_DIR = ./objects/$(PLATFORM)/$(DESIGN_NICKNAME)
export REPORTS_DIR = ./reports/$(PLATFORM)/$(DESIGN_NICKNAME)
export RESULTS_DIR = ./results/$(PLATFORM)/$(DESIGN_NICKNAME)

export SCRIPTS_DIR = ./scripts
export UTILS_DIR   = ./util
export TEST_DIR    = ./test
export SIM_DIR     = $(PWD)/../simulation

# export MACRO_PLACEMENT = $(RESULTS_DIR)/six_stage.macro_placment.cfg

# export BASE        = /shared/OpenFASOC/generators/temp-sense-gen/flow
# export LOG_DIR     = $(BASE)/logs/$(PLATFORM)/$(DESIGN_NICKNAME)
# export OBJECTS_DIR = $(BASE)/objects/$(PLATFORM)/$(DESIGN_NICKNAME)
# export REPORTS_DIR = $(BASE)/reports/$(PLATFORM)/$(DESIGN_NICKNAME)
# export RESULTS_DIR = $(BASE)/results/$(PLATFORM)/$(DESIGN_NICKNAME)
#
# export SCRIPTS_DIR = $(BASE)/scripts
# export UTILS_DIR   = $(BASE)/util
# export TEST_DIR    = $(BASE)/test

# Tool Options
SHELL = /bin/bash -o pipefail
TIME_CMD = /usr/bin/time -f "%Eelapsed %PCPU %MmemKB"
export NUM_CORES = $(shell grep -c ^processor /proc/cpuinfo)

OPENROAD_CMD = openroad -no_init -exit

# OPENROAD_CMD = docker run --rm -v /shared/OpenLane:/openLANE_flow \
                               -v /shared/OpenFASOC/generators/cryo-gen/:/shared/OpenFASOC/generators/cryo-gen/ \
			       -e PDK_ROOT=/shared/OpenLane --user 1001:1002 efabless/openlane:2021.09.02_03.15.28 \
			       openroad -no_init -exit

WRAPPED_LEFS = $(foreach lef,$(notdir $(WRAP_LEFS)),$(OBJECTS_DIR)/lef/$(lef:.lef=_mod.lef))
WRAPPED_LIBS = $(foreach lib,$(notdir $(WRAP_LIBS)),$(OBJECTS_DIR)/$(lib:.lib=_mod.lib))
export WRAPPED_GDS  = $(foreach lef,$(notdir $(WRAP_LEFS)),$(OBJECTS_DIR)/$(lef:.lef=_mod.gds))
export ADDITIONAL_LEFS += $(WRAPPED_LEFS) $(WRAP_LEFS)
export LIB_FILES += $(WRAP_LIBS) $(WRAPPED_LIBS)

$(RESULTS_DIR)/sc_aux_merged.cdl: $(CDL_FILE) $(ADDITIONAL_CDL_FILE)
	cat $(CDL_FILE) $(ADDITIONAL_CDL_FILE) > $(RESULTS_DIR)/sc_aux_merged.cdl


export DONT_USE_LIBS   = $(addprefix $(OBJECTS_DIR)/lib/, $(notdir $(LIB_FILES)))
export DONT_USE_SC_LIB = $(OBJECTS_DIR)/lib/$(notdir $(firstword $(LIB_FILES)))

# Utility to print tool version information
#-------------------------------------------------------------------------------
versions.txt:
	@yosys -V > $(abspath $@)
	@echo openroad `openroad -version` >> $(abspath $@)
	@klayout -zz -v >> $(abspath $@)

# Pre-process Lefs
# ==============================================================================

# Modify lef files for TritonRoute
$(OBJECTS_DIR)/merged_spacing.lef: $(TECH_LEF) $(SC_LEF) $(ADDITIONAL_LEFS)
	mkdir -p $(OBJECTS_DIR)
	$(UTILS_DIR)/mergeLef.py --inputLef $(TECH_LEF) $(SC_LEF) $(ADDITIONAL_LEFS) --outputLef $@

# Create special generic lef for TritonRoute if required.
ifneq ($(GENERIC_TECH_LEF),)
$(OBJECTS_DIR)/generic_merged_spacing.lef: $(GENERIC_TECH_LEF) $(SC_LEF) $(ADDITIONAL_LEFS)
	mkdir -p $(OBJECTS_DIR)
	$(UTILS_DIR)/mergeLef.py --inputLef $(GENERIC_TECH_LEF) $(SC_LEF) $(ADDITIONAL_LEFS) --outputLef $@
endif

# Pre-process libraries
# ==============================================================================

# Create temporary Liberty files which have the proper dont_use properties set
# For use with Yosys and ABC
.SECONDEXPANSION:
$(DONT_USE_LIBS): $$(filter %$$(@F),$(LIB_FILES))
	@mkdir -p $(OBJECTS_DIR)/lib
	$(UTILS_DIR)/markDontUse.py -p "$(DONT_USE_CELLS)" -i $^ -o $@

# Pre-process KLayout tech
# ==============================================================================
 $(OBJECTS_DIR)/klayout.lyt: $(KLAYOUT_TECH_FILE)
	mkdir -p $(OBJECTS_DIR)
	sed '/OR_DEFAULT/d' $(TECH_LEF) > $(OBJECTS_DIR)/klayout_tech.lef
	sed 's,<lef-files>.*</lef-files>,$(foreach file, $(OBJECTS_DIR)/klayout_tech.lef $(SC_LEF) $(ADDITIONAL_LEFS),<lef-files>$(abspath $(file))</lef-files>),g' $^ > $@

$(OBJECTS_DIR)/klayout_wrap.lyt: $(KLAYOUT_TECH_FILE)
	mkdir -p $(OBJECTS_DIR)
	sed 's,<lef-files>.*</lef-files>,$(foreach file, $(OBJECTS_DIR)/klayout_tech.lef $(WRAP_LEFS),<lef-files>$(abspath $(file))</lef-files>),g' $^ > $@
# Create Macro wrappers (if necessary)
# ==============================================================================
WRAP_CFG = $(PLATFORM_DIR)/wrapper.cfg


export TCLLIBPATH := util/cell-veneer $(TCLLIBPATH)
$(WRAPPED_LEFS):
	mkdir -p $(OBJECTS_DIR)/lef $(OBJECTS_DIR)/def
	util/cell-veneer/wrap.tcl -cfg $(WRAP_CFG) -macro $(filter %$(notdir $(@:_mod.lef=.lef)),$(WRAP_LEFS))
	mv $(notdir $@) $@
	mv $(notdir $(@:lef=def)) $(dir $@)../def/$(notdir $(@:lef=def))

$(WRAPPED_LIBS):
	mkdir -p $(OBJECTS_DIR)/lib
	sed 's/library(\(.*\))/library(\1_mod)/g' $(filter %$(notdir $(@:_mod.lib=.lib)),$(WRAP_LIBS)) | sed 's/cell(\(.*\))/cell(\1_mod)/g' > $@

# ==============================================================================
#  ______   ___   _ _____ _   _ _____ ____ ___ ____
# / ___\ \ / / \ | |_   _| | | | ____/ ___|_ _/ ___|
# \___ \\ V /|  \| | | | | |_| |  _| \___ \| |\___ \
#  ___) || | | |\  | | | |  _  | |___ ___) | | ___) |
# |____/ |_| |_| \_| |_| |_| |_|_____|____/___|____/
#
synth: versions.txt \
       $(RESULTS_DIR)/1_synth.v \
       $(RESULTS_DIR)/1_synth.sdc
# ==============================================================================


# Run Synthesis using yosys
#-------------------------------------------------------------------------------
SYNTH_SCRIPT ?= scripts/synth.tcl

$(RESULTS_DIR)/1_1_yosys.v: $(DONT_USE_LIBS) $(WRAPPED_LIBS)
	mkdir -p $(RESULTS_DIR) $(LOG_DIR) $(REPORTS_DIR)
	($(TIME_CMD) yosys -c $(SYNTH_SCRIPT)) 2>&1 | tee $(LOG_DIR)/1_1_yosys.log

$(RESULTS_DIR)/1_synth.v: $(RESULTS_DIR)/1_1_yosys.v
	mkdir -p $(RESULTS_DIR) $(LOG_DIR) $(REPORTS_DIR)
	cp $< $@

$(RESULTS_DIR)/1_synth.sdc: $(SDC_FILE)
	mkdir -p $(RESULTS_DIR) $(LOG_DIR) $(REPORTS_DIR)
	cp $< $@

clean_synth:
	rm -f  $(RESULTS_DIR)/1_*.v $(RESULTS_DIR)/1_synth.sdc
	rm -f  $(REPORTS_DIR)/synth_*
	rm -f  $(LOG_DIR)/1_*
	rm -rf _tmp_yosys-abc-*


# ==============================================================================
#  _____ _     ___   ___  ____  ____  _        _    _   _
# |  ___| |   / _ \ / _ \|  _ \|  _ \| |      / \  | \ | |
# | |_  | |  | | | | | | | |_) | |_) | |     / _ \ |  \| |
# |  _| | |__| |_| | |_| |  _ <|  __/| |___ / ___ \| |\  |
# |_|   |_____\___/ \___/|_| \_\_|   |_____/_/   \_\_| \_|
#
floorplan: $(RESULTS_DIR)/2_floorplan.def \
           $(RESULTS_DIR)/2_floorplan.sdc
# ==============================================================================


# STEP 1: Translate verilog to def
#-------------------------------------------------------------------------------
$(RESULTS_DIR)/2_1_floorplan.def: $(RESULTS_DIR)/1_synth.v $(RESULTS_DIR)/1_synth.sdc $(ADDITIONAL_LEFS)
	echo $(PWD)
	($(TIME_CMD) $(OPENROAD_CMD) $(SCRIPTS_DIR)/floorplan.tcl -metrics $(LOG_DIR)/2_1_floorplan.json) 2>&1 | tee $(LOG_DIR)/2_1_floorplan.log

# STEP 1.1: DEF manipulation
#-------------------------------------------------------------------------------
#$(RESULTS_DIR)/six_stage.macro_placment.cfg:
#	python3 $(UTILS_DIR)/place_six_stage.py

# STEP 2: IO Placement
#-------------------------------------------------------------------------------
$(RESULTS_DIR)/2_2_floorplan_io.def: $(RESULTS_DIR)/2_1_floorplan.def
	($(TIME_CMD) $(OPENROAD_CMD) $(SCRIPTS_DIR)/io_placement.tcl -metrics $(LOG_DIR)/2_2_floorplan_io.json) 2>&1 | tee $(LOG_DIR)/2_2_floorplan_io.log

# STEP 3: Timing Driven Mixed Sized Placement
#-------------------------------------------------------------------------------
$(RESULTS_DIR)/2_3_floorplan_tdms.def: $(RESULTS_DIR)/2_2_floorplan_io.def $(RESULTS_DIR)/1_synth.v $(RESULTS_DIR)/1_synth.sdc $(LIB_FILES)
	($(TIME_CMD) $(OPENROAD_CMD) $(SCRIPTS_DIR)/tdms_place.tcl -metrics $(LOG_DIR)/2_3_tdms.json) 2>&1 | tee $(LOG_DIR)/2_3_tdms_place.log

# STEP 4: Macro Placement
#-------------------------------------------------------------------------------
$(RESULTS_DIR)/2_4_floorplan_macro.def: $(RESULTS_DIR)/2_3_floorplan_tdms.def $(RESULTS_DIR)/1_synth.v $(RESULTS_DIR)/1_synth.sdc $(IP_GLOBAL_CFG)
	($(TIME_CMD) $(OPENROAD_CMD) $(SCRIPTS_DIR)/macro_place.tcl -metrics $(LOG_DIR)/2_4_mplace.json) 2>&1 | tee $(LOG_DIR)/2_4_mplace.log

# STEP 5: Tapcell and Welltie insertion
#-------------------------------------------------------------------------------
$(RESULTS_DIR)/2_5_floorplan_tapcell.def: $(RESULTS_DIR)/2_4_floorplan_macro.def
	($(TIME_CMD) $(OPENROAD_CMD) $(SCRIPTS_DIR)/tapcell.tcl -metrics $(LOG_DIR)/2_5_tapcell.json) 2>&1 | tee $(LOG_DIR)/2_5_tapcell.log

# STEP 6: PDN generation
#-------------------------------------------------------------------------------
$(RESULTS_DIR)/2_6_floorplan_pdn.def: $(RESULTS_DIR)/2_5_floorplan_tapcell.def
	($(TIME_CMD) $(OPENROAD_CMD) $(SCRIPTS_DIR)/pdn.tcl -metrics $(LOG_DIR)/2_6_pdn.json) 2>&1 | tee $(LOG_DIR)/2_6_pdn.log

$(RESULTS_DIR)/2_floorplan.def: $(RESULTS_DIR)/2_6_floorplan_pdn.def
	cp $< $@

$(RESULTS_DIR)/2_floorplan.sdc: $(RESULTS_DIR)/2_1_floorplan.def


clean_floorplan:
	rm -f $(RESULTS_DIR)/2_*floorplan*.def $(RESULTS_DIR)/2_floorplan.sdc
	rm -f $(REPORTS_DIR)/2_*
	rm -f $(LOG_DIR)/2_*

# ==============================================================================
#  ____  _        _    ____ _____
# |  _ \| |      / \  / ___| ____|
# | |_) | |     / _ \| |   |  _|
# |  __/| |___ / ___ \ |___| |___
# |_|   |_____/_/   \_\____|_____|
#
place: $(RESULTS_DIR)/3_place.def \
       $(RESULTS_DIR)/3_place.sdc
# ==============================================================================

# STEP 1: Global placement + IO placement (not random)
#-------------------------------------------------------------------------------
$(RESULTS_DIR)/3_1_place_gp.def: $(RESULTS_DIR)/2_floorplan.def $(RESULTS_DIR)/2_floorplan.sdc
	($(TIME_CMD) $(OPENROAD_CMD) $(SCRIPTS_DIR)/global_place.tcl -metrics $(LOG_DIR)/3_1_place_gp.json) 2>&1 | tee $(LOG_DIR)/3_1_place_gp.log

# These steps are not needed in tempsensor design
# # STEP 2: IO placement (non-random)
# #-------------------------------------------------------------------------------
# $(RESULTS_DIR)/3_2_place_iop.def: $(RESULTS_DIR)/3_1_place_gp.def
# 	($(TIME_CMD) $(OPENROAD_CMD) $(SCRIPTS_DIR)/io_placement.tcl -metrics $(LOG_DIR)/3_2_place_iop.json) 2>&1 | tee $(LOG_DIR)/3_2_place_iop.log
#
# # STEP 3: Resizing & Buffering
# #-------------------------------------------------------------------------------
# $(RESULTS_DIR)/3_3_place_resized.def: $(RESULTS_DIR)/3_2_place_iop.def $(RESULTS_DIR)/2_floorplan.sdc
# 	($(TIME_CMD) $(OPENROAD_CMD) $(SCRIPTS_DIR)/resize.tcl -metrics $(LOG_DIR)/3_3_resizer.json) 2>&1 | tee $(LOG_DIR)/3_3_resizer.log
#
# clean_resize:
# 	rm -f $(RESULTS_DIR)/3_3_place_resized.def

# STEP 4: Detail placement
#-------------------------------------------------------------------------------
$(RESULTS_DIR)/3_4_place_dp.def: $(RESULTS_DIR)/3_1_place_gp.def
	($(TIME_CMD) $(OPENROAD_CMD) $(SCRIPTS_DIR)/detail_place.tcl -metrics $(LOG_DIR)/3_4_opendp.json) 2>&1 | tee $(LOG_DIR)/3_4_opendp.log

$(RESULTS_DIR)/3_place.def: $(RESULTS_DIR)/3_4_place_dp.def
	cp $< $@

$(RESULTS_DIR)/3_place.sdc: $(RESULTS_DIR)/2_floorplan.sdc
	cp $< $@

# Clean Targets
#-------------------------------------------------------------------------------
clean_place:
	rm -f $(RESULTS_DIR)/3_*place*.def
	rm -f $(RESULTS_DIR)/3_place.sdc
	rm -f $(REPORTS_DIR)/3_*
	rm -f $(LOG_DIR)/3_*


# ==============================================================================
#   ____ _____ ____
#  / ___|_   _/ ___|
# | |     | | \___ \
# | |___  | |  ___) |
#  \____| |_| |____/
#
cts: $(RESULTS_DIR)/4_cts.def \
     $(RESULTS_DIR)/4_cts.sdc
# ==============================================================================

# This step is not needed in tempsensor design
# # Run TritonCTS
# # ------------------------------------------------------------------------------
# $(RESULTS_DIR)/4_1_cts.def: $(RESULTS_DIR)/3_place.def $(RESULTS_DIR)/3_place.sdc
# 	($(TIME_CMD) $(OPENROAD_CMD) $(SCRIPTS_DIR)/cts.tcl -metrics $(LOG_DIR)/4_1_cts.json) 2>&1 | tee $(LOG_DIR)/4_1_cts.log

# Filler cell insertion
# ------------------------------------------------------------------------------
$(RESULTS_DIR)/4_2_cts_fillcell.def: $(RESULTS_DIR)/3_place.def
	($(TIME_CMD) $(OPENROAD_CMD) $(SCRIPTS_DIR)/fillcell.tcl -metrics $(LOG_DIR)/4_2_cts_fillcell.json) 2>&1 | tee $(LOG_DIR)/4_2_cts_fillcell.log

$(RESULTS_DIR)/4_cts.sdc: $(RESULTS_DIR)/3_place.sdc
	cp $< $@

$(RESULTS_DIR)/4_cts.def: $(RESULTS_DIR)/4_2_cts_fillcell.def
	cp $< $@

clean_cts:
	rm -rf $(RESULTS_DIR)/4_*cts*.def $(RESULTS_DIR)/4_cts.sdc
	rm -f  $(REPORTS_DIR)/4_*
	rm -f  $(LOG_DIR)/4_*


# ==============================================================================
#  ____   ___  _   _ _____ ___ _   _  ____
# |  _ \ / _ \| | | |_   _|_ _| \ | |/ ___|
# | |_) | | | | | | | | |  | ||  \| | |  _
# |  _ <| |_| | |_| | | |  | || |\  | |_| |
# |_| \_\\___/ \___/  |_| |___|_| \_|\____|
#
route: $(RESULTS_DIR)/5_route.def \
       $(RESULTS_DIR)/5_route.sdc
# ==============================================================================

ifneq ($(ADD_NDR_RULE),)
$(RESULTS_DIR)/5_0_ndr.def: $(RESULTS_DIR)/4_cts.def
	python util/add_ndr_rule.py --nets $(NDR_RULE_NETS) --rule $(NDR_RULE) --inputDef $(RESULTS_DIR)/4_cts.def --outputDef $(RESULTS_DIR)/5_0_ndr.def
else
$(RESULTS_DIR)/5_0_ndr.def: $(RESULTS_DIR)/4_cts.def
	cp $< $@
endif



# STEP 1: Run global route
#-------------------------------------------------------------------------------
$(RESULTS_DIR)/route.guide: $(RESULTS_DIR)/5_0_ndr.def
	($(TIME_CMD) $(OPENROAD_CMD) $(SCRIPTS_DIR)/global_route.tcl -metrics $(LOG_DIR)/5_1_fastroute.json) 2>&1 | tee $(LOG_DIR)/5_1_fastroute.log


# STEP 2: Run detail route
#-------------------------------------------------------------------------------

# Generate param file for TritonRoute
#-------------------------------------------------------------------------------
ifneq ($(GENERIC_TECH_LEF),)
  export TRITON_ROUTE_LEF := $(OBJECTS_DIR)/generic_merged_spacing.lef
else
  export TRITON_ROUTE_LEF := $(OBJECTS_DIR)/merged_spacing.lef
endif

$(OBJECTS_DIR)/TritonRoute.param: $(TRITON_ROUTE_LEF)
ifeq ($(USE_WXL),)
	echo "guide:$(RESULTS_DIR)/route.guide" >> $@
endif
	echo "outputguide:$(RESULTS_DIR)/output_guide.mod" >> $@
	echo "outputDRC:$(REPORTS_DIR)/5_route_drc.rpt" >> $@
	echo "outputMaze:$(RESULTS_DIR)/maze.log" >> $@
	echo "threads:$(NUM_CORES)" >> $@
	echo "bottomRoutingLayer:met1" >> $@
	echo "topRoutingLayer:met5" >> $@
	echo "cpxthreads:1" >> $@
	echo "verbose:1" >> $@
	echo "gap:0" >> $@
	echo "timeout:2400" >> $@
ifneq ($(dbProcessNode),)
	echo "dbProcessNode:$(dbProcessNode)" >> $@
endif

# Run TritonRoute
#-------------------------------------------------------------------------------
ifeq ($(USE_WXL),)
$(RESULTS_DIR)/5_route.def: $(RESULTS_DIR)/route.guide
endif
$(RESULTS_DIR)/5_route.def: $(OBJECTS_DIR)/TritonRoute.param $(RESULTS_DIR)/4_cts.def
	($(TIME_CMD) $(OPENROAD_CMD) $(SCRIPTS_DIR)/detail_route.tcl -metrics $(LOG_DIR)/5_2_TritonRoute.json) 2>&1 | tee $(LOG_DIR)/5_2_TritonRoute.log

$(RESULTS_DIR)/5_route.sdc: $(RESULTS_DIR)/4_cts.sdc
	cp $< $@

clean_route:
	rm -rf output*/ results*.out.dmp layer_*.mps
	rm -rf *.gdid *.log *.met *.sav *.res.dmp
	rm -rf $(RESULTS_DIR)/route.guide $(OBJECTS_DIR)/TritonRoute.param
	rm -rf $(RESULTS_DIR)/5_route.def $(RESULTS_DIR)/5_route.sdc
	rm -f  $(REPORTS_DIR)/5_*
	rm -f  $(LOG_DIR)/5_*

klayout_tr_rpt: $(RESULTS_DIR)/5_route.def $(OBJECTS_DIR)/klayout.lyt
	klayout -rd in_drc="$(REPORTS_DIR)/5_route_drc.rpt" \
	        -rd in_def="$<" \
	        -rd tech_file=$(OBJECTS_DIR)/klayout.lyt \
	        -rm $(UTILS_DIR)/viewDrc.py

klayout_guides: $(RESULTS_DIR)/5_route.def
	klayout -rd in_guide="$(RESULTS_DIR)/route.guide" \
	        -rd in_def="$<" \
	        -rd net_name=$(GUIDE_NET) \
	        -rd tech_file=$(OBJECTS_DIR)/klayout.lyt \
	        -rm $(UTILS_DIR)/viewGuide.py

# ==============================================================================
#  _____ ___ _   _ ___ ____  _   _ ___ _   _  ____
# |  ___|_ _| \ | |_ _/ ___|| | | |_ _| \ | |/ ___|
# | |_   | ||  \| || |\___ \| |_| || ||  \| | |  _
# |  _|  | || |\  || | ___) |  _  || || |\  | |_| |
# |_|   |___|_| \_|___|____/|_| |_|___|_| \_|\____|
#
finish:	$(REPORTS_DIR)/6_final_report.rpt \
        $(RESULTS_DIR)/6_final.v \
        $(RESULTS_DIR)/6_final.gds \
        $(RESULTS_DIR)/6_final.cdl
# ==============================================================================

ifneq ($(USE_FILL),)
$(RESULTS_DIR)/6_1_fill.def: $(RESULTS_DIR)/5_route.def
	($(TIME_CMD) $(OPENROAD_CMD) $(SCRIPTS_DIR)/density_fill.tcl -metrics $(LOG_DIR)/6_density_fill.json) 2>&1 | tee $(LOG_DIR)/6_density_fill.log
else
$(RESULTS_DIR)/6_1_fill.def: $(RESULTS_DIR)/5_route.def
	cp $< $@
endif

$(RESULTS_DIR)/6_1_fill.sdc: $(RESULTS_DIR)/5_route.sdc
	cp $< $@

$(REPORTS_DIR)/6_final_report.rpt: $(RESULTS_DIR)/6_1_fill.def $(RESULTS_DIR)/6_1_fill.sdc
	($(TIME_CMD) $(OPENROAD_CMD) $(SCRIPTS_DIR)/final_report.tcl -metrics $(LOG_DIR)/6_report.json) 2>&1 | tee $(LOG_DIR)/6_report.log

$(RESULTS_DIR)/6_final.def: $(REPORTS_DIR)/6_final_report.rpt

# Merge wrapped macros using Klayout
#-------------------------------------------------------------------------------
$(WRAPPED_GDS): $(OBJECTS_DIR)/klayout_wrap.lyt $(WRAPPED_LEFS)
	($(TIME_CMD) klayout -zz -rd design_name=$(basename $(notdir $@)) \
	        -rd in_def=$(OBJECTS_DIR)/def/$(notdir $(@:gds=def)) \
	        -rd in_files="$(ADDITIONAL_GDS)" \
	        -rd config_file=$(FILL_CONFIG) \
	        -rd seal_file="" \
	        -rd out_file=$@ \
	        -rd tech_file=$(OBJECTS_DIR)/klayout_wrap.lyt \
	        -r $(UTILS_DIR)/def2stream.py) 2>&1 | tee $(LOG_DIR)/6_merge_$(basename $(notdir $@)).log

# Merge GDS using Klayout
#-------------------------------------------------------------------------------
$(RESULTS_DIR)/6_1_merged.gds: $(OBJECTS_DIR)/klayout.lyt $(GDS_FILES) $(WRAPPED_GDS) $(RESULTS_DIR)/6_final.def
	($(TIME_CMD) stdbuf -o L klayout -zz -rd design_name=$(DESIGN_NAME) \
		-rd in_def=$(RESULTS_DIR)/6_final.def \
                -rd in_files="$(GDS_FILES) $(WRAPPED_GDS)" \
                -rd config_file=$(FILL_CONFIG) \
                -rd seal_file="$(SEAL_GDS)" \
                -rd out_file=$@ \
                -rd tech_file=$(OBJECTS_DIR)/klayout.lyt \
                -r $(UTILS_DIR)/def2stream.py) 2>&1 | tee $(LOG_DIR)/6_1_merge.log

$(RESULTS_DIR)/6_final.v: $(REPORTS_DIR)/6_final_report.rpt

$(RESULTS_DIR)/6_final.gds: $(RESULTS_DIR)/6_1_merged.gds
	cp $^ $@

drc: $(REPORTS_DIR)/6_drc.lyrdb

$(REPORTS_DIR)/6_drc.lyrdb: $(RESULTS_DIR)/6_final.gds $(KLAYOUT_DRC_FILE)
ifneq ($(KLAYOUT_DRC_FILE),)
	($(TIME_CMD) klayout -zz -rd in_gds="$<" \
	        -rd report_file=$(abspath $@) \
	        -r $(KLAYOUT_DRC_FILE)) 2>&1 | tee $(LOG_DIR)/6_drc.log
	# Hacky way of getting DRV count (don't error on no matches)
	grep -c "<value>" $@ > $(REPORTS_DIR)/6_drc_count.rpt || [[ $$? == 1 ]]
else
	echo "DRC not supported on this platform" > $@
endif

$(RESULTS_DIR)/6_final.cdl: $(RESULTS_DIR)/6_final.v $(RESULTS_DIR)/sc_aux_merged.cdl
	($(TIME_CMD) $(OPENROAD_CMD) $(SCRIPTS_DIR)/cdl.tcl) 2>&1 | tee $(LOG_DIR)/6_cdl.log

$(OBJECTS_DIR)/6_final_concat.cdl: $(RESULTS_DIR)/6_final.cdl $(RESULTS_DIR)/sc_aux_merged.cdl
	cat $^ > $@

lvs: $(RESULTS_DIR)/6_lvs.lvsdb

$(RESULTS_DIR)/6_lvs.lvsdb: $(RESULTS_DIR)/6_final.gds $(KLAYOUT_LVS_FILE) $(OBJECTS_DIR)/6_final_concat.cdl
ifneq ($(KLAYOUT_LVS_FILE),)
	($(TIME_CMD) klayout -b -rd in_gds="$<" \
	        -rd cdl_file=$(abspath $(OBJECTS_DIR)/6_final_concat.cdl) \
	        -rd report_file=$(abspath $@) \
	        -r $(KLAYOUT_LVS_FILE)) 2>&1 | tee $(LOG_DIR)/6_lvs.log
else
	echo "LVS not supported on this platform" > $@
endif


export COMMON_VERIF_DIR = ../../../common/drc-lvs-check

magic_drc: $(RESULTS_DIR)/6_final.gds
	$(COMMON_VERIF_DIR)/run_drc.sh
	# magic -rcfile $(COMMON_VERIF_DIR)/sky130A/sky130A.magicrc -noconsole -dnull $(COMMON_VERIF_DIR)/magic_commands.tcl < /dev/null

netgen_lvs: $(RESULTS_DIR)/6_final.gds

	python util/cdl_parser.py -i $(RESULTS_DIR)/6_final.cdl -s $(RESULTS_DIR)/sc_aux_merged.cdl -l $(OBJECTS_DIR)/merged_spacing.lef -o $(DESIGN_NAME).spice
	$(COMMON_VERIF_DIR)/run_lvspex.sh $(RESULTS_DIR)/6_final.gds $(DESIGN_NAME) $(REPORTS_DIR)/6_final_lvs.rpt

clean_finish:
	rm -rf $(RESULTS_DIR)/6_*.gds $(RESULTS_DIR)/6_*.def $(RESULTS_DIR)/6_*.v
	rm -rf $(REPORTS_DIR)/6_*.rpt
	rm -f  $(LOG_DIR)/6_*



# ==============================================================================
#  __  __ ___ ____   ____
# |  \/  |_ _/ ___| / ___|
# | |\/| || |\___ \| |
# | |  | || | ___) | |___
# |_|  |_|___|____/ \____|
#
# ==============================================================================

all: $(SDC_FILE) $(WRAPPED_LIBS) $(DONT_USE_LIBS) $(OBJECTS_DIR)/TritonRoute.param $(OBJECTS_DIR)/klayout.lyt $(WRAPPED_GDS)
	mkdir -p $(RESULTS_DIR) $(LOG_DIR) $(REPORTS_DIR)
	($(TIME_CMD) $(OPENROAD_CMD) $(SCRIPTS_DIR)/run_all.tcl -metrics $(LOG_DIR)/run_all.json) 2>&1 | tee $(LOG_DIR)/run_all.log

clean:
	@echo
	@echo "Make clean disabled."
	@echo "Use make clean_all or clean individual steps:"
	@echo "  clean_synth clean_floorplan clean_place clean_cts clean_route clean_finish"
	@echo

clean_all: clean_synth clean_floorplan clean_place clean_cts clean_route clean_finish
	rm -rf $(OBJECTS_DIR)
	rm -f cryoInst*

nuke: clean_test clean_issues
	rm -rf ./results ./logs ./reports ./objects
	rm -rf layer_*.mps macrocell.list *best.plt *_pdn.def dummy.guide run.param
	rm -rf *.rpt *.rpt.old *.def.v pin_dumper.log
	rm -rf versions.txt
	rm -f *.ext *.spice


# DEF/GDS viewer shortcuts
#-------------------------------------------------------------------------------
RESULTS_DEF = $(notdir $(sort $(wildcard $(RESULTS_DIR)/*.def)))
RESULTS_GDS = $(notdir $(sort $(wildcard $(RESULTS_DIR)/*.gds)))
$(foreach file,$(RESULTS_DEF) $(RESULTS_GDS),klayout_$(file)): klayout_%: $(OBJECTS_DIR)/klayout.lyt
	klayout -nn $(OBJECTS_DIR)/klayout.lyt $(RESULTS_DIR)/$*

gui_final: $(RESULTS_DIR)/6_final.def
	openroad -gui $(SCRIPTS_DIR)/gui.tcl


# Utilities
#-------------------------------------------------------------------------------
include $(UTILS_DIR)/utils.mk
export PRIVATE_DIR = ../../private_tool_scripts
-include $(PRIVATE_DIR)/util/utils.mk
