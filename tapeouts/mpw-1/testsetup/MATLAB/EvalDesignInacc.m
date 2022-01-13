function [design, inacc_sub_arr, inacc_sub_arr_sec, pos_inacc, neg_inacc, sigma, sigma_sec, pos_sigma_inacc, neg_sigma_inacc] = EvalDesignInacc(drange, inacc_arr, inacc_arr_sec, inacc_B_arr, indlist_B_arr, tstart_ind, twin_len)
% Find the best design based on inacc_B given design # range, and evaluate
% its inaccuracies

[~, design] = min(inacc_B_arr(1, drange));
design = drange(design);

inacc_sub_arr = inacc_arr(tstart_ind:(tstart_ind + twin_len), indlist_B_arr(1, :, design), design);
inacc_sub_arr_sec = inacc_arr_sec(tstart_ind:(tstart_ind + twin_len), indlist_B_arr(1, :, design), design);
    % Calculate Max/Min Inaccuracy
pos_inacc = max(max(inacc_sub_arr));
neg_inacc = min(min(inacc_sub_arr));
pos_inacc_sec = max(max(inacc_sub_arr_sec));
neg_inacc_sec = min(min(inacc_sub_arr_sec));
pos_inacc = [pos_inacc; pos_inacc_sec];
neg_inacc = [neg_inacc; neg_inacc_sec];
    % Calculate 3-sigma Inaccuracy
sigma = [3*std(inacc_sub_arr, 1, 2), -3*std(inacc_sub_arr, 1, 2)] + mean(inacc_sub_arr, 2);
pos_sigma_inacc = max(max(sigma));
neg_sigma_inacc = min(min(sigma));
sigma_sec = [3*std(inacc_sub_arr_sec, 1, 2), -3*std(inacc_sub_arr_sec, 1, 2)] + mean(inacc_sub_arr_sec, 2);
pos_sigma_inacc_sec = max(max(sigma_sec));
neg_sigma_inacc_sec = min(min(sigma_sec));
pos_sigma_inacc = [pos_sigma_inacc; pos_sigma_inacc_sec];
neg_sigma_inacc = [neg_sigma_inacc; neg_sigma_inacc_sec];

end

