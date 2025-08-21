import numpy as np
import random
from scipy.spatial.distance import pdist
from scipy.stats import qmc


# === Budget Allocation & Validation ===


def allocate_budget_fixed_total(d_dims, N_total):
   total_dim = sum(d_dims)
   raw = [N_total * (d / total_dim) for d in d_dims]
   floors = [int(np.floor(x)) for x in raw]
   remainder = N_total - sum(floors)
   frac_parts = [(x - f, i) for i, (x, f) in enumerate(zip(raw, floors))]
   for _, idx in sorted(frac_parts, reverse=True)[:remainder]:
       floors[idx] += 1
   return floors


def _budgets_valid(budgets, level_counts):
   """
   Check each budget is divisible by all integer OA level counts for that PCell.
   level_counts: list of lists, per-PCell integer axis levels.
   """
   for b, levels in zip(budgets, level_counts):
       for s in levels:
           if b % s != 0:
               return False
   return True


def find_valid_N_total(d_dims, level_counts, N_start, max_search=10000):
   for N in range(N_start, N_start + max_search):
       budgets = allocate_budget_fixed_total(d_dims, N)
       if _budgets_valid(budgets, level_counts):
           return N, budgets
   raise ValueError("No valid N_total found")


# === LHS + Maximin ===


def min_pairwise_distance(points):
   if len(points) < 2:
       return 0.0
   return pdist(points, metric='euclidean').min()


def lhs_maximin(d, n, patience=100, seed=None):
   engine = qmc.LatinHypercube(d, seed=seed)
   sample = engine.random(n)
   best = sample.copy()
   best_min = min_pairwise_distance(best)
  
   no_improve = 0
   while no_improve < patience:
       i, j = random.sample(range(n), 2)
       axis = random.randrange(d)
       cand = best.copy()
       cand[i, axis], cand[j, axis] = cand[j, axis], cand[i, axis]
       cand_min = min_pairwise_distance(cand)
       if cand_min > best_min:
           best, best_min = cand, cand_min
           no_improve = 0
       else:
           no_improve += 1
  
   return best


# === OA Sampling for Integer and Categorical Axes ===


def sample_integer_oa(minv, maxv, N, seed=None):
   random.seed(seed)
   levels = list(range(minv, maxv + 1))
   s = len(levels)
   if N % s != 0:
       raise ValueError(f"N ({N}) not a multiple of {s}")
   repeats = N // s
   seq = levels * repeats
   random.shuffle(seq)
   return seq


def sample_categorical_oa(levels, N, seed=None):
   """
   OA sampling for categorical variables.
   levels: list of category values
   N: number of samples (must be divisible by len(levels))
   Returns: list of N categorical samples with balanced representation
   """
   random.seed(seed)
   s = len(levels)
   if N % s != 0:
       raise ValueError(f"N ({N}) not a multiple of number of levels ({s})")
   repeats = N // s
   seq = levels * repeats
   random.shuffle(seq)
   return seq


# === PCell Configuration Specs ===


# Continuous specs: (axis_name, min, max, count)
cont_specs = {
   'fvf': [
       ('width', 0.5, 20.0, 2),
       ('length', 0.15, 4.0, 2),
   ],
   'txgate': [
       ('width', 0.5, 20.0, 2),
       ('length', 0.15, 4.0, 2),
   ],
   'current_mirror': [
       ('width', 0.5, 20.0, 1),
       ('length', 0.15, 4.0, 1),
   ],
   'diff_pair': [
       ('width', 0.5, 20.0, 1),
       ('length', 0.15, 4.0, 1),
   ],
   'opamp': [
       ('half_diffpair_params_w', 5, 7, 1),  # width, length (fingers is int) - constrained length
       ('half_diffpair_params_l', 0.5, 1.5, 1),  # width, length (fingers is int) - constrained length
       ('diffpair_bias_w', 5, 7, 1),  # width, length (fingers is int) - constrained length
       ('diffpair_bias_l', 1.5, 2.5, 1),  # width, length (fingers is int) - constrained length
       ('half_common_source_params_w', 6, 8, 1),  # width, length (fingers, mults are int) - much shorter length
       ('half_common_source_params_l', 0.5, 1.5, 1),  # width, length (fingers, mults are int) - much shorter length
       ('half_common_source_bias_w', 5, 7, 1),  # width, length (fingers, mults are int) - constrained length
       ('half_common_source_bias_l', 1.5, 2.5, 1),  # width, length (fingers, mults are int) - constrained length
       ('output_stage_params', 0.5, 1.5, 2),  # width, length (fingers is int) - constrained length
       ('output_stage_bias', 1.5, 2.5, 2),  # width, length (fingers is int) - constrained length
       ('half_pload_w', 5, 7, 1),  # width, length (fingers is int) - constrained length
       ('half_pload_l', 0.5, 1.5, 1),  # width, length (fingers is int) - constrained length
       ('mim_cap_size', 10.0, 15.0, 2),  # width, height
   ],
   'lvcm': [
       ('width', 0.5, 20.0, 2),  # tuple of 2 widths
       ('length', 0.15, 4.0, 1),  # single length
   ],
}


# Integer (OA) specs: (axis_name, min, max)
int_specs = {
   'fvf': [
       ('fingers', 1, 5),
       ('multipliers', 1, 2),
   ],
   'txgate': [
       ('fingers', 1, 5),
       ('multipliers', 1, 2),
   ],
   'current_mirror': [
       ('numcols', 1, 5),
   ],
   'diff_pair': [
       ('fingers', 1, 5),
   ],
   'opamp': [
       ('half_diffpair_fingers', 1, 2),
       ('diffpair_bias_fingers', 1, 2),
       ('half_common_source_fingers', 8, 12),
       ('half_common_source_mults', 2, 4),
       ('half_common_source_bias_fingers', 7, 9),
       ('half_common_source_bias_mults', 2, 3),
       ('output_stage_fingers', 1, 12),
       ('output_stage_bias_fingers', 1, 6),
       ('half_pload_fingers', 4, 6),
       ('mim_cap_rows', 1, 5),
       ('rmult', 1, 3),
       ('with_antenna_diode_on_diffinputs', 0, 8),  # Allow 0 or 2-8; we'll remap 1 to 0 later
   ],
   'lvcm': [
       ('fingers', 1, 5),  # tuple of 2 finger counts
       ('multipliers', 1, 3),  # tuple of 2 multiplier counts
   ],
}


# Categorical specs: (axis_name, [levels])
cat_specs = [
   ('type', ['nmos','pmos']),
   ('placement', ['horizontal','vertical']),
   ('short_source', [False, True]),
   # For opamp we always disable the optional buffer → single-level categorical (all False)
   ('add_output_stage', [False]),
]


# === Helper: Merge LHS & OA into Mixed Samples ===


def generate_mixed_samples(pcell, lhs_pts, int_oa, cat_oa):
   """
   lhs_pts: array (n_p, d_p) for continuous dims
   int_oa: dict axis_name -> list of N integer OA samples
   cat_oa: dict axis_name -> list of N OA category choices
   Returns list of dicts of raw samples.
   """
   samples = []
   n_p = lhs_pts.shape[0]
  
   # Build flat continuous spec list
   flat_cont = []
   for name, mn, mx, cnt in cont_specs[pcell]:
       for _ in range(cnt):
           flat_cont.append((name, mn, mx))
  
   for i in range(n_p):
       raw = {}
       # Continuous dims
       for dim_idx, (name, mn, mx) in enumerate(flat_cont):
           val = lhs_pts[i, dim_idx] * (mx - mn) + mn
           raw.setdefault(name, []).append(val)
      
       # Special handling for specific pcells
       if pcell == 'opamp':
           # For opamp, the complex parameter tuples will be constructed later
           # Just convert continuous params to tuples for now
           for name in list(raw.keys()):
               raw[name] = tuple(raw[name])
       elif pcell == 'lvcm':
           # Convert width to tuple, length stays single value
           processed_params = {}
           if 'width' in raw:
               processed_params['width'] = (raw['width'][0], raw['width'][1])
           if 'length' in raw:
               processed_params['length'] = raw['length'][0]  # Single value
           raw = processed_params
       elif pcell in ['current_mirror', 'diff_pair']:
           # These circuits expect scalar values for width and length
           processed_params = {}
           if 'width' in raw:
               processed_params['width'] = raw['width'][0]  # Single scalar value
           if 'length' in raw:
               processed_params['length'] = raw['length'][0]  # Single scalar value
           raw = processed_params
       else:
           # Convert lists to tuples for other pcells
           for name in list(raw.keys()):
               raw[name] = tuple(raw[name])
      
       # Integer axes from OA
       for name, _, _ in int_specs[pcell]:
           if pcell in ['fvf', 'txgate'] and name in ['fingers', 'multipliers']:
               # For fvf and txgate, these should be tuples of 2 values
               raw[name] = (int_oa[name][i], int_oa[name][i])
           elif pcell == 'lvcm' and name in ['fingers', 'multipliers']:
               # For lvcm, these should be tuples of 2 values
               raw[name] = (int_oa[name][i], int_oa[name][i])
           else:
               raw[name] = int_oa[name][i]
      
       # Special post-processing for opamp to construct proper parameter tuples
       if pcell == 'opamp':
            # Ensure antenna diode count is valid
            if raw.get('with_antenna_diode_on_diffinputs', 0) == 1:
               raw['with_antenna_diode_on_diffinputs'] = 0
            # Extract scalar values from single-element tuples/lists
            def get_scalar(v):
                return v[0] if isinstance(v, (list, tuple)) else v
            # Construct parameter tuples with scalar values
            raw['half_diffpair_params'] = (
                    get_scalar(raw['half_diffpair_params_w']),
                    get_scalar(raw['half_diffpair_params_l']),
                    raw['half_diffpair_fingers']
                    )
            raw['diffpair_bias'] = (
                    get_scalar(raw['diffpair_bias_w']),
                    get_scalar(raw['diffpair_bias_l']),
                    raw['diffpair_bias_fingers']
                    )
            raw['half_common_source_params'] = (
                    get_scalar(raw['half_common_source_params_w']),
                    get_scalar(raw['half_common_source_params_l']),
                    raw['half_common_source_fingers'],
                    raw['half_common_source_mults']
                    )
            raw['half_common_source_bias'] = (
                    get_scalar(raw['half_common_source_bias_w']),
                    get_scalar(raw['half_common_source_bias_l']),
                    raw['half_common_source_bias_fingers'],
                    raw['half_common_source_bias_mults']
                    )
            raw['output_stage_params'] = (
                    get_scalar(raw['output_stage_params'][0]),
                    get_scalar(raw['output_stage_params'][1]),
                    raw['output_stage_fingers']
                    )
            raw['output_stage_bias'] = (
                    get_scalar(raw['output_stage_bias'][0]),
                    get_scalar(raw['output_stage_bias'][1]),
                    raw['output_stage_bias_fingers']
                    )
            raw['half_pload'] = (
                    get_scalar(raw['half_pload_w']),
                    get_scalar(raw['half_pload_l']),
                    raw['half_pload_fingers']
                    )
            # Cleanup temporary keys
            keys_to_delete = [
                    'half_diffpair_fingers', 'diffpair_bias_fingers',
                    'half_common_source_fingers', 'half_common_source_mults',
                    'half_common_source_bias_fingers', 'half_common_source_bias_mults',
                    'output_stage_fingers', 'output_stage_bias_fingers', 'half_pload_fingers',
                    'half_diffpair_params_w','half_diffpair_params_l',
                    'diffpair_bias_w','diffpair_bias_l',
                    'half_common_source_params_w', 'half_common_source_params_l',
                    'half_common_source_bias_w', 'half_common_source_bias_l',
                    'half_pload_w', 'half_pload_l'
                    ]
            for key in keys_to_delete:
                raw.pop(key, None)      
       # Categorical OA sampling - only add parameters that circuits actually accept
       if pcell == 'diff_pair':
           # diff_pair accepts n_or_p_fet as boolean (True for nfet, False for pfet)
           if 'type' in cat_oa:
               raw['n_or_p_fet'] = cat_oa['type'][i] == 'nmos'
       elif pcell == 'opamp':
           # opamp accepts add_output_stage boolean
           if 'add_output_stage' in cat_oa:
               raw['add_output_stage'] = cat_oa['add_output_stage'][i]
       # Skip other categorical parameters as most circuits don't accept them
      
       samples.append(raw)
   return samples


# === Main Generation Flow ===


def generate_all_samples():
   """Generate all samples for all PCells using the 8-hour runtime-aware budget from budgets_8h_runtime_aware_measuredTp_dpCorrected.json"""
   # Sample counts from budgets_8h_runtime_aware_measuredTp_dpCorrected.json
   # Total samples: 40,814 across 8 hours on 26 cores with 1.2x overhead
   inventory_np = {
       'fvf'           :  10886,   # Flipped-voltage follower  
       'txgate'        :  3464,    # Transmission gate
       'current_mirror':  7755,    # Current mirror            
       'diff_pair'     :  9356,    # Differential pair         
       'lvcm'          :  3503,    # Low-V current mirror      
       'opamp'         :  5850,    # Two-stage op-amp
   }


   # 2) List the PCells in the same order as your specs dicts:
   pcells = ['fvf','txgate','current_mirror','diff_pair','lvcm','opamp']
  
   # For reproducibility - using seed 1337 to match budget plan
   random.seed(1337)


   # 3) Loop over each PCell, pulling its LHS dim and inventory np:
   all_samples = {}
   for pcell in pcells:
       # how many continuous dims for this PCell?
       d_p = sum(cnt for *_ , cnt in cont_specs[pcell])
       # override budget with inventory np
       n_p = inventory_np[pcell]
      
       # Skip PCells with 0 samples
       if n_p == 0:
           all_samples[pcell] = []
           print(f"{pcell}: skipped (inventory np = 0)")
           continue


       # a) Continuous LHS + adaptive maximin
       lhs_pts = lhs_maximin(d_p, n_p, patience=10*d_p, seed=42)


       # b) Integer OA sampling (with fallback to random if N not divisible)
       int_oa = {}
       for name, mn, mx in int_specs.get(pcell, []):
           levels = list(range(mn, mx + 1))
           s = len(levels)
           if n_p % s == 0:
               int_oa[name] = sample_integer_oa(mn, mx, n_p, seed=hash(f"{pcell}_{name}"))
           else:
               # Fallback to random sampling for integers
               print(f"Warning: {pcell} has {n_p} samples, not divisible by {s} levels for {name}, using random sampling")
               random.seed(hash(f"{pcell}_{name}"))
               int_oa[name] = [random.randint(mn, mx) for _ in range(n_p)]


       # c) OA categoricals
       cat_oa = {}
       for name, levels in cat_specs:
           # For OA to work, N must be divisible by number of levels
           s = len(levels)
           if n_p % s == 0:
               cat_oa[name] = sample_categorical_oa(levels, n_p, seed=hash(f"{pcell}_{name}"))
           else:
               # If N is not divisible, fall back to random for this categorical
               print(f"Warning: {pcell} has {n_p} samples, not divisible by {s} levels for {name}, using random sampling")
               cat_oa[name] = [random.choice(levels) for _ in range(n_p)]


       # d) Merge into full mixed-level samples
       samples = generate_mixed_samples(pcell, lhs_pts, int_oa, cat_oa)
       all_samples[pcell] = samples


       print(f"{pcell}: generated {len(samples)} samples (inventory np = {n_p})")
       # Print a few examples for verification
       print(f"First 3 samples for {pcell}:")
       for s in samples[:3]:
           print(s)
       print()


   return all_samples


# Generate samples at module level so they can be imported
all_samples = generate_all_samples()


if __name__ == "__main__":
   import json
   import os
  
   # Save samples to JSON files
   # output_dir = os.path.join(os.path.dirname(__file__), "gen_params_32hr")
   output_dir = os.path.join(os.path.dirname(__file__), "gen_params_8h_runtime_aware")
   os.makedirs(output_dir, exist_ok=True)
  
   for pcell, samples in all_samples.items():
       # Match naming style used for other datasets
       fname = f"{pcell}_params.json"
       output_file = os.path.join(output_dir, fname)
       with open(output_file, 'w') as f:
           json.dump(samples, f, indent=2)
       print(f"Saved {len(samples)} samples to {output_file}")
  
   print("\n8-hour runtime-aware dataset generation with budget-prescribed sample counts completed.")
   print("Sample counts:")
   for pcell, samples in all_samples.items():
       print(f"  {pcell}: {len(samples)} samples")
   print("\nTotal samples across all PCells:", sum(len(samples) for samples in all_samples.values()))
   print("Expected total from budget: 40,814 samples")

