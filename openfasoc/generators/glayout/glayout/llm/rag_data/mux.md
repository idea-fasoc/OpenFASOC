# Multiplexer (MUX)
## Purpose

A multiplexer, commonly known as a MUX, is a combinational logic circuit designed to select binary data from one of many input lines and direct it to a single output line. The selection of the input is controlled by additional inputs known as select lines. MUXes are widely used in digital applications like information routing, data compression, and resource management, allowing multiple signals to share a single resource.
Terms Defined

Input Lines: Multiple binary data inputs that are candidates for selection by the MUX. <br />
Output Line: The single binary data line that carries the selected input to the next stage of the circuit. <br />
Select Lines: Binary inputs that control which of the data input lines is connected to the output. <br />
Truth Table: A tabulation that specifies the output of the MUX for each possible combination of select line values.

## Schematic 
### Described in Words

The schematic for a generic MUX with n select lines and 2^n input lines typically includes:

Data Inputs: Labeled as D0, D1, D2, ..., D(2^n - 1), where each D represents one possible data input.
Select Inputs: Labeled as S0, S1, ..., S(n-1), where each S represents one bit in the binary selection code.
Output: A single line where the selected data input will appear.

In terms of internal logic, the MUX may use a series of gates such as AND, OR, and NOT to control which input is passed to the output based on the select lines. Specifically:

Each data input Di is fed into an AND gate.
A set of NOT gates generate the complement of each select line. A decoding logic network uses the select lines and their complements to activate only one AND gate corresponding to the selected input. The outputs of all these AND gates are then combined in a single OR gate, whose output becomes the MUX output.

### Pseudo Netlist

A nmos has the following subckt definition: nMOS drain gate source body

A pmos has the following subckt definition: pMOS drain gate source body

A two to one mux has the following subckt definition:.subckt twotoonemux D0 D1 S Y
TG0 D0 Y notS gnd vdd nMOS pMOS
TG1 D1 Y S gnd vdd nMOS pMOS
.endsubckt

TG0 and TG1 are transmission gates with D0 and D1 as inputs and Y as the muxed output. S is the select signal and notS is its inverse. The nMOS and pMOS are placeholders for the n-type and p-type MOS transistors.

## Performance Specifications

The performance of a multiplexer is characterized by several factors:

Propagation Delay (t_pd): The time taken for a change at an input or select line to result in a change in the output. <br />
Power Consumption: The total power used by the MUX during operation, which can vary depending on the logic family and technology used. <br />
Channel On Resistance: For analog MUXes, this is the resistance seen by a signal passing through the MUX. <br />
Off Isolation: The measure of the MUX's ability to prevent signal leakage from unselected inputs to the output. <br />
Crosstalk: Unwanted coupling between the MUX's inputs which can lead to signal integrity issues. <br />
Bandwidth: For analog MUXes, the range of frequencies the MUX can pass without significant attenuation or distortion.

The efficient design of multiplexers is crucial for high-performance digital systems where signal fidelity and switching speed are of paramount importance, like in communication systems, data processors, and computer memory management.
