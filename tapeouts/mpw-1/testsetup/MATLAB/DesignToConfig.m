clc; clear all;
% This script generates an excel sheet that maps the design number of a
% sensor to its silicon configurations: header type, std cell type, N_hdr
% and N_inv.

% Initialize Arrays
SensorDesign = zeros(64,1);
HeaderType = strings(64,1);
StdCellType = strings(64,1);
N_hdr = zeros(64,1);
N_inv = zeros(64,1);

for i = 0:63
    SensorDesign(i+1, 1) = i;

    % Determine Header Type
    hdrType = floor(i/32);
    if (hdrType == 0)
        HeaderType(i+1, 1) = "A";
    else
        HeaderType(i+1, 1) = "B";
    end

    % Determine StdCellType
    stdCellType = floor(mod(i, 32)/16);
    if (stdCellType == 0)
        StdCellType(i+1, 1) = "hs";
    else
        StdCellType(i+1, 1) = "hd";
    end

    % Determine N_hdr
    N_hdr(i+1, 1) = 2*floor(mod(i, 16)/4) + 3;

    % Determine N_inv
    N_inv(i+1, 1) = 2*mod(i, 4) + 5;
end

T = table(SensorDesign, HeaderType, StdCellType, N_hdr, N_inv);
filename = "../SensorToConfigMapping.xlsx";
writetable(T, filename, 'Sheet', 'Sheet', 'WriteVariableNames', true);