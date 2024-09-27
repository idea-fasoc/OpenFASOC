# Machine Learning Optimization
Code for reinforcement learning loop with openfasoc generators for optimizing metrics

## Supported Versions
Please note that this program has only been tested with python3.10 and ngspice v40s

## Quick Start
run `bash quickstart.bash` to get an example RL run optimizing opamps.

## Code Setup
The code is setup as follows:

The top level directory contains two sub-directories:
* model.py: top level RL script, used to set hyperparameters and run training
* run_training.py: contains all OpenAI Gym environments. These function as the agent in the RL loop and contain information about parameter space, valid action steps and reward.
* eval.py: contains all of the code for evaluation
* gen_spec.py: contains all of the random specification generation

## Training
Make sure that you have OpenAI Gym and Ray installed. To do this, run the following command:

To generate the design specifications that the agent trains on, run:
```
python3.10 gen_specs.py
```
The result is a yaml file dumped to the ../generators/gdsfactory-gen/.

To train the agent, open ipython from the top level directory and then: 
```
python3.10 model.py
```
The training checkpoints will be saved in your home directory under ray\_results. Tensorboard can be used to load reward and loss plots using the command:

```
tensorboard --logdir path/to/checkpoint
```

## Validation
The evaluation script takes the trained agent and gives it new specs that the agent has never seen before. To generate new design specs, run the gen_specs.py file again with your desired number of specs to validate on. To run validation:

```
python3.10 eval.py
```

The evaluation result will be saved to the ../generators/glayout/.

## Results
example resulting opamps (parameter arrays and names provided)

```
# transistor parameters provided as (width, length, fingers, multipliers)
# all parameters are listed in floating point format (even integers) for processing purposes

153 MegHz UGB, 91db DC Gain, 166uW power
[3.0, 0.5, 6.0, 7.0, 1.5, 10.0, 5.0, 0.7, 8.0, 3.0, 5.0, 1.2, 12.0, 3.0, 5.0, 1.0, 16.0, 6.0, 2.0, 4.0, 4.0, 0.5, 5.0, 12.0, 12.0, 3.0, 2.0]
{'diffpair': (3.0, 0.5, 6.0), 'diffpair_bias': (7.0, 1.5, 10.0), 'secondstage': (5.0, 0.7, 8.0, 3.0), 'secondstage_bias': (5.0, 1.2, 12.0, 3.0), 'output_stage_params': (5.0, 1.0, 16.0), 'output_stage_bias': (6.0, 2.0, 4.0), 'firststage': (4.0, 0.5, 5.0), 'mim_cap_size': (12.0, 12.0), 'mim_cap_rows': 3, 'rmult': 2}

143 MegHz UGB, 95db DC Gain, 179uW power
[2.0, 0.6, 4.0, 4.0, 1.0, 7.0, 4.0, 0.7, 13.0, 3.0, 4.0, 1.1, 12.0, 3.0, 5.0, 1.0, 16.0, 6.0, 2.0, 4.0, 3.0, 0.5, 5.0, 12.0, 12.0, 3.0, 2.0]
{'diffpair': (2.0, 0.6, 4.0), 'diffpair_bias': (4.0, 1.0, 7.0), 'secondstage': (4.0, 0.7, 13.0, 3.0), 'secondstage_bias': (4.0, 1.1, 12.0, 3.0), 'output_stage_params': (5.0, 1.0, 16.0), 'output_stage_bias': (6.0, 2.0, 4.0), 'firststage': (3.0, 0.5, 5.0), 'mim_cap_size': (12.0, 12.0), 'mim_cap_rows': 3, 'rmult': 2}

137 MegHz UGB, 95db DC Gain, 41uW power
[3.0, 0.5, 4.0, 4.0, 1.0, 7.0, 4.0, 0.8, 14.0, 3.0, 4.0, 1.2, 11.0, 3.0, 5.0, 1.0, 16.0, 6.0, 2.0, 4.0, 3.0, 0.5, 5.0, 12.0, 12.0, 3.0, 2.0]
{'diffpair': (3.0, 0.5, 4.0), 'diffpair_bias': (4.0, 1.0, 7.0), 'secondstage': (4.0, 0.8, 14.0, 3.0), 'secondstage_bias': (4.0, 1.2, 11.0, 3.0), 'output_stage_params': (5.0, 1.0, 16.0), 'output_stage_bias': (6.0, 2.0, 4.0), 'firststage': (3.0, 0.5, 5.0), 'mim_cap_size': (12.0, 12.0), 'mim_cap_rows': 3, 'rmult': 2}
```

