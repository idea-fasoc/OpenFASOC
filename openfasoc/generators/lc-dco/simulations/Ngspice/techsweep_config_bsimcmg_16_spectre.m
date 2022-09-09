% Configuration for techsweep_spectre_run.m
% Boris Murmann, Stanford University
% Tested with MMSIM12.11.134
% September 21, 2019

function c = techsweep_config_bsimcmg_16_spectre

% Models and file paths
c.modelfile1 = '"toplevel.scs" section=top_tt';
c.modelfile2 = '"usage.scs" section=pre_simu';
c.modelinfo = 'TSMC 16nm';
c.corner = 'NOM';
c.temp = 273+65;

if(0)
    c.modeln = 'nch_svt_mac';
    c.modelp = 'pch_svt_mac';
    c.savefilen = '16nch_svt';
    c.savefilep = '16pch_svt';
else
    c.modeln = 'nch_lvt_mac';
    c.modelp = 'pch_lvt_mac';
    c.savefilen = '16nch_lvt';
    c.savefilep = '16pch_lvt';
end  

c.simcmd = 'module load cadence/mmsim/15.10.644; spectre techsweep.scs >! techsweep.out';
c.outfile = 'techsweep.raw';
c.sweep = 'sweepvds_sweepvgs-sweep';
c.sweep_noise = 'sweepvds_noise_sweepvgs_noise-sweep';

% Sweep parameters
c.VGS_step = 20e-3;
c.VDS_step = 20e-3;
c.VSB_step = 0.1;
c.VGS_max = 1.0;
c.VDS_max = 1.0;
c.VSB_max = 0.1;
c.VGS = 0:c.VGS_step:c.VGS_max;
c.VDS = 0:c.VDS_step:c.VDS_max;
c.VSB = 0:c.VSB_step:c.VSB_max;
c.LENGTH = [0.016 0.02 0.036 0.072];
c.NFIN  = 4;
c.NF = 4;
c.WIDTH = c.NF*0.154;

% Variable mapping
c.outvars =            {'ID','VT','IGD','IGS','GM','GMB','GDS','CGG','CGS','CSG','CGD','CDG','CGB','CDD','CSS'};
c.n{1}= {'mn:ids','A',   [1    0    0     0     0    0     0     0     0     0     0     0     0     0     0  ]};
c.n{2}= {'mn:vth','V',   [0    1    0     0     0    0     0     0     0     0     0     0     0     0     0  ]};
c.n{3}= {'mn:igd','A',   [0    0    1     0     0    0     0     0     0     0     0     0     0     0     0  ]};
c.n{4}= {'mn:igs','A',   [0    0    0     1     0    0     0     0     0     0     0     0     0     0     0  ]};
c.n{5}= {'mn:gm','S',    [0    0    0     0     1    0     0     0     0     0     0     0     0     0     0  ]};
c.n{6}= {'mn:gmbs','S',  [0    0    0     0     0    1     0     0     0     0     0     0     0     0     0  ]};
c.n{7}= {'mn:gds','S',   [0    0    0     0     0    0     1     0     0     0     0     0     0     0     0  ]};
c.n{8}= {'mn:cgg','F',   [0    0    0     0     0    0     0     1     0     0     0     0     0     0     0  ]};
c.n{9}= {'mn:cgs','F',   [0    0    0     0     0    0     0     0     1     0     0     0     0     0     0  ]};
c.n{10}={'mn:cgd','F',   [0    0    0     0     0    0     0     0     0     0     1     0     0     0     0  ]};
c.n{11}={'mn:cge','F',   [0    0    0     0     0    0     0     0     0     0     0     0     1     0     0  ]};
c.n{12}={'mn:cdd','F',   [0    0    0     0     0    0     0     0     0     0     0     0     0     1     0  ]};
c.n{13}={'mn:cdg','F',   [0    0    0     0     0    0     0     0     0     0     0     1     0     0     0  ]};
c.n{14}={'mn:css','F',   [0    0    0     0     0    0     0     0     0     0     0     0     0     0     1  ]};
c.n{15}={'mn:csg','F',   [0    0    0     0     0    0     0     0     0     1     0     0     0     0     0  ]};
c.n{16}={'mn:cjdt','F',  [0    0    0     0     0    0     0     0     0     0     0     0     0     1     0  ]};
c.n{17}={'mn:cjst','F',  [0    0    0     0     0    0     0     0     0     0     0     0     0     0     1  ]};
%
%                      {'ID','VT','IGD','IGS','GM','GMB','GDS','CGG','CGS','CSG','CGD','CDG','CGB','CDD','CSS'};
c.p{1}= {'mp:ids','A',   [-1   0    0     0     0    0     0     0     0     0     0     0     0     0     0  ]};
c.p{2}= {'mp:vth','V',   [0   -1    0     0     0    0     0     0     0     0     0     0     0     0     0  ]};
c.p{3}= {'mp:igd','A',   [0    0   -1     0     0    0     0     0     0     0     0     0     0     0     0  ]};
c.p{4}= {'mp:igs','A',   [0    0    0    -1     0    0     0     0     0     0     0     0     0     0     0  ]};
c.p{5}= {'mp:gm','S',    [0    0    0     0     1    0     0     0     0     0     0     0     0     0     0  ]};
c.p{6}= {'mp:gmbs','S',  [0    0    0     0     0    1     0     0     0     0     0     0     0     0     0  ]};
c.p{7}= {'mp:gds','S',   [0    0    0     0     0    0     1     0     0     0     0     0     0     0     0  ]};
c.p{8}= {'mp:cgg','F',   [0    0    0     0     0    0     0     1     0     0     0     0     0     0     0  ]};
c.p{9}= {'mp:cgs','F',   [0    0    0     0     0    0     0     0     1     0     0     0     0     0     0  ]};
c.p{10}={'mp:cgd','F',   [0    0    0     0     0    0     0     0     0     0     1     0     0     0     0  ]};
c.p{11}={'mp:cge','F',   [0    0    0     0     0    0     0     0     0     0     0     0     1     0     0  ]};
c.p{12}={'mp:cdd','F',   [0    0    0     0     0    0     0     0     0     0     0     0     0     1     0  ]};
c.p{13}={'mp:cdg','F',   [0    0    0     0     0    0     0     0     0     0     0     1     0     0     0  ]};
c.p{14}={'mp:css','F',   [0    0    0     0     0    0     0     0     0     0     0     0     0     0     1  ]};
c.p{15}={'mp:csg','F',   [0    0    0     0     0    0     0     0     0     1     0     0     0     0     0  ]};
c.p{16}={'mp:cjdt','F',  [0    0    0     0     0    0     0     0     0     0     0     0     0     1     0  ]};
c.p{17}={'mp:cjst','F',  [0    0    0     0     0    0     0     0     0     0     0     0     0     0     1  ]};
%
c.outvars_noise = {'STH','SFL'};
c.n_noise{1}= {'mn:therm_sid', 'mn_nch_svt_mac_10:therm_sid'};
c.n_noise{2}= {'mn:flicker', 'mn_nch_svt_mac_10:flicker'};
%
c.p_noise{1}= {'mp:therm_sid', 'mp_pch_svt_mac_10:therm_sid'};
c.p_noise{2}= {'mp:flicker', 'mp_pch_svt_mac_10:flicker'};



% Simulation netlist
netlist = sprintf([...
'//techsweep.scs \n'...
'include  %s\n'...
'include  %s\n'...
'include "techsweep_params.scs" \n'...
'save mn \n'...
'save mp \n'...
'parameters gs=0 ds=0 \n'...
'vnoi     (vx  0)         vsource dc=0  \n'...
'vdsn     (vdn vx)        vsource dc=ds  \n'...
'vgsn     (vgn 0)         vsource dc=gs  \n'...
'vbsn     (vbn 0)         vsource dc=-sb \n'...
'vdsp     (vdp vx)        vsource dc=-ds \n'...
'vgsp     (vgp 0)         vsource dc=-gs \n'...
'vbsp     (vbp 0)         vsource dc=sb  \n'...
'\n'...
'//NOTE: YOUR MODELS SHOULD BE SET UP SUCH THAT THE STRESS PARAMS (SA, SB, etc.) ARE AUTOMATICALLY COMPUTED\n'...
'mn (vdn vgn 0 vbn) %s l=length*1e-6 nfin=%d nf=%d\n'...
'mp (vdp vgp 0 vbp) %s l=length*1e-6 nfin=%d nf=%d\n'...
'\n'...
'options1 options gmin=1e-13 reltol=1e-4 vabstol=1e-6 iabstol=1e-10 temp=%d tnom=27 rawfmt=psfbin rawfile="./techsweep.raw" \n'...
'sweepvds sweep param=ds start=0 stop=%d step=%d { \n'...
'   sweepvgs dc param=gs start=0 stop=%d step=%d \n'...
'}\n'...
'sweepvds_noise sweep param=ds start=0 stop=%d step=%d { \n'...
'   sweepvgs_noise noise freq=1 oprobe=vnoi param=gs start=0 stop=%d step=%d \n'...
'}\n'...

], c.modelfile1, c.modelfile2,...
c.modeln,...
c.NFIN,...
c.NF,...
c.modelp,...
c.NFIN,...
c.NF,...
c.temp-273, ...
c.VDS_max, c.VDS_step, ...
c.VGS_max, c.VGS_step, ...
c.VDS_max, c.VDS_step, ...
c.VGS_max, c.VGS_step);

% Write netlist
fid = fopen('techsweep.scs', 'w');
fprintf(fid, netlist);
fclose(fid);

return
