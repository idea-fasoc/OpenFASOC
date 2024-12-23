# FVF based super class AB OTA
This topology of class AB OTA uses flipped voltage followers as voltage shifters to boost gain and slew rate. It can provide **slew performance independent of bias current**. LCMFB is also used to boost the slew rate even more.
## Pcells used
![WhatsApp Image 2024-12-01 at 22 18 40](https://github.com/user-attachments/assets/99d3a1b1-7842-42dc-9033-9e7f452b4a54)
![otagds](https://github.com/user-attachments/assets/4da02a37-eacb-4d2e-9e33-c0ddd4d95a79)
### Flipped Voltage Follower
Used as voltage shifters. Also used to crete a low voltage current mirror for biasing. Pcell can be found under ``` glayout/flow/blocks/elementary/FVF/ ```
### Transmission gate
Due to unavailability of resistors in Glayout, trasmission gates were used as LCMFB resistors. However, this limits ther slew performance. Pcell can be found here ``` glayout/flow/blocks/elementary/trasmission_gate/ ```
### Low Voltage Current Mirror
Low voltage current mirror are used to set a **bias current of 10uA**. The python code can be found in this directory itself.
### Others
Some already existing pcells were used, like current mirrors and four_transistor_interdigitized block.
## Parameterization
```
def super_class_AB_OTA(
        pdk: MappedPDK,
        input_pair_params: tuple[float,float]=(4,2),
        fvf_shunt_params: tuple[float,float]=(2.75,1),
        local_current_bias_params: tuple[float,float]=(3.76,3.0),
        diff_pair_load_params: tuple[float,float]=(9,1),
        ratio: int=1,
        current_mirror_params: tuple[float,float]=(2.25,1),
        resistor_params: tuple[float,float,float,float]=(0.5,3,4,4),
        global_current_bias_params: tuple[float,float,float]=(8.3,1.42,2)
        ) -> Component:
    """
    creates a super class AB OTA using flipped voltage follower at biasing stage and local common mode feedback to give dynamic current and gain boost much less dependent on biasing current
    NB:- This block can only support device dimensions which achieve our design goal. In future steps will be taken to make it more flexible.
    pdk: pdk to use
    input_pair_params: differential input pair(N-type) - (width,length), input nmoses of the fvf get the same dimensions
    fvf_shunt_params: feedback fet of fvf - (width,length)
    local_current_bias_params: local currrent mirror which directly biases each fvf - (width,length)
    diff_pair_load_params: creates a p_block consisting of both input stage pmos loads and output stage pmoses - (width,length) 
    ratio: current mirroring ratio from input stage to output stage
    current_mirror_params: output stage N-type currrent mirrors - (width, length)
    resistor_params: passgates are used as resistors for LCMFB - ((width of nmos, width of pmos),(length of nmos, length of pmos))
    global_current_bias_params: A low voltage current mirror for biasing - consists of 5 nmoses of (W/L) and one nmos of (W'/L) - ((W,W'),L)
    """
```
## Layout generation, PEX and post-layout simulations
### sky130_ota_tapeout.py
This file is used to generate layout genration, PEX and post-layout simulations. [sky130_nist_tapeout.py](https://github.com/idea-fasoc/OpenFASOC/blob/main/openfasoc/generators/glayout/tapeout/tapeout_and_RL/sky130_nist_tapeout.py) was taken as a reference.
Run this command to see various modes in which it can be run
``` python3 sky130_ota_tapeout_py --h ```
#### gen_ota mode
This generates a complete layout, **with LVT layers and labels added by default**. Custom parameters can be given. Run ``` python3 sky130_ota_tapeout.py gen_ota --h ``` to see the options.

**N.B-** 
_1. The default widths and lengths assume that the lvt layer is added. Different widths and lengths must be given to get an OTA with desired performance if no lvt layer is added.

2. There is an option to add pads. For now this is set as False by default._
#### test mode
This mode creates a complete layout with default parameter values, performs PEX (add --noparasitics to do just LVS but PEX is encouraged for better results) and then does some transient, ac, power and noise analysis to get results. The spice testbench ``` ota_perf_eval.sp ``` can be found in this directory itself.
Run python3 ``` sky130_ota_tapeout.py test --output_dir test ```. This puts the simulation results inside test directory.
