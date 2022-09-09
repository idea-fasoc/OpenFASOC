% Rev. 20190422, Boris Murmann
% The function "look_upVGS" is a companion function to "look_up." It finds
% the transistor VGS for a given inversion level (GM_ID) or current density
% (ID/W)and given terminal voltages. The function interpolates when the
% requested points lie off the simulation grid
%
% There are two basic usage scenarios:
% (1) Lookup VGS with known voltage at the source terminal
% (2) Lookup VGS with unknown source voltage, e.g. when the source of the
% transistor is the tail node of a differential pair
%
% At most one of the input arguments can be a vector; the otehr must be
% scalars. The output is a column vector.
%
% In usage mode (1), the inputs to the function are GM_ID (or ID/W), L, 
% VDS and VSB. Basic examples:
%
% VGS = look_upVGS(nch, 'GM_ID', 10, 'VDS', 0.6, 'VSB', 0.1, 'L', 0.1)
% VGS = look_upVGS(nch, 'GM_ID', 10:15, 'VDS', 0.6, 'VSB', 0.1, 'L', 0.1)
% VGS = look_upVGS(nch, 'ID_W', 1e-4, 'VDS', 0.6, 'VSB', 0.1, 'L', 0.1)
% VGS = look_upVGS(nch, 'ID_W', 1e-4, 'VDS', 0.6, 'VSB', 0.1, 'L', [0.1:0.1:0.5])
%
% When VSB, VDS or L are not specified, their default values are assumed:
%
% VSB = 0;
% L = min(data.L); (minimum length)
% VDS = max(data.VDS)/2; (VDD/2)
%
% In usage mode (2), VDB and VGB must be supplied to the function, for
% example:
%
% VGS = lookup_VGS(nch, 'GM_ID', 10, 'VDB', 0.6, 'VGB', 1, 'L', 0.1)
% VGS = lookup_VGS(nch, 'ID_W', 1e-4, 'VDB', 0.6, 'VGB', 1, 'L', 0.1)
%
% The default interpolation method for the final 1D interpolation is 
% "pchip". It can be set to a different method by passing e.g. 'METHOD',
% 'linear' to the function. All other multidimensional interpolation
% operations use 'linear' (fixed), since any other method requires
% continuous derivates; this is rarely satisfiead across all dimensions,
% even with the best device models.
%
function output = look_upVGS(data, varargin)

% default values for parameters
defaultL = min(data.L);
defaultVDS = max(data.VDS)/2;
defaultVDB = NaN;
defaultVGB = NaN;
defaultGM_ID = NaN;
defaultID_W = NaN;
defaultVSB  = 0;
defaultMETHOD  = 'pchip';

% parse arguments
p = inputParser; 
p.addParamValue('L', defaultL);
p.addParamValue('VGB', defaultVGB);
p.addParamValue('GM_ID', defaultGM_ID);
p.addParamValue('ID_W', defaultID_W);
p.addParamValue('VDS', defaultVDS);
p.addParamValue('VDB', defaultVDB);
p.addParamValue('VSB', defaultVSB);
p.addParamValue('METHOD', defaultMETHOD);
p.KeepUnmatched = false;
p.parse(varargin{:});
par = p.Results;

% determine usage mode
if(isnan(par.VGB(1)) && isnan(par.VDB(1)) )
    mode = 1;
else if (~isnan(par.VGB(1)) && ~isnan(par.VDB(1)) )
    mode = 2;
else
    disp('Invalid syntax or usage mode! Please type "help look_upVGS".')
    output = [];
    return;       
    end
end

% Check whether GM_ID or ID_W was passed to function
if ~isnan(par.ID_W(1))
    ratio_string = 'ID_W';
    ratio_data = par.ID_W;
else if ~isnan(par.GM_ID(1))
    ratio_string = 'GM_ID';
    ratio_data = par.GM_ID;
    else
    disp('look_upVGS: Invalid syntax or usage mode! Please type "help lookupVGS".')
    output = [];
    return;      
    end
end

if  mode == 1
    VGS = data.VGS;
    ratio = look_up(data, ratio_string, 'VGS', VGS, 'VDS', par.VDS, 'VSB', par.VSB, 'L', par.L);

else % mode == 2
    step   = data.VGS(1)-data.VGS(2);
    VSB    = (max(data.VSB):step:min(data.VSB))';
    VGS    = par.VGB - VSB;
	VDS    = par.VDB - VSB;
	ratio  = look_up(data, ratio_string, 'VGS', VGS, 'VDS', VDS, 'VSB', VSB, 'L', ones(length(VSB),1)*par.L);
    idx    = isfinite(ratio);
    ratio  = ratio(idx);
    VGS    = VGS(idx);
end    
    
% Permutation needed if L is passed as a vector
if length(par.L) > 1
    ratio = permute(ratio, [2, 1]);
end

% Interpolation loop
s = size(ratio);
output = NaN(s(2), length(ratio_data));
for j = 1:s(2)
    ratio_range = ratio(:,j);
    VGS_range = VGS;
    % If gm/ID, find maximum and limit search range to VGS values to the right
    if strcmp(ratio_string,'GM_ID')
        [m, idx] = max(ratio_range);
        VGS_range = VGS_range(idx:end);
        ratio_range = ratio_range(idx:end);
        if max(ratio_data) > m
            disp('look_upVGS: GM_ID input larger than maximum!')
        end
    end
    output(j,:) = interp1(ratio_range, VGS_range, ratio_data, par.METHOD, NaN);
    output = output(:);
end
return
