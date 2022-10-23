import os, argparse, re
import subprocess as sp
import hypertune
from pandas import read_csv

def get_args():
    '''Parses args. Must include all hyperparameters you want to tune.'''

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--vin_route_conn',
        required=True,
        type=int,
        help='VIN_ROUTE_CONNECTION_POINTS',
    )
    parser.add_argument(
        '--header_starting_row',
        required=True,
        type=int,
        help='HEADERS_STARTING_ROW',
    )
    args = parser.parse_args()
    return args

def configure_generator(input_args):
    '''Sets the respective environment variables to configure the Generator according to the input arguments'''

    for var in input_args.__dict__:
        os.environ[var] = str(input_args.__dict__[var])

def run_generator():
    sp.run(
        "git clone https://github.com/idea-fasoc/OpenFASOC.git",
        shell=True
    )
    # Change simulation step time to 100ns to increase simulation time
    with open('OpenFASOC/openfasoc/generators/temp-sense-gen/simulations/templates/tempsenseInst_ngspice.sp', 'r') as rf:
        filedata = rf.read()
        filedata = re.sub('.TRAN ([0-9]+.)', '.TRAN 100n', filedata)
    with open('OpenFASOC/openfasoc/generators/temp-sense-gen/simulations/templates/tempsenseInst_ngspice.sp', 'w') as wf:
        wf.write(filedata)
    # Run generator
    sp.run(
        "cd OpenFASOC/openfasoc/generators/temp-sense-gen && \
            make sky130hd_temp_full 1> /dev/null",
        shell=True
    )
         

def read_sim_results_power():
    '''Gets the simulation results for the Generator. Must return the metric you want to evaluate.'''

    sim_output_path = "OpenFASOC/openfasoc/generators/temp-sense-gen/work/prePEX_sim_result"
    with open(sim_output_path, 'r') as f:
        data = read_csv(f, sep=' ', header=1)
        # Dataframe of the type:
        #
        # Temp Frequency Power Error
        # 20.000000 3726.641874560489 3.084857e-04 -100.0
        # 40.000000 13541.845249750899 4.135856e-04 0.0
    
    # Calculate average power for all temperatures
    sum_pow = 0
    for pow in data['Power']:
        sum_pow = sum_pow + pow * 1e6
    avg_power = sum_pow / len(data['Power']) # in uW

    return avg_power

def main():
    args = get_args()
    configure_generator(args)
    run_generator()

    # Define metric
    dse_metric = read_sim_results_power()

    hpt = hypertune.HyperTune()
    hpt.report_hyperparameter_tuning_metric(
        hyperparameter_metric_tag='power',
        metric_value=dse_metric,
    )

if __name__ == "__main__":
    main()