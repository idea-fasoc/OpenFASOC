#env import
import gymnasium as gym
from gymnasium import spaces
from gymnasium.spaces import Discrete
from gymnasium.wrappers import EnvCompatibility
from ray.rllib.env.wrappers.multi_agent_env_compatibility import MultiAgentEnvCompatibility
from sky130_nist_tapeout import single_build_and_simulation
sky130_nist_tapeout.path.append('../generators/gdsfactory-gen/tapeout_and_RL')
import numpy as np
import random
import psutil

from multiprocessing import Pool
from collections import OrderedDict
import yaml
import yaml.constructor
import statistics
import os
import itertools
import pickle
import yaml
from pathlib import Path

#
#environment set up
class Envir(gym.Env):
    metadata = {'render.modes': ['human']}

    PERF_LOW = -1
    PERF_HIGH = 1

    def __init__(self, env_config):
        PERF_LOW = -1
        PERF_HIGH = 1
        self.multi_goal = env_config.get("multi_goal",False)
        self.generalize = env_config.get("generalize",False)
        num_valid = env_config.get("num_valid",50)
        self.specs_save = env_config.get("save_specs", False)
        self.valid = env_config.get("run_valid", False)
        self.horizon = env_config.get("horizon", 100)
        inputspec = env_config.get("inputspec",{})

        self.env_steps = 0
        #data = np.load('./training_params.npy')
        #result = np.load('./training_results.npy')
        #self.result = result
        self.epi_steps = 0

        # design specs
        if self.generalize == True:
            if self.valid == False:
                specs = yaml.safe_load(Path('train1.yaml').read_text())
            else:
                specs = inputspec
                
        self.specs = specs

        self.specs_ideal = []
        self.specs_id = list(self.specs.keys())
        self.fixed_goal_idx = -1
        self.num_os = len(list(self.specs.values())[0])

        # param array
        params = {
                  "diffpair_params0" : [1, 8, 1],       
                  "diffpair_params1" : [0.5, 2.1, 0.1],   
                  "diffpair_params2" : [1, 5, 1],
                  "Diffpair_bias0" : [1, 8, 1],
                  "Diffpair_bias1" : [1, 4.5, 0.5],
                  "Diffpair_bias2" : [3, 13, 1],
                  "pamp_hparams0" : [1, 8, 1], 
                  "pamp_hparams1" : [0.5, 2.1, 0.1], 
                  "pamp_hparams2" : [3, 13, 1],
                  "bias0" : [1, 8, 1], 
                  "bias1" : [0.5, 2.1, 0.1], 
                  "bias2" : [3, 13, 1],
                  "bias3" : [2, 4, 1],
                  "mim_cap_rows" : [1, 4, 1],
                  }
        self.params = []
        self.params_id = list(params.keys())

        for value in params.values():
            param_vec = np.arange(value[0], value[1], value[2])
            self.params.append(param_vec)

        #initialize sim environment
        self.action_meaning = [-1,0,1]
        self.action_space = spaces.Tuple([spaces.Discrete(len(self.action_meaning))]*len(self.params_id))
        #self.action_space = spaces.Discrete(len(self.action_meaning)**len(self.params_id))
        self.observation_space = spaces.Box(
            low=np.array([PERF_LOW]*2*len(self.specs_id)+len(self.params_id)*[0]),
            high=np.array([PERF_HIGH]*2*len(self.specs_id)+len(self.params_id)*[100]), dtype=np.float32)

        #initialize current param/spec observations
        self.cur_specs = np.zeros(len(self.specs_id), dtype=np.float32)
        self.cur_params_idx = np.zeros(len(self.params_id), dtype=np.int32)

        #Get the g* (overall design spec) you want to reach
        self.global_g = []
        for spec in list(self.specs.values()):
                self.global_g.append(float(spec[self.fixed_goal_idx]))
        self.g_star = np.array(self.global_g)
        self.global_g = np.array([3000338000.0, 1.0*10**13])

        #objective number (used for validation)g
        self.obj_idx = 0

    def reset(self, *, seed=None, options=None):
        #if multi-goal is selected, every time reset occurs, it will select a different design spec as objective
        if self.generalize == True:
            if self.valid == True:
                if self.obj_idx > self.num_os-1:
                    self.obj_idx = 0
                idx = self.obj_idx
                self.obj_idx += 1
            else:
                idx = random.randint(0,self.num_os-1)
            self.specs_ideal = []
            for spec in list(self.specs.values()):
                self.specs_ideal.append(spec[idx])
            self.specs_ideal = np.array(self.specs_ideal)
        else:
            if self.multi_goal == False:
                self.specs_ideal = self.g_star
            else:
                idx = random.randint(0,self.num_os-1)
                self.specs_ideal = []
                for spec in list(self.specs.values()):
                    self.specs_ideal.append(spec[idx])
                self.specs_ideal = np.array(self.specs_ideal)
        print("num total:"+str(self.num_os) + "new reset!!!")

        #applicable only when you have multiple goals, normalizes everything to some global_g
        self.specs_ideal_norm = self.lookup(self.specs_ideal, self.global_g)

        #initialize current parameters
        self.cur_params_idx = np.array([1, 5, 3, 5, 2, 1, 6, 0, 5, 5, 1, 1, 1, 0])
        # param array
        self.cur_specs = self.update(self.cur_params_idx)
        cur_spec_norm = self.lookup(self.cur_specs, self.global_g)
        reward = self.reward(self.cur_specs, self.specs_ideal)
        self.epi_steps = 0
        #observation is a combination of current specs distance from ideal, ideal spec, and current param vals
        self.ob = np.concatenate([cur_spec_norm, self.specs_ideal_norm, self.cur_params_idx])
        return self.ob, {}

    def step(self, action):
        """
        :param action: is vector with elements between 0 and 1 mapped to the index of the corresponding parameter
        :return:cur observations & reward
        """
        #Take action that RL agent returns to change current params
        prevreward = self.reward(self.cur_specs, self.specs_ideal)
        action = list(np.reshape(np.array(action),(np.array(action).shape[0],)))
        self.cur_params_idx = self.cur_params_idx + np.array([self.action_meaning[a] for a in action])

#        self.cur_params_idx = self.cur_params_idx + np.array(self.action_arr[int(action)])
        self.cur_params_idx = np.clip(self.cur_params_idx, [0]*len(self.params_id), [(len(param_vec)-1) for param_vec in self.params])
        #Get current specs and normalize
        self.cur_specs = self.update(self.cur_params_idx)
        cur_spec_norm  = self.lookup(self.cur_specs, self.global_g)
        reward = self.reward(self.cur_specs, self.specs_ideal)
        terminated = False
        #f = open("newnew_5.txt", "a")
        f = open("record2.txt", "a")
        #incentivize reaching goal state
        if(prevreward >= 2.0 and reward < 2.0):
            terminated = True
        if (reward >= 2.0):
            if (reward < prevreward):
                terminated = True
            f.write('-'*10 +'\n')
            f.write('params = '+str(self.cur_params_idx)+'\n')
            f.write('specs:'+str(self.cur_specs)+'\n')
            f.write('ideal specs:'+str(self.specs_ideal)+'\n')
            f.write('re:'+str(reward)+'\n')
            f.write('-'*10+'\n')
            print('-'*10)
            print('params = ', self.cur_params_idx)
            print('specs:', self.cur_specs)
            print('ideal specs:', self.specs_ideal)
            print('re:', reward)
            print('-'*10)

        self.ob = np.concatenate([cur_spec_norm, self.specs_ideal_norm, self.cur_params_idx])
        self.env_steps = self.env_steps + 1
        self.epi_steps = self.epi_steps + 1

        truncated = self.epi_steps >= self.horizon
        f.write('params: ' + str(self.cur_params_idx) +'\n')
        f.write('cur ob:' + str(self.cur_specs) +'\n')
        f.write('ideal spec:' + str(self.specs_ideal)+'\n')
        f.write('cur reward:' + str(reward)+'\n')
        f.write('epi step:' + str(self.epi_steps)+'\n')
        f.write('env steps:' + str(self.env_steps)+'\n')

        print('cur ob:' + str(self.cur_specs))
        print('ideal spec:' + str(self.specs_ideal))
        print('cur reward:' + str(reward))
        print('epi step:' + str(self.epi_steps))
        print('env steps:' + str(self.env_steps))
        return self.ob, reward, terminated, truncated, {}

    def lookup(self, spec, goal_spec):
        goal_spec = [float(e) for e in goal_spec]
        norm_spec = (spec-goal_spec)/(goal_spec+spec)
        for i in range(len(spec)):
            if spec[i] <= -1:
                norm_spec[i] = -1
            #if(norm_spec[i] > 0):
                #norm_spec[i] = 0
        return norm_spec

    def reward(self, spec, goal_spec):
        rel_specs = self.lookup(spec, goal_spec)
        pos_val = []
        reward = 0.0
        for i,rel_spec in enumerate(rel_specs):
            #if(self.specs_id[i] == 'ibias_max'):
                #rel_spec = rel_spec*-1.0#/10.0
            if rel_spec < 0:
                reward += rel_spec
                pos_val.append(0)
            else:
                if(self.specs_id[i] == 'FOM'):
                    reward += rel_spec
                pos_val.append(1)

        trueorfalse = True
        for i,rel_spec in enumerate(rel_specs):
            if rel_spec < -0.02:
                trueorfalse = False
        
        if trueorfalse:
            return 2.0+reward
        else:
            return reward

    def update(self, params_idx):
        #impose constraint tail1 = in
        #params_idx[0] = params_idx[3]
        params = np.array([self.params[i][params_idx[i]] for i in range(len(self.params_id))])
        #param_val = np.array[OrderedDict(list(zip(self.params_id,params)))]

        #run param vals and simulate
        #cur_specs = OrderedDict(sorted(self.sim_env.create_design_and_simulate(param_val[0])[1].items(), key=lambda k:k[0]))
        inputparam = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.0, 0.0, 0.0, 0.0, 0.0, 5.0, 1.0, 16.0, 6.0, 2.0, 4.0, 12.0, 12.0, 0.0, 2.0])
        inputparam[0:3] = params[0:3]
        inputparam[3:6] = params[3:6]
        inputparam[6:9] = params[6:9]
        inputparam[10:14] = params[9:13]
        inputparam[22] = params[13]
        result = single_build_and_simulation(inputparam,-269)
        specs = np.array([0.0 , 0.0])
        specs[0] = result["ugb"]
        specs[1] = result["ugb"]/result["power"]
        cur_specs = specs

        return cur_specs
#env end

def main():
  env_config = {"generalize":True, "valid":True}
  env = Envir(env_config)
  env.reset()
  env.step([2,2,2,2,2,2,2,2,2,2])


if __name__ == "__main__":
  main()
