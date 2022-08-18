# ==============================================================================
# Run temp sensor design
# ==============================================================================

# sky130hd

sky130hd_cryo_verilog:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130hd --mode verilog --ninv 144

sky130hd_cryo:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130hd --mode macro --ninv 144

sky130hd_cryo_full:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130hd --mode full --ninv 144

# sky130hvl

sky130hvl_cryo_verilog:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130hvl --mode verilog --ninv 144

sky130hvl_cryo:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130hvl --mode macro --ninv 144

sky130hvl_cryo_full:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130hvl --mode full --ninv 144

# sky130hs

sky130hs_cryo_verilog:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130hs --mode verilog --ninv 144

sky130hs_cryo:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130hs --mode macro --ninv 144

sky130hs_cryo_full:
	python3 tools/cryo-gen.py --specfile test.json --outputDir ./work --platform sky130hs --mode full --ninv 144

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
	cd simulation && rm -f *.log *.sp *.out
