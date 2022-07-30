conda -V 
conda list | grep -e openroad -e magic -e yosys -e open_pdks.sky130a -e netgen | tr -s ' '| cut -d " " -f 1-2

