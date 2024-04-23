#!/bin/bash

if !command -v conda &> /dev/null
then 
    echo "Conda not found. Exiting..."
    exit 1
fi

PATH=/usr/bin/miniconda3/bin:$PATH

conda update conda --all -y
update_successful=true
echo "trying to install open_pdks"

mkdir ./mycondaenv

conda create --prefix ./mycondaenv -y
source /usr/bin/miniconda3/etc/profile.d/conda.sh
conda activate ./mycondaenv

conda install -c anaconda -c conda-forge -c litex-hub open_pdks.gf180mcuc -y;if [ $? != 0 ]; then update_successful=false; echo "open_pdks could not be updated"; fi
conda install -c anaconda -c conda-forge -c litex-hub open_pdks.sky130A -y;if [ $? != 0 ]; then update_successful=false; echo "open_pdks could not be updated"; fi


mkdir gf180mcuC
mkdir sky130A
cp ./mycondaenv/share/pdk/gf180mcuC/libs.tech/magic/gf180mcuC.magicrc ./gf180mcuC
cp ./mycondaenv/share/pdk/sky130A/libs.tech/magic/sky130A.magicrc ./sky130A
cp ./mycondaenv/share/pdk/gf180mcuC/libs.tech/netgen/gf180mcuC_setup.tcl ./gf180mcuC
cp ./mycondaenv/share/pdk/sky130A/libs.tech/netgen/sky130A_setup.tcl ./sky130A

rm -r ./mycondaenv