OpenFASoC
===================

**OpenFASoC: Fully Open-Source Autonomous SoC Synthesis using Customizable Cell-Based Synthesizable Analog Circuits**

.. image:: https://readthedocs.org/projects/openfasoc/badge/?version=latest
    :target: https://openfasoc.readthedocs.io/en/latest/?badge=latest


OpenFASOC is focused on open-source automated analog generation from user specification to GDSII with fully open-sourced tools.
This project is led by a team of researchers at the University of Michigan and is inspired by FASoC, that sits on proprietary tools. (See more about FaSoC at `website <https://fasoc.engin.umich.edu/>`_)


* **Temperature sensor -**
    .. image:: https://github.com/idea-fasoc/OpenFASOC/actions/workflows/tempSense_sky130hd.yml/badge.svg
        :target: https://github.com/idea-fasoc/OpenFASOC/actions/workflows/tempSense_sky130hd.yml

    .. image:: https://github.com/idea-fasoc/OpenFASOC/actions/workflows/verify_latest_tools_versions.yml/badge.svg
        :target: https://github.com/idea-fasoc/OpenFASOC/actions/workflows/verify_latest_tools_versions.yml

    .. image:: https://colab.research.google.com/assets/colab-badge.svg
        :target: https://colab.research.google.com/github/idea-fasoc/OpenFASOC/blob/main/docs/source/notebooks/temp-sense-gen/temp_sense_genCollab.ipynb

* **LDO -**
    .. image:: https://github.com/idea-fasoc/OpenFASOC/actions/workflows/ldo_sky130hvl.yml/badge.svg
        :target: https://github.com/idea-fasoc/OpenFASOC/actions/workflows/ldo_sky130hvl.yml

    .. image:: https://colab.research.google.com/assets/colab-badge.svg
        :target: https://colab.research.google.com/github/idea-fasoc/OpenFASOC/blob/main/docs/source/notebooks/ldo-gen/LDO_notebook.ipynb

* **Cryogenic -**
    .. image:: https://github.com/idea-fasoc/OpenFASOC/actions/workflows/cryo_gen.yml/badge.svg
        :target: https://github.com/idea-fasoc/OpenFASOC/actions/workflows/cryo_gen.yml

* **Glayout Generators -**
    `Installation and Running <https://github.com/idea-fasoc/OpenFASOC/tree/main/openfasoc/generators/gdsfactory-gen/tapeout_and_RL/README.md>`_


Getting Started
****************

Install all the prerequisites using the `dependencies.sh` script provided in the home location of this project (where this README.rst file is found). Supports CentOS7, Ubuntu 20.04 LTS and Ubuntu 22.04 LTS.

.. code-block:: bash

    $ sudo ./dependencies.sh

For more info on getting-started, please refer to ["Getting Started" section ](https://openfasoc.readthedocs.io/en/latest/getting-started.html)

Below are the tool requirements along with their currently support versions that are updated regularly upon testing againsts the generators.

  1. `Magic <https://github.com/RTimothyEdwards/magic>`_ (version:8.3.453)

  2. `Netgen <https://github.com/RTimothyEdwards/netgen>`_ (version:1.5.264)

  3. `Klayout <https://github.com/KLayout/klayout>`_ (version:0.28.12-1)

      - Please use this command to build preferably: `./build.sh -option '-j8' -noruby -without-qt-multimedia -without-qt-xml -without-qt-svg`


  4. `Yosys <https://github.com/The-OpenROAD-Project/yosys>`_ (version:0.36+8)


  5. `OpenROAD <https://github.com/The-OpenROAD-Project/OpenROAD>`_ (version:2.0_10905)

  6. `Open_pdks <https://github.com/RTimothyEdwards/open_pdks>`_ (version:1.0.286)

   - open_pdks is required to run drc/lvs check and the simulations
   - After open_pdks is installed, please update the **open_pdks** key in `common/platform_config.json` with the installed path, down to the sky130A folder

  7. `Xyce <https://github.com/Xyce/Xyce>`_ (version: 7.6)

   - Once the Xyce installation is complete, please make sure to add Xyce binary to $PATH environment variable.

  **Other notice:**

   - Python 3.7 is used in this generator.
   - All the required tools need to be loaded into the environment before running this generator.



Generators
********************

+------------------------------------------+--------------------+----------------------------+----------------------------------------------------------------------------------------------------------------+
| Generator                                | Technology nodes   | Supported                  | Documentation                                                                                                  |
|                                          |                    |                            |                                                                                                                |
+==========================================+====================+============================+================================================================================================================+
| Temperature Sensor                       | sky130hd           |    Yes                     | https://openfasoc.readthedocs.io/en/latest/flow-tempsense.html                                                 |       
+------------------------------------------+--------------------+----------------------------+----------------------------------------------------------------------------------------------------------------+
| Low dropout Voltage Regulator (LDO)      | sky130hvl          |    Yes                     | https://openfasoc.readthedocs.io/en/latest/flow-ldo.html                                                       |  
+------------------------------------------+--------------------+----------------------------+----------------------------------------------------------------------------------------------------------------+ 
| Cryogenic                                | sky130hs,          |    No (In-progress)        | https://openfasoc.readthedocs.io/en/latest/flow-cryo.html                                                      |                                      
|                                          | sky130hd,          |                            |                                                                                                                |                        
|                                          | sky130hvl          |                            |                                                                                                                |                                     
+------------------------------------------+--------------------+----------------------------+----------------------------------------------------------------------------------------------------------------+
| Glayout                                  | sky130,            |     Yes                    | https://github.com/idea-fasoc/OpenFASOC/tree/main/openfasoc/generators/gdsfactory-gen/tapeout_and_RL/README.md |
|                                          | gf180              |                            |                                                                                                                |
+------------------------------------------+--------------------+----------------------------+----------------------------------------------------------------------------------------------------------------+


Tapeouts and testing setup
*********************************

Please refer to our testing setup in our `tapeouts and testing setup section <https://github.com/idea-fasoc/openfasoc-tapeouts>`_.

Citation
****************

If you find this tool useful in your research, we kindly request to cite our papers:

 - Tutu Ajayi et al., "`An Open-source Framework for Autonomous SoC Design with Analog Block Generation <https://ieeexplore.ieee.org/document/9344104>`_," 2020 IFIP/IEEE 28th International Conference on Very Large Scale Integration (VLSI-SOC), 2020, pp. 141-146.

 - Qirui Zhang et al., "`An Open-Source and Autonomous Temperature Sensor Generator Verified With 64 Instances in SkyWater 130 nm for Comprehensive Design Space Exploration <https://ieeexplore.ieee.org/abstract/document/9816083>`_," in IEEE Solid-State Circuits Letters, vol. 5, pp. 174-177, 2022.
