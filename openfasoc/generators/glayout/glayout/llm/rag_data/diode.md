# Diode

## Purpose

A diode is a two-terminal semiconductor device that allows current to flow primarily in one direction (forward direction), showing a low resistance, while offering high resistance to current in the opposite (reverse) direction. Diodes are fundamental components used in various electronic circuits for rectification, signal modulation, voltage regulation, switching, signal mixing, and many other applications.

## Terms Defined

Anode: The terminal through which conventional current flows into the diode, typically marked with a plus sign.
Cathode: The terminal through which conventional current flows out of the diode, often denoted with a line or band on the diode body.
Forward Bias: A condition where the anode is more positive relative to the cathode, allowing current flow.
Reverse Bias: A condition where the cathode is more positive in relation to the anode, restricting current flow.
Forward Voltage Drop (Vf): The potential difference across the diode terminals when current is conducted in the forward direction, typically 0.7V for silicon diodes and 0.3V for germanium diodes.
Reverse Breakdown Voltage (V_br): The voltage at which the diode will conduct a significant reverse current, potentially leading to device damage if sustained.

## Theory

A semiconductor diode is an electronic component that conducts current primarily in one direction. It consists of a p-n junction, which forms when p-type and n-type semiconductor materials are joined together. When a diode is forward biased (anode voltage is higher than cathode voltage), the junction's depletion zone narrows, allowing current to flow easily due to a reduction in the barrier potential. The forward current increases exponentially with the voltage applied across the diode, as defined by the Shockley diode equation. In contrast, when the diode is reverse biased (cathode voltage is higher than anode voltage), the depletion zone and barrier potential grow, inhibiting current flow except for a tiny leakage current due to minority carriers. If the reverse bias voltage exceeds a critical threshold, known as the breakdown voltage, the diode will start conducing in reverse, which can be destructive unless the current is limited. Diodes are thus key in directing current in circuits and are used for various purposes, including rectification, regulation, and protection against voltage spikes.

## Schematic

### In Words

A diode symbol in a schematic circuit diagram is represented by a triangle pointing towards a line. The triangle symbolizes the direction of the allowable current flow (pointing from anode to cathode), and the line symbolizes the barrier that prevents current in the reverse direction.

The anode is connected to the end of the triangle.
The cathode is connected to the line.


### Pseudo Netlist

.subckt diode anode cathode D1 anode cathode DIODE_MODEL .endsubckt

DIODE_MODEL represents the specific parameters or model of the diode, which might be defined elsewhere in the netlist file with characteristics like saturation current, breakdown voltage, and more.

## Performance Specifications

The performance of a diode can be defined by several characteristics:

Maximum Forward Current (If_max): The maximum allowable current the diode can conduct in the forward direction without overheating or damage. <br />
Maximum Reverse Voltage (Vr_max): The maximum voltage the diode can withstand in the reverse direction before breakdown occurs. <br />
Forward Voltage Drop (Vf): Voltage required across the diode to start conducting substantially. <br />
Reverse Leakage Current (Ir): The small current that flows through the diode when reverse biased. <br />
Reverse Recovery Time (trr): The time it takes for the diode to stop conducting after switching from forward to reverse bias. <br />
Junction Capacitance (Cj): An intrinsic property that affects the diode's response to AC signals, higher at lower reverse biases.

Diodes come in many types to serve specific functions such as general-purpose rectification (rectifier diodes), signal detection (small-signal diodes), voltage clamping (zener diodes), fast switching (Schottky diodes), and light emission (LEDs).