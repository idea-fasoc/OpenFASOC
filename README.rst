OpenFASoC
===================

**OpenFASoC: Fully Open-Source Autonomous SoC Synthesis using Customizable Cell-Based Synthesizable Analog Circuits**

.. image:: https://readthedocs.org/projects/openfasoc/badge/?version=latest
    :target: https://openfasoc.readthedocs.io/en/latest/?badge=latest


OpenFASOC is focused on open-source automated analog generation from user specification to GDSII with fully open-sourced tools.

Contact: mehdi_saligane@brown.edu or mehdi@umich.edu

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

    `Installation and Running <https://github.com/idea-fasoc/OpenFASOC/tree/main/openfasoc/generators/glayout/tapeout/tapeout_and_RL/README.md>`_  

    .. image:: https://github.com/idea-fasoc/OpenFASOC/actions/workflows/glayout_sky130.yml/badge.svg
        :target: https://github.com/idea-fasoc/OpenFASOC/actions/workflows/glayout_sky130.yml
    
    .. image:: https://github.com/idea-fasoc/OpenFASOC/actions/workflows/glayout_opamp_sim.yml/badge.svg
        :target: https://github.com/idea-fasoc/OpenFASOC/actions/workflows/glayout_opamp_sim.yml

    Opamp Notebook 

    .. image:: https://colab.research.google.com/assets/colab-badge.svg
        :target: https://github.com/idea-fasoc/OpenFASOC/blob/7dc5eb42cec94c02b74e72483df6fdc2b2603fb9/docs/source/notebooks/glayout/glayout_opamp.ipynb 

    Via Notebook 

    .. image:: https://colab.research.google.com/assets/colab-badge.svg
        :target: https://github.com/idea-fasoc/OpenFASOC/blob/7dc5eb42cec94c02b74e72483df6fdc2b2603fb9/docs/source/notebooks/glayout/GLayout_Via.ipynb  

    Current Mirror Notebook 

    .. image:: https://colab.research.google.com/assets/colab-badge.svg
        :target: https://github.com/idea-fasoc/OpenFASOC/blob/7dc5eb42cec94c02b74e72483df6fdc2b2603fb9/docs/source/notebooks/glayout/GLayout_Cmirror.ipynb


Getting Started
****************
There are two methods to install the prerequisites to use OpenFASOC generators:  

1. Express Installation 

  Install all the prerequisites using the `dependencies.sh` script provided in the home location of this project (where this README.rst file is found). Supports CentOS7, Ubuntu 20.04 LTS and Ubuntu 22.04 LTS.

  .. code-block:: bash

      $ sudo ./dependencies.sh

  For more info on getting-started, please refer to `"Getting Started" section's express install section <https://openfasoc.readthedocs.io/en/latest/getting-started.html#express-installation>`_

2. Containerized Installation 
 
  This method uses `Docker <https://www.docker.com/#build>`_ to build a custom image, on top of which a container is created, in which the generators can be run. This allows the user to create a persistent snapshot of an environment where are tools are installed. **Note: If you do not have Docker Installed, refer to** `the instructions here <https://docs.docker.com/engine/install/>`_
  
  .. code-block:: bash

       $ cd docker/conda
       $ sudo docker build -t <image_name> .
       $ cd ../..
       $ sudo docker run -v $(pwd):$(pwd) -w $(pwd) --name <container_name> -it <image_name>
       $ pip install -r requirements.txt

  Where `<image_name>` is the name that you want to tag the built image with and `<container_name>` is the name of the container that will be run. This container will use the OpenFASOC directory as the working directory and bind mount it to the container's present working directory. 

3. Manual Install 

  Below are the tool requirements along with their currently support versions that are updated regularly upon testing againsts the generators.

    1. `Magic <https://github.com/RTimothyEdwards/magic>`_ (version:8.3.464)

    2. `Netgen <https://github.com/RTimothyEdwards/netgen>`_ (version:1.5.272)

    3. `Klayout <https://github.com/KLayout/klayout>`_ (version:0.28.17-1)

        - Please use this command to build preferably: `./build.sh -option '-j8' -noruby -without-qt-multimedia -without-qt-xml -without-qt-svg`


    4. `Yosys <https://github.com/The-OpenROAD-Project/yosys>`_ (version:0.38+92)


    5. `OpenROAD <https://github.com/The-OpenROAD-Project/OpenROAD>`_ (version:2.0_12381)
 
    6. `Open_pdks <https://github.com/RTimothyEdwards/open_pdks>`_ (version:1.0.471)

     - open_pdks is required to run drc/lvs check and the simulations
     - After open_pdks is installed, please update the **open_pdks** key in `common/platform_config.json` with the installed path, down to the sky130A folder

    7. `Xyce <https://github.com/Xyce/Xyce>`_ (version: 7.6)

     - Once the Xyce installation is complete, please make sure to add Xyce binary to $PATH environment variable.

  **Other notice:**

   - Python 3.10 is used in this generator.
   - All the required tools need to be loaded into the environment before running this generator.
   - Glayout is now available as a `python package <https://pypi.org/project/glayout/>`_ and can be installed using `pip install glayout`


Generators
********************

.. list-table::
   :widths: 30 20 20 30
   :header-rows: 1

   * - Generator
     - Technology nodes
     - Supported
     - Documentation
   * - Temperature Sensor
     - sky130hd
     - Yes
     - `Temperature Sensor Docs <https://openfasoc.readthedocs.io/en/latest/flow-tempsense.html>`_
   * - Low dropout Voltage Regulator (LDO)
     - sky130hvl
     - Yes
     - `LDO Voltage Regulator Docs <https://openfasoc.readthedocs.io/en/latest/flow-ldo.html>`_
   * - Cryogenic
     - sky130hs, sky130hd, sky130hvl
     - No (In-progress)
     - `Cryogenic Docs <https://openfasoc.readthedocs.io/en/latest/flow-cryo.html>`_
   * - Glayout
     - sky130, gf180
     - Yes
     - `Glayout Docs <https://github.com/idea-fasoc/OpenFASOC/tree/main/openfasoc/generators/glayout/tapeout/tapeout_and_RL/README.md>`_



Tapeouts and testing setup
*********************************

Please refer to our testing setup in our `tapeouts and testing setup section <https://github.com/idea-fasoc/openfasoc-tapeouts>`_.

Citation
****************

If you find this tool useful in your research, we kindly request to cite our papers:

 - A\. Hammoud, C. Goyal, S. Pathen, A. Dai, A. Li, G. Kielian, and M. Saligane,  “Human Language to Analog Layout Using Glayout Layout Automation Framework,” Accepted at MLCAD, 2024.

 - A\. Hammoud, A. Li, A. Tripathi, W. Tian, H. Khandeparkar, R. Wans, G. Kielian, B. Murmann, D. Sylvester, and M. Saligane, "Reinforcement Learning-Enhanced Cloud-Based Open Source Analog Circuit Generator for Standard and Cryogenic Temperatures in 130-nm and 180-nm OpenPDKs,” Accepted at ICCAD, 2024

 - C\. Goyal, H. Khandeparkar, S. Charan, J. S. M. Baquero, A. Li, J. Euphrosine, T. Ansell, M. Saligane, "`Disrupting Conventional Chip Design through the Open Source EDA Ecosystem <https://ieeexplore.ieee.org/document/10511336/authors#authors>`_," 2024 8th IEEE Electron Devices Technology & Manufacturing Conference (EDTM), Bangalore, India, 2024, pp. 1-3.

 - A\. Li, J. Lee, P. Mukim, B. D. Hoskins, P. Shrestha, D. Wentzloff, D. Blaauw, D. Sylvester, M. Saligane, "`A Fully Integrated, Automatically Generated DC–DC Converter Maintaining >75% Efficiency From 398 K Down to 23 K Across Wide Load Ranges in 12-nm FinFET <https://www.nist.gov/publications/fully-integrated-automatically-generated-dc-dc-converter-maintaining-75-efficiency-398>`_," in IEEE Solid-State Circuits Letters, vol. 7, pp. 42-45, 2024.

 - A\. Hammoud, V. Shankar, R. Mains, T. Ansell, J. Matres and M. Saligane, "`OpenFASOC: An Open Platform Towards Analog and Mixed-Signal Automation and Acceleration of Chip Design <https://ieeexplore.ieee.org/document/10153547>`_," 2023 International Symposium on Devices, Circuits and Systems (ISDCS), Higashihiroshima, Japan, 2023, pp. 01-04. 

 - Y\. K. Cherivirala, M. Saligane and D. D. Wentzloff, "`An Open Source Compatible Framework to Fully Autonomous Digital LDO Generation <https://ieeexplore.ieee.org/document/10071546>`_," 2023 IEEE International Symposium on Circuits and Systems (ISCAS), Monterey, CA, USA, 2023, pp. 1-5.

 - Q\. Zhang, W. Duan, T. Edwards, T. Ansell, D. Blaauw, D. Sylvester, M. Saligane, "`An Open-Source and Autonomous Temperature Sensor Generator Verified With 64 Instances in SkyWater 130 nm for Comprehensive Design Space Exploration <https://ieeexplore.ieee.org/abstract/document/9816083>`_," in IEEE Solid-State Circuits Letters, vol. 5, pp. 174-177, 2022.

 - T\. Ajayi, S. Kamineni, Y. K. Cherivirala, M. Fayazi, K. Kwon, M. Saligane, S. Gupta, C. H. Chen, D. Sylvester, D. Blaauw, R. Dreslinski Jr., B. Calhoun, D. D. Wentzloff, "`An Open-source Framework for Autonomous SoC Design with Analog Block Generation <https://ieeexplore.ieee.org/document/9344104>`_," 2020 IFIP/IEEE 28th International Conference on Very Large Scale Integration (VLSI-SOC), 2020, pp. 141-146.


