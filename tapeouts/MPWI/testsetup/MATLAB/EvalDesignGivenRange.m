function [params, inacc_arr, params_sec, inacc_arr_sec, Nc_A, indlist_A, inacc_B, indlist_B] = ...
    EvalDesignGivenRange(freq_arr, tlist, tstart_ind, twin_len, pcalib, inacc_th, Nc_B, order_sec)
% This function evaluate a single temperature design/instance's inaccuracy
% across multiple chips under a given temperature range. 
% It returns fitted parameter pairs for each chip,
% inaccuracies across chips and temperatures, and
% metric A: the number of chips with inaccuracy below a threshold and 
% their indices, and
% metric B: the minimal-possible max-inaccuracy given the number of good 
% chips we need, also return the their indices.

% metric A is about the best reliability or least variation
% while metric B is about the best inaccuracy 

% Input: 
%   freq_arr - Ntemp x Nchip
%   tlist - Ntemp x 1
%   tstart_ind - 1x1, index of starting temperature
%   twin_len - 1x1, length of temperature range, in 10C-step indices
%   pcalib - 1x1, calibration point index w.r.t. tstart_ind, e.g., 2 means
%       20C above tlow and under thigh
%   inacc_th - 1x1, threshold of inaccuracy
%   Nc_B - 1x1, number of good chips we need

% Output:
%   params - 2 x Nchip
%   inacc_arr - Ntemp x Nchip
%   Nc_A - 1x1, the number of chips with inaccuracy below a threshold
%   indlist_A - 2 x Nchip, the chip indices for metric A
%   inacc_B - 1x1, the minimal-possible max-inaccuracy given Nc_B, 
%   indlist_B - 2 x Nc_B, the chip indices for metric B 

TZiK = 273.15; scale = 1;

[Ntemp, Nchip] = size(freq_arr);
params = zeros(2, Nchip);
T_array = zeros(Ntemp, Nchip);
inacc_arr = zeros(Ntemp, Nchip);
metric_arr = zeros(3, Nchip);

% Fit the design for each chip
p1 = tstart_ind + pcalib;
p2 = tstart_ind + twin_len - pcalib;
for c = 1:Nchip
    % Fit the curve
    flist = freq_arr(:, c);
    k = (tlist(p2) - tlist(p1)) / (log(flist(p2)) * (tlist(p2) + TZiK) * scale - log(flist(p1)) * (tlist(p1) + TZiK) * scale);
    b = tlist(p1) - k * log(flist(p1)) * (tlist(p1) + TZiK) * scale;
    params(1, c) = k; params(2, c) = b;
    
    % Calculate estimated temperatures and inaccuracies
    for t = 1:Ntemp
        T_array(t, c) = (scale * TZiK * k * log(flist(t)) + b) / (1 - scale * k * log(flist(t)));
        inacc_arr(t, c) = T_array(t, c) - tlist(t);
    end
    
    % Calculate max inaccuracies in the given range
    if ( sum(isnan(inacc_arr(tstart_ind:(tstart_ind + twin_len), c))) == 0 )
        metric_arr(1, c) = max(inacc_arr(tstart_ind:(tstart_ind + twin_len), c)); % largest positive error
        metric_arr(2, c) = min(inacc_arr(tstart_ind:(tstart_ind + twin_len), c)); % largest negative error
        metric_arr(3, c) = max(abs(metric_arr(1,c)), abs(metric_arr(2,c))); % largest absolute error
    else
        metric_arr(:, c) = [NaN; NaN; NaN];
    end
end

% Metric A
Nc_A = 0; indlist_A = zeros(2, Nchip);
for c = 1:Nchip
    if (metric_arr(3, c) <= inacc_th)
        Nc_A = Nc_A + 1;
        indlist_A(:, Nc_A) = [c; metric_arr(3,c)];
    end
end

% Metric B
[sorted_inacc, sorted_ind] = sort(metric_arr(3, :));
inacc_B = sorted_inacc(Nc_B);
indlist_B = [sorted_ind(1:Nc_B); sorted_inacc(1:Nc_B)];

% Systematic Error Correction
if (inacc_B < 20) % Only do SEC when inaccuracy is not too bad
        % get the estimated temp of best Nc_B chips
    T_est = T_array(tstart_ind:(tstart_ind + twin_len), indlist_B(1, :));
        % define Nth-order polynomial correction: T_sec = pN * T_est^N + ... + p1 * T_est + p0
        % param = [p0, p1, ... pN]
    T_left = tlist(tstart_ind:(tstart_ind + twin_len))';
    T_sec  = @(param, T) PolyNthOrder(param, T);
    T_right = @(param, T) mean(T_sec(param, T), 2);
        % Do Optimization
    param0 = zeros(1, order_sec + 1); param0(2) = 1;
    opts = optimoptions('lsqcurvefit', 'Display','off');
    [params_sec, ~, ~, ~, ~] = lsqcurvefit(T_right, param0, T_est, T_left, [], [], opts);        
        % Calculate Corrected Temperature estimation and errors
    T_array_sec = T_sec(params_sec, T_array);
    inacc_arr_sec = T_array_sec - tlist';
else
    params_sec = zeros(1, order_sec+1); params_sec(2) = 1;
    inacc_arr_sec = inacc_arr;
end

end
