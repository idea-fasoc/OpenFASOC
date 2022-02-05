module DCDC_HUNIT_CONV2to1 (
    inout    VDD,
    inout    VSS,
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
        .VDD(VDD),
        .VSS(VSS),
        .vIN(vhigh),
        .vOUT0(y0),
        .vOUT1(y1),
        .clk(clk1b),
        .clkb(clk0b)
    );

    DCDC_XSW_NMOS u_DCDC_XSW_NMOS (
        .VDD(VDD),
        .VSS(VSS),
        .vIN(vlow),
        .vOUT0(y0),
        .vOUT1(y1),
        .clk(clk1),
        .clkb(clk0)
    );

endmodule