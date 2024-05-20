# Static CMOS Inverter

## Purpose
An inverter is used to implement the logic function NOT by inverting the input voltage from high to low or from low to high.

## Terms Defined
VTC: voltage transfer characteristic, a graph that describes the relationship between voltage and time based on certain inputs. <br /> Sizing Ratio: the ratio between the pmos and the nmos. used to tune the speed and strength of the various components of the inverter

## Theory
An inverter is a simple logic circuit that can be implemented by two transistors: an nmos and pmos. This method of implementing an inverter is called a static cmos logic inverter. 

The pmos is typically placed above the nmos since the pmos is responsible for pulling up while the nmos is responsible for pulling down. When a high input voltage is given to the inverter, the nmos is switched ON and pulls the circuit down. Meanwhile, when a low input voltage is given, the pmos is switched OFF and pulls the circuit up.

An ideal inverter has a VTC curve that switches from high to low voltage or low to high voltage instantaneously. An advantage of the static cmos inverter is that a pmos is very good for pulling up and an nmos is good for pulling down, making a Voltage Transfer Characteristic that is very sharp.

## Schematic

### In Words
An inverter has an nmos and a pmos. The pmos is above the nmos and it's source is tied to Vdd. The nmos' source is tied to ground. The drains for the nmos and pmos are connected together. The output voltage can be measured at this node that connects the nmos and pmos. Additionally, the nmos and pmos are tied together at its gate as well. This is where the input voltage is measured. The sizing ratio between the pmos and nmos is typically the most optimal when it is 2:1.

### Pseudo Netlist
A nmos has the following subckt definition: NMOS drain gate source body

A pmos has the following subckt definition: PMOS drain gate source body

A CMOS Inverter has the following subckt definition: .subckt inverter inputvoltage outputvoltage NMOS PMOS gnd vdd .endsubckt

## Performance Specifications
The specifications that define an inverter are as follows: Propagation Delay (tpd), Power Dissipation and Noise Margins.

Propagation delay is the average time it takes for the output to switch states when the input is changed. It is generally defined between the 50% points of voltage levels during a transition. Propagation delay can be controlled by the sizing ratio

Power Dissipation is a negative side effect of that inverters have. Its typically caused in two instances, static and dynamic. Dynamic power dissipation occurs when switching occurs an a short circuit briefly happens. Static power dissipation happens when the circuit is in steady state.

Noise margins are the amount of noise voltage that can be fed into the input voltage without affecting the output.