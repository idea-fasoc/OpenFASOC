# ==============================================================================
# Run temp sensor design
# ==============================================================================

sim_pex=
sim=
inv=
head=

ifneq ("$(sim)","")
	sim_pex = --pex
endif

ifneq ("$(ninv)","")
	inv="--ninv"
endif

ifneq ("$(nhead)","")
	head="--nhead"
endif


help:banner
	@@echo "OpenFASOC is focused on open source automated analog generation"
	@@echo "from user specification to GDSII with fully open-sourced tools."
	@@echo "This project is led by a team of researchers at the University of Michigan and is inspired from FASOC"
	@@echo "For more info, visit https://fasoc.engin.umich.edu/"
	@@echo  ""
	@@echo "IP: Temperature Sensor \nSupported Technology: Sky130A \nSupported Library: sky130hd"
	@@echo ""
	@@echo "Targets supported:"
	@@echo "1. make sky130hd_temp_verilog"
	@@echo "    >> This will create the verilog file for the thermal sensor IP. It doesn't create a macro, won't create lef/def/gds files and won't run simulations "
	@@echo "2. make sky130hd_temp [ninv=<num>] [nhead=<num>]"
	@@echo "    >> This will create the macro for the thermal sensor, creates the lef/def/gds/spice netlist files and performs lvs/drc checks. But this won't run simulations."
	@@echo "3. make sky130hd_temp_full [ninv=<num>] [nhead=<num>] [sim=pex]"
	@@echo "    >> This will create the macro for the thermal sensor, creates the lef/def/gds/spice netlist files, performs lvs/drc checks and also runs simulations."
	@@echo "    >> Note: Only Pre-PEX simulations are performed, by default, under this target. To perform Post-PEX simulations as well, set sim to 'pex' as shown in the target definition"
	@@echo "4. make clean"
	@@echo "    >> This will clean all files generated during the run inside the run/, flow/ and work/ directories"
	@@echo "5. make help"
	@@echo "    >> Displays this message"

sky130hd_temp_verilog:
	python3 tools/temp-sense-gen.py --specfile test.json --outputDir ./work --platform sky130hd --mode verilog

sky130hd_temp:
	@python3 tools/temp-sense-gen.py --specfile test.json --outputDir ./work $(inv) $(ninv) $(head) $(nhead) --prepex $(sim_pex) --platform sky130hd --mode macro
	@python3 tools/parse_rpt.py
	@tools/verify_op.sh
	@@echo "=================================================================================="
	@@echo "Thank you for using OpenFASOC"
	@@echo "For more info, please read the latest documentation on openfasoc.readthedocs.io"
	@@echo "For any issues, please feel free to open an issue on GitHub repository"
	@@echo "=================================================================================="

sky130hd_temp_full:
	# add --pex to also run pex simulations
	@python3 tools/temp-sense-gen.py --specfile test.json --outputDir ./work --platform sky130hd --mode full --prepex $(sim_pex) $(inv) $(ninv) $(head) $(nhead)
	@python3 tools/parse_rpt.py
	@tools/verify_op.sh
	@@echo "=================================================================================="
	@@echo "Thank you for using OpenFASOC"
	@@echo "For more info, please read the latest documentation on openfasoc.readthedocs.io"
	@@echo "For any issues, please feel free to open an issue on GitHub repository"
	@@echo "=================================================================================="

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
