Steps to install on Centos7
===============================

Install all dependent packages
-------------------------------

In this tutorial, it is considered that the installation is happening on a clean centos7 OS.

`yum install m4 tcsh libX11-devel tcl-devel tk-devel ncurses-devel bzip2 mesa-libGL-devel freeglut freeglut-devel gcc-c++ python3 make git clang -y`


Install Magic
---------------

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
----------------

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
------------------

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
-----------------------------

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
-------------------

First, the Yosys code repository needs to be cloned to the local machine -

* `git clone https://github.com/YosysHQ/yosys.git`

Then, change to the cloned yosys directory and begin the installation process -

* `cd yosys`

Below commands will build yosys binary on your local machine -

* `make config-clang`
* `make`
* `make install`