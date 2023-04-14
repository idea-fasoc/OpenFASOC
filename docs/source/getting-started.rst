Getting Started
===============================

.. contents:: Contents


Installation
--------------

#. `Express Installation`_
#. `Manual Installation`_
#. `Running via Docker`_

Express Installation
#####################

First, ``cd`` into a directory of your choice and clone the OpenFASoC repository:

.. code-block:: bash

  git clone https://github.com/idea-fasoc/openfasoc

Now go to the home location of this repository (where the README.rst file is located) and run `sudo ./dependencies.sh`. This will install the necessary version of all Python libraries, tools (OpenROAD, Yosys, Magic, Netgen) and skywater-pdk as required by OpenFASoC **via Conda packages**. It will also set the ``PDK_ROOT`` environment variable to the pdk data location.

.. warning::

  The ``dependencies.sh`` script supports Ubuntu and CentOS (except simulators). In RHEL 7 and 8, the script will install all required conda packages but not Simulators (ngspice and Xyce) and KLayout, which has to be installed manually.

.. note::

  gdsfactory, a Python package used by some of the generators, requires Python version ``>=3.7``. If your machine does not have a supported version, the installation of gdsfactory is skipped.

Done!

Manual Installation
#####################

Standalone
^^^^^^^^^^^

First install all the dependencies required by OpenFASoC:

.. include:: ../../README.rst
  :start-after: Please install the following tools with the recommended commit ids for a stable functioning of the flow:
  :end-before: Design Generation

.. note::

  We recommend installing OpenROAD with the GUI enabled for easier debugging.

Check if the installed tools are in your PATH by running their respective commands in a terminal: ``magic``, ``netgen``, ``klayout``, ``yosys`` and ``openroad``.

Now ``cd`` into a directory of your choice and clone the OpenFASoC repository:

.. code-block:: bash

  git clone https://github.com/idea-fasoc/openfasoc

Go to the root directory of the repo and install all required Python libraries using:

.. code-block:: bash

  pip install -r requirements.txt

.. note::

  If you plan to contribute, you should also run ``pip install -r requirements_dev.txt``.

Using Conda
^^^^^^^^^^^^

Conda is an open source package, dependency and environment management system available in many platforms.

OpenFASoC's dependencies can be very easily installed if you're using a Conda environment. If you're not, start by `installing Miniconda <https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html>`_.

The `conda-eda <https://github.com/hdl/conda-eda>`_ project keeps periodic builds of most tools required by OpenFASoC in the `LiteX-Hub channel <https://anaconda.org/LiteX-Hub/>`_. To install them, start by creating a new environment for OpenFASoC (if you don't have one already):

.. code-block:: bash

  conda create --name "openfasoc" python=3.8

Then, install the available dependencies within Conda:

.. code-block:: bash

  conda install -c litex-hub magic netgen yosys openroad open_pdks.sky130a

.. note::

  KLayout isn't available yet as a Conda package at the time of writing, thus it has to be manually installed. See `their website <https://www.klayout.de/build.html>`_ for instructions.

Now ``cd`` into a directory of your choice and clone the OpenFASoC repository:

.. code-block:: bash

  git clone https://github.com/idea-fasoc/openfasoc

Finally, ``cd`` to the root of the cloned repository and install all required Python packages in your Conda environment:

.. code-block::

  conda install --file requirements.txt


Running via Docker
#####################

Another way to run the generators is using the OpenFASoC Docker image which is currently used to test the temp-sense generator flow during CI. This alternative doesn't require to install all dependencies in your machine.

Install `Docker <https://docs.docker.com/engine/install/ubuntu/>`_ in your machine before you proceed.

1. Clone the OpenFASOC repository:

.. code-block:: bash

  git clone https://github.com/idea-fasoc/OpenFASOC.git

2. Run this command to access OpenFASOC folder from the container:

.. code-block:: bash

  docker run -v </path/to/OpenFASOC/clone>:/shared/OpenFASOC/ -w /shared/OpenFASOC/ msaligane/openfasoc:stable bash -c "pip3 install -r requirements.txt && cd openfasoc/generators/temp-sense-gen/ && make clean && make sky130hd_temp"

3. To view results after the flow ran (see `Run OpenFASoC flow`_), go to `/<path_to_OpenFASOC>/openfasoc/generators/temp-sense-gen/work` where you can find the final GDS and DEF files, DRC and LVS reports, the spice netlists and the Verilog file.

4. To view results after the full run (including simulations), go to `/<path_to_OpenFASOC>/openfasoc/generators/temp-sense-gen/simulations/run/` where you can find the directory for the type of inverter-header combination in which you can find the simulation log files along with the spice netlists for various temperature calibrations.

.. warning::

  In this case, files are be generated with root privileges. So, when cleaning the run, use `sudo` to have a complete clean.


Run OpenFASoC Flow
--------------------

Generic way
############

* First ``cd`` into the directory where the OpenFASoC repository was cloned;

* Now edit the `platform_config.json <https://github.com/idea-fasoc/OpenFASOC/blob/main/openfasoc/common/platform_config.json>`_ file, replacing the ``open_pdks`` value with the path to the sky130A/ directory;

* Export the ``PDK_ROOT`` environment variable to your skywater-pdk location until the sky130A/ directory (not required if the dependencies are installed via the dependencies.sh script);

* Now go to one of the generators with ``cd openfasoc/generators/<generator_name>`` and run ``make`` to list down all the generator specific targets;

* Run ``make <library>_<generator>_<mode>`` to begin the flow.

Below is an example of options for the temp-sense generator:

.. code-block:: bash

    $ cd openfasoc/generators/temp-sense-gen/
    $ make
    ==============================================================
      ___  _____ ______ _   _ _____  _     ____   ___   ____
      / _ \|  _  \| ____| \ | |  ___|/ \   / ___| / _ \ / ___|
    | | | | |_) ||  _| |  \| | |_  / _ \  \___ \| | | | |    
    | |_| |  __/ | |___| |\  |  _|/ ___ \  ___) | |_| | |___ 
      \___/|_|    |_____|_| \_|_| /_/   \_\|____/ \___/ \____|

    ===============================================================
    OpenFASOC is focused on open source automated analog generation
    from user specification to GDSII with fully open-sourced tools.
    This project is led by a team of researchers at the University of Michigan and is inspired from FASOC
    For more info, visit https://fasoc.engin.umich.edu/

    IP: Temperature Sensor 
    Supported Technology: Sky130A 
    Supported Library: sky130hd

    Targets supported:
    1. make sky130hd_temp_verilog
        >> This will create the verilog file for the thermal sensor IP. It doesn't create a macro, won't create lef/def/gds files and won't run simulations 
    2. make sky130hd_temp [ninv=<num>] [nhead=<num>]
        >> This will create the macro for the thermal sensor, creates the lef/def/gds/spice netlist files and performs lvs/drc checks. But this won't run simulations.
    3. make sky130hd_temp_full [ninv=<num>] [nhead=<num>] [sim=pex]
        >> This will create the macro for the thermal sensor, creates the lef/def/gds/spice netlist files, performs lvs/drc checks and also runs simulations.
        >> Note: Only Pre-PEX simulations are performed, by default, under this target. To perform Post-PEX simulations as well, set sim to 'pex' as shown in the target definition
    4. make clean
        >> This will clean all files generated during the run inside the run/, flow/ and work/ directories
    5. make help
        >> Displays this message


    $ make sky130hd_temp

Additional Resources
---------------------

For more information on how each generator works and what circuits they're creating, check :doc:`generators`.

You can also find more examples of how to use OpenFASoC in the :doc:`examples` page.

Tapeouts done with OpenFASoC are described in :doc:`tapeouts`.
