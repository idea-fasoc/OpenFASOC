% Matlab script for technology characterization
% Boris Murmann
% Stanford University
% September 12, 2017

clearvars;
close all;

% Load configuration
c = techsweep_config_bsim3_180_hspice;

% Simulation loop
for i = 1:length(c.LENGTH)
    str=sprintf('L = %2.2f', c.LENGTH(i));
    disp(str);
    tic
    for j = 1:length(c.VSB)
        % Write simulation parameters
        fid=fopen('techsweep_params.sp', 'w');
        fprintf(fid,'.param length = %d\n', c.LENGTH(i));
        fprintf(fid,'.param sb = %d\n', c.VSB(j));
        fprintf(fid,'.data data1 \n');
        fprintf(fid,'+ gs ds \n');
        for m=1:length(c.VDS)
            for n=1:length(c.VGS)
                fprintf(fid,'+ %d %d \n', c.VGS(n), c.VDS(m));
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
        
        %Read and store results
        h = loadsig(c.outfile);
        for n = 1: length(c.outvars)
            nch.(c.outvars{n})(i,:,:,j)  = evalsig(h, c.nvars{n});
            pch.(c.outvars{n})(i,:,:,j)  = evalsig(h, c.pvars{n});
        end
        h = loadsig(c.outfile_noise);
        for n = 1: length(c.outvars_noise)
            values_vec = evalsig(h, c.nvars_noise{n});
            values = vec2mat(values_vec, length(c.VDS))';
            nch.(c.outvars_noise{n})(i,:,:,j)  = values;
            values_vec = evalsig(h, c.pvars_noise{n});
            values = vec2mat(values_vec, length(c.VDS))';
            pch.(c.outvars_noise{n})(i,:,:,j)  = values;
        end
        
    end
    toc
end
% Include sweep info
nch.INFO   = c.modelinfo; 
nch.CORNER = c.corner; 
nch.TEMP   = c.temp; 
nch.VGS    = c.VGS';
nch.VDS    = c.VDS';
nch.VSB    = c.VSB';
nch.L      = c.LENGTH';
nch.W      = c.WIDTH;
nch.NFING  = c.NFING;
pch.INFO   = c.modelinfo;
pch.CORNER = c.corner; 
pch.TEMP   = c.temp; 
pch.VGS    = c.VGS';
pch.VDS    = c.VDS';
pch.VSB    = c.VSB';
pch.L      = c.LENGTH';
pch.W      = c.WIDTH;
pch.NFING  = c.NFING;

save(c.savefilen, 'nch');
save(c.savefilep, 'pch');
