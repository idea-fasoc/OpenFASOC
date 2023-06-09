OpenFASoC
===================

**OpenFASoC: Fully Open-Source Autonomous SoC Synthesis using Customizable Cell-Based Synthesizable Analog Circuits**

.. image:: https://readthedocs.org/projects/openfasoc/badge/?version=latest
    :target: https://openfasoc.readthedocs.io/en/latest/?badge=latest


OpenFASOC is focused on open-source automate analog generation from user specification to GDSII with fully open-sourced tools.
This project is led by a team of researchers at the University of Michigan is inspired from FASoC whcih sits on proprietary tools. (See more about FaSoC at `website <https://fasoc.engin.umich.edu/>`_)


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

Prerequisites
****************

Install all the prerequisites using `dependencies.sh` script provided in the home location of this project (where this README.rst file is found). Supports CentOS7 and Ubuntu20.


(Or) Please install the following tools by building the tools manually from their code base with the recommended commit ids for a stable functioning of the flow:

  1. `Magic <https://github.com/RTimothyEdwards/magic>`_ (version:8.3.389)

  2. `Netgen <https://github.com/RTimothyEdwards/netgen>`_ (version:1.5.251)

  3. `Klayout <https://github.com/KLayout/klayout>`_ (version:0.28.6-1)

      - Please use this command to build preferably: `./build.sh -option '-j8' -noruby -without-qt-multimedia -without-qt-xml -without-qt-svg`


  4. `Yosys <https://github.com/The-OpenROAD-Project/yosys>`_ (version:0.27+30)


  5. `OpenROAD <https://github.com/The-OpenROAD-Project/OpenROAD>`_ (version:2.0_6895)

  6. `Open_pdks <https://github.com/RTimothyEdwards/open_pdks>`_ (version:1.0.405)

   - open_pdks is required to run drc/lvs check and the simulations
   - After open_pdks is installed, please update the **open_pdks** key in `common/platform_config.json` with the installed path, down to the sky130A folder

  7. `Xyce <https://github.com/Xyce/Xyce>`_ (version: 7.6)

   - Once the Xyce installation is complete, please make sure to add Xyce binary to $PATH environment variable.

  **Other notice:**

   - Python 3.7 is used in this generator.
   - All the required tools need to be loaded into the environment before running this generator.


Design Generation
********************

Generators
^^^^^^^^^^^^^^
**Temperature Sensor (temp-sense-gen)** - `link <https://github.com/idea-fasoc/OpenFASOC/tree/main/openfasoc/generators/temp-sense-gen/>`_

A fully automated SoC generator that uses an all-digital temperature sensor architecture, that relies on a new subthreshold oscillator (achieved using the auxiliary cell “Header Cell“) for realizing synthesizable thermal sensors.

  Block Architecture:
   - Temperature-sensitive ring oscillator and stacked zero-VT devices.

.. image:: https://github.com/idea-fasoc/OpenFASOC/blob/main/openfasoc/generators/temp-sense-gen/readme_imgs/tempSensor-BA.png
   :target: https://github.com/idea-fasoc/OpenFASOC/blob/main/openfasoc/generators/temp-sense-gen/readme_imgs/tempSensor-BA.png

**LDO Generator (ldo-gen)** - `link <https://github.com/idea-fasoc/OpenFASOC/tree/main/openfasoc/generators/ldo-gen>`_

The main idea behind a Digital LDO is the use of an array of small power transistors that operate as switches. The use of power transistors as switches facilitates low VDD power management and process scalability which makes Digital LDOs a good potential candidate for power management as we go to lower nodes. With the “Unit Power Switch” as the auxiliary cell, an automatic LDO design tool “LDO_GEN” is developed as part of this project.

  Block Architecture:
     - Synchronous Digital LDO with optional stochastic flash ADC.

.. image:: https://github.com/idea-fasoc/OpenFASOC/blob/main/openfasoc/generators/ldo-gen/readme_images/LDO-BA.png
   :target: https://github.com/idea-fasoc/OpenFASOC/blob/main/openfasoc/generators/ldo-gen/readme_images/LDO-BA.png

**DC-DC Generator (dcdc-gen)** - `link <https://github.com/idea-fasoc/OpenFASOC/tree/main/openfasoc/generators/dcdc-gen>`_

 For synthesizable on-chip power management circuits, we use the “2:1 SC Cell” auxiliary cell for implementing a switched-capacitor (SC) based DC-DC converter. By varying the number of auxiliary cells, we can achieve a wide range of conversion ratios with fine-grain resolution. It operates similarly to a successive approximation analog to digital converter (SAR ADC). Furthermore, since the total structure is simply composed of auxiliary cells, it is ideal for the proposed flow of automating the analog block design.


**Cryo Generator (cryo-gen)** - `link <https://github.com/idea-fasoc/OpenFASOC/tree/main/openfasoc/generators/cryo-gen>`_ TBA

**GDS Factory (gdsfactory)** - `link <https://github.com/idea-fasoc/OpenFASOC/tree/main/openfasoc/generators/gdsfactory>`_ TBA

**LC-DCO Generator (lc-dco)** - `link <https://github.com/idea-fasoc/OpenFASOC/tree/main/openfasoc/generators/lc-dco>`_ TBA

**SCPA Generator (cpa-gen)** - `link <https://github.com/idea-fasoc/OpenFASOC/tree/main/openfasoc/generators/scpa-gen>`_ TBA

Our fully open-source flow only supports the temperature sensor generation so far. We are working on adding additional generators in the near future.

The generators are located inside `openfasoc/generators/`, the target for temperature sensor generation is `sky130hd_temp` and located inside `openfasoc/generators/temp-sense-gen`, the following parameters are supported:

- --specfile: input specifications where the min/max temperature for the temp sensor are specified
- --outputDir: output folder where the gds/def results will be exported
- --platform: only sky130hd platform is supported for now
- --clean: clean flow folder and start a fresh design flow
- --mode: support verilog/macro/full modes, macro mode runs through APR/DRC/LVS steps to generate macros, full mode completes macro generation + simulations
- --nhead: specify a fixed number of headers (optional)
- --ninv: specify a fixed number of inverters (optional)

Look more into "getting-started" section on how to run the OpenFASOC flow


Spice Simulation Flow
**************************

To run the simulation, please edit your local model file in `common/platform_config.json`:

- simTool:  simulation tool, only ngspice is supported for now -- We plan to support Xyce in the future

- simMode: `partial` (recommended to reduce runtime) or `full`, partial simulation only includes headers and cells in low voltage domain to calculate the frequency errors, full simulation includes the internal counter (full simulation is slow using ngspice and is still being tested)

- nominal_voltage: the nominal voltage of the specified technology, it is used to set a supply voltage in the simulation testbench

- model_file: the path to the top model lib file

- model_corner: the corner used in the simulation

- an example of the `common/platform_config.json` looks like:

.. code-block:: json

      {
        "simTool": "ngspice",
        "simMode": "partial",
        "platforms": {
          "sky130hd": {
            "nominal_voltage": 1.8,
            "model_file": "~/open_pdks/pdks/sky130A/libs.tech/ngspice/sky130.lib.spice",
            "model_corner": "tt"
          }
        }
      }


Tapeouts and testing setup
*********************************

Please refer to our testing setup in our `tapeouts and testing setup section <https://github.com/idea-fasoc/openfasoc-tapeouts>`_.

Citation
****************

If you find this tool useful in your research, we kindly request to cite our papers:

 - Tutu Ajayi et al., "`An Open-source Framework for Autonomous SoC Design with Analog Block Generation <https://ieeexplore.ieee.org/document/9344104>`_," 2020 IFIP/IEEE 28th International Conference on Very Large Scale Integration (VLSI-SOC), 2020, pp. 141-146.

 - Qirui Zhang et al., "`An Open-Source and Autonomous Temperature Sensor Generator Verified With 64 Instances in SkyWater 130 nm for Comprehensive Design Space Exploration <https://ieeexplore.ieee.org/abstract/document/9816083>`_," in IEEE Solid-State Circuits Letters, vol. 5, pp. 174-177, 2022.
