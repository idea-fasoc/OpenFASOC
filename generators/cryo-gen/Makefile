# ==============================================================================
# Run temp sensor design
# ==============================================================================

sky130hd_cryo_verilog:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130hd --mode verilog --ninv 144

sky130hd_cryo:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130hd --mode macro
	python3 tools/parse_rpt.py

sky130hd_cyro_full:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130hd --mode full

clean:
	rm -f error_within_x.csv golden_error_opt.csv search_result.csv
	rm -rf work
	rm -rf tools/*.pyc tools/__pycache__/
	cd flow && make nuke
	cd simulations && rm -rf run


