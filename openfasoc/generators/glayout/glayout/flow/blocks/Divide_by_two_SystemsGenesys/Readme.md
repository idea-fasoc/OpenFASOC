# Divide-by-2 Frequency Divider Circuit

This project implements a digital frequency divider circuit using NMOS-only transistors, developed with the `sky130` PDK (Process Design Kit) for the OpenFASOC platform. The circuit design and layout are generated programmatically using Python in a Jupyter notebook and `gdsfactory` library.

## Circuit Overview

The Divide-by-2 frequency divider circuit is composed of two cross-coupled NMOS latches arranged to halve the input clock frequency. It has applications in digital clock management, signal processing, and low-power frequency division circuits.

### Key Components

- **NMOS Latches**: Two NMOS-based latches (flip-flops) form the core of the circuit.
- **Cross-Coupled Inverters**: Cross-coupled inverters within each latch store binary states (Q and Q') for feedback stability.
- **Current Mirror and Transmission Gates**: These NMOS structures facilitate controlled switching and stable latch operation.
- **Feedback Routing**: Feedback from the output of the second latch to the input of the first latch ensures accurate toggling and frequency division.

## Repository Contents

- **`Divide_by_2.ipynb`**: Jupyter notebook containing the Python code for building and simulating the divide-by-2 circuit layout.
- **`divide_two.gds`**: Generated GDS file of the layout, ready for physical verification and integration with other IC designs.
- **`README.md`**: Documentation file describing the project and usage.

## Prerequisites

- **Python** (3.7 or later)
- **Jupyter Notebook**
- **gdsfactory**: For creating and visualizing IC layouts
- **sky130 PDK**: Process Design Kit from SkyWater, available [here](https://github.com/google/skywater-pdk)
- **glayout**: Layout tools compatible with `gdsfactory` and SkyWater PDK

