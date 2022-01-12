# ==============================================================================
# Run temp sensor design
# ==============================================================================

# sky130hd

sky130hd_cryo_verilog:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130hd --mode verilog --ninv 144

sky130hd_cryo:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130hd --mode macro --ninv 144
	python3 tools/parse_rpt.py

sky130hd_cyro_full:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130hd --mode full --ninv 144

# sky130hvl

sky130hvl_cryo_verilog:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130hvl --mode verilog --ninv 144

sky130hvl_cryo:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130hvl --mode macro --ninv 144
	python3 tools/parse_rpt.py

sky130hvl_cyro_full:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130hvl --mode full --ninv 144

# sky130hs

sky130hs_cryo_verilog:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130hs --mode verilog --ninv 144

sky130hs_cryo:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130hs --mode macro --ninv 144
	python3 tools/parse_rpt.py

sky130hs_cyro_full:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130hs --mode full --ninv 144

# sky130osu12Ths

sky130osu12Ths_cryo_verilog:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130osu12Ths --mode verilog --ninv 144

sky130osu12Ths_cryo:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130osu12Ths --mode macro --ninv 144
	python3 tools/parse_rpt.py

sky130osu12Ths_cyro_full:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130osu12Ths --mode full --ninv 144

# sky130osu12Tms

sky130osu12Tms_cryo_verilog:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130osu12Tms --mode verilog --ninv 144

sky130osu12Tms_cryo:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130osu12Tms --mode macro --ninv 144
	python3 tools/parse_rpt.py

sky130osu12Tms_cyro_full:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130osu12Tms --mode full --ninv 144

# sky130osu18Ths

sky130osu18Ths_cryo_verilog:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130osu18Ths --mode verilog --ninv 144

sky130osu18Ths_cryo:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130osu18Ths --mode macro --ninv 144
	python3 tools/parse_rpt.py

sky130osu18Ths_cyro_full:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130osu18Ths --mode full --ninv 144
	
clean:
	rm -f error_within_x.csv golden_error_opt.csv search_result.csv
	rm -rf work
	rm -rf tools/*.pyc tools/__pycache__/
	cd flow && make nuke
	cd simulations && rm -rf run


