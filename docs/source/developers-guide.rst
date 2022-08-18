Developer's Guide
===============================

* First setup the environment by installing all dependencies using the Dependencies.sh script present in the home of OpenFASOC github repository. To test whether the installation happened correctly or not, try running the temp-sense-gen.

* Once the setup is ready, read the "Things to improve" under this section (right below) and start working on them.

* You can also start working on improving the code base, docs, CI flow, improving the generators or creating your own generator.


Things to improve
********************

To improve our tools, flow, and QoR. The following limitations are currently being addressed -

* In OpenROAD tool -
    - Add the power pins extraction in OpenROAD tool
    - LEF modification for NDR needs to be within the tool (no additional script)
    - write_cdl bug fix in source code
    - fence aware placement step needs to be added
    - ioplacment step is now skipped at placement and is set to random palcement by default at floorplaning so it doesn't put power pins of additional voltage domains at the edge
* Enable the stable spice simulation flow and modeling (ngspice and Xyce)
* Add sky130_fd_sc_hs support
