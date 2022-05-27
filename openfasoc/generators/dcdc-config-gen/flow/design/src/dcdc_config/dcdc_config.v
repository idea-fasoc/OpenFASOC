module dcdc_config (
	a, s);
  input  [5:0] a;
  output [11:0]s;
  wire wire_12 , wire_14;
  assign s[11]  = ~s[10] ;
  assign s[10]  = (a[1]  & a[0]  & s[8] ) | (~a[5]  & ~a[3]  & ~a[1]  & ~s[8]  & ~wire_12 );
  assign s[9]  = s[10]  ? a[0]  : ~s[8] ;
  assign s[8]  = a[0]  ? (~a[1]  | (a[5]  & a[4]  & a[3]  & a[2] )) : a[1] ;
  assign s[7]  = wire_14 | (s[8]  & s[6] );
  assign s[6]  = s[8]  ? a[5]  : (a[2]  ? ~a[1]  : a[0] );
  assign s[5]  = s[4]  ^ wire_14;
  assign s[4]  = s[8]  ? a[4]  : (s[6]  ? a[5]  : (a[3]  ^ a[0] ));
  assign s[3]  = (s[2]  & (~s[5]  | s[4] )) | (~s[1]  & s[0] );
  assign s[2]  = (a[4]  & ((~s[7]  & s[6] ) | (~a[1]  & ~s[4] ))) | (a[3]  & (s[8]  | (~a[4]  & a[0]  & ~s[6] ))) | (a[5]  & ~s[6]  & s[4] );
  assign s[1]  = (~s[8]  & ((a[3]  & s[6] ) | (a[4]  & ~s[6]  & s[4] ))) | (a[2]  & s[8] ) | (a[5]  & ~s[4]  & wire_12 );
  assign s[0]  = s[1]  | (~s[4]  & ~s[2]  & wire_14);
  assign wire_12  = a[4]  | a[2] ;
  assign wire_14 = s[9]  & ~s[6] ;
endmodule
