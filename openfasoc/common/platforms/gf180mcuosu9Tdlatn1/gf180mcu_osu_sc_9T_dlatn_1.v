// Copyright 2022 Google LLC
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_dlatn_1 (Q, D, CLKN);
	output Q;
	input D, CLKN;
	reg notifier;
	wire delayed_D, delayed_CLKN;

	// Function
	wire int_fwire_IQ;

	altos_latch (int_fwire_IQ, notifier, delayed_CLKN, delayed_D);
	buf (Q, int_fwire_IQ);

	// Timing
	specify
		(D => Q) = 0;
		(posedge CLKN => (Q+:D)) = 0;
		$setuphold (negedge CLKN, posedge D, 0, 0, notifier,,, delayed_CLKN, delayed_D);
		$setuphold (negedge CLKN, negedge D, 0, 0, notifier,,, delayed_CLKN, delayed_D);
		$width (posedge CLKN &&& D, 0, 0, notifier);
		$width (posedge CLKN &&& ~D, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine
