# Bipolar Junction Transistor (BJT) 

## Purpose

Bipolar Junction Transistors (BJTs) are versatile electronic devices that can act as amplifiers, switches, or in voltage regulation applications. BJTs come in two primary types: NPN and PNP, which refers to the arrangement of n-type and p-type semiconductor materials used in their construction. They are called "bipolar" because they operate with both electrons and holes as charge carriers.
Semiconductor Basics

N-type Material: Doped with elements that have more electrons than silicon, providing extra free electrons as charge carriers.
P-type Material: Doped with elements that have fewer electrons than silicon, resulting in holes that act as positive charge carriers.

## BJT Structure

A BJT consists of three regions: the Emitter (E), Base (B), and Collector (C). In an NPN transistor, a thin p-type base is sandwiched between an n-type emitter and an n-type collector. For a PNP transistor, the material types for each region are reversed.

## Operation Modes

Active Mode: The emitter-base junction is forward-biased, and the collector-base junction is reverse-biased. In this mode, a small base current controls a much larger emitter-collector current.
Saturation Mode: Both the emitter-base and collector-base junctions are forward-biased. The BJT acts like a closed switch, allowing maximum current to flow from the collector to the emitter.
Cut-off Mode: Both the emitter-base and collector-base junctions are reverse-biased. The BJT acts as an open switch, with no current flowing through the collector-emitter path.

## Current Flow

In an NPN transistor, when the base-emitter junction is forward-biased, electrons move from the emitter into the base. Because the base is thin and lightly doped, most of these electrons cross through to the collector which is reverse-biased relative to the base. The movement of electrons constitutes the collector current (I_C), which is controlled by the base current (I_B).

## Characteristics

Beta (β or hFE): The current gain of a transistor in the active region, defined as the ratio of collector current to base current (β = I_C / I_B).
Alpha (α): Common-base current gain, defined as the ratio of collector current to emitter current (α = I_C / I_E).

## Schematic Symbol

An NPN BJT's schematic symbol consists of an arrow on the emitter pointing outwards, indicating conventional current flow from collector to emitter. The PNP symbol has the arrow pointing towards the base, indicating that the conventional current enters the emitter.

## Pseudo Netlist

A bjt has the following subckt definition: BJT Collector Base Emitter Transistor_Model

In this simplified netlist structure, BJT denotes the transistor name, followed by the connection points for the collector, base, and emitter, respectively, and the last parameter is the specific model describing the BJT characteristics.

