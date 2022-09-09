% Matlab script for technology characterization
% Debug version (one HSpice run + display)
% Boris Murmann
% Stanford University
% September 12, 2017

clearvars;
close all;

tic
% Load configuration
c = techsweep_config_bsim3_180_hspice;

% Write simulation parameters
fid=fopen('techsweep_params.sp', 'w');
fprintf(fid,'.param length = %d\n', c.LENGTH(1));
fprintf(fid,'.param sb = %d\n', c.VSB(1));
fprintf(fid,'.data data1 \n');
fprintf(fid,'+ gs ds \n');
for i=1:length(c.VDS)
    for j=1:length(c.VGS)
        fprintf(fid,'+ %d %d \n', c.VGS(j), c.VDS(i));
    end 
end
fprintf(fid,'.enddata \n');
fclose(fid);

% Run simulator
[status,result] = system(c.simcmd);
if(status)
    disp('Simulation did not run properly. Check techsweep.out.')
    return;
end

%Read and display results
h = loadsig(c.outfile);
lssig(h)
hn = loadsig(c.outfile_noise);
lssig(hn)

% Display data for middle of sweep
idx1 = round(length(c.VGS)/2);
idx2 = round(length(c.VDS)/2);
s = sprintf('Data for VGS = %d, VDS = %d, VSB = %d, L = %d', c.VGS(idx1), c.VDS(idx2), c.VSB(1), c.LENGTH(1));
disp(s)

% Read and display raw parameters and created output
for k = 1:length(c.nvars)
    values = evalsig(h, c.nvars{k});
    s = sprintf('%s = %d', c.nvars{k}, values(idx1, idx2));
    disp(s);
    nch.(c.outvars{k}) = values(idx1, idx2);
end
for k = 1:length(c.nvars_noise)
    values_vec = evalsig(hn, c.nvars_noise{k});
    values = vec2mat(values_vec, length(c.VDS))';    
    s = sprintf('%s = %d', c.nvars_noise{k}, values(idx1, idx2));
    disp(s);
    nch.(c.outvars_noise{k}) = values(idx1, idx2);
end
disp(nch);

for k = 1:length(c.pvars)
    values = evalsig(h, c.pvars{k});
    s = sprintf('%s = %d', c.pvars{k}, values(idx1, idx2));
    disp(s);
    pch.(c.outvars{k}) = values(idx1, idx2);
end
for k = 1:length(c.pvars_noise)
    values_vec = evalsig(hn, c.pvars_noise{k});
    values = vec2mat(values_vec, length(c.VDS))';
    s = sprintf('%s = %d', c.pvars_noise{k}, values(idx1, idx2));
    disp(s);
    pch.(c.outvars_noise{k}) = values(idx1, idx2);
end
disp(pch);
toc

% check comversion from vector to array
vgn = evalsig(h, 'v_vgn');
vgn_vec = evalsig(hn, 'sw_gs');
vgn1 = vec2mat(vgn_vec, length(c.VDS))';
find(vgn-vgn1)

gm = evalsig(h, 'n_gm');
id = evalsig(h, 'n_id');
figure;
plot(gm./id)
gm = evalsig(h, 'p_gm');
id = evalsig(h, 'p_id');
figure;
plot(gm./id)



