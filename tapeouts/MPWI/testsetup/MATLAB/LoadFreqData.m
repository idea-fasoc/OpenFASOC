% Define chip list and full temp range
clist = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24];
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