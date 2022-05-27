clc; clear all;

% Define chip list and full temp range
clist = [11, 12, 13, 14, 15, 16, 17];
tlist = -40:10:120;
Ntemp = length(tlist);
Nchip = length(clist);

% Re-organize Measured Data
freq_data_array = zeros(Ntemp, Nchip, 64);
for c = 1:Nchip
    for t = 1:Ntemp
        file = ['../MeasResults/ChipNo', num2str(clist(c)), '/Meas_ChipNo', num2str(clist(c)), '_Vdio3.0Vdd1.8_', num2str(tlist(t)), 'C.csv'];
        dtable = readtable(file, 'PreserveVariableNames', 1);
        for design = 1:64
            freq_data_array(t, c, design) = table2array(dtable(design, 'Freq0 (kHz)'));
        end
    end
end

% Define temperature range to explore
tstart_ind  = 1; % 0C
twin_len    = 10; % 0C + 100C = 100C
pcalib      = 1; % +/-20C calibration

% How good we want the performance to be
inacc_th    = 2.5;
Nc_B        = 6;

% Explore the best designs out of 64
params_arr = zeros(2, Nchip, 64);
inacc_arr  = zeros(Ntemp, Nchip, 64);
Nc_A_arr = zeros(1, 64);
indlist_A_arr = zeros(2, Nchip, 64);
inacc_B_arr = zeros(1, 64);
indlist_B_arr = zeros(2, Nc_B, 64);
for design = 1:64
    freq_arr = freq_data_array(:, :, design);
    [params, inacc, Nc_A, indlist_A, inacc_B, indlist_B] = EvalDesignGivenRange(freq_arr, tlist, tstart_ind, twin_len, pcalib, inacc_th, Nc_B);
    params_arr(:, :, design) = params;
    inacc_arr(:, :, design) = inacc;
    Nc_A_arr(:, design) = Nc_A;
    indlist_A_arr(:, :, design) = indlist_A;
    inacc_B_arr(:, design) = inacc_B;
    indlist_B_arr(:, :, design) = indlist_B;
end
