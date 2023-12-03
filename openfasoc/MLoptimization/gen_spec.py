#!/usr/bin/env python3
## Generate the design specifications and then save to a pickle file

import random
import argparse

def generate_random_specs(env, num_specs):
  specs_range = {
                "gain_min" : [float(14003380.0), float(50003380.0)],
                "FOM" : [float(4e11), float(4e11)]
                }
  specs_range_vals = list(specs_range.values())
  specs_valid = []
  for spec in specs_range_vals:
      if isinstance(spec[0],int):
          list_val = [random.randint(int(spec[0]),int(spec[1])) for x in range(0,num_specs)]
      else:
          list_val = [random.uniform(float(spec[0]),float(spec[1])) for x in range(0,num_specs)]
      specs_valid.append(tuple(list_val))
  i=0
  for key,value in specs_range.items():
      specs_range[key] = specs_valid[i]
      i+=1

  output = str(specs_range)
  with open(env, 'w') as f:
    f.write(output.replace('(','[').replace(')',']').replace(',',',\n'))

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--num_specs', type=str)
  args = parser.parse_args()

  generate_random_specs("train.yaml", int(100))

if __name__=="__main__":
  main()
