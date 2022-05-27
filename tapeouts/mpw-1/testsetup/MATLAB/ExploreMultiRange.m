clc; clear all;

% Load Tested Frequency Data
LoadFreqData;

% Explore best designs of low, mid and high temperature ranges
    % How good we want the performance to be
inacc_th    = 2.5;
Nc_B        = 8;
    % Polynomial SEC Order
order_sec = 3;
    % Explore
fig = 1;
ExploreLowRange;
ExploreMidRange;
ExploreHighRange;
