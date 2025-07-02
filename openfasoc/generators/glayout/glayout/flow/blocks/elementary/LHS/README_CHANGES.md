# LHS Dataset Extension Summary

This document summarizes the modifications made to include **lvcm** (Low Voltage Current Mirror) and prepare for **opamp** circuits in the LHS dataset generation pipeline. Note: opamp is temporarily disabled due to upstream implementation issues.

## Files Modified

### 1. `elhs.py` - Core Parameter Generation
**Changes:**
- Added `lvcm` to the PCells list (opamp temporarily disabled)
- Extended `cont_specs` with lvcm continuous parameters:
  - **lvcm**: 2 parameter groups (width tuple, length scalar) = 3 total continuous dims
- Extended `int_specs` with integer parameters:
  - **lvcm**: 2 integer parameters (fingers tuple, multipliers tuple)
- Enhanced `generate_mixed_samples()` to handle different parameter structures:
  - **fvf, txgate**: Parameters as tuples (width, length, fingers, multipliers)
  - **current_mirror, diff_pair**: Parameters as scalars (width, length) 
  - **lvcm**: Mixed parameters (width tuple, length scalar, fingers/multipliers tuples)
  - **diff_pair**: Special handling for n_or_p_fet boolean parameter

### 2. `sweeper.py` - Parallel Execution Engine
**Changes:**
- Uncommented all functional code
- Added imports for lvcm circuit:
  ```python
  from lvcm import add_lvcm_labels, low_voltage_cmirror
  ```
- Extended `PCELL_FUNCS` dictionary with lvcm factory function:
  ```python
  'lvcm': lambda pdk, **kwargs: add_lvcm_labels(low_voltage_cmirror(pdk, **kwargs), pdk),
  ```

### 3. `opamp.py` - Opamp Circuit with Labels (Prepared but disabled)
**Changes:**
- Fixed import path for opamp function
- Corrected main function to use proper PDK reference
- Added `add_output_stage=False` parameter to work around upstream bug

### 4. Parameter Compatibility Fixes
**Major corrections made:**
- **fvf, txgate**: Changed fingers and multipliers to tuples as expected by circuits
- **current_mirror, diff_pair**: Changed width/length to scalars instead of tuples
- **diff_pair**: Fixed n_or_p_fet parameter to be boolean (True=nfet, False=pfet)
- **lvcm**: Maintained tuple structure for width, fingers, multipliers; scalar for length
- Removed incompatible categorical parameters (type, placement, short_source) that circuits don't accept

## Current Working Circuits (5/6)

### 1. **FVF (Flipped Voltage Follower)** - 60 samples
- Parameters: `width: tuple(2)`, `length: tuple(2)`, `fingers: tuple(2)`, `multipliers: tuple(2)`

### 2. **TXGATE (Transmission Gate)** - 60 samples  
- Parameters: `width: tuple(2)`, `length: tuple(2)`, `fingers: tuple(2)`, `multipliers: tuple(2)`

### 3. **Current Mirror** - 30 samples
- Parameters: `width: float`, `length: float`, `numcols: int`

### 4. **Differential Pair** - 30 samples
- Parameters: `width: float`, `length: float`, `fingers: int`, `n_or_p_fet: bool`

### 5. **LVCM (Low Voltage Current Mirror)** - 45 samples
- Parameters: `width: tuple(2)`, `length: float`, `fingers: tuple(2)`, `multipliers: tuple(2)`

### 6. **Opamp** - Temporarily disabled
- Issue: Upstream bug in `__add_output_stage` function causes KeyError: 'top_met_E'
- Status: Parameter structure prepared, can be re-enabled when upstream fix is available

## Sample Counts
Current budget allocation produces:
- **fvf**: 60 samples
- **txgate**: 60 samples  
- **current_mirror**: 30 samples
- **diff_pair**: 30 samples
- **lvcm**: 45 samples
- **Total**: 225 samples

## Validation Results
✅ **End-to-end test successful**: All 5 working circuits successfully instantiated and wrote GDS files
✅ **Parameter generation**: Proper tuple/scalar structure for each circuit type
✅ **LHS sampling**: Latin Hypercube Sampling with maximin optimization working
✅ **Parallel evaluation**: Sweeper framework ready for full dataset generation

## Usage
Run the complete pipeline:
```bash
cd /home/arnavshukla/OpenFASOC/openfasoc/generators/glayout/glayout/flow/blocks/elementary/LHS

# Test small subset (2 samples per circuit)
python test_small_sweep.py

# Generate full dataset (225 samples total)
python sweeper.py

# Convert to different formats
python assemble_dataset.py     # Convert to JSONL and CSV formats
python data_diagnostics.py     # Analyze parameter space coverage
```

## Future Work
1. **Fix opamp upstream bug**: Resolve the c_route port naming issue in the output stage
2. **Add more circuits**: Extend to additional analog building blocks
3. **Parameter optimization**: Fine-tune parameter ranges based on evaluation results
4. **Evaluation metrics**: Enhance the evaluation wrapper with more comprehensive metrics

The pipeline now supports 5 different analog circuit types with comprehensive parameter sampling using Latin Hypercube Sampling with maximin optimization.
