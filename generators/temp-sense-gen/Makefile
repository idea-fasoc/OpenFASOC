# ==============================================================================
# Run temp sensor design
# ==============================================================================

sky130hd_temp_verilog:
	python tools/temp-sense-gen.py --specfile test.json --outputDir ./work --platform sky130hd --mode verilog

sky130hd_temp:
	python tools/temp-sense-gen.py --specfile test.json --outputDir ./work --platform sky130hd --mode macro

sky130hd_temp_full:
	python tools/temp-sense-gen.py --specfile test.json --outputDir ./work --platform sky130hd --mode full

clean:
	rm -f error_within_x.csv golden_error_opt.csv search_result.csv
	rm -rf work
	rm tools/*.pyc
	cd flow && make clean_all
	cd simulations && rm -rf run


