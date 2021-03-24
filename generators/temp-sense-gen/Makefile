# ==============================================================================
# Run temp sensor design
# ==============================================================================

sky130hd_temp:
	python tools/temp-sense-gen.py --specfile test.json --outputDir ./work --platform sky130hd --mode macro

clean:
	rm -f error_within_x.csv golden_error_opt.csv search_result.csv
	rm -rf work


