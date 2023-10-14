Common Python API
=================

.. contents:: Contents
    :local:

Introduction
------------

OpenFASoC generators have a Python script that runs the generator flow (See `Generators <generators.html>`_ for more information). Many of the steps in the Python script are common across generators.

A common Python module is exported in ``openfasoc/generators/common/``to reduce code duplication and simplify the creation of new generators. This module exports various functions and constants which may be used in generators.

Importing
---------
Since the common Python module is in the ``openfasoc/generators/common/`` directory, which is a parent directory, the path to this directory must be added using ``sys.path.append()``.

.. code-block:: python

    import sys
    sys.path.append(
        # This is the relative path to the `openfasoc/generators/common/` directory.
        os.path.join(os.path.dirname(__file__), '..', '..')
    )

Once the directory is added to the path, the exported modules can be imported using the standard Python import syntax.

.. code-block:: python

    from common.verilog_generation import generate_verilog

See `Exported Modules`_ for a list of exported modules and their respective functions and constants.

Exported Modules
----------------
The top level module ``common`` exports the following submodules.

1. Verilog Generation (``common.verilog_generation``)
#####################################################
This module exports functions and constants used in the Verilog generation step. See `Temperature Sensor Generator <flow-tempsense.html#verilog-generation>`_ for more about Verilog generation.

This module uses the `Mako <https://www.makotemplates.org/>`_ templating library to convert source Verilog templates into final Verilog files used in the OpenROAD flow.

Functions
^^^^^^^^^
1. ``generate_verilog(parameters: dict, src_dir: str, out_dir: str) -> None``

    Reads source Verilog files from ``src_dir`` and generates output Verilog files for synthesis in the OpenROAD flow. The source files are `Mako <https://makotemplates.org>`_ templates.

    The ``parameters`` argument is a dictionary of all the parameters used in the source Verilog Mako templates. Use the ``${parameter}}`` syntax in the source files to insert parameters. For example, the number of inverters in the `Temperature Sensor Generator <flow-tempsense.html>`_ is a parameter.

    This function maintains the source directory (``src_dir``) structure in the output directory (``out_dir``). i.e., source files from a subdirectory of the ``src_dir`` will be generated in a subdirectory in ``out_dir`` with the same name.

    Arguments:
        - ``src_dir`` (str): Path to the directory with the source Verilog templates. (default: ``src/``)
        - ``out_dir`` (str): Path to the directory in which the output will be generated. (default: ``flow/design/src/``)
        - ``parameters`` (dict): Dictionary of all the parameters used in the `Mako templates <https://makotemplates.org>`_.

    Example:
        .. code-block:: python

            generate_verilog(
                # Generates the output in flow/design/src/
                out_dir=os.path.join('flow', 'design', 'src', 'tempsense'),
                # Sets the parameters used in the design
                parameters={
                    "ninv": 6,
                    "nhead": 3,
                    "design_name": "tempsenseInst_error",
                }
            )

        See the generators' Python files in ``tools/`` for more examples.

    This function also appends (can be directly used in the source Verilog files) the following Mako `defs <https://docs.makotemplates.org/en/latest/defs.html>`_:
        - ``cell(name)``

            This def returns the name of a standard cell for a given platform. Currently, it only supports the sky130 platform. The naming scheme for sky130 is ``${cell_prefix}${name}${cell_suffix}``.

            Here ``name`` is an argument passed to the ``cell()`` def, and ``cell_prefix`` and ``cell_suffix`` are set in the ``parameters`` argument passed to the ``generate_verilog()`` function.

            For example, an inverter cell can be inserted using the syntax ``${cell('inv')}``. If the prefix is ``sky130_fd_sc_hd__`` (sky130hd) and the suffix is ``_1``, the cell will be replaced with ``sky130_fd_sc_hd__inv_1``. The same statement will be replaced with ``sky130_fd_sc_hs__inv_1`` for the sky130hs platform.

            Use the constant ``COMMON_PLATFORMS_PREFIX_MAP`` for mapping a sky130 platform to its platform.

Constants
^^^^^^^^^
1. ``COMMON_PLATFORMS_PREFIX_MAP``

    This is a dictionary of common platforms (currently sky130) and their cell naming prefixes. See the ``cell()`` def in the ``generate_verilog()`` function for more information on how to use it.

2. Simulation (``common.simulation``)
#####################################################
This module exports functions used to simulate SPICE testbenches with multiple parameters.

This module supports the use of `Mako <https://www.makotemplates.org/>`_ templating library to insert parameters into SPICE templates.

Functions
^^^^^^^^^
1. ``run_simulations(parameters: dict, platform: str, simulation_dir: str, template_path: str, runs_dir: str, sim_tool: str, num_concurrent_sims: int, netlist_path: str) -> int``

    Generates configurations of all combinations of the given ``parameters`` and runs simulations for each case. The testbench SPICE file, configuration parameters, and the ouptut for each run are generated in ``{simulation_dir}/{runs_dir}``.

    The testbench SPICE file given by ``template_path`` follows the `Mako <https://makotemplates.org>`_ templating syntax. Use the ``${parameter}`` syntax for inserting parameters in the file. The following parameters are automatically inserted during each run.

    - ``run_number`` (int): The number/index of the run/configuration.
    - ``sim_tool`` (str): Command for the simulation tool used.
    - ``platform`` (str): The platform/PDK.
    - ``template`` (str): Path to the SPICE testbench template.
    - ``netlist_path`` (str): Absolute path to the SPICE netlist of the design to be simulated.

    Example SPICE template: (From the `Temperature Sensor Generator <flow-tempsense.html>`_)
        .. code-block:: spice

            .lib '${model_file}' ${model_corner}
            .include '${netlist_path}'

            .param temp_var = ${temp}
            .param vvdd = 1.8
            .param sim_end = '800m/exp(0.04*temp_var)'

    Each configuration is run/simulated in a directory in the ``runs_dir``. Each run directory contains the final SPICE testbench with the parameters inserted, a ``parameters.txt`` file containing the values of each parameter, and the output log file.

    ``parameters`` is a dict with keys corresponding to the parameter's name and the values of one of the following types.

    1. A constant value.
    The value of this parameter will be the same for every configuration/run.
        .. code-block:: python

            {'param': 'value'}

    2. Array of integer/float/string constants.
    Each of the values in the array will be swept.
        .. code-block:: python

            {'param': [1, 2, 3, 8]}
            # OR
            {
                'param': {
                    'values': [1, 2, 3, 8]
                }
            }

    3. Increments.
    All values starting from ``start`` (included) and ending at ``end`` (included if it is ``start + n * step``) will be swept with a step of ``step``. The default value for ``step`` is ``1``.
        .. code-block:: python

            {'param': {
                'start': 10,
                'end': 50,
                'step': 10
            }}
            # param will take values 10, 20, 30, 40, 50

    Example parameters:
        .. code-block:: python

            # Runs 10 total simulations
            # Sweeps through all temperatures from 10 to 100 (both included) with increments of 10.
            example1 = {
                'temp': {'start': 10, 'end': 100, 'step': 10}
            }

            # Runs 9 total simulations
            # Sweeps through all the 3 input voltages as well as all the 3 temperatures
            example2 = {
                'input_voltage': [1, 2, 3],
                'temp': [20, 30, 40]
            }

            # Runs 4 total simulations
            # Duty cycle and aux_spice_path remain the same in all simulations
            # input_voltage is swept
            example3 = {
                'duty_cycle': 10,
                'aux_spice_path': 'auxcell.cdl',
                'input_voltage': [1, 2, 3]
            }

    See the generators' Python files in ``tools/`` for more examples.

    Arguments:
        - ``parameters`` (dict): Dictionary of parameters. Explained above.
        - ``platform`` (str): Platform/PDK. (eg: ``sky130hd```)
        - ``simulation_dir`` (str): Path to the directory where the simulation source files are placed and the outputs will be generated. (Default: ``simulations``)
        - ``template_path`` (str): Path to the SPICE template file for the testbench. (Default: ``templates/template.sp``)
        - ``runs_dir`` (str): Path to a directory inside the ``simulation_dir`` directory where the outputs for the simulations will be generated. (Default: ``runs``)
        - ``sim_tool`` (str): Command for the simulation tool. ``ngspice``, ``xyce``, and ``finesim`` are supported. (Default: ``ngspice``)
        - ``num_concurrent_sims`` (int): The maximum number of concurrent simulations. (Default: ``4``)
        - ``netlist_path`` (str): Path to the SPICE netlist inside the ``simulation_dir`` of the design to be simulated. (Default: ``netlist.sp``)

    **Returns (int)**: The total number of simulations run.

    Overall example: (From the `Temperature Sensor Generator <flow-tempsense.html>`_)
        .. code-block:: python

            run_simulations(
                parameters={
                    'temp': {'start': tempStart, 'end': tempStop, 'step': tempStep},
                    'model_file': model_file,
                    'model_corner': platformConfig['model_corner'],
                    'nominal_voltage': platformConfig['nominal_voltage'],
                    'design_name': designName
                },
                platform="sky130hd",
                simulation_dir="simulations",
                template_path=os.path.join("templates", f"tempsenseInst_{simTool}.sp"),
                runs_dir=f"run/prePEX_inv{num_inv}_header{num_header}/",
                sim_tool=simTool,
                netlist_path=dstNetlist
            )