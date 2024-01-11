# Table of Contents
- [Description](#description)
- [Directory Structure](#directory-structure)
- [Workflow jobs](#workflow-jobs)
- [Synchronous jobs](#1-cron-jobs)
- [PR verification jobs](#2-pr-verification-jobs)
- [Flow result checks](#flow-result-verification)
# Description

OpenFASoC makes use of the Github actions based CI workflow. Through the use of YAML workflow files and pythonic verification scripts (`parse_rpt.py`), the changes made in pull requests are verified.

<b>Disclaimer: specific functionality information is present as docstrings in each file</b>

# Directory Structure 

```
.github
├── scripts
│   ├── dependencies
│   │   ├── get_tag.py
│   │   └── tool_metadata.py
│   ├── expected_drc_reports
│   │   └── expected_ldo_drc.rpt
│   ├── expected_sim_outputs
│   │   ├── cryo-gen
│   │   ├── ldo-gen
│   │   └── temp-sense-gen
│   │       ├── postPEX_sim_result
│   │       └── prePEX_sim_result
│   ├── Dockerfile
│   ├── get_docker_config.py
│   ├── gh.py
│   ├── parse_rpt.py
│   ├── tool_metadata.py
│   ├── tool.py
│   └── update_tools.py
└── workflows
    ├── cryo_gen.yml
    ├── ldo_sky130hvl.yml
    ├── tempSense_sky130hd.yml
    ├── test_python_api.yml
    └── verify_latest_tools_version.yml
```
# Workflow jobs
The repo supports 2 kinds of workflow runs

## 1. CRON jobs
- `workflows/verify_latest_tools_version.yml`
        
    This job automatically runs at 1 A.M. UTC and is used to verify functionality with the latest version of the toolset that the flow uses. 
    It makes use of the `workflows/verify_latest_tools_version.yml` file and builds a docker <i>alpha</i> image with the latest version of the toolset. 

    Should the generator workflow runs (temp-sense, cryo-gen and ldo-gen) run to completion, the <i>alpha</i> image is tagged as <i>stable</i> and pushed to the dockerhub, which will thereafter be used for PR verification runs

    The toolset version info is also updated in the required places in the repository with an automated PR, issued by the same `.yml` file.
- `workflows/test_python_api.yml`

    This job runs at 2 A.M. UTC. Using `pytest`, the common python API developed for the temperature sensor generator. 

    Verilog generation and simulations are run for the temperature sensor generator for python versions `3.8`, `3.9`, and `3.10`.

    Successful completion of all jobs is required to guarantee that the tool is working properly.
## 2. PR verification jobs
These workflow jobs, which include - 
* `cryo_gen.yml`
* `tempSense_sky130hd.yml`
* `ldo_sky130hvl.yml`

are run to verify the potential changes made to the repository via pull requests. 

These workflows run the verilog generation and openroad flows for the 3 generators and spice simulations are run specifically for the temperature sensor generator.

# Flow Result Verification

The generator flows run by the CI workflow jobs specified in the `.yml` files produce results which are verified by the `scripts/parse_rpt.py` file.

The script checks - 
* DRC results
* LVS results
* OpenROAD flow results
    - existence of `.cdl, .sdc, .def, .gds, .v, .spice`, etc. files in the right directories
    - existence of optimum configuration search result `.csv` files for the temp-sense generator
* Simulation results for temp-sense
    - if the generated frequency, power and error results are within an allowable range from the stored simulation results
    - if the number of failed simulations returned by the run is 0
    - if the run result files (`.sp, .log and parameters.txt`) exist for all inverter-header configurations
