function [figout, hdl] = PlotInacc(figin, tlist, inacc_arr, inacc_arr_sec, sigmas_sec, design)
% Plot Inaccuracy and 3-sigma against temp

sigmas = sigmas_sec;
hdl = figure(figin);
[~, Nchip] = size(inacc_arr);
fs = 28;
fs_axis = 20;
fs_legend = 18;
fs_txtbox = 20;

% Plot inaccuracies
for i = 1:Nchip
    hold on;
    p_inacc_sec = plot(tlist, inacc_arr_sec(:, i), '-bo', 'MarkerSize', 12, 'LineWidth', 1);
    hold off;
    hold on;
    p_inacc = plot(tlist, inacc_arr(:, i), '-c', 'MarkerSize', 12, 'LineWidth', 1);
    hold off;
end

% Plot 3-sigma
hold on;
plot(tlist, sigmas(:, 1), '--rs', 'MarkerSize', 12, 'LineWidth', 1);
hold off;
hold on;
psigma = plot(tlist, sigmas(:, 2), '--rs', 'MarkerSize', 12, 'LineWidth', 1);
hold off;

% Axis
xlim([tlist(1)-10, tlist(length(tlist))+10]);
neg = min(min(min(inacc_arr)), min(min(sigmas))); pos = max(max(max(inacc_arr)), max(max(sigmas)));
ylim([min(neg*1.5, -1.5), max(pos*1.5, 1.5)]);
set(gca,'FontSize',fs_axis);

% Labels
xlabel('Temperature (°C)', 'FontSize', fs);
ylabel('Error (°C)', 'FontSize', fs);

% Set figure position and size
set(gcf, 'Position', [0 0 800 400]);

% Legend
leg = legend([p_inacc, p_inacc_sec, psigma], 'w/o SEC', 'w/ SEC', '3\sigma w/ SEC', 'FontSize', fs_legend, 'Box', 'off');
rect = [0.65, 0.62, 0.25, 0.25];
set(leg, 'Position', rect)
leg.ItemTokenSize = [50, 18];

% % Text Box for Min/Max error
% err_neg = min(min(inacc_arr)); err_pos = max(max(inacc_arr));
% sigma_err = [num2str(err_neg, '%.2f'), '/+', num2str(err_pos, '%.2f'), '°C'];
% str = ['Min/Max error w/o SEC: ', 10, sigma_err];
% annotation('textbox', [0.2, 0.75, 0.1, 0.1], 'String', str, 'FitBoxToText', 'on', 'FontSize', 18);

% Text Box for 3sigma error
err_neg = min(min(sigmas)); err_pos = max(max(sigmas));
sigma_err = [num2str(err_neg, '%.2f'), '/+', num2str(err_pos, '%.2f'), '°C'];
str = ['3\sigma error w/ SEC: ', sigma_err];
annotation('textbox', [0.15, 0.75, 0.1, 0.1], 'String', str, 'EdgeColor','none', 'FontSize', fs_txtbox);

% title
sel_design = dec2bin(design - 1, 6);
hdr_list = ['A';'B'];
hdr = hdr_list(bin2dec(sel_design(1))+1, :);
cell_list = ['hs';'hd'];
cell = cell_list(bin2dec(sel_design(2))+1, :);
Nhdr_list = [3, 5, 7, 9];
Nhdr = Nhdr_list(bin2dec(sel_design(3:4))+1);
Ninv_list = [5, 7, 9, 11];
Ninv = Ninv_list(bin2dec(sel_design(5:6))+1);

tlow = tlist(1); thigh = tlist(length(tlist));
fig_title = [num2str(tlow), '°C ~ ', num2str(thigh), '°C, Instance ', ...
            hdr, num2str(Nhdr), '-', cell, '-', num2str(Ninv)];
title(fig_title, 'FontSize', fs);

% Turn on grid
grid on;

figout = figin + 1;
end

