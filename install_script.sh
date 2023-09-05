#!/bin/bash

sudo apt install gcc g++

mv docker/conda/scripts/get_conda.sh .

chmod +x get_conda.sh
chmod +x dependencies.sh

./get_conda.sh
sudo ./dependencies.sh
source ~/.bashrc
