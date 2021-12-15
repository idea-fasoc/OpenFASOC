ChipNo_list = [11, 12, 13, 14, 15, 16];
temp_list = -40:10:120;
supply_list = [1.8];
TZiK = 273.15; scale = 1;
p1 = 5; % 0C
p2 = 13; % 80C

plim_low = 3; % -20C
plim_high = 15; % 100C

% Re-organize Measured Data
freq_data_array = zeros(length(temp_list), length(supply_list), length(ChipNo_list), 64);
for c=1:length(ChipNo_list)
    for t=1:length(temp_list)
        for s=1:length(supply_list)
            file = ['../MeasResults/ChipNo', num2str(ChipNo_list(c)), '/Meas_ChipNo', num2str(ChipNo_list(c)), '_Vdio3.0Vdd', num2str(supply_list(s)), '_', num2str(temp_list(t)), 'C.csv'];
            dtable = readtable(file, 'PreserveVariableNames', 1);
            for design = 1:64
                freq_data_array(t, s, c, design) = table2array(dtable(design, 'Freq0 (kHz)'));
            end
        end
    end
end

% Fit each node
param_array = zeros(2, length(supply_list), length(ChipNo_list), 64);
T_array = zeros(length(temp_list), length(supply_list), length(ChipNo_list), 64);
T_err_array = zeros(length(temp_list), length(supply_list), length(ChipNo_list), 64);
err_range_array = zeros(4, length(supply_list), length(ChipNo_list), 64);

for c=1:length(ChipNo_list)
    for design = 1:64
        for s = 1:length(supply_list)
            freq_list = freq_data_array(:, s, c, design);
            k = (temp_list(p2)-temp_list(p1)) / (log(freq_list(p2))*(temp_list(p2) + TZiK)*scale - log(freq_list(p1))*(temp_list(p1) + TZiK)*scale);
            b = -k*log(freq_list(p1))*(temp_list(p1) + TZiK)*scale;
            param_array(1, s, c, design) = k; param_array(2, s, c, design) = b;
            
            for t = 1:length(temp_list)
                T_array(t, s, c, design) = (scale * TZiK * k * log(freq_list(t)) + b) / (1 - scale * k * log(freq_list(t)));
                T_err_array(t, s, c, design) = T_array(t, s, c, design) - temp_list(t);
            end
            err_range_array(1, s, c, design) = max(T_err_array(plim_low:plim_high, s, c, design)); % largest positive error
            err_range_array(2, s, c, design) = min(T_err_array(plim_low:plim_high, s, c, design)); % largest negative error
            err_range_array(3, s, c, design) = max(abs(T_err_array(plim_low:plim_high, s, c, design))); % largest absolute error
            err_range_array(4, s, c, design) = sum(abs(T_err_array(plim_low:plim_high, s, c, design)))/(plim_high - plim_low + 1 - 2); % mean absolute error
        end
    end
end

c = 4;
[max_abs_error_lst, design] = min(err_range_array(3, 1, c, :));
fprintf("At 1.8V, Design %d has lowest maximum absolute error of %.4f \n", design, max_abs_error_lst);
[mean_abs_error_lst, design] = min(err_range_array(4, 1, c, :));
fprintf("At 1.8V, Design %d has lowest mean absolute error of %.4f \n", design, mean_abs_error_lst);

%[max_abs_error_lst, design] = min(err_range_array(3, 2, c, :));
%fprintf("At 1.2V, Design %d has lowest maximum absolute error of %.4f \n", design, max_abs_error_lst);
%[mean_abs_error_lst, design] = min(err_range_array(4, 2, c, :));
%fprintf("At 1.2V, Design %d has lowest mean absolute error of %.4f \n", design, mean_abs_error_lst);