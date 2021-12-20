
.SUBCKT TEMP_sensor EN OUT VPWR VIN VGND
@@ xin@x1 EN n@n0 VGND VGND VIN VIN n@n1 sky130_fd_sc_hd__nand2_1
@@ xii@x2 n@n2 VGND VGND VIN VIN n@n3 sky130_fd_sc_hd__inv_1
@@ xib@x3 n@n4 VGND VGND VIN VIN OUT sky130_fd_sc_hd__inv_1
@@ xih@x4 VGND VIN VGND VPWR HEADER
.ends TEMP_sensor
