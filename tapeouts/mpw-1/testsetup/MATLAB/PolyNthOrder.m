function [Y] = PolyNthOrder(param, X)
% Nth-Order Polynomial of an input matrix X

order = length(param);
Y = zeros(size(X));
for i = 1:order
    Y = Y + param(i) .* (X.^(i-1));
end

end
