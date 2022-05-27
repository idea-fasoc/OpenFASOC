fprintf("Explore High Temp Range......\n");
% Explore high-temp range
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

% Calculate FoMs
freq_arr_20C = freq_data_array(7, :, :);
    % Calculate resolution type-1
freq_pres1_arr_20C = freq_arr_20C + res_data_array(1, :, :);
freq_nres1_arr_20C = freq_arr_20C - res_data_array(1, :, :);
T_pres1_arr_20C = abs((scale .* TZiK .* params_arr(1, :, :) .* log(freq_pres1_arr_20C) + params_arr(2, :, :)) ./ (1 - scale .* params_arr(1, :, :) .* log(freq_pres1_arr_20C)));
T_nres1_arr_20C = abs((scale .* TZiK .* params_arr(1, :, :) .* log(freq_nres1_arr_20C) + params_arr(2, :, :)) ./ (1 - scale .* params_arr(1, :, :) .* log(freq_nres1_arr_20C)));
T_res1_arr_20C = (T_pres1_arr_20C - T_nres1_arr_20C) / 2;
    % Calculate resolution type-2
freq_pres2_arr_20C = freq_arr_20C + res_data_array(2, :, :);
freq_nres2_arr_20C = freq_arr_20C - res_data_array(2, :, :);
T_pres2_arr_20C = abs((scale .* TZiK .* params_arr(1, :, :) .* log(freq_pres2_arr_20C) + params_arr(2, :, :)) ./ (1 - scale .* params_arr(1, :, :) .* log(freq_pres2_arr_20C)));
T_nres2_arr_20C = abs((scale .* TZiK .* params_arr(1, :, :) .* log(freq_nres2_arr_20C) + params_arr(2, :, :)) ./ (1 - scale .* params_arr(1, :, :) .* log(freq_nres2_arr_20C)));
T_res2_arr_20C = (T_pres2_arr_20C - T_nres2_arr_20C) / 2;
    % Calculate type-1 FoM for all
FoM_data_array = EnC_data_array(1, :, :) .* (T_res1_arr_20C .^ 2) * 1e3; % pJ * K^2
FoM_B_arr = zeros(1, Nc_B, 64); power_B_arr = zeros(1, Nc_B, 64);
T_res1_B_arr = zeros(1, Nc_B); T_res2_B_arr = zeros(1, Nc_B, 64); EnC_B_arr = zeros(1, Nc_B, 64);
for d = 1:64
    FoM_B_arr(1, :, d) = FoM_data_array(1, indlist_B_arr(1, :, d), d);
    power_B_arr(1, :, d) = power_data_array(1, indlist_B_arr(1, :, d), d);
    T_res1_B_arr(1, :, d) = T_res1_arr_20C(1, indlist_B_arr(1, :, d), d);
    T_res2_B_arr(1, :, d) = T_res2_arr_20C(1, indlist_B_arr(1, :, d), d);
    EnC_B_arr(1, :, d) = EnC_data_array(1, indlist_B_arr(1, :, d), d);
end

% Best FoM design with header-A
min_order = 1; err_th = 3;
[design, FoM, power, res, EnC] = EvalDesignFoM(1:32, min_order, inacc_B_arr, err_th, FoM_B_arr, power_B_arr, T_res1_B_arr, EnC_B_arr);
[design, inacc_sub_arr, inacc_sub_arr_sec, pos_inacc, neg_inacc, ~, sigma_sec, pos_sigma_inacc, neg_sigma_inacc] = ...
    EvalDesignInacc(design, inacc_arr, inacc_arr_sec, inacc_B_arr, indlist_B_arr, tstart_ind, twin_len);
fprintf("Header-A Design %d has lowest FoM. \n", design);
fprintf("Max/Min error w/o SEC is %f/+%f degreeC. \n", neg_inacc(1), pos_inacc(1));
fprintf("3-sigma error w/o SEC is %f/+%f degreeC. \n", neg_sigma_inacc(1), pos_sigma_inacc(1));
fprintf("Max/Min error w/ SEC is %f/+%f degreeC. \n", neg_inacc(2), pos_inacc(2));
fprintf("3-sigma error w/ SEC is %f/+%f degreeC. \n", neg_sigma_inacc(2), pos_sigma_inacc(2));
    % Plot Inaccuracy and 3-sigma against temp
[fig, hdl] = PlotInacc(fig, tlist(tstart_ind:(tstart_ind + twin_len)), inacc_sub_arr, inacc_sub_arr_sec, sigma_sec, design);
saveas(hdl, './Figures/InaccVStemp_hdrA_hr.emf');
    % Report FoM
fprintf("Power, EnC, res and FoM are %fuW, %fnJ, %fK, %fpJ*K^2. \n", power, EnC, res, FoM);
fprintf("\n");

% Best FoM design with header-B
min_order = 1; err_th = 4;
[design, FoM, power, res, EnC] = EvalDesignFoM(33:64, min_order, inacc_B_arr, err_th, FoM_B_arr, power_B_arr, T_res1_B_arr, EnC_B_arr);
[design, inacc_sub_arr, inacc_sub_arr_sec, pos_inacc, neg_inacc, sigma, sigma_sec, pos_sigma_inacc, neg_sigma_inacc] = ...
    EvalDesignInacc(design, inacc_arr, inacc_arr_sec, inacc_B_arr, indlist_B_arr, tstart_ind, twin_len);
fprintf("Header-B Design %d has lowest FoM. \n", design);
fprintf("Max/Min error w/o SEC is %f/+%f degreeC. \n", neg_inacc(1), pos_inacc(1));
fprintf("3-sigma error w/o SEC is %f/+%f degreeC. \n", neg_sigma_inacc(1), pos_sigma_inacc(1));
fprintf("Max/Min error w/ SEC is %f/+%f degreeC. \n", neg_inacc(2), pos_inacc(2));
fprintf("3-sigma error w/ SEC is %f/+%f degreeC. \n", neg_sigma_inacc(2), pos_sigma_inacc(2));
    % Plot Inaccuracy and 3-sigma against temp
[fig, hdl] = PlotInacc(fig, tlist(tstart_ind:(tstart_ind + twin_len)), inacc_sub_arr, inacc_sub_arr_sec, sigma_sec, design);
saveas(hdl, './Figures/InaccVStemp_hdrB_hr.emf');
    % Report FoM
fprintf("Power, EnC, res and FoM are %fuW, %fnJ, %fK, %fpJ*K^2. \n", power, EnC, res, FoM);
fprintf("\n");
