techsweep.sp 
.inc ../hspice_lib/45nm_NMOS_bulk_tt.pm 
.inc ../hspice_lib/45nm_PMOS_bulk_tt.pm 
.inc techsweep_params.sp 
.temp 27 
vnoi     vx  0         dc 0  
vdsn     vdn vx        dc 'ds'  
vgsn     vgn 0         dc 'gs'  
vbsn     vbn 0         dc '-sb' 
vdsp     vdp vx        dc '-ds' 
vgsp     vgp 0         dc '-gs' 
vbsp     vbp 0         dc 'sb'  
h1       vn  0        ccvs  vnoi  1 
* NOTE: YOUR MODELS SHOULD BE SET UP SUCH THAT THE STRESS PARAMS (SA, SB, etc.) ARE AUTOMATICALLY COMPUTED
mn       vdn vgn 0 vbn nmos  L='length*1e-6' W=2.000000e-06 
mp       vdp vgp 0 vbp pmos  L='length*1e-6' W=2.000000e-06 
.options dccap post brief accurate 

.dc gs 0 1 2.500000e-02 ds 0 1 2.500000e-02 
.ac lin 1 1 1 sweep data=data1 
.noise v(vn) vnoi

.probe dc n_id   = par('id(mn)') 
.probe dc n_vt   = par('vth(mn)') 
.probe dc n_gm   = par('gmo(mn)')   
.probe dc n_gmb  = par('gmbso(mn)') 
.probe dc n_gds  = par('gdso(mn)')  
.probe dc n_cgg  = par('cggbm(mn)') 
.probe dc n_cgs  = par('-cgsbm(mn)') 
.probe dc n_cgd  = par('-cgdbm(mn)') 
.probe dc n_cgb  = par('cggbm(mn)-(-cgsbo(mn))-(-cgdbo(mn)) ') 
.probe dc n_cdd  = par('cddbm(mn)') 
.probe dc n_css  = par('-cgsbm(mn)-cbsbo(mn)') 

.probe dc p_id   = par('-id(mp)') 
.probe dc p_vt   = par('vth(mp)') 
.probe dc p_gm   = par('gmo(mp)') 
.probe dc p_gmb  = par('gmbso(mp)') 
.probe dc p_gds  = par('gdso(mp)') 
.probe dc p_cgg  = par('cggbm(mp)') 
.probe dc p_cgs  = par('-cgsbm(mp)') 
.probe dc p_cgd  = par('-cgdbm(mp)') 
.probe dc p_cgb  = par('cggbm(mp)-(-cgsbo(mp))-(-cgdbo(mp)) ') 
.probe dc p_cdd  = par('cddbm(mp)') 
.probe dc p_css  = par('-cgsbm(mp)-cbsbo(mp)') 
.end 
