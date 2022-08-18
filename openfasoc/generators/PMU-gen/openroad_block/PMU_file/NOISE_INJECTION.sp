.subckt NOISE_INJECTION D[3] D[2] D[1] D[0] Noise_in bias_out VSS
X0  Noise_in GND_virtual0 sky130_fd_pr__cap_mim_m3_1 l=3.4e+06u w=4e+06u
X1  bias_out GND_virtual0 sky130_fd_pr__cap_mim_m3_1 l=3.4e+06u w=4e+06u
X2  Noise_in GND_virtual1 sky130_fd_pr__cap_mim_m3_1 l=3.4e+06u w=4e+06u
X3  bias_out GND_virtual1 sky130_fd_pr__cap_mim_m3_1 l=3.4e+06u w=4e+06u
X4  Noise_in GND_virtual2 sky130_fd_pr__cap_mim_m3_1 l=3.4e+06u w=4e+06u
X5  bias_out GND_virtual2 sky130_fd_pr__cap_mim_m3_1 l=3.4e+06u w=4e+06u
X6  Noise_in GND_virtual3 sky130_fd_pr__cap_mim_m3_1 l=3.4e+06u w=4e+06u
X7  bias_out GND_virtual3 sky130_fd_pr__cap_mim_m3_1 l=3.4e+06u w=4e+06u
X8  GND_virtual0 D[0] VSS VSS sky130_fd_pr__nfet_01v8 w=420000u l=150000u m=6
X9  GND_virtual1 D[1] VSS VSS sky130_fd_pr__nfet_01v8 w=420000u l=150000u m=6
X10 GND_virtual2 D[2] VSS VSS sky130_fd_pr__nfet_01v8 w=420000u l=150000u m=6
X11 GND_virtual3 D[3] VSS VSS sky130_fd_pr__nfet_01v8 w=420000u l=150000u m=6
.ends NOISE_INJECTION
