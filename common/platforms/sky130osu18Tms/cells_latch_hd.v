module $_DLATCH_P_(input E, input D, output Q);
    sky130_osu_sc_18T_ms__dlat_1 _TECHMAP_REPLACE_ (
        .D(D),
        .E(E),
        .Q(Q)
        );
endmodule

module $_DLATCH_N_(input E, input D, output Q);
    sky130_osu_sc_18T_ms__dlatn_1 _TECHMAP_REPLACE_ (
        .D(D),
        .E(E),
        .Q(Q)
        );
endmodule
