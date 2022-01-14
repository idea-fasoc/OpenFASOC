clc; clear all;
TZiK = 273.15; scale = 1;
% Load and pre-process power and resolution data
LoadPowerRes;
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
FoM2_data_array = EnC_data_array(2, :, :) .* (T_res2_arr_20C .^ 2); % nJ * K^2
FoM_B_arr = zeros(1, Nc_B, 64); FoM2_B_arr = zeros(1, Nc_B, 64); power_B_arr = zeros(1, Nc_B, 64);
T_res1_B_arr = zeros(1, Nc_B); T_res2_B_arr = zeros(1, Nc_B, 64); EnC_B_arr = zeros(1, Nc_B, 64);
for d = 1:64
    FoM_B_arr(1, :, d) = FoM_data_array(1, indlist_B_arr(1, :, d), d);
    FoM2_B_arr(1, :, d) = FoM2_data_array(1, indlist_B_arr(1, :, d), d);
    power_B_arr(1, :, d) = power_data_array(1, indlist_B_arr(1, :, d), d);
    T_res1_B_arr(1, :, d) = T_res1_arr_20C(1, indlist_B_arr(1, :, d), d);
    T_res2_B_arr(1, :, d) = T_res2_arr_20C(1, indlist_B_arr(1, :, d), d);
    EnC_B_arr(1, :, d) = EnC_data_array(1, indlist_B_arr(1, :, d), d);
end

% Best FoM design in each group
hdrA_hs_scatter_data = [];
hdrA_hd_scatter_data = [];
hdrB_hs_scatter_data = [];
hdrB_hd_scatter_data = [];

err_th = 5.0; order_min = 1;
for d = 1:32
    % Only plot designs with a reasonable inaccuracy
    if (inacc_B_arr(1, d) < err_th)
        [~, sorted_ind] = sort(FoM2_B_arr(1, :, d));
        for i = order_min:Nc_B
            if (FoM2_B_arr(1, sorted_ind(i), d) > 0) && (T_res2_B_arr(1, sorted_ind(i), d) > 0.01)
                power_mean =  power_B_arr(1, sorted_ind(i), d);
                res_mean = T_res2_B_arr(1, sorted_ind(i), d);
                FoM2_mean = FoM2_B_arr(1, sorted_ind(i), d);
                break;
            end
        end
        if (d <= 16) % hdrA_hs
            data = [d; power_mean; res_mean; FoM2_mean];
            hdrA_hs_scatter_data = [hdrA_hs_scatter_data, data];
        elseif (d <= 32) % hdrA_hd
            data = [d; power_mean; res_mean; FoM2_mean];
            hdrA_hd_scatter_data = [hdrA_hd_scatter_data, data];                 
        end
    end
end

err_th = 5.0; order_min = 1;
for d = 33:64
    % Only plot designs with a reasonable inaccuracy
    if (inacc_B_arr(1, d) < err_th) 
        [~, sorted_ind] = sort(FoM2_B_arr(1, :, d));
        for i = order_min:Nc_B
            if (FoM2_B_arr(1, sorted_ind(i), d) > 0) && (T_res2_B_arr(1, sorted_ind(i), d) > 0.01)
                power_mean =  power_B_arr(1, sorted_ind(i), d);
                res_mean = T_res2_B_arr(1, sorted_ind(i), d);
                FoM2_mean = FoM2_B_arr(1, sorted_ind(i), d);
                break;
            end
        end
        if (d <= 48) % hdrB_hs
            data = [d; power_mean; res_mean; FoM2_mean];
            hdrB_hs_scatter_data = [hdrB_hs_scatter_data, data];                
        else % hdrB_hd
            data = [d; power_mean; res_mean; FoM2_mean];
            hdrB_hd_scatter_data = [hdrB_hd_scatter_data, data];        
        end
    end
end

% Scatter Plot
hdl = figure(1);
color = {'blue', '#4DBEEE', 'red', '#EDB120'};
MarkerSize = 120; LineWidth = 1.5;
s1 = scatter(hdrA_hs_scatter_data(2,:), hdrA_hs_scatter_data(3,:), MarkerSize, 'p', 'MarkerEdgeColor', cell2mat(color(1)), 'LineWidth', LineWidth); hold on;
s2 = scatter(hdrA_hd_scatter_data(2,:), hdrA_hd_scatter_data(3,:), MarkerSize, 's', 'MarkerEdgeColor', cell2mat(color(2)), 'LineWidth', LineWidth); hold on;
s3 = scatter(hdrB_hs_scatter_data(2,:), hdrB_hs_scatter_data(3,:), MarkerSize, 'd', 'MarkerEdgeColor', cell2mat(color(3)), 'LineWidth', LineWidth); hold on;
s4 = scatter(hdrB_hd_scatter_data(2,:), hdrB_hd_scatter_data(3,:), MarkerSize, 'o', 'MarkerEdgeColor', cell2mat(color(4)), 'LineWidth', LineWidth); hold on;
    % Axis
xlim([0.05, 100]); xticks([0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100]);
ylim([0.025 0.18]); yticks(0.025:0.025:0.18);
set(gca,'xscale','log', 'FontSize', 18);
    % Labels
xlabel('Power (uW)', 'FontSize', 18);
ylabel('RMS Resolution (K)', 'FontSize', 18);
    % Legend
leg = legend([s1, s2, s3, s4], ...
            "Header A and 'hs' cells", "Header A and 'hd' cells", ...
            "Header B and 'hs' cells", "Header B and 'hd' cells", ... 
            'FontSize', 18, 'Location', 'NorthEast');
leg.ItemTokenSize = [24, 24];
    % Set Figure Size
set(gcf, 'Position', [0 0 1000 400]);
    % Grid on
grid on;
    % Save figure
saveas(hdl, './Figures/PowerResScatter.emf');

% hdl = figure(2);
% color = {'blue', '#4DBEEE', 'red', '#EDB120'};
% MarkerSize = 100; LineWidth = 1.5;
% s1 = scatter(hdrA_hs_scatter_data(2,:), hdrA_hs_scatter_data(4,:), MarkerSize, 'p', 'MarkerEdgeColor', cell2mat(color(1)), 'LineWidth', LineWidth); hold on;
% s2 = scatter(hdrA_hd_scatter_data(2,:), hdrA_hd_scatter_data(4,:), MarkerSize, 's', 'MarkerEdgeColor', cell2mat(color(2)), 'LineWidth', LineWidth); hold on;
% s3 = scatter(hdrB_hs_scatter_data(2,:), hdrB_hs_scatter_data(4,:), MarkerSize, 'd', 'MarkerEdgeColor', cell2mat(color(3)), 'LineWidth', LineWidth); hold on;
% s4 = scatter(hdrB_hd_scatter_data(2,:), hdrB_hd_scatter_data(4,:), MarkerSize, 'o', 'MarkerEdgeColor', cell2mat(color(4)), 'LineWidth', LineWidth); hold on;
%     % Axis
% xlim([0.1, 100]); xticks([0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100]);
% ylim([10 1000]); % yticks(0.02:0.02:0.16);
% set(gca,'xscale','log', 'FontSize', 14);
% set(gca,'yscale','log', 'FontSize', 14);
%     % Labels
% xlabel('Power (uW)', 'FontSize', 14)
% ylabel('FoM (pJ·K^{2})', 'FontSize', 14);
%     % Legend
% leg = legend([s1, s2, s3, s4], ...
%             "Header A and 'hs' cells", "Header A and 'hd' cells", ...
%             "Header B and 'hs' cells", "Header B and 'hd' cells", ... 
%             'FontSize', 16);
% leg.ItemTokenSize = [24, 24];
%     % Grid on
% grid on;
%     % Save figure
% saveas(hdl, './Figures/PowerFoMScatter.emf');
