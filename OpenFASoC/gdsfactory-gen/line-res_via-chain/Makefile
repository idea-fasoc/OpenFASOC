# Via Chain and Line Resistance Makefile

# met1 = layer 68, width = via_dim + 2 * 0.06, spacing = seg_length = width + 0.14 (met1 spacing)
met1:
	python3 via_chain_gen.py --dimension 40 --spacing 0.43 --width 0.29 --res_sets 40 --via_sets 20 --seg_length 0.43 --seg_width 0.2 --via_dim 0.17 --wire_layer 68
	python3 line_res_gen.py --dimension 40 --spacing 0.43 --width 0.29 --res_sets 40 --wire_layer 68
	python3 line_res_gen.py --dimension 40 --spacing 2 --width 1 --res_sets 10 --wire_layer 68 --mode 1

# met2 = layer 69, width = via_dim + 2 * 0.085, spacing = seg_length = width + 0.14
met2:
	python3 via_chain_gen.py --dimension 40 --spacing 0.46 --width 0.32 --res_sets 40 --via_sets 20 --seg_length 0.46 --seg_width 0.32 --via_dim 0.15 --wire_layer 69
	python3 line_res_gen.py --dimension 40 --spacing 0.46 --width 0.32 --res_sets 40 --wire_layer 69
	python3 line_res_gen.py --dimension 40 --spacing 2 --width 1 --res_sets 10 --wire_layer 69 --mode 1

# met3 = layer 70, width = via_dim + 2 * 0.065, seg_width = via_dim + 2 * 0.085, spacing = seg_length = width + 0.3
met3:
	python3 via_chain_gen.py --dimension 40 --spacing 0.63 --width 0.33 --res_sets 30 --via_sets 20 --seg_length 0.63 --seg_width 0.37 --via_dim 0.2 --wire_layer 70
	python3 line_res_gen.py --dimension 40 --spacing 0.63 --width 0.33 --res_sets 30 --wire_layer 70
	python3 line_res_gen.py --dimension 40 --spacing 2 --width 1 --res_sets 10 --wire_layer 70 --mode 1

# met4 = layer 71, width = via_dim + 2 * 0.065, seg_width = via_dim + 2 * 0.09, spacing = seg_length = width + 0.3
met4:
	python3 via_chain_gen.py --dimension 40 --spacing 0.68 --width 0.33 --res_sets 28 --via_sets 20 --seg_length 0.68 --seg_width 0.38 --via_dim 0.2 --wire_layer 71
	python3 line_res_gen.py --dimension 40 --spacing 0.68 --width 0.33 --res_sets 28 --wire_layer 71
	python3 line_res_gen.py --dimension 40 --spacing 2 --width 1 --res_sets 10 --wire_layer 71 --mode 1

# met5 = layer 72, width = via_dim + 2 * 0.31, seg_width = via_dim + 2 * 0.19, spacing = seg_length = width + 1.6
met5:
	python3 via_chain_gen.py --dimension 40 --spacing 3.2 --width 1.6 --res_sets 6 --via_sets 4 --seg_length 3.2 --seg_width 1.18 --via_dim 0.8 --wire_layer 72
	python3 line_res_gen.py --dimension 40 --spacing 3.2 --width 1.6 --res_sets 6 --wire_layer 72
	python3 line_res_gen.py --dimension 40 --spacing 5 --width 2.5 --res_sets 4 --wire_layer 72 --mode 1

merge:
	python3 merge_structures.py

all:	met1 met2 met3 met4 met5 merge


clean:
	rm -f *.gds
	rm *_drc.txt
