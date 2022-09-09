% Matlab script for technology characterization
% Boris Murmann, Stanford University
% Tested with MMSIM12.11.134
% September 12, 2017

clearvars; 
close all;

% Load configuration
%c = techsweep_config_psp_65_spectre;
c = techsweep_config_bsim4_28_spectre;

% Write sweep info
nch.INFO   = c.modelinfo;
nch.CORNER = c.corner;
nch.TEMP   = c.temp;
nch.NFING  = c.NFING;
nch.L      = c.LENGTH';
nch.W      = c.WIDTH;
nch.VGS    = c.VGS';
nch.VDS    = c.VDS';
nch.VSB    = c.VSB';
%
pch.INFO   = c.modelinfo;
pch.CORNER = c.corner;
pch.TEMP   = c.temp;
pch.NFING  = c.NFING;
pch.L      = c.LENGTH';
pch.W      = c.WIDTH;
pch.VGS    = c.VGS';
pch.VDS    = c.VDS';
pch.VSB    = c.VSB';

% Simulation loop
for i = 1:length(c.LENGTH)
    str=sprintf('L = %2.3f', c.LENGTH(i));
    disp(str);
    for j = 1:length(c.VSB)
        % Write simulation parameters
        fid=fopen('techsweep_params.scs', 'w');
        fprintf(fid,'parameters length = %d\n', c.LENGTH(i));
        fprintf(fid,'parameters sb = %d\n', c.VSB(j));
        fclose(fid);
        
        pause(5)
        
        % Run simulator
        [status,result] = system(c.simcmd);
        if(status)
            disp('Simulation did not run properly. Check techsweep.out.')
            return;
        end    
        
        % Initialize data blocks
        for m = 1:length(c.outvars)
            nch.(c.outvars{m})(i,:,:,j) = zeros(length(c.VGS), length(c.VDS));
            pch.(c.outvars{m})(i,:,:,j) = zeros(length(c.VGS), length(c.VDS));
        end
        
        % Read and store results
        for k = 1:length(c.n)
            params_n = c.n{k};
            struct_n = cds_srr(c.outfile, c.sweep, params_n{1});
            values_n = struct_n.(params_n{2});
            params_p = c.p{k};
            struct_p = cds_srr(c.outfile, c.sweep, params_p{1});
            values_p = struct_p.(params_p{2});
            for m = 1:length(c.outvars)
                nch.(c.outvars{m})(i,:,:,j)  = squeeze(nch.(c.outvars{m})(i,:,:,j)) + values_n*params_n{3}(m);
                pch.(c.outvars{m})(i,:,:,j)  = squeeze(pch.(c.outvars{m})(i,:,:,j)) + values_p*params_p{3}(m);
            end
        end
        % Noise results
        for k = 1:length(c.n_noise)
            params_n = c.n_noise{k};
            % note: using cds_innersrr, since cds_srr is buggy for noise
            struct_n = cds_innersrr(c.outfile, c.sweep_noise, params_n{1},0);
            field_names = fieldnames(struct_n);
            values_n = struct_n.(field_names{4});
            params_p = c.p_noise{k};
            % note: using cds_innersrr, since cds_srr is buggy for noise
            struct_p = cds_innersrr(c.outfile, c.sweep_noise, params_p{1},0);
            field_names = fieldnames(struct_p);
            values_p = struct_p.(field_names{4});
            nch.(c.outvars_noise{k})(i,:,:,j) = squeeze(values_n);
            pch.(c.outvars_noise{k})(i,:,:,j) = squeeze(values_p);
        end
    end
end

save(c.savefilen, 'nch');
save(c.savefilep, 'pch');
