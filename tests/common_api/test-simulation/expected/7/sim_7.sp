

.OPTION temp = -5

.subckt TEST_NETLIST V1 V2
C1 V1 V0 C=5
R1 V0 V2 R=5k
.ends

X0 V1 0 TEST_NETLIST

VPOWER V1 0 AC SIN(0 10 10k 0 0 0)

.TRAN 0.01 1

.MEAS tran vrms RMS par('V(V1)')
.MEAS tran irms RMS par('I(VPOWER)')

.END
