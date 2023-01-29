import ltspice
import statistics
import matplotlib.pyplot as plt
import numpy as np
import os

cap_list = ["1p", "5p"]
cap_len = len(cap_list)
fig1, axes1 = plt.subplots(len(cap_list), sharex=True, sharey=True)
fig2, axes2 = plt.subplots(len(cap_list))
fig3, axes3 = plt.subplots(len(cap_list))
fig4, axes4 = plt.subplots(len(cap_list))
fig5, axes5 = plt.subplots(len(cap_list))
fig6, axes6 = plt.subplots(3)
for i in range(cap_len):
    l = ltspice.Ltspice(cap_list[i] + "_" + "cap_output.raw")
    l.parse()
    # get data
    VREG = l.get_data("v(vreg)")
    VREF = l.get_data("v(vref)")
    cmp_out = l.get_data("v(cmp_out)")
    clk = l.get_data("v(clk)")
    ctrl0 = l.get_data("v(ctrl_out[0])")
    ctrl1 = l.get_data("v(ctrl_out[1])")
    ctrl2 = l.get_data("v(ctrl_out[2])")
    ctrl3 = l.get_data("v(ctrl_out[3])")
    ctrl4 = l.get_data("v(ctrl_out[4])")
    ctrl5 = l.get_data("v(ctrl_out[5])")
    ctrl6 = l.get_data("v(ctrl_out[6])")
    ctrl7 = l.get_data("v(ctrl_out[7])")
    ctrl8 = l.get_data("v(ctrl_out[8])")
    time = l.get_time()

    VREG_list = VREG.tolist()  # converts numpy array to list
    VREF_list = VREF.tolist()
    time_list = time.tolist()

    VREG_ripple_list = VREG_list[-9:]
    VREF_ripple_list = VREF_list[-9:]
    time_ripple_list = time_list[-9:]
    VREG_min = min(VREG_ripple_list)
    VREG_max = max(VREG_ripple_list)
    VREG_ripple = VREG_max - VREG_min

    axes1[i].set_title("VREG vs Time" + " " + str(cap_list[i]))
    axes1[i].ticklabel_format(style="sci", axis="x", scilimits=(-6, -6))
    axes1[i].plot(time_list, VREG_list, label="VREG")
    axes1[i].plot(time_list, VREF_list, label="VREF")
    axes1[i].legend(loc="lower right")
    fig1.text(0.5, 0.04, "Time [us]", ha="center")
    fig1.text(0.04, 0.5, "Vreg and Vref [V]", va="center", rotation="vertical")

    num_of_switches = (
        ctrl0
        + 2 * ctrl1
        + 4 * ctrl2
        + 8 * ctrl3
        + 16 * ctrl4
        + 32 * ctrl5
        + 64 * ctrl6
        + 128 * ctrl7
        + 256 * ctrl8
    ) / 3.3
    num_of_switches_plot = num_of_switches[50:]
    axes6[i].set_title("Number of Switches vs Time" + " " + str(cap_list[i]))
    axes6[i].ticklabel_format(style="sci", axis="x", scilimits=(-6, -6))
    axes6[i].plot(time_list[50:], num_of_switches_plot, label="VREG")
    axes6[i].legend(loc="lower right")
    fig6.text(0.5, 0.04, "Time [us]", ha="center")
    fig6.text(0.04, 0.5, "Number of Switches ", va="center", rotation="vertical")

    axes2[i].set_title("V_difference vs Time" + " " + str(cap_list[i]))
    axes2[i].ticklabel_format(style="sci", axis="x", scilimits=(-6, -6))
    axes2[i].plot(time, VREF - VREG, label="VREF-VREG")
    axes2[i].legend(loc="upper right")
    fig2.text(0.5, 0.04, "Time [us]", ha="center")
    fig2.text(0.04, 0.5, "Vref-Vreg [V]", va="center", rotation="vertical")

    axes3[i].set_title("V_Ripple vs Time " + " " + str(cap_list[i]))
    axes3[i].ticklabel_format(style="sci", axis="x", scilimits=(-6, -6))
    axes3[i].plot(time_list[-10:], VREG_list[-10:], label="VREF-VREG")
    axes3[i].legend(loc="upper right")
    fig3.text(0.5, 0.04, "Time [us]", ha="center")
    fig3.text(0.04, 0.5, "Vref-Vreg [V] (Zoomed)", va="center", rotation="vertical")

    axes4[i].set_title("Comp_out vs Time" + " " + str(cap_list[i]))
    axes4[i].ticklabel_format(style="sci", axis="x", scilimits=(-6, -6))
    axes4[i].plot(time, cmp_out, label="cmp_out")
    axes4[i].legend(loc="upper right")
    fig4.text(0.5, 0.04, "Time [us]", ha="center")
    fig4.text(0.04, 0.5, "Cmp_out [V]", va="center", rotation="vertical")

    VREG_ripple_data = []  # creates and empty list
    VREG_ripple_data.append(VREG_ripple)
    print("Ripple at output for" + str(cap_list[i]) + " is" + str(VREG_ripple_data))

    VREG_sample = VREG[100:]
    test = np.where(VREG_sample >= 1.8)
    test_first = test[0]
    VREG_sample_dev = VREG[100 + test_first[0] :]
    time_sample_dev = time[100 + test_first[0] :]
    VREG_sample_dev_max = max(VREG_sample_dev)
    VREG_sample_dev_min = min(VREG_sample_dev)
    VREG_dev = VREG_sample_dev_max - VREG_sample_dev_min
    print(
        "Time to reach stable VREG for "
        + str(cap_list[i])
        + " is "
        + str(time_sample_dev[0])
    )
    print("VREG oscillation at output for " + str(cap_list[i]) + " is " + str(VREG_dev))
    print(
        "VREG max oscillation at output for "
        + str(cap_list[i])
        + " is "
        + str(VREG_sample_dev_max)
    )
    print(
        "VREG min oscillation at output for "
        + str(cap_list[i])
        + " is "
        + str(VREG_sample_dev_min)
    )
    axes5[i].set_title("VREG_dev_test vs Time" + " " + str(cap_list[i]))
    axes5[i].ticklabel_format(style="sci", axis="x", scilimits=(-6, -6))
    axes5[i].plot(time_sample_dev, VREG_sample_dev, label="VREG_dev")
    axes5[i].legend(loc="upper right")
    fig5.text(0.5, 0.04, "Time [us]", ha="center")
    fig5.text(0.04, 0.5, "VREG_dev_test [V]", va="center", rotation="vertical")


fig1.savefig("VREG output")
fig2.savefig("VREG-VREF")
fig3.savefig("VREG ripple")
fig4.savefig("Cmp_out")
fig5.savefig("VREG oscillation")
fig6.savefig("Number of Switches")
