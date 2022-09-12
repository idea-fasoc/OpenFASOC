clc; clear all;
% This script generates the temperature sensor model file in SkyWater 130nm
% basing on real measurement results of 64 designs from 15 chips.

% Load and pre-process power and resolution data
LoadPowerRes;

% Load Tested Frequency Data
LoadFreqData;

% Set the temperature range here
% Temperature starts from -40C with a step of 10C
% [-20C, 100C] for the model file
tstart_ind  = 3; % -20C
twin_len    = 12; % -20C + 120C = 100C
pcalib      = 1; % +/- 10C calibration. Trim points are -10C and 90C.

% Calculate inaccuracies
  % Parameters
inacc_th    = 5; % Tolerable upper limit for MAE is 5C. Only count chips with MAE less than this.
Nc_B        = 5; % Not used for model file.
order_sec = 3; % Not used for model file.
  % Result Arrays
params_arr = zeros(2, Nchip, 64);
inacc_arr  = zeros(Ntemp, Nchip, 64);
params_sec_arr = zeros(order_sec + 1, 64);
inacc_arr_sec = zeros(Ntemp, Nchip, 64);
Nc_A_arr = zeros(1, 64);
indlist_A_arr = zeros(2, Nchip, 64);
inacc_B_arr = zeros(1, 64);
indlist_B_arr = zeros(2, Nc_B, 64);
  % Calculation
for design = 1:64
    freq_arr = freq_data_array(:, :, design);
    [params, inacc, params_sec, inacc_sec, Nc_A, indlist_A, inacc_B, indlist_B] = ...
        EvalDesignGivenRange(freq_arr, tlist, tstart_ind, twin_len, pcalib, inacc_th, Nc_B, order_sec);
    params_arr(:, :, design) = params;
    inacc_arr(:, :, design) = inacc;
    params_sec_arr(:, design) = params_sec;
    inacc_arr_sec(:, :, design) = inacc_sec;
    Nc_A_arr(:, design) = Nc_A;
    indlist_A_arr(:, :, design) = indlist_A;
    inacc_B_arr(:, design) = inacc_B;
    indlist_B_arr(:, :, design) = indlist_B;
end

% Generate Model File
  % Parameters
t_ind_mf = 3:2:15; % -20C:20C:100C
Ntemp_mf = length(t_ind_mf);
Ndesign_mf = 64;
  % Model file arrays
Temp = zeros(Ntemp_mf*Ndesign_mf,1);
Frequency = zeros(Ntemp_mf*Ndesign_mf,1);
Power = zeros(Ntemp_mf*Ndesign_mf,1);
Error = zeros(Ntemp_mf*Ndesign_mf,1);
inv = zeros(Ntemp_mf*Ndesign_mf,1);
header = zeros(Ntemp_mf*Ndesign_mf,1);
HeaderType = strings(Ntemp_mf*Ndesign_mf,1);
StdCellType = strings(Ntemp_mf*Ndesign_mf,1);
  % Calculate model file arrays
for design = 1:Ndesign_mf
    for tt = 1:Ntemp_mf
        % Temperature
        Temp((design-1)*Ntemp_mf + tt, 1) = tlist(t_ind_mf(tt));

        % Determine which chips to use for the design
        clist_mf = indlist_A_arr(1, :, design);
        Nchip_mf = sum(clist_mf > 0);

        % Frequency, Power and Error
        if (Nchip_mf > 0)
            % if the design "works"
            Frequency((design-1)*Ntemp_mf + tt, 1) = mean(freq_data_array(t_ind_mf(tt), clist_mf(1:Nchip_mf), design))*1e3; % Hz
            Power((design-1)*Ntemp_mf + tt, 1) = mean(power_data_array(1, clist_mf(1:Nchip_mf), design))*1e-6; % W
            Error((design-1)*Ntemp_mf + tt, 1) = mean(inacc_arr(t_ind_mf(tt), clist_mf(1:Nchip_mf), design)); % C
        else
            % if the design does not "work" (Accuracy too bad - No chip with MAE less than inacc_th)
            Frequency((design-1)*Ntemp_mf + tt, 1) = 0; % Set all frequency to 0
            Power((design-1)*Ntemp_mf + tt, 1) = inf; % Set all power to infinity
            Error((design-1)*Ntemp_mf + tt, 1) = inf; %  Set all error to infinity
        end

        % Circuit Config
          % Determine No. inverter
        inv((design-1)*Ntemp_mf + tt, 1) = 2*mod(design-1, 4) + 4;
          % Determine No. header
        header((design-1)*Ntemp_mf + tt, 1) = 2*floor(mod(design-1, 16)/4) + 3;
          % Determine Header Type
        hdrType = floor((design-1)/32);
        if (hdrType == 0)
            HeaderType((design-1)*Ntemp_mf + tt, 1) = "A";
        else
            HeaderType((design-1)*Ntemp_mf + tt, 1) = "B";
        end
          % Determine StdCellType
        stdCellType = floor(mod(design-1, 32)/16);
        if (stdCellType == 0)
            StdCellType((design-1)*Ntemp_mf + tt, 1) = "hs";
        else
            StdCellType((design-1)*Ntemp_mf + tt, 1) = "hd";
        end
    end
end

T = table(Temp, Frequency, Power, Error, inv, header, HeaderType, StdCellType);
filename = "../modelfile_Sky130Silicon.csv";
writetable(T, filename, 'WriteVariableNames', true);
