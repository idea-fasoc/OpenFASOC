# Add glayout to path
import sys
sys.path.append('../generators/gdsfactory-gen')
sys.path.append('../generators/gdsfactory-gen/tapeout_and_RL')

#training import
import numpy as np
from ray.rllib.algorithms.ppo import PPO
from run_training import Envir
import pickle
import yaml
from pathlib import Path
import argparse

def unlookup(norm_spec, goal_spec):
    spec = -1*np.multiply((norm_spec+1), goal_spec)/(norm_spec-1)
    return spec

def evaluate_model():
    specs = yaml.safe_load(Path('newnew_eval_3.yaml').read_text())

    #training set up
    env_config = {
                "generalize":True,
                "num_valid":2,
                "save_specs":False,
                "inputspec":specs,
                "run_valid":True,
                "horizon":25,
                }

    config_eval = {
                #"sample_batch_size": 200,
                "env": Envir,
                "env_config":{
                                "generalize":True,
                                "num_valid":2,
                                "save_specs":False,
                                "inputspec":specs,
                                "run_valid":True,
                                "horizon":25,
                            },
                }

    parser = argparse.ArgumentParser()
    parser.add_argument('--checkpoint_dir', '-cpd', type=str)
    args = parser.parse_args()
    env = Envir(env_config=env_config)

    agent = PPO.from_checkpoint("./last_checkpoint")

    norm_spec_ref = env.global_g
    spec_num = len(env.specs)

    rollouts = []
    next_states = []
    obs_reached = []
    obs_nreached = []
    action_array = []
    action_arr_comp = []
    rollout_steps = 0
    reached_spec = 0
    f = open("newnewnew_eval__3.txt", "a")

    while rollout_steps < 100:
        rollout_num = []
        state, info = env.reset()

        done = False
        truncated = False
        reward_total = 0.0
        steps=0
        f.write('new----------------------------------------')
        while not done and not truncated:
            action = agent.compute_single_action(state)
            action_array.append(action)

            next_state, reward, done, truncated, info = env.step(action)
            f.write(str(action)+'\n')
            f.write(str(reward)+'\n')
            f.write(str(done)+'n')
            print(next_state)
            print(action)
            print(reward)
            print(done)
            reward_total += reward

            rollout_num.append(reward)
            next_states.append(next_state)

            state = next_state

        norm_ideal_spec = state[spec_num:spec_num+spec_num]
        ideal_spec = unlookup(norm_ideal_spec, norm_spec_ref)
        if done == True:
            reached_spec += 1
            obs_reached.append(ideal_spec)
            action_arr_comp.append(action_array)
            action_array = []
            pickle.dump(action_arr_comp, open("action_arr_test", "wb"))
        else:
            obs_nreached.append(ideal_spec)          #save unreached observation
            action_array=[]

        f.write('done----------------------------------------')
        rollouts.append(rollout_num)

        print("Episode reward", reward_total)
        rollout_steps+=1

        #if out is not None:
        #pickle.dump(rollouts, open(str(out)+'reward', "wb"))
        pickle.dump(obs_reached, open("opamp_obs_reached_test","wb"))
        pickle.dump(obs_nreached, open("opamp_obs_nreached_test","wb"))

        f.write("Specs reached: " + str(reached_spec) + "/" + str(len(obs_nreached)))
        print("Specs reached: " + str(reached_spec) + "/" + str(len(obs_nreached)))

    print("Num specs reached: " + str(reached_spec) + "/" + str(1))

if __name__ == "__main__":
    evaluate_model()
