#!/bin/bash

for file in error_within_x.csv golden_error_opt.csv search_result.csv
do
	if ! [ -e $file ]
	then
	       echo "[ERROR] $file is not created"
	fi
done

module_name=$(grep "module_name" test.json | cut -d "\"" -f 4)

if [ -e work ]
then
	cd work
	for file in $module_name.def $module_name.gds $module_name\_pex.spice $module_name.spice $module_name.v $module_name.sdc
	do
        	if ! [ -e $file ]
        	then
               		echo "[ERROR] $file is not created"
        	fi
	done
else
	echo "[ERROR] Work directory not created"
fi
