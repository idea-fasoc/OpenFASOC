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
module gf180mcu_osu_sc_9T_addf_1 (CO, S, A, B, CI);
	output CO, S;
	input A, B, CI;

	// Function
	wire A__bar, B__bar, CI__bar;
	wire int_fwire_0, int_fwire_1, int_fwire_2;
	wire int_fwire_3, int_fwire_4, int_fwire_5;
	wire int_fwire_6;

	and (int_fwire_0, B, CI);
	and (int_fwire_1, A, CI);
	and (int_fwire_2, A, B);
	or (CO, int_fwire_2, int_fwire_1, int_fwire_0);
	not (B__bar, B);
	not (A__bar, A);
	and (int_fwire_3, A__bar, B__bar, CI);
	not (CI__bar, CI);
	and (int_fwire_4, A__bar, B, CI__bar);
	and (int_fwire_5, A, B__bar, CI__bar);
	and (int_fwire_6, A, B, CI);
	or (S, int_fwire_6, int_fwire_5, int_fwire_4, int_fwire_3);

	// Timing
	specify
		if ((B & ~CI))
			(A => CO) = 0;
		if ((~B & CI))
			(A => CO) = 0;
		ifnone (A => CO) = 0;
		if ((A & ~CI))
			(B => CO) = 0;
		if ((~A & CI))
			(B => CO) = 0;
		ifnone (B => CO) = 0;
		if ((A & ~B))
			(CI => CO) = 0;
		if ((~A & B))
			(CI => CO) = 0;
		ifnone (CI => CO) = 0;
		if ((B & CI))
			(A => S) = 0;
		if ((~B & ~CI))
			(A => S) = 0;
		ifnone (A => S) = 0;
		if ((B & ~CI))
			(A => S) = 0;
		if ((~B & CI))
			(A => S) = 0;
		if ((A & CI))
			(B => S) = 0;
		if ((~A & ~CI))
			(B => S) = 0;
		ifnone (B => S) = 0;
		if ((A & ~CI))
			(B => S) = 0;
		if ((~A & CI))
			(B => S) = 0;
		if ((A & B))
			(CI => S) = 0;
		if ((~A & ~B))
			(CI => S) = 0;
		ifnone (CI => S) = 0;
		if ((A & ~B))
			(CI => S) = 0;
		if ((~A & B))
			(CI => S) = 0;
	endspecify
endmodule
`endcelldefine
