# Temp Sensor generator

An all-digital temperature sensor, that relies on a new subthreshold oscillator (achieved using the auxiliary cell “Header Cell“) for realizing synthesizable thermal sensors.

![plot](./readme_imgs/temp_sensor_IO.PNG)

 ## Inputs
 *  CLK_REF:- System clock taken from input.
 *  RESET_COUNTERn:- Input signal to reset the module initial state.
 *  VIN :-  The input voltage that is also output just like  a feedback loop.
 * SEL_CONV_TIME:- Four bit input used to select how many times the 1 bit of the output DOUT is fractionated (0-16).

 ## Outputs
 *  DOUT:-  The output voltage whose frequency is dependent on temperature.
 *  DONE:- Validity signal for DOUT
