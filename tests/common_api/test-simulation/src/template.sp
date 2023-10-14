.OPTION temp = ${temp}

.subckt TEST_NETLIST V1 V2
C1 V1 V0 C=5
R1 V0 V2 R=5k
.ends

X0 V1 0 ${netlist_subckt_name}

VPOWER V1 0 AC SIN(0 ${Vhigh} ${freq} 0 0 0)

.TRAN 0.01 ${end_time}

.MEAS tran vrms RMS par('V(V1)')
.MEAS tran irms RMS par('I(VPOWER)')

.END
