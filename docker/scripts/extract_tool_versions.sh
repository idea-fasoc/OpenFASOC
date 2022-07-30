#!/bin/bash

echo "klayout - $(dpkg -l | grep klayout | tr -s " " | cut -d " " -f 3)"
echo "OpenROAD - $(conda list | grep -e openroad | tr -s " " | cut -d " " -f 2 | cut -d "_" -f 1-2)"
echo "yosys - $(yosys -version | cut -d " " -f 2)"
echo "magic - $(magic --version)"
echo "netgen - $(conda list | grep netgen | tr -s " " | cut -d " " -f 2 | cut -d "_" -f 1)"
echo "open_pdks - $(cat $PDK_ROOT/sky130A/.config/nodeinfo.json | grep open_pdks | grep "\." | cut -d "\"" -f 4)"