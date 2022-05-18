# ==============================================================================
# Run dcdc design
# ==============================================================================

# sky130hd

sky130hd_dcdc_verilog:
	python3 tools/dcdc_gen.py --specfile test.json --outputDir ./work --platform sky130hd --mode verilog

sky130hs_dcdc_verilog:
	python3 tools/dcdc_gen.py --specfile test.json --outputDir ./work --platform sky130hs --mode verilog

# sky130hd_dcdc:
	# python3 tools/dcdc_gen.py --specfile test.json --outputDir ./work --platform sky130hd --mode macro
	# python3 tools/parse_rpt.py

# sky130hd_dcdc_full:
	# python3 tools/dcdc_gen.py --specfile test.json --outputDir ./work --platform sky130hd --mode full

clean:
	rm -f error_within_x.csv golden_error_opt.csv search_result.csv
	rm -rf work
	rm -rf tools/*.pyc tools/__pycache__/
	cd flow && make nuke
	cd simulations && rm -rf run
