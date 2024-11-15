# Transmission gate block for SAR A/D converter
- Team: SaltyChip
- Design (our target): DAC for 6-bit A/D converter
- Progress: ongoing, 03/11/2024 

| Design File | Description | Remark |
| --- | --- | --- |
| inv_lib.py | Layout generation of inverter for controlling the transmission gate's PMOS and NMOS | |
| transmission_gate.py | Layout generation of a transmission gate | The layout is still under construction |
| mimcap_array.py | Layout generation of a 8x8 MIM capacitor array | Transmission gate combined with a MIM capacitor array is the aim in this project |

---

Submission of PR Draft (deadline: 24/11/2024)

- ToDo list
- Transmission gate
    - [x] Layout
    - [ ] Add ports w/ labels onto the layout (for the subsequent LVS)
    - [ ] DRC of the layout w/o error (Magic)
    - [ ] DRC of the layout w/o error (Klayout)
    - [ ] Create the baseline schematic of the created component
    - [ ] LVS w/o error
    - [ ] Document about the PCell specification
    - [ ] PEX and create the testbench
    - [ ] Verification gets passed
- MIMI capacitor array 
    - [x] Layout
    - [ ] Add ports w/ labels onto the layout (for the subsequent LVS)
    - [ ] DRC of the layout w/o error (Magic)
    - [ ] DRC of the layout w/o error (Klayout)
    - [ ] Create the baseline schematic of the created component
    - [ ] LVS w/o error
    - [ ] Document about the PCell specification
    - [ ] PEX and create the testbench
    - [ ] Verification gets passed