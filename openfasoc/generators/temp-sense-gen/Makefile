# ==============================================================================
# Run temp sensor design
# ==============================================================================

help:banner
	@@echo "OpenFASOC is focused on open source automated analog generation"
	@@echo "from user specification to GDSII with fully open-sourced tools."
	@@echo "This project is led by a team of researchers at the University of Michigan and is inspired from FASOC"
	@@echo "For more info, visit https://fasoc.engin.umich.edu/"
	@@echo  ""
	@@echo "IP: Temperature Sensor \nSupported Technology: Sky130A \nSupported Library: sky130hd"
	@@echo ""
	@@echo "Targets supported:"
	@@echo "1. make sky130hd_temp"
	@@echo "    >> This will create the macro for the thermal sensor, creates the lef/def/gds files and performs lvs/drc checks. It won't run simulations."
	@@echo "2. make sky130hd_temp_verilog"
	@@echo "    >> This will create the verilog file for the thermal sensor IP. It doesn't create a macro, won't create lef/def/gds files and won't run simulations "
	@@echo "3. make sky130hd_temp_full"
	@@echo "    >> This will create the macro for the thermal sensor, creates the lef/def/gds files, performs lvs/drc checks and also runs simulations."
	@@echo "    >> [Warning] Currently, this target is in alpha phase"
	@@echo "4. make clean"
	@@echo "    >> This will clean all files generated during the run inside the run/, flow/ and work/ directories"
	@@echo "5. make help"
	@@echo "    >> Displays this message"

sky130hd_temp_verilog:
	python3 tools/temp-sense-gen.py --specfile test.json --outputDir ./work --platform sky130hd --mode verilog

sky130hd_temp:
	python3 tools/temp-sense-gen.py --specfile test.json --outputDir ./work --platform sky130hd --mode macro
	python3 tools/parse_rpt.py
	tools/verify_op.sh

sky130hd_temp_full:
	# add --pex to also run pex simulations
	python3 tools/temp-sense-gen.py --specfile test.json --outputDir ./work --platform sky130hd --mode full --prepex

clean:
	rm -f error_within_x.csv golden_error_opt.csv search_result.csv
	rm -rf work
	rm -rf tools/*.pyc tools/__pycache__/
	cd flow && make clean_all
	cd simulations && rm -rf run

banner:
	@@echo "=============================================================="
	@@echo "   ___  _____ ______ _   _ _____  _     ____   ___   ____"
	@@echo "  / _ \|  _  \| ____| \ | |  ___|/ \   / ___| / _ \ / ___|"
	@@echo " | | | | |_) ||  _| |  \| | |_  / _ \  \___ \| | | | |    "
	@@echo " | |_| |  __/ | |___| |\  |  _|/ ___ \  ___) | |_| | |___ "
	@@echo "  \___/|_|    |_____|_| \_|_| /_/   \_\|____/ \___/ \____|"
	@@echo ""
	@@echo "==============================================================="
