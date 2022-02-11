// Design: DCDC_CONV2TO1
// Description: 2:1 Converter slice
// Author：Jeongsup Lee
// Updated by: Wanyue Xu
// Last update: 02/08/22

module DCDC_CONV2TO1 (
    inout    VDD,
    inout    VSS,
    inout    vhigh,
    inout    vlow,
    inout    vmid,
    inout    y1_top,
    inout    y0_top,
    inout    y1_bot,
    inout    y0_bot,

    input    clk0,
    input    clk0b,
    input    clk1,
    input    clk1b
);

    DCDC_HUNIT_CONV2to1 u_high_DCDC_HUNIT_CONV2to1 (
        .VDD(VDD),
        .VSS(VSS),
        .vhigh(vhigh),
        .vlow(vmid),
        .y0(y0_top),
        .y1(y1_top),

        .clk0(clk0),
        .clk0b(clk0b),
        .clk1(clk1),
        .clk1b(clk1b)
    );

    DCDC_HUNIT_CONV2to1 u_low_DCDC_HUNIT_CONV2to1 (
        .VDD(VDD),
        .VSS(VSS),
        .vhigh(vmid),
        .vlow(vlow),
        .y0(y0_bot),
        .y1(y1_bot),

        .clk0(clk0),
        .clk0b(clk0b),
        .clk1(clk1),
        .clk1b(clk1b)
    );

endmodule