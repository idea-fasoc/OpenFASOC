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
module gf180mcu_osu_sc_9T_mux2_1 (Y, A, B, Sel);
	output Y;
	input A, B, Sel;

	// Function
	wire int_fwire_0, int_fwire_1, Sel__bar;

	and (int_fwire_0, B, Sel);
	not (Sel__bar, Sel);
	and (int_fwire_1, A, Sel__bar);
	or (Y, int_fwire_1, int_fwire_0);

	// Timing
	specify
		(A => Y) = 0;
		(B => Y) = 0;
		if ((~A & B))
			(Sel => Y) = 0;
		if ((A & ~B))
			(Sel => Y) = 0;
	endspecify
endmodule
`endcelldefine
