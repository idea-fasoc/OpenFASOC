#!/bin/bash -f
# Run ngspice Command Serial or Parallel (Update the link to your ngspice path) Like: /usr/bin/ngspice
type=$1
echo "Type is $type (Allowed type are serial or parallel"
if [ "$type" == "serial" ]; then
	/usr/local/bin/ngspice ${2} -b -o ${2}.log
elif [ "$type" == "parallel" ]; then
	/home/chandru/Tools/ngspice_klu/ngspice-ngspice/release/src/ngspice ${2} -b -o ${2}_parallel.log
else
	echo "Incorrect Options only serial and parallel allowed"
fi
