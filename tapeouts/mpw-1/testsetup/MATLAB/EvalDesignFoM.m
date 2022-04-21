function [design, FoM, power, res, EnC] = EvalDesignFoM(drange, min_order, inacc_B_arr, inacc_th, FoM_B_arr, power_B_arr, res_B_arr, EnC_B_arr)
% Find the best design based on FoM

design = 1;
FoM_min = 1e6;
for i = 1:length(drange)
    d = drange(i);
    % Only find for those with a reasonable inaccuracy
    if (inacc_B_arr(1, d) < inacc_th)
        [~, sorted_ind] = sort(FoM_B_arr(1, :, d));
        FoM_Nth_min = FoM_B_arr(1, sorted_ind(min_order), d);
        if (FoM_Nth_min < FoM_min) && (FoM_Nth_min > 0)
            FoM_min = FoM_Nth_min;
            design = d;
        end
    end
end

[~, sorted_ind] = sort(FoM_B_arr(1, :, design));
FoM = FoM_B_arr(1, sorted_ind(min_order), design);
power = power_B_arr(1, sorted_ind(min_order), design);
res = res_B_arr(1, sorted_ind(min_order), design);
EnC = EnC_B_arr(1, sorted_ind(min_order), design);

end
