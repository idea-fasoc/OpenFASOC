
.lib '@@PATH_TO_LIB' tt
.include '@@PATH_TO_DUT_SP'
.include '@@PATH_TO_SC_SP'

.param vvdd = 1.8

xi1 EBL OUT VDD VSS cryoInst

vEBL EBL 0 pwl 0 0 10n 0 '10n+1f' 'vvdd'
vVDD VDD 0 dc 'vvdd'
vVSS VSS 0 dc 0

c0 OUT 0 1f

.TRAN 50p 100n

.control
run
set filetype=ascii
exit

.endc

.END
