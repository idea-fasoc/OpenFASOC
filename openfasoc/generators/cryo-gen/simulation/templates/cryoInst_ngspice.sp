
.lib '@@PATH_TO_LIB' tt
.include '@@PATH_TO_DUT_SP'
.include '@@PATH_TO_SC_SP'

.param vvdd = 1.8

xi1 EBL OUT VDD VSS cryoInst

vEBL EBL 0 pwl 0 0 10n 0 '10n+1f' 'vvdd'
vVDD VDD 0 dc 'vvdd'
vVSS VSS 0 dc 0

*change c0 to avoid "timestep is too small" error
c0 OUT 0 25f

*change step size and transient analysis time
.TRAN 0.4n 24u

.control
run
set filetype=ascii
hardcopy @@PATH_TO_RES OUT
exit

.endc

.END
