% Test script for function "look_up"
clearvars;
close all;

% load data in strcuture format
% all nmos data is contained in structure nch
% all pmos data is contained in structure pch
load 180nch.mat;
load 180pch.mat;
device = nch;
L = device.L;

%Plot ID versus VDS
vds = device.VDS;
vgs = 0.4:0.05:0.6;
ID = look_up(device, 'ID', 'VDS', vds, 'VGS', vgs);
figure;
plot(vds, ID)
ylabel('I_D [A]')
xlabel('V_D_S [V]')
grid;

% Plot Vt against L
vt = look_up(device, 'VT', 'VGS', 0.6, 'L', L);
figure;
plot(vt, L)
ylabel('V_t [V]')
xlabel('L [um]')
grid;

% Plot ft against gm_id for different L
gm_id = 5:0.1:20;
ft = look_up(device, 'GM_CGG', 'GM_ID', gm_id, 'L', min(L):0.05:0.3)/2/pi;
figure;
plot(gm_id, ft)
xlabel('g_m/I_D [S/A]')
ylabel('f_T [Hz]')
grid;

%Plot id/w against gm_id for different L
gm_id = 5:0.1:20;
id_w = look_up(device, 'ID_W', 'GM_ID', gm_id, 'L', min(L):0.05:0.3);
figure;
semilogy(gm_id, id_w)
xlabel('g_m/I_D [S/A]')
ylabel('I_D/W [A/m]')

%Plot id/w against gm_id for different VDS (at minimum L)
gm_id = 5:0.1:20;
id_w = look_up(device, 'ID_W', 'GM_ID', gm_id, 'VDS', [0.8 1.0 1.2]);
figure;
semilogy(gm_id, id_w)
xlabel('g_m/I_D [S/A]')
ylabel('I_D/W [A/m]')

%Plot gm/gds against gm_id (at minimum L and default VDS)
gm_id = 5:0.1:20;
gm_gds = look_up(device,'GM_GDS','GM_ID', gm_id);
figure;
semilogy(gm_id, gm_gds)
xlabel('g_m/I_D [S/A]')
ylabel('g_m/g_d_s')

%try invalid syntax
ID = look_up(nch, 'ID', 'GM_ID', 8, 'GM', 0.00345)

%try invalid syntax
wt = look_up(nch, 'CGD', 'GM_ID', 10);
