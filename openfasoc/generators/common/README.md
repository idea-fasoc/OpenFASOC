# Description
This folder contains python script files that are common to all generators, used as config or result parse files for generator flows and simulations

### File Tree
```
|_ generators/common/
    |_ simulation/
        |_ simulation_config.py
        |_ simulation_run.py
        |_ utils.py
        |_ init.py
    |_ init.py
    |_ check_gen_files.py
    |_ classify_sim_error.py
    |_ get_ngspice_version.py
    |_ verilog_generation.py
```
### Verilog Generation
The file `verilog_generation.py` is used to convert verilog files such that they use the mako templating library for simpler and more readable syntax. Specific function descriptions are present in as docstrings in the file.

### Simulations
The files found in the `simulation/` directory are used as pythonic script files to run simulations for each generator. These files mainly generate configurations and run files for the simulations, which are used by each of the generators. Specific function descriptions are found in the respective files

### Flow result checks
The file `check_gen_files.py` is used to check if simulations can be run correctly for a generator. Specifically, it is used in the `parse_rpt.py` file found in the `tools/` folder of each generator. This file runs at the end of each generator flow to check for successful completion.       

Only temp-sense-gen, cryo-gen and ldo-gen are currently supported. For these generators, this file checks if the necessary `work/` directory and the simulation generated files are present (such as `.sdc`, `.cdl`, `.gds`, `.def`, among others).  

The file also checks if the necessary optimum inverter-header configuration search results are present for the temp-sense-gen flow (in the form of the error optimisation `.csv` files)

Check the docstrings in each file for specific function definitions.
### Simulation Result Checks
The files `classify_sim_error.py` and `get_ngspice_version.py` together, are used to check for errors in the simulation runs for each generator. These files use a dictionary of maximum and minimum allowable deviations of simulation results from an ideal set of result files present in `.github/scripts/expected_sim_outputs/*`. The dictionary of deviations, called "errors" is used for the same
```python
errors = {
        'frequency': { 'max': 1, 'min': 0.5 },
        'power': { 'max': 1000, 'min': 1000 },
        'error': { 'max': 100, 'min': 50 },
    }
```
If the deviation  of the current run results (in percentage) is greater than the maximum allowable deviation for any of the results, the file returns an urgent "red" alert, which raises a ValueError in the `parse_rpt.py` file.  

If the deviations lie between the maximum and minimum allowable deviations, the script returns an "amber" alert, which raises a soft warning.  

If the deviations are all less than minimum allowable deviation, the script returns "green", which does not reflect anything in the `parse_rpt.py` file. 

If the current ngspice version does not match with the ngspice version stored at the time the templates were stored, the function `check_ngspice_version()` from `check_ngspice_version.py` returns 0, which leads to a soft warning raised in the `parse_rpt.py` file, to notify the maintainers about the same.
