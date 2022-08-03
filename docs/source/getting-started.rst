Getting Started with OpenFASoC
===============================

Install Dependencies
###########################

Go to the home location of this repository (where this README.rst file is located) and run `source ./Dependencies.sh`. This will install all the python libraries required for OpenFASoC, tools (openroad, Yosys, magic, netgen, Klayout) via conda packages and skywater-pdk on your machine. This will also set the environment variable PDK_ROOT to the pdk data location. The script supports Ubuntu20.04 and Centos7. 


Run OpenFASoC flow
##############################

Generic way
.................

* First clone the OpenFASoC github repository using the command - `git clone https://github.com/idea-fasoc/openfasoc`

* Now edit the platform_config.json file as suggested in the `Spice Simulation Flow` subsection under OpenFASoC section

* Edit the open_pdks location according to the PDK_ROOT variable

* Set the PDK_ROOT variable to your skywater-pdk location till the sky130A level (not required if the dependencies are installed via the dependencies.sh script)

* Now go to one of the generators and run `make` to list down all the generator specific targets.

* Run `make <library>_<generator>_<mode>` to begin the flow

Below is an example for the temp-sense generator


.. code-block:: bash

    $cd openfasoc/generators/temp-sense-gen
    $make
    ==============================================================
     ___  _____ ______ _   _ _____  _     ____   ___   ____
    / _ \|  _  \| ____| \ | |  ___|/ \   / ___| / _ \ / ___|
   | | | | |_) ||  _| |  \| | |_  / _ \  \___ \| | | | |
   | |_| |  __/ | |___| |\  |  _|/ ___ \  ___) | |_| | |___
    \___/|_|    |_____|_| \_|_| /_/   \_\|____/ \___/ \____|

    ===============================================================
    OpenFASOC is focused on open-source automate analog generation
    from user specification to GDSII with fully open-sourced tools.
    This project is led by a team of researchers at the Universities of Michigan is inspired from FASOC whcih sits on proprietary tools
    For more info, visit https://fasoc.engin.umich.edu/

    IP: Temperature Sensor
    Supported Technology: Sky130A
    Supported Library: sky130hd

    Targets supported:
    1. make sky130hd_temp
        >> This will create the macro for the thermal sensor, creates the lef/def/gds files and performs lvs/drc checks. It won't run simulations.
    2. make sky130hd_temp_verilog
        >> This will create the verilog file for the thermal sensor IP. It doesn't create a macro, won't create lef/def/gds files and won't run simulations
    3. make sky130hd_temp_full
        >> This will create the macro for the thermal sensor, creates the lef/def/gds files, performs lvs/drc checks and also runs simulations.
        >> [Warning] Currently, this target is in alpha phase
    4. make clean
        >> This will clean all files generated during the run inside the run/, flow/ and work/ directories
    5. make help
        >> Displays this message
    $make sky130hd_temp


Run OpenFASoC via docker
.........................

**Another way to run the generators is using the efabless docker image which is currently used to test the temp-sense generator flow during smoke test**

Install docker on your machine before you proceed

1. Clone the OpenFASOC repository - `git clone https://github.com/idea-fasoc/OpenFASOC.git`

2. Run this command to access OpenFASOC folder from the container - `docker run -v /path/to/OpenFASOC/clone:/shared/OpenFASOC/ -w /shared/OpenFASOC/ saicharan0112/openfasoc_ci:klayout_deb bash -c "pip3 install -r requirements.txt && cd openfasoc/generators/temp-sense-gen/ && make clean && make sky130hd_temp"`

3. To view results, go to `/<path_to_OpenFASOC>/openfasoc/generators/temp-sense/work` where you could find the final gds and def files, drc and lvs reports, the spice netlists and the verilog file.

**Note** Files will be generated with root privileges. So, while cleaning the run, use `sudo` to have a complete clean.
