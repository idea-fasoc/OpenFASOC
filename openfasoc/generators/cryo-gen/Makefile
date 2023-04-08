# ==============================================================================
# Run temp sensor design
# ==============================================================================
sim_pex=
sim=

ifneq ("$(sim)","")
	sim_pex = --pex
endif

help:banner
	@@echo "OpenFASOC is focused on open source automated analog generation"
	@@echo "from user specification to GDSII with fully open-sourced tools."
	@@echo "This project is led by a team of researchers at the University of Michigan and is inspired from FASOC"
	@@echo "For more info, visit https://fasoc.engin.umich.edu/"
	@@echo  ""
	@@echo "IP: Cryo \nSupported Technology: Sky130A \nSupported Library: sky130hd, sky130hvl, sky130hs"
	@@echo ""
	@@echo "Targets supported:"
	@@echo "1. make [sky130hd, sky130hvl, sky130hs]_cryo_verilog"
	@@echo "    >> This will create the verilog file for the cryo IP. It doesn't create a macro, won't create lef/def/gds files and won't run simulations "
	@@echo "2. make [sky130hd, sky130hvl, sky130hs]_cryo"
	@@echo "    >> This will create the macro for the cryo, creates the lef/def/gds/spice netlist files and performs lvs/drc checks. But this won't run simulations."
	@@echo "3. make [sky130hd, sky130hvl, sky130hs]_temp_full [sim=pex]"
	@@echo "    >> This will create the macro for the cryo, creates the lef/def/gds/spice netlist files, performs lvs/drc checks and also runs simulations."
	@@echo "    >> Note: Only Pre-PEX simulations are performed, by default, under this target. To perform Post-PEX simulations as well, set sim to 'pex' as shown in the target definition"
	@@echo "4. make clean"
	@@echo "    >> This will clean all files generated during the run inside the run/, flow/ and work/ directories"
	@@echo "5. make help"
	@@echo "    >> Displays this message"


# sky130hd

sky130hd_cryo_verilog:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130hd --mode verilog --ninv 144

sky130hd_cryo:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130hd --mode macro --ninv 144 --prepex $(sim_pex)

sky130hd_cryo_full:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130hd --mode full --ninv 144 --prepex $(sim_pex)

# sky130hvl

sky130hvl_cryo_verilog:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130hvl --mode verilog --ninv 144

sky130hvl_cryo:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130hvl --mode macro --ninv 144 --prepex $(sim_pex)

sky130hvl_cryo_full:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130hvl --mode full --ninv 144 --prepex $(sim_pex)

# sky130hs

sky130hs_cryo_verilog:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130hs --mode verilog --ninv 144

sky130hs_cryo:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130hs --mode macro --ninv 144 --prepex $(sim_pex)

sky130hs_cryo_full:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130hs --mode full --ninv 144 --prepex $(sim_pex)

# sky130osu12Ths

sky130osu12Ths_cryo_verilog:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130osu12Ths --mode verilog --ninv 144

sky130osu12Ths_cryo:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130osu12Ths --mode macro --ninv 144

# sky130osu12Tms

sky130osu12Tms_cryo_verilog:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130osu12Tms --mode verilog --ninv 144

sky130osu12Tms_cryo:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130osu12Tms --mode macro --ninv 144

# sky130osu12Tls

sky130osu12Tls_cryo_verilog:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130osu12Tls --mode verilog --ninv 144

sky130osu12Tls_cryo:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130osu12Tls --mode macro --ninv 144

# sky130osu15Ths

sky130osu15Ths_cryo_verilog:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130osu15Ths --mode verilog --ninv 144

sky130osu15Ths_cryo:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130osu15Ths --mode macro --ninv 144

# sky130osu15Tms

sky130osu15Tms_cryo_verilog:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130osu15Tms --mode verilog --ninv 144

sky130osu15Tms_cryo:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130osu15Tms --mode macro --ninv 144

# sky130osu15Tls

sky130osu15Tls_cryo_verilog:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130osu15Tls --mode verilog --ninv 144

sky130osu15Tls_cryo:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130osu15Tls --mode macro --ninv 144

# sky130osu18Ths

sky130osu18Ths_cryo_verilog:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130osu18Ths --mode verilog --ninv 144

sky130osu18Ths_cryo:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130osu18Ths --mode macro --ninv 144

# sky130osu18Tms

sky130osu18Tms_cryo_verilog:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130osu18Tms --mode verilog --ninv 144

sky130osu18Tms_cryo:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130osu18Tms --mode macro --ninv 144

# sky130osu18Tls

sky130osu18Tls_cryo_verilog:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130osu18Tls --mode verilog --ninv 144

sky130osu18Tls_cryo:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130osu18Tls --mode macro --ninv 144

clean:
	rm -f error_within_x.csv golden_error_opt.csv search_result.csv
	rm -rf work
	rm -rf tools/*.pyc tools/__pycache__/
	cd flow && make nuke
	cd simulation && rm -f *.log *.sp *.out *.ps

banner:
	@@echo "=============================================================="
	@@echo "   ___  _____ ______ _   _ _____  _     ____   ___   ____"
	@@echo "  / _ \|  _  \| ____| \ | |  ___|/ \   / ___| / _ \ / ___|"
	@@echo " | | | | |_) ||  _| |  \| | |_  / _ \  \___ \| | | | |    "
	@@echo " | |_| |  __/ | |___| |\  |  _|/ ___ \  ___) | |_| | |___ "
	@@echo "  \___/|_|    |_____|_| \_|_| /_/   \_\|____/ \___/ \____|"
	@@echo ""
	@@echo "==============================================================="