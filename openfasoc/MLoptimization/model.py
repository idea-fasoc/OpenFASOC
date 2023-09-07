#training import
import gym
import ray
import ray.tune as tune
from ray.rllib.algorithms.ppo import PPO
from run_training import Envir
from sky130_nist_tapeout import single_build_and_simulation
sky130_nist_tapeout.path.append('../generators/gdsfactory-gen/')

import argparse
#
#training set up
parser = argparse.ArgumentParser()
parser.add_argument('--checkpoint_dir', '-cpd', type=str)
args = parser.parse_args()
ray.init(num_cpus=33, num_gpus=0,include_dashboard=True, ignore_reinit_error=True)

#configures training of the agent with associated hyperparameters
config_train = {
            #"sample_batch_size": 200,
            "env": Envir,
            "train_batch_size": 1000,
            #"sgd_minibatch_size": 1200,
            #"num_sgd_iter": 3,
            #"lr":1e-3,
            #"vf_loss_coeff": 0.5,
            #"rollout_fragment_length":  63,
            "model":{"fcnet_hiddens": [64, 64]},
            "num_workers": 32,
            "env_config":{"generalize":True, "run_valid":False, "horizon":20},
            }

#Runs training and saves the result in ~/ray_results/train_ngspice_45nm
#If checkpoint fails for any reason, training can be restored
trials = tune.run(
    "PPO", #You can replace this string with ppo.PPOTrainer if you want / have customized it
    name="brandnewBound_1", # The name can be different.
    stop={"episode_reward_mean": 12, "training_iteration": 15},
    checkpoint_freq=1,
    config=config_train,
    #restore="/home/wentian/ray_results/brandnewBound/PPO_Envir_cc8be_00000_0_2023-08-16_01-11-16/checkpoint_000002",
    #restore="/home/wentian/ray_results/brandnewBound/PPO_Envir_f6236_00000_0_2023-08-16_04-40-01/checkpoint_000003",
    #restore="/home/wentian/ray_results/brandnewBound/PPO_Envir_4615a_00000_0_2023-08-16_06-58-15/checkpoint_000006"
    #restore="/home/wentian/ray_results/brandnewBound/PPO_Envir_d8b02_00000_0_2023-08-17_02-07-41/checkpoint_000012",
    restore="/home/wentian/ray_results/brandnewBound_1/PPO_Envir_d6a0f_00000_0_2023-08-18_05-19-43/checkpoint_000012",
)
#