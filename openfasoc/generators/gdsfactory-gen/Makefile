# ======================================
# GDSFACTORY generators
# ======================================

.DEFAULT_GOAL := help

help:banner
	@@echo "GDSFACTORY generators :"
	@@echo ""
	@@echo "There are two generators available right now:"
	@@echo "	1. Line Resistance with Via Chain"
	@@echo "	2. MIM Cap Array"
	@@echo ""
	@@echo "The flow is currently supported for skywater 130nm process"
	@@echo ""
	@@echo "Targets supported : "
	@@echo "1. make gen_tc__line_res_via_chain"
	@@echo "	> This will generate the merged structure of met1, met2, met3, met4 and met5 line resistances and the intermediate via chains"
	@@echo ""
	@@echo "2. make gen_tc__mimcap_array"
	@@echo "	> This will generate the mimcap array of met3 and met4"
	@@echo ""
	@@echo "3. make run_drc__line_res_via_chain"
	@@echo "	> This will run drc on the merged gds available in the result_dir/line-res_via-chain/ directory"
	@@echo ""
	@@echo "4. make run_drc__mimcap_array"
	@@echo "	> This will run drc on the gds available in the result_dir/mimcap-array/ directory"
	@@echo ""
	@@echo "5. make run_flow"
	@@echo "	> This will run the above targets in sequence"
	@@echo ""	
	@@echo "6. make clean"
	@@echo "	> This will clean all the files in the result_dir"
	@@echo ""

gen_tc__line_res_via_chain:
	cp ./scripts/line-res_via-chain/pad_forty_met1_met5.GDS ./result_dir/line-res_via-chain/
	make lr_vc__all

gen_tc__mimcap_array:
	cp ./scripts/mimcap-array/pad_forty_met1_met5.GDS ./result_dir/mimcap-array/
	make mimcap_m3

run_drc__line_res_via_chain:
	./scripts/line-res_via-chain/drc-check/run_drc.sh

run_drc__mimcap_array:
	./scripts/mimcap-array/drc-check/run_drc.sh

run_flow:
	make clean
	make gen_tc__line_res_via_chain
	make gen_tc__mimcap_array
	make run_drc__line_res_via_chain
	make run_drc__mimcap_array

# Via Chain and Line Resistance targets

# met1 = layer 68, width = via_dim + 2 * 0.06, spacing = seg_length = width + 0.14 (met1 spacing)
lr_vc__met1:
	python3 ./scripts/line-res_via-chain/via_chain_gen.py --dimension 40 --spacing 0.43 --width 0.29 --res_sets 40 --via_sets 20 --seg_length 0.43 --seg_width 0.2 --via_dim 0.17 --wire_layer 68 --output_dir=./result_dir/line-res_via-chain 
	python3 ./scripts/line-res_via-chain/line_res_gen.py --dimension 40 --spacing 0.43 --width 0.29 --res_sets 40 --wire_layer 68 --output_dir=./result_dir/line-res_via-chain
	python3 ./scripts/line-res_via-chain/line_res_gen.py --dimension 40 --spacing 2 --width 1 --res_sets 10 --wire_layer 68 --mode 1 --output_dir=./result_dir/line-res_via-chain

# met2 = layer 69, width = via_dim + 2 * 0.085, spacing = seg_length = width + 0.14
lr_vc__met2:
	python3 ./scripts/line-res_via-chain/via_chain_gen.py --dimension 40 --spacing 0.46 --width 0.32 --res_sets 40 --via_sets 20 --seg_length 0.46 --seg_width 0.32 --via_dim 0.15 --wire_layer 69 --output_dir=./result_dir/line-res_via-chain
	python3 ./scripts/line-res_via-chain/line_res_gen.py --dimension 40 --spacing 0.46 --width 0.32 --res_sets 40 --wire_layer 69 --output_dir=./result_dir/line-res_via-chain
	python3 ./scripts/line-res_via-chain/line_res_gen.py --dimension 40 --spacing 2 --width 1 --res_sets 10 --wire_layer 69 --mode 1 --output_dir=./result_dir/line-res_via-chain

# met3 = layer 70, width = via_dim + 2 * 0.065, seg_width = via_dim + 2 * 0.085, spacing = seg_length = width + 0.3
lr_vc__met3:
	python3 ./scripts/line-res_via-chain/via_chain_gen.py --dimension 40 --spacing 0.63 --width 0.33 --res_sets 30 --via_sets 20 --seg_length 0.63 --seg_width 0.37 --via_dim 0.2 --wire_layer 70 --output_dir=./result_dir/line-res_via-chain
	python3 ./scripts/line-res_via-chain/line_res_gen.py --dimension 40 --spacing 0.63 --width 0.33 --res_sets 30 --wire_layer 70 --output_dir=./result_dir/line-res_via-chain
	python3 ./scripts/line-res_via-chain/line_res_gen.py --dimension 40 --spacing 2 --width 1 --res_sets 10 --wire_layer 70 --mode 1 --output_dir=./result_dir/line-res_via-chain

# met4 = layer 71, width = via_dim + 2 * 0.065, seg_width = via_dim + 2 * 0.09, spacing = seg_length = width + 0.3
lr_vc__met4:
	python3 ./scripts/line-res_via-chain/via_chain_gen.py --dimension 40 --spacing 0.68 --width 0.33 --res_sets 28 --via_sets 20 --seg_length 0.68 --seg_width 0.38 --via_dim 0.2 --wire_layer 71 --output_dir=./result_dir/line-res_via-chain
	python3 ./scripts/line-res_via-chain/line_res_gen.py --dimension 40 --spacing 0.68 --width 0.33 --res_sets 28 --wire_layer 71 --output_dir=./result_dir/line-res_via-chain
	python3 ./scripts/line-res_via-chain/line_res_gen.py --dimension 40 --spacing 2 --width 1 --res_sets 10 --wire_layer 71 --mode 1 --output_dir=./result_dir/line-res_via-chain

# met5 = layer 72, width = via_dim + 2 * 0.31, seg_width = via_dim + 2 * 0.19, spacing = seg_length = width + 1.6
lr_vc__met5:
	python3 ./scripts/line-res_via-chain/via_chain_gen.py --dimension 40 --spacing 3.2 --width 1.6 --res_sets 6 --via_sets 4 --seg_length 3.2 --seg_width 1.18 --via_dim 0.8 --wire_layer 72 --output_dir=./result_dir/line-res_via-chain
	python3 ./scripts/line-res_via-chain/line_res_gen.py --dimension 40 --spacing 3.2 --width 1.6 --res_sets 6 --wire_layer 72 --output_dir=./result_dir/line-res_via-chain
	python3 ./scripts/line-res_via-chain/line_res_gen.py --dimension 40 --spacing 5 --width 2.5 --res_sets 4 --wire_layer 72 --mode 1 --output_dir=./result_dir/line-res_via-chain

lr_vc__merge:
	python3 ./scripts/line-res_via-chain/merge_structures.py --output_dir=./result_dir/line-res_via-chain

lr_vc__all:	lr_vc__met1 lr_vc__met2 lr_vc__met3 lr_vc__met4 lr_vc__met5 lr_vc__merge


# Mimcap targets

mimcap_m3:
	python3 ./scripts/mimcap-array/mimcap_gen.py --input_file ./scripts/mimcap-array/sky130_fd_pr__cap_mim_m3_1_FJK8MM.gds --pitch 2.48 --wtop 0.3 --wbot 0.3 --lyrtop 71 --output_dir=./result_dir/mimcap-array

mimcap_m4:
	python3 ./scripts/mimcap-array/mimcap_gen.py --input_file ./scripts/mimcap-array/sky130_fd_pr__cap_mim_m3_2_FJK8MM.gds --pitch 4 --wtop 1.6 --wbot 0.3 --lyrtop 72 --output_dir=./result_dir/mimcap-array



clean:
	rm -f ./result_dir/line-res_via-chain/*.gds
	rm -f ./result_dir/line-res_via-chain/*.GDS
	rm -f ./result_dir/line-res_via-chain/*.rpt
	rm -f ./result_dir/mimcap-array/*.gds
	rm -f ./result_dir/mimcap-array/*.GDS
	rm -f ./result_dir/mimcap-array/*.rpt

banner:
	@@echo "==============================================================="
	@@echo "   ___  _____ ______ _   _ _____  _     ____   ___   ____      "
	@@echo "  / _ \|  _  \| ____| \ | |  ___|/ \   / ___| / _ \ / ___|     "
	@@echo " | | | | |_) ||  _| |  \| | |_  / _ \  \___ \| | | | |         "
	@@echo " | |_| |  __/ | |___| |\  |  _|/ ___ \  ___) | |_| | |___      "
	@@echo "  \___/|_|    |_____|_| \_|_| /_/   \_\|____/ \___/ \____|     "
	@@echo "						               "
	@@echo "==============================================================="
	@@echo "OpenFASOC is focused on open source automated analog generation"
	@@echo "from user specification to GDSII with fully open-sourced tools."
	@@echo "This project is led by a team of researchers at the University of Michigan and is inspired from FASOC"
	@@echo ""
