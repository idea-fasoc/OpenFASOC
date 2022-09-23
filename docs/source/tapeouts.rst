Tapeouts
=========================

This page contains documentation on tapeouts of circuits generated with OpenFASoC, along with auxiliary files and experimental results. Source is uploaded in the `openfasoc-tapeouts <https://github.com/idea-fasoc/openfasoc-tapeouts>`_ repository.

The tapeouts repository is included as a git submodule in OpenFASoC. To download it, run this command after having cloned OpenFASoC:

.. code-block::

  git submodule update --init tapeouts

Files will be downloaded to the `tapeouts/` folder. In case they are not updated with the latest additions in openfasoc-tapeouts, run:

.. code-block::

  git submodule update --remote tapeouts

This will pull the latest commits to the submodule.

.. include:: ../../tapeouts/README.rst
  :start-after: .. openfasoc_docs
