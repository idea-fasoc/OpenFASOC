// Design: DCDC_HUNIT_CONV2to1
// Description: 2:1 Converter PMOS/NMOS switch pair
// Author：Jeongsup Lee
// Updated by: Wanyue Xu
// Last update: 02/08/22

module DCDC_HUNIT_CONV2to1 (
    inout    vhigh,
    inout    vlow,
    inout    y0,
    inout    y1,

    input    clk0,
    input    clk0b,
    input    clk1,
    input    clk1b
);

    DCDC_XSW_PMOS u_DCDC_XSW_PMOS (
        .vIN(vhigh),
        .vOUT0(y0),
        .vOUT1(y1),
        .clk(clk1b),
        .clkb(clk0b)
    );

    DCDC_XSW_NMOS u_DCDC_XSW_NMOS (
        .vIN(vlow),
        .vOUT0(y0),
        .vOUT1(y1),
        .clk(clk0),
        .clkb(clk1)
    );

endmodule