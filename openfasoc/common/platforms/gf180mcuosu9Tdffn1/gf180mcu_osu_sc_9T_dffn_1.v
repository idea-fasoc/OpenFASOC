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
module gf180mcu_osu_sc_9T_dffn_1 (Q, QN, D, CLKN);
	output Q, QN;
	input D, CLKN;
	reg notifier;
	wire delayed_D, delayed_CLKN;

	// Function
	wire int_fwire_IQ, int_fwire_IQN, xcr_0;

	altos_dff_err (xcr_0, delayed_CLKN, delayed_D);
	altos_dff (int_fwire_IQ, notifier, delayed_CLKN, delayed_D, xcr_0);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (QN, int_fwire_IQN);

	// Timing
	specify
		(posedge CLKN => (Q+:D)) = 0;
		(posedge CLKN => (QN-:D)) = 0;
		$setuphold (posedge CLKN, posedge D, 0, 0, notifier,,, delayed_CLKN, delayed_D);
		$setuphold (posedge CLKN, negedge D, 0, 0, notifier,,, delayed_CLKN, delayed_D);
		$width (posedge CLKN &&& D, 0, 0, notifier);
		$width (negedge CLKN &&& D, 0, 0, notifier);
		$width (posedge CLKN &&& ~D, 0, 0, notifier);
		$width (negedge CLKN &&& ~D, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine
