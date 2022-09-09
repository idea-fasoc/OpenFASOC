% Rev. 20190422, Boris Murmann
% The function "look_up" extracts a desired subset from the 4-dimensional simulation data
% The function interpolates when the requested points lie off the simulation grid
%
% There are three usage modes:
% (1) Simple lookup of parameters at some given (L, VGS, VDS, VSB)
% (2) Lookup of arbitrary ratios of parameters, e.g. GM_ID, GM_CGG at given (L, VGS, VDS, VSB)
% (3) Cross-lookup of one ratio against another, e.g. GM_CGG for some GM_ID
%
% In usage modes (1) and (2) the input parameters (L, VGS, VDS, VSB) can be 
% listed in any order and default to the following values when not specified:
%
% L = min(data.L); (minimum length used in simulation)
% VGS = data.VGS; (VGS vector used during simulation)
% VDS = max(data.VDS)/2; (VDD/2)
% VSB = 0;
%
% Note: To find the device width used in the underlying data set being read,
% you can type data.W (example: nch.W) at the Matlab command line. This of
% course assumes that the data file was properly set up/configured and 
% populated with this info.
%
% In usage mode (3), the output and input parameter ratios must be specified first.
% The example below outputs GM_CGG at GM_ID between 5 and 20 S/A
%
% wt = look_up(nch, 'GM_CGG', 'GM_ID', 5:0.1:20);
%
% The cross-lookup between the two ratios is based on evaluating both
% parameters across the given range of data.VGS, and finding the
% intersects at the desired points. If GM_ID is passed as the third
% argument, special care is taken to look only "to the right" of the
% maximum gm/ID value in the gm/ID vs. VGS plane. Similar functionality is
% implemented for GM_CGG and GM_CGS (lookup limited to the left of maximum).
%
% The default interpolation method in mode 3 for the final 1-D interpolation
% is "pchip". It can be set to a different method by passing e.g. 'METHOD',
% 'linear' to the function. All other multidimensional interpolation
% operations use 'linear' (fixed), since any other method requires
% continuous derivates; this is rarely satisfiead across all dimensions,
% even with the best device models.
%
% In the previous example, L, VDS and VS are assumed to be at the default values, 
% but they can also be specified explicitly, for example:
%
% wt = look_up(nch, 'GM_CGG', 'GM_ID', 5:0.1:20, 'VDS', 0.7);
%
% When more than one parameter is passed to the function as a vector, the output
% becomes multidimensional. This behavior is inherited from the Matlab function 
% “interpn”, which is at the core of the lookup function. The following example
% produces an 11x11 matrix as the output:
%
% look_up(nch,'ID', 'VGS', 0:0.1:1, 'VDS', 0:0.1:1)
%
% The dimensions of the output array are ordered such that the largest dimension
% comes first. For example, one dimensional output data is an (n x 1) column vector.
% For two dimensions, the output is (m x n) and m > n.
%
% As another variant of the above example, if we want to access only the
% values of ID for which VGS=VDS (i.e. given that there is an element to element
% correspondence between the two input vectors), the vector of interest is simply
% the diagonal of the full matrix:
%
% diag(look_up(nch,'ID', 'VGS', 0:0.1:1, 'VDS', 0:0.1:1))

function output = look_up(data, outvar, varargin)

% default values for parameters
defaultL = min(data.L);
defaultVGS = data.VGS;
defaultVDS = max(data.VDS)/2;
defaultVSB  = 0;
defaultMETHOD  = 'pchip';
defaultWARNING  = 'on';

% parse arguments to determine range of output evaluation
p = inputParser; 
p.addParamValue('L', defaultL);
p.addParamValue('VGS', defaultVGS);
p.addParamValue('VDS', defaultVDS);
p.addParamValue('VSB', defaultVSB);
p.addParamValue('METHOD', defaultMETHOD);
p.addParamValue('WARNING', defaultWARNING);
p.KeepUnmatched = true;
p.parse(varargin{:});
par = p.Results;

% check if desired output is a ratio of two parameters
out_ratio = ~isempty(strfind(outvar, '_'));
% check if first variable argument is a ratio of two parameters
if nargin > 2
    var_ratio = ~isempty(strfind(varargin{1}, '_'));
else
    var_ratio = 0;
end

% determine usage mode
if(out_ratio && var_ratio) mode = 3;
else if (out_ratio && ~var_ratio) mode = 2;
    else if (~out_ratio && ~var_ratio) mode = 1;
        else
            disp('Invalid syntax or usage mode! Please type "help look_up".')
            output = [];
            return;       
        end
    end
end

% output is a ratio in modes 2 and 3
if mode == 2 || mode == 3
    underscore = strfind(outvar, '_');
    numerator = outvar(1:underscore-1);
    denominator = outvar(underscore+1:end);
    ydata = eval(strcat('data.', numerator))./eval(strcat('data.', denominator));
else
% simple output in mode 1
    ydata = eval(strcat('data.', outvar));
end

% input is a ratio in mode 3
if mode == 3
    firstarg = varargin{1};
    underscore = strfind(firstarg, '_');
    numerator = firstarg(1:underscore-1);
    denominator = firstarg(underscore+1:end);
    xdata = eval(strcat('data.', numerator))./eval(strcat('data.', denominator));
    xdesired = varargin{2};
       
    % assemble x and y data, then find y values at desired x
    x = interpn(data.L, data.VGS, data.VDS, data.VSB, xdata, ... 
                        par.L, par.VGS, par.VDS, par.VSB);
    y = interpn(data.L, data.VGS, data.VDS, data.VSB, ydata, ... 
                        par.L, par.VGS, par.VDS, par.VSB);
            
    % permute so that VGS dimension always comes first
    x = squeeze(permute(x, [2 1 3 4]));
    y = squeeze(permute(y, [2 1 3 4]));                

    dim = size(x);
    output = zeros(dim(2), length(xdesired));

    for i = 1:dim(2)
        for j = 1:length(xdesired)
            [m, idx] = max(x(:, i));
            if max( xdesired(j)) > m && strcmp(par.WARNING, 'on')
                s = sprintf('look_up warning: %s_%s input larger than maximum! (output is NaN)', numerator, denominator);
                disp(s);
            end
            % If gm/ID is the x value, find maximum and limit search range to VGS values to the RIGHT
            if strcmp(numerator,'GM') && strcmp(denominator,'ID')
                x_right = x(idx:end, i);
                y_right = y(idx:end, i);
                output(i, j) = interp1(x_right, y_right, xdesired(j), par.METHOD, NaN);
                % If gm/Cgg of gm/Cgs is the x value, find maximum and limit search range to VGS values to the LEFT
            elseif strcmp(numerator,'GM') && (strcmp(denominator,'CGG') || strcmp(denominator,'CGG'))
                x_left = x(1:idx, i);
                y_left = y(1:idx, i);
                output(i, j) = interp1(x_left, y_left, xdesired(j), par.METHOD, NaN);
            else
                crossings = length(find(diff(sign(x(:, i) - xdesired(j)+eps))));
                if crossings > 1
                    output = [];
                    beep;
                    disp('*** look_up: Error! There are multiple curve intersections.');
                    disp('*** Try to reduce the search range by specifying the VGS vector explicitly.');
                    disp('*** Example: look_up(nch, ''ID_W'', ''GM_GDS'', gm_gds, ''VGS'', nch.VGS(10:end))');
                    disp(' ')
                    figure(1000)
                    plot(1:length(x(:,i)), x(:,i), '-x', 1:length(x(:,i)), ones(1, length(x(:,i)))*xdesired(j));
                    return
                end    
                output(i, j) = interp1(x(:, i), y(:, i), xdesired(j), par.METHOD, NaN);
            end    
        end
    end
    
else
    % simple interpolation in modes 1 and 2
    if length(data.VSB) > 1
    output = squeeze(interpn(data.L, data.VGS, data.VDS, data.VSB, ydata, ... 
                        par.L, par.VGS, par.VDS, par.VSB));
    else
    output = squeeze(interpn(data.L, data.VGS, data.VDS, ydata, ... 
                        par.L, par.VGS, par.VDS));
    end                
end

% Force column vector if the output is one dimensional
if length(size(output))==2 && min(size(output))==1
    output = output(:);
end
                   
return
