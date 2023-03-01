# ==============================================================================
# Run LDO generator
# ==============================================================================

# read arguments into UserSpec
ifdef specfile
UserSpec += --specfile $(specfile)
endif
ifdef VoltsOut
UserSpec += --vref $(VoltsOut)
endif
ifdef AmpsMax
UserSpec += --imax $(AmpsMax)
endif
ifdef ModuleName
UserSpec += --name $(ModuleName)
endif

help:banner
	@@echo "OpenFASOC is focused on open source automated analog generation"
	@@echo "from user specification to GDSII with fully open-sourced tools."
	@@echo "This project is led by a team of researchers at the University of Michigan and is inspired from FASOC"
	@@echo "For more info, visit https://fasoc.engin.umich.edu/"
	@@echo  ""
	@@echo "IP: LDO \nSupported Technology: Sky130A \nSupported Library: sky130hvl"
	@@echo ""
	@@echo "Targets supported:"
	@@echo  ""
	@@echo "1. make sky130hvl_ldo [VoltsOut=insert_voltage_here] [AmpsMax=insert_current_here] [ModuleName=insert_name_here] [specfile=insert_spec_file]"
	@@echo "    >> This will create the macro for the LDO, creates the lef/def/gds files , performs lvs/drc checks and creates spice netlists.It won't run simulations."
	@@echo  ""
	@@echo "2. make sky130hvl_ldo_verilog [VoltsOut=insert_voltage_here] [AmpsMax=insert_current_here] [ModuleName=insert_name_here] [specfile=insert_spec_file]"
	@@echo "    >> This will create the verilog file for the digital LDO IP. It doesn't create a macro, won't create lef/def/gds files and won't run simulations"
	@@echo  ""
	@@echo "3. make sky130hvl_ldo_full [VoltsOut=insert_voltage_here] [AmpsMax=insert_current_here] [ModuleName=insert_name_here] [specfile=insert_spec_file]"
	@@echo "    >> This will create the macro for the digital LDO, creates the lef/def/gds files, performs lvs/drc checks and also runs simulations."
	@@echo  ""
	@@echo "4. make clean"
	@@echo "    >> This will clean all files generated during the run inside the run/, flow/ and work/ directories"
	@@echo  ""
	@@echo "5. make clean_sims"
	@@echo "    >> This will clean all simulations (allows for re-running simulations)"
	@@echo  ""
	@@echo "6. make JSONspec VoltsOut=insert_voltage_here AmpsMax=insert_current_here ModuleName=insert_name_here"
	@@echo "    >> Dump a JSON file containing the input specifications"
	@@echo  ""
	@@echo "7. make help"
	@@echo "    >> Displays this message"

sky130hvl_ldo_verilog:
	python3 ./tools/ldo-gen.py --output ./work --platform sky130hvl --mode verilog $(UserSpec)

sky130hvl_ldo:
	python3 ./tools/ldo-gen.py --output ./work --platform sky130hvl --mode macro $(UserSpec)
	@@echo "=================================================================================="
	@@echo "Thank you for using OpenFASOC"
	@@echo "For more info, please read the latest documentation on openfasoc.readthedocs.io"
	@@echo "For any issues, please feel free to open an issue on GitHub repository"
	@@echo "=================================================================================="

sky130hvl_ldo_full:
	python3 ./tools/ldo-gen.py --output ./work --platform sky130hvl --mode full $(UserSpec)
	@@echo "=================================================================================="
	@@echo "Thank you for using OpenFASOC"
	@@echo "For more info, please read the latest documentation on openfasoc.readthedocs.io"
	@@echo "For any issues, please feel free to open an issue on GitHub repository"
	@@echo "=================================================================================="

JSONspec:
	python3 ./tools/ldo-gen.py --output ./work --platform sky130hvl --mode dump $(UserSpec)

clean:
	-rm -f error_within_x.csv golden_error_opt.csv search_result.csv
	-rm -rf work
	-rm -rf tools/*.pyc tools/__pycache__/
	-cd flow && make nuke
	-rm -f blocks/sky130hvl/ldo_custom_net.txt blocks/sky130hvl/ldo_domain_insts.txt
	-rm -rf ../../common/drc-lvs-check/sky130A

clean_sims:
	cd simulations && rm -rf run

code_reset:
	git checkout ./flow
	git clean -f -d ./flow

banner:
	@@echo "=============================================================="
	@@echo "   ___  _____ ______ _   _ _____  _     ____   ___   ____"
	@@echo "  / _ \|  _  \| ____| \ | |  ___|/ \   / ___| / _ \ / ___|"
	@@echo " | | | | |_) ||  _| |  \| | |_  / _ \  \___ \| | | | |    "
	@@echo " | |_| |  __/ | |___| |\  |  _|/ ___ \  ___) | |_| | |___ "
	@@echo "  \___/|_|    |_____|_| \_|_| /_/   \_\|____/ \___/ \____|"
	@@echo ""
	@@echo "==============================================================="
