# ==============================================================================
# Run LDO generator
# ==============================================================================

help:banner
	@@echo "OpenFASOC is focused on open source automated analog generation"
	@@echo "from user specification to GDSII with fully open-sourced tools."
	@@echo "This project is led by a team of researchers at the University of Michigan and is inspired from FASOC"
	@@echo "For more info, visit https://fasoc.engin.umich.edu/"
	@@echo  ""
	@@echo "IP: LDO \nSupported Technology: Sky130A \nSupported Library: sky130hvl"
	@@echo ""
	@@echo "Targets supported:"
	@@echo "1. make sky130hvl_ldo"
	@@echo "    >> This will create the macro for the LDO, creates the lef/def/gds files and performs lvs/drc checks. It won't run simulations."
	@@echo "2. make sky130hvl_ldo_verilog"
	@@echo "    >> This will create the verilog file for the digital LDO IP. It doesn't create a macro, won't create lef/def/gds files and won't run simulations "
	@@echo "3. make sky130hvl_ldo_full"
	@@echo "    >> This will create the macro for the digital LDO, creates the lef/def/gds files, performs lvs/drc checks and also runs simulations."
	@@echo "4. make clean"
	@@echo "    >> This will clean all files generated during the run inside the run/, flow/ and work/ directories"
	@@echo "4. make clean_sims"
	@@echo "    >> This will clean all simulations (allows for re-running simulations)"
	@@echo "5. make help"
	@@echo "    >> Displays this message"

sky130hvl_ldo_verilog:
	python3 ./tools/ldo-gen.py --specfile test.json --output ./work --platform sky130hvl --mode verilog

sky130hvl_ldo:
	python3 ./tools/ldo-gen.py --specfile test.json --output ./work --platform sky130hvl --mode macro
	@@echo "=================================================================================="
	@@echo "Thank you for using OpenFASOC"
	@@echo "For more info, please read the latest documentation on openfasoc.readthedocs.io"
	@@echo "For any issues, please feel free to open an issue on GitHub repository"
	@@echo "=================================================================================="

sky130hvl_ldo_full:
	python3 ./tools/ldo-gen.py --specfile test.json --output ./work --platform sky130hvl --mode full
	@@echo "=================================================================================="
	@@echo "Thank you for using OpenFASOC"
	@@echo "For more info, please read the latest documentation on openfasoc.readthedocs.io"
	@@echo "For any issues, please feel free to open an issue on GitHub repository"
	@@echo "=================================================================================="

clean:
	-rm -f error_within_x.csv golden_error_opt.csv search_result.csv
	-rm -rf work
	-rm -rf tools/*.pyc tools/__pycache__/
	-cd flow && make nuke

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
