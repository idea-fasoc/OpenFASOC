Getting Started with OpenFASoC
===============================


Steps to install on Centos7
###############################

Install all dependent packages
...................................

In this tutorial, it is considered that the installation is happening on a clean centos7 OS.

`yum install m4 tcsh libX11-devel tcl-devel tk-devel ncurses-devel bzip2 mesa-libGL-devel freeglut freeglut-devel gcc-c++ python3 make git clang -y`


Install Magic
.................

First, the magic code repository needs to be cloned to the local machine -

* `git clone git://opencircuitdesign.com/magic`

Then, change to the cloned magic directory and begin the installation process -

* `cd magic`

This command will verify the dependencies required for magic installation. -

* `./configure`

This command will compile the code -

* `make`

This command will install the binary in the directed location (Default location is /usr/local/bin) -

* `make install`


Install Netgen
................

First, the magic code repository needs to be cloned to the local machine -

* `git clone git://opencircuitdesign.com/netgen`

Then, change to the cloned netgen directory and begin the installation process -

* `cd netgen`

This command will verify the dependencies required for netgen installation. -

* `./configure`

This command will compile the code -

* `make`

This command will install the binary in the directed location (Default location is /usr/local/bin) -

* `make install`


Install OpenROAD
...................

First, clone the OpenROAD git repository on to your local machine. This will also recursively initialize the third-party submodules -

* `git clone --recursive https://github.com/The-OpenROAD-Project/OpenROAD.git`

Now change to the cloned repository -

* `cd OpenROAD/`

This shell script will install all the dependencies required for OpenROAD to build -

* `./etc/DependencyInstaller.sh -dev`

In the end, run this two commands as directed by the script -

* `source /opt/rh/devtoolset-8/enable`
* `source /opt/rh/llvm-toolset-7.0/enable`

Now, this shell script will build the OpenROAD app and store it in build/src folder by default -

* `./etc/Build.sh`

Now move the generated binary from the default location to the /usr/bin so that it can be accessed from the command line by directly typing the *openroad* command -

* `cp build/src/openroad /usr/bin/.`


Install Skywater 130nm PDK
..............................

Similar to above installation process, clone the skywater-pdk git repository from the github -

* `git clone https://github.com/google/skywater-pdk`

Change to the cloned repository and start initializing the submodules -

* `cd skywater-pdk`

Note that you can initialize a set of libraries as per your requirement. Below initializes the basic libraries -

* `git submodule init libraries/sky130_fd_io/latest`
* `git submodule init libraries/sky130_fd_pr/latest`
* `git submodule init libraries/sky130_fd_sc_hd/latest`
* `git submodule init libraries/sky130_fd_sc_hvl/latest`
* `git submodule update`

Now build the timing files for the above selected libraries -

* `make timing`

This completes the first step in the process of installating the PDK. Now use the open_pdks installer to build the PDK from the libraries to use them across the OSEDA tools. -

* `cd ../`

Clone the open_pdks github repository -

* `git clone https://github.com/RTimothyEdwards/open_pdks.git`
* `cd open_pdks`

Run the below command which verifies all the dependencies required for this PDK build. Notice that the *--enable-sky130-pdk* option is pointing to the libraries location which we had arranged in the first step. The *--prefix* option will tell the installer to place the PDK files in a particular location. In this case, the PDK files will be installed in the location */pdks/share/pdk/* -

* `./configure --enable-sky130-pdk=/pdks/skywater-pdk --prefix=/pdks`

This command will compile all the files (builds gds files, does the replacement inside the files if required) -

* `make`

This command will install the PDK data in the respective location (the default location will be /usr/share/pdk. Else the location given with the *--prefix* is considered) -

* `make install`

It is suggested to declare an environment variable which points to the pdk data location and place it in the .bashrc (or your terminla environment file). Below is an example on how to declare the pdk data environment variable. -

* `export PDK_ROOT=/pdks/share/pdk/`


Install Klayout
.................

First, the Yosys code repository needs to be cloned to the local machine -

* `git clone https://github.com/YosysHQ/yosys.git`

Then, change to the cloned yosys directory and begin the installation process -

* `cd yosys`

Below commands will build yosys binary on your local machine -

* `make config-clang`
* `make`
* `make install`


Steps to install on Ubuntu20
##############################

Install all dependent packages
..................................

In this tutorial, it is considered that the installation is happening on a clean centos7 OS.

`apt install python3 m4 libx11-dev gcc mesa-common-dev libglu1-mesa-dev csh tcl-dev tk-dev git clang -y`


Install Magic
....................

First, the magic code repository needs to be cloned to the local machine -

* `git clone git://opencircuitdesign.com/magic`

Then, change to the cloned magic directory and begin the installation process -

* `cd magic`

This command will verify the dependencies required for magic installation. -

* `./configure`

This command will compile the code -

* `make`

This command will install the binary in the directed location (Default location is /usr/local/bin) -

* `make install`


Install Netgen
....................

First, the magic code repository needs to be cloned to the local machine -

* `git clone git://opencircuitdesign.com/netgen`

Then, change to the cloned netgen directory and begin the installation process -

* `cd netgen`

This command will verify the dependencies required for netgen installation. -

* `./configure`

This command will compile the code -

* `make`

This command will install the binary in the directed location (Default location is /usr/local/bin) -

* `make install`


Install OpenROAD
.....................

First, clone the OpenROAD git repository on to your local machine. This will also recursively initialize the third-party submodules -

* `git clone --recursive https://github.com/The-OpenROAD-Project/OpenROAD.git`

Now change to the cloned repository -

* `cd OpenROAD/`

This shell script will install all the dependencies required for OpenROAD to build -

* `./etc/DependencyInstaller.sh -dev`

Now, this shell script will build the OpenROAD app and store it in build/src folder by default -

* `./etc/Build.sh`

Now move the generated binary from the default location to the /usr/bin so that it can be accessed from the command line by directly typing the *openroad* command -

* `cp build/src/openroad /usr/bin/.`


Install Skywater 130nm PDK
.................................

Similar to above installation process, clone the skywater-pdk git repository from the github -

* `git clone https://github.com/google/skywater-pdk`

Change to the cloned repository and start initializing the submodules -

* `cd skywater-pdk`

Note that you can initialize a set of libraries as per your requirement. Below initializes the basic libraries -

* `git submodule init libraries/sky130_fd_io/latest`
* `git submodule init libraries/sky130_fd_pr/latest`
* `git submodule init libraries/sky130_fd_sc_hd/latest`
* `git submodule init libraries/sky130_fd_sc_hvl/latest`
* `git submodule update`

Now build the timing files for the above selected libraries -

* `make timing`

This completes the first step in the process of installating the PDK. Now use the open_pdks installer to build the PDK from the libraries to use them across the OSEDA tools. -

* `cd ../`

Clone the open_pdks github repository -

* `git clone https://github.com/RTimothyEdwards/open_pdks.git`
* `cd open_pdks`

Run the below command which verifies all the dependencies required for this PDK build. Notice that the *--enable-sky130-pdk* option is pointing to the libraries location which we had arranged in the first step. The *--prefix* option will tell the installer to place the PDK files in a particular location. In this case, the PDK files will be installed in the location */pdks/share/pdk/* -

* `./configure --enable-sky130-pdk=/pdks/skywater-pdk --prefix=/pdks`

This command will compile all the files (builds gds files, does the replacement inside the files if required) -

* `make`

This command will install the PDK data in the respective location (the default location will be /usr/share/pdk. Else the location given with the *--prefix* is considered) -

* `make install`

It is suggested to declare an environment variable which points to the pdk data location and place it in the .bashrc (or your terminla environment file). Below is an example on how to declare the pdk data environment variable. -

* `export PDK_ROOT=/pdks/share/pdk/`


Install Klayout
.......................

First, the Yosys code repository needs to be cloned to the local machine -

* `git clone https://github.com/YosysHQ/yosys.git`

Then, change to the cloned yosys directory and begin the installation process -

* `cd yosys`

Below commands will build yosys binary on your local machine -

* `make config-clang`
* `make`
* `make install`


Run OpenFASoC flow
##############################

Generic way
.................

* First clone the OpenFASoC github repository using the command - `git clone https://github.com/idea-fasoc/openfasoc`

* Now edit the platform_config.json file as suggested in the `Spice Simulation Flow` subsection under OpenFASoC section

* Set the PDK_ROOT variable to your skywater-pdk location till the sky130A level

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

2. Change to the OpenFASOC directory - `cd OpenFASOC`

3. Run this command to access OpenFASOC folder from the container - `docker run -it -v $PWD:$PWD -e PDK_ROOT='/pdk_data' -w $PWD saicharan0112/openfasoc:stable`

4. To test, go to `openfasoc/generators/temp-sense` and type `make sky130hd_temp` to run the temp-sense generator.

**Note** Files will be generated with root privileges. So, while cleaning the run, use `sudo` to have a complete clean.
