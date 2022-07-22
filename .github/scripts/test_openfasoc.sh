#!/bin/bash

#git clone https://github.com/saicharan0112/OpenFASOC.git
#cd OpenFASOC
make install
cd openfasoc/generators/temp-sense-gen
make sky130hd_temp > file.log
if grep "\[ERROR\]" file.log; then exit 1; else exit 0; fi
