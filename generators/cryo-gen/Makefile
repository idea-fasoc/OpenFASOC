# ==============================================================================
# Run temp sensor design
# ==============================================================================

sky130hd_temp_verilog:
	python3 tools/temp-sense-gen.py --specfile test.json --outputDir ./work --platform sky130hd --mode verilog

sky130hd_temp:
	python3 tools/temp-sense-gen.py --specfile test.json --outputDir ./work --platform sky130hd --mode macro
	python3 tools/parse_rpt.py

sky130hd_temp_full:
	python3 tools/temp-sense-gen.py --specfile test.json --outputDir ./work --platform sky130hd --mode full

clean:
	rm -f error_within_x.csv golden_error_opt.csv search_result.csv
	rm -rf work
	rm -rf tools/*.pyc tools/__pycache__/
	cd flow && make nuke
	cd simulations && rm -rf run


