clc; clear all;
% Load Tested Frequency Data
LoadFreqData;
    % How good we want the performance to be
inacc_th    = 2.5;
Nc_B        = 8;
    % Polynomial SEC Order
order_sec = 3;

% Explore temp range
tstart_ind  = 5; % 0C
twin_len    = 12; % 0C + 120C = 120C
pcalib      = 1; % +/- 10C calibration
    % Explore the best designs out of 64
params_arr = zeros(2, Nchip, 64);
inacc_arr  = zeros(Ntemp, Nchip, 64);
params_sec_arr = zeros(order_sec + 1, 64);
inacc_arr_sec = zeros(Ntemp, Nchip, 64);
Nc_A_arr = zeros(1, 64);
indlist_A_arr = zeros(2, Nchip, 64);
inacc_B_arr = zeros(1, 64);
indlist_B_arr = zeros(2, Nc_B, 64);
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

% Find the best designs in each group
inacc_hist_design = zeros(2, 16);
inacc_hist_minmax = zeros(2, 16);
inacc_hist_minmax_sec = zeros(2, 16);
inacc_hist_sigma  = zeros(2, 16);
inacc_hist_sigma_sec  = zeros(2, 16);

for i = 1:16
    % Find the best design in the group
    [design, inacc_sub_arr, inacc_sub_arr_sec, pos_inacc, neg_inacc, sigma, sigma_sec, pos_sigma_inacc, neg_sigma_inacc] = ...
        EvalDesignInacc((4*i-3):4*i, inacc_arr, inacc_arr_sec, inacc_B_arr, indlist_B_arr, tstart_ind, twin_len);
    inacc_hist_design(1, i) = design;
    inacc_hist_minmax(1, i) = pos_inacc(1); inacc_hist_minmax(2, i) = neg_inacc(1);
    inacc_hist_minmax_sec(1, i) = pos_inacc(2); inacc_hist_minmax_sec(2, i) = neg_inacc(2);
    inacc_hist_sigma(1, i) = pos_sigma_inacc(1); inacc_hist_sigma(2, i) = neg_sigma_inacc(1);
    inacc_hist_sigma_sec(1, i) = pos_sigma_inacc(2); inacc_hist_sigma_sec(2, i) = neg_sigma_inacc(2);
    % If max pre-SEC inacc is too large, treat it as not working across multiple chips
    if max(abs(inacc_hist_minmax(:, i))) >= 5.0
        inacc_hist_design(2, i) = 0;
    else
        inacc_hist_design(2, i) = 1;
    end
    inacc_hist_minmax = inacc_hist_minmax .* inacc_hist_design(2, :);
    inacc_hist_minmax_sec = inacc_hist_minmax_sec .* inacc_hist_design(2, :);
    inacc_hist_sigma = inacc_hist_sigma .* inacc_hist_design(2, :);
    inacc_hist_sigma_sec = inacc_hist_sigma_sec .* inacc_hist_design(2, :);
end

fprintf("Plot Inaccuracy Histogram across Designs......\n");
fig = 1;
    % Plot min/max error spread across designs
[fig, hdl_minmax] = PlotInaccHist(fig, inacc_hist_minmax, inacc_hist_minmax_sec, 0);
saveas(hdl_minmax, './Figures/InaccHist_MinMax.emf');
    % Plot 3-sigma error spread across designs
[fig, hdl_sigma] = PlotInaccHist(fig, inacc_hist_sigma, inacc_hist_sigma_sec, 1);
saveas(hdl_sigma, './Figures/InaccHist_3sigma.emf');
