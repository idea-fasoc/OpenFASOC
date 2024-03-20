Developer's Guide for Generators
==================================

* First setup the environment by installing all dependencies . There are multiple ways to get all dependencies installed in your environment.

  * Run ``dependencies.sh`` script present in the home of OpenFASOC github repository to auto install all dependencies. This script only supports ubuntu and centOS. To test whether the installation happened correctly or not, try running the temp-sense-gen or ldo-gen generators;

  * If you are not sure about the script, run commands from the above script that are relevant to your OS. It is recommended to install all tools via its conda package. This will help in updating the version or downgrading the version, for debugging, without any hustle.

  * A workflow runs everyday testing all the active generators with the latest version of dependencies available out there. If those versions are supporting the generators, the versions list is captured and stored in ``conda_versions.txt`` file.

* Once the environment is ready, start working on developing the generator flow for the desired block. There are a few things that is expected to follow for a better usage and flexibility of the generator. Look into modularity and regression pages that are linked below.


--------

.. toctree::

    stages
    regression
    ci

.. note::

    If you'd like to suggest new features, enhancements or bug fixes, feel free to `submit an issue <https://github.com/idea-fasoc/OpenFASOC/issues>`_ in the GitHub repo.
