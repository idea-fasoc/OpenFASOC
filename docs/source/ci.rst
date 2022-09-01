Continuous Integration
===========================

The Continuous Integration and Deployment for OpenFASoC will be running via GitHub Actions. The CI/CD flow is described like below -

.. image:: openfasoc_ci.png
  :width: 500

A Cron job is triggered at 1 AM PST everyday to test the enabled generators with the latest tool environments and upon successful run, the tool versions are updated in the README file accordingly.

Docker Images
##############

The docker image is build on an ubuntu image using conda packages (currently) and KLayout is built from the .deb package
If the CI works, the tool versions will be  mentioned in the README file beside the tool name. The docker image contains the working environment for OpenFASOC.

Alpha image of OpenFASoC environment - `docker pull msaligane/openfasoc:latest`

Stable image of OpenFASoC environment - `docker pull msaligane/openfasoc:stable`
