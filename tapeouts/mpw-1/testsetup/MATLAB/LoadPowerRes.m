% Define chip list and full temp range
clist = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24];
Nchip = length(clist);
temp = 20; % Measured @ 20C
VDD1v8 = 1.8; % V
freq_ref = 32.768; % kHz

% Re-organize Measured Data
power_data_array = zeros(1, Nchip, 64);
tconv_data_array = zeros(2, Nchip, 64);
res_data_array = zeros(2, Nchip, 64);
EnC_data_array = zeros(2, Nchip, 64);
FoM_data_array = zeros(1, Nchip, 64);
    % Parse Power
for c = 1:Nchip
    file = ['../MeasResults/Power', '/Power_ChipNo', num2str(clist(c)), '_Vdio3.0Vdd1.8_', num2str(temp), 'C.csv'];
    dtable = readtable(file, 'PreserveVariableNames', 1);
    for design = 1:64
        power_data_array(1, c, design) = table2array(dtable(design, 'Ivdd1v8 (A)'));
    end
    min_current = min(power_data_array(1, c, :));
    power_data_array(1, c, :) = power_data_array(1, c, :) - min_current;
    power_data_array(1, c, :) = power_data_array(1, c, :) * 1.8 * 1e6; % uW
end
    % Parse Resolution
for c = 1:Nchip
    file = ['../MeasResults/Resolution', '/Res_ChipNo', num2str(clist(c)), '_Vdio3.0Vdd1.8_', num2str(temp), 'C.csv'];
    dtable = readtable(file, 'PreserveVariableNames', 1);
    for design = 1:64
        tconv_data_array(1, c, design) = table2array(dtable(design, 'CTR1'));
        tconv_data_array(2, c, design) = table2array(dtable(design, 'CTR2'));
        res_data_array(1, c, design) = table2array(dtable(design, 'Res1 (kHz)'));
        res_data_array(2, c, design) = table2array(dtable(design, 'Res2 (kHz)'));
    end
    tconv_data_array(1, c, :) = 32 * (2.^tconv_data_array(1, c, :)) / freq_ref; % ms
    tconv_data_array(2, c, :) = 32 * (2.^tconv_data_array(2, c, :)) / freq_ref; % ms
end
    % Calculate Energy-per-Conversion
EnC_data_array(1, :, :) = power_data_array .* tconv_data_array(1, :, :);
EnC_data_array(2, :, :) = power_data_array .* tconv_data_array(2, :, :);
