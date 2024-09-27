# Opamp or Operational Amplifier
An operational amplifier or opamp is a voltage amplifying device. A 4 stage opamp consists of several integrator stages. A 2 stage opamp can be created using the following components:
## First Stage
Place the following: 
Two nfet differential pair transistors called diffpair_left and diffpair_right, two load current mirror pmos transistors called load_mirr and load_ref, two tail current mirror nmos transistors called tail_mirr and tail_ref. the tail_mirr transistor should be placed at the bottom. The diffpair_left transistor should be placed above the tail_mirr transistor and the diffpair_right transistor should be placed above the tail_ref transistor. The load_mirr transistor should be placed above the diffpair_left transistor and the load_ref transistor should be placed above the diffpair_right transistor.
## Second stage
Place the following:
A common source pmos transistor called pamp, two current mirror nmos transistors called pamp_mirr and pamp_ref. There is also a miller capacitance, which uses a mimcap array called miller_cap. 
The pamp transistor should be placed above the pamp_mirr and pamp_ref transistor. pamp_ref should be to the right of pamp_mirr. The miller_cap should be placed above the pamp transistor.
## Routing
Only route together these ports, nothing else
1. Connect the source of diffpair_left to the source of diffpair_right.
2. Connect the drain of diffpair_left to the drain of load_ref.
3. Connect the drain of diffpair_right to the drain of load_mirr. 
4. Connect the gate of load_mirr to the gate of load_ref. 
5. Connetc the drain of load_ref to the gate of load_ref. 
6. Connect the source of diffpair_left to the drain of tail_mirr.
7. Connect the gate of tail_mirr to the gate of tail_ref.
8. Connect the source of tail_mirr to the source of tail_ref.
9. Connect the source of load_ref to the source of load_mirr. 
10. Connect the drain of tail_ref to the gate of tail_ref. 
11. Connect the drain of diffpair_right to the gate of pamp. 
12. Connect the source of pamp to the drain of pamp_mirr.
13. Connect the source of pamp_ref to the source of pamp_mirr. 
14. Connect the drain of pamp_ref to the gate of pamp_mirr. 
15. Connect the gate of pamp_ref to the gate of pamp_mirr.
16. Connect the drain of diffpair_right to the top metal of first capacitor of miller_cap.
17. Connect the drain of pamp to the top metal of the last capacitor in miller_cap.
