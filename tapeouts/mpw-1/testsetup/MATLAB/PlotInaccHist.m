function [figout, hdl] = PlotInaccHist(figin, inacc_hist, inacc_hist_sec, err_type)
% Plot histogram of inaccuracies for 16 groups

%groups = {'hdrA3'; 'hdrA5'; 'hdrA7' ; 'hdrA9'; 'hdrA3'; 'hdrA5'; 'hdrA7' ; 'hdrA9';...
%          'hdrB3'; 'hdrB5'; 'hdrB7' ; 'hdrB9';'hdrB3'; 'hdrB5'; 'hdrB7' ; 'hdrB9'};

groups = {'A3-hs'; 'A5-hs'; 'A7-hs'; 'A9-hs'; 'A3-hd'; 'A5-hd'; 'A7-hd' ; 'A9-hd';...
          'B3-hs'; 'B5-hs'; 'B7-hs'; 'B9-hs'; 'B3-hd'; 'B5-hd'; 'B7-hd' ; 'B9-hd'};

hdl = figure(figin);

%color = {'red', '#EDB120', 'blue', '#4DBEEE'};
color = {'red', '#EDB120', 'red', '#EDB120'};

% Plot Bars
    % hs instances with header A
b1_pos = bar(1:4, [inacc_hist(1, 1:4); inacc_hist_sec(1, 1:4)]); hold on;
b1_neg = bar(1:4, [inacc_hist(2, 1:4); inacc_hist_sec(2, 1:4)]); hold on;
b1_pos(1,1).FaceColor = cell2mat(color(1)); b1_pos(1,1).EdgeColor = cell2mat(color(1));
b1_pos(1,2).FaceColor = cell2mat(color(2)); b1_pos(1,2).EdgeColor = cell2mat(color(2));
b1_neg(1,1).FaceColor = cell2mat(color(1)); b1_neg(1,1).EdgeColor = cell2mat(color(1));
b1_neg(1,2).FaceColor = cell2mat(color(2)); b1_neg(1,2).EdgeColor = cell2mat(color(2));
    % hd instances with header A
b2_pos = bar(5:8, [inacc_hist(1, 5:8); inacc_hist_sec(1, 5:8)]); hold on;
b2_neg = bar(5:8, [inacc_hist(2, 5:8); inacc_hist_sec(2, 5:8)]); hold on;
b2_pos(1,1).FaceColor = cell2mat(color(3)); b2_pos(1,1).EdgeColor = cell2mat(color(3));
b2_pos(1,2).FaceColor = cell2mat(color(4)); b2_pos(1,2).EdgeColor = cell2mat(color(4));
b2_neg(1,1).FaceColor = cell2mat(color(3)); b2_neg(1,1).EdgeColor = cell2mat(color(3));
b2_neg(1,2).FaceColor = cell2mat(color(4)); b2_neg(1,2).EdgeColor = cell2mat(color(4));
    % hs instances with header B
b3_pos = bar(9:12, [inacc_hist(1, 9:12); inacc_hist_sec(1, 9:12)]); hold on;
b3_neg = bar(9:12, [inacc_hist(2, 9:12); inacc_hist_sec(2, 9:12)]); hold on;
b3_pos(1,1).FaceColor = cell2mat(color(1)); b3_pos(1,1).EdgeColor = cell2mat(color(1));
b3_pos(1,2).FaceColor = cell2mat(color(2)); b3_pos(1,2).EdgeColor = cell2mat(color(2));
b3_neg(1,1).FaceColor = cell2mat(color(1)); b3_neg(1,1).EdgeColor = cell2mat(color(1));
b3_neg(1,2).FaceColor = cell2mat(color(2)); b3_neg(1,2).EdgeColor = cell2mat(color(2));
    % hd instances with header B
b4_pos = bar(13:16, [inacc_hist(1, 13:16); inacc_hist_sec(1, 13:16)]); hold on;
b4_neg = bar(13:16, [inacc_hist(2, 13:16); inacc_hist_sec(2, 13:16)]); hold on;
b4_pos(1,1).FaceColor = cell2mat(color(3)); b4_pos(1,1).EdgeColor = cell2mat(color(3));
b4_pos(1,2).FaceColor = cell2mat(color(4)); b4_pos(1,2).EdgeColor = cell2mat(color(4));
b4_neg(1,1).FaceColor = cell2mat(color(3)); b4_neg(1,1).EdgeColor = cell2mat(color(3));
b4_neg(1,2).FaceColor = cell2mat(color(4)); b4_neg(1,2).EdgeColor = cell2mat(color(4));
    
    % Plot a black baseline
plot(0:17, zeros(1, 18), '-k', 'LineWidth', 1);
xlim([0.5, 16.5]);
ylim([-2 2.5]); yticks(-2:0.5:2.5);
    
    % X-axis labels
set(gca, 'XTick', 1:16, 'XTickLabel', groups, 'FontSize', 16);
set(gcf, 'Position', [0 0 2000 400]);
grid on;
    % Y-axis label
ylabel('Error (°C)', 'FontSize', 24);

    % Legends
% legend([b1_pos(1, 1), b1_pos(1, 2), b2_pos(1, 1), b2_pos(1, 2)], ...
%     'High-speed (hs) intances w/o SEC', 'High-speed (hs) intances w/ SEC', ...
%     'High-density (hd) intances w/o SEC', 'High-density (hd) intances w/ SEC', ...
%     'FontSize', 18, 'Location', 'Northwest', 'Box', 'off');
legend([b1_pos(1, 1), b1_pos(1, 2)], ...
    'w/o SEC', 'w/ SEC', ...
    'FontSize', 18, 'Location', 'Northwest', 'Box', 'off');     

    % title
if err_type == 0 % Min/Max
    err_type = 'Min/Max';
else
    err_type = '3\sigma';
end
title(['20°C ~ 120°C ', err_type, ' Errors of Representative Instances from Each Group'], 'FontSize', 24);
    
figout = figin + 1;
end

