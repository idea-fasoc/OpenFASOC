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