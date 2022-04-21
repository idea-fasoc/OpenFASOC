// Programmable Synchronizer

module synchronizer(sync_clock, in_data, sync_data, reset);
    parameter SyncDepth=2;
    parameter DataWidth=1;
    input wire [DataWidth-1:0] in_data;
    output wire [DataWidth-1:0] sync_data;
    input wire reset;
    input wire sync_clock;

    genvar i;

    reg [SyncDepth-1:0] sync_reg [DataWidth-1:0];
    generate
        for (i=0; i <DataWidth; i++) begin
            always @(posedge sync_clock) begin
                if (reset) begin
                    sync_reg[i] <= {SyncDepth}*1'b0;
                end else begin
                    sync_reg[i] <= {sync_reg[i][SyncDepth-2:0], in_data[i]};
                end
            end
        end
    endgenerate
endmodule : synchronizer
