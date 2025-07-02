# LHS Dataset Extension Summary

This document summarizes the modifications made to include **lvcm** (Low Voltage Current Mirror) and prepare for **opamp** circuits in the LHS dataset generation pipeline. Note: opamp is temporarily disabled due to upstream implementation issues.

## File Structure and Roles

### Core Parameter Generation
- **`elhs.py`** - Enhanced Latin Hypercube Sampling implementation with parameter specifications for all circuit types
- **`elementary_inventory.py`** - Circuit inventory and parameter definitions

### Circuit Implementations
- **`fvf.py`** - Flipped Voltage Follower circuit with labeling
- **`transmission_gate.py`** - Transmission gate (txgate) circuit implementation
- **`current_mirror.py`** - Current mirror circuit generator
- **`diff_pair.py`** - Differential pair circuit implementation
- **`lvcm.py`** - Low Voltage Current Mirror circuit
- **`opamp.py`** - Operational amplifier (currently disabled due to upstream bugs)

### Dataset Generation Engines
- **`sweeper.py`** - Parallel processing sweeper for large-scale dataset generation
- **`sequential_sweeper.py`** - Sequential processing sweeper to avoid file conflicts
- **`enhanced_sweeper.py`** - Enhanced version with better error handling and progress tracking

### Evaluation Framework
- **`evaluator_wrapper.py`** - Main evaluation coordinator that runs DRC, LVS, PEX, and geometric analysis
- **`evaluator_box/`** - Comprehensive evaluation modules:
  - **`verification.py`** - DRC and LVS verification using Magic VLSI and Netgen
  - **`physical_features.py`** - PEX extraction, area calculation, and symmetry analysis
  - **`evaluator_wrapper.py`** - Backup evaluator wrapper

### Dataset Processing and Analysis
- **`assemble_dataset.py`** - Converts raw JSON results to structured JSONL and CSV formats
- **`dataset_curator.py`** - Quality control and data validation for generated datasets
- **`data_diagnostics.py`** - Comprehensive analysis of parameter space coverage and dataset quality

### Testing and Validation
- **`simple_test.py`** - Basic functionality tests for individual circuits
- **`run_fvf.py`** - Standalone FVF circuit testing
- **`test_output/`** - Directory containing test results and validation data

### Infrastructure and Configuration
- **`sky130A.magicrc`** - Magic VLSI configuration file for SKY130 PDK
- **`run_pex.sh`** - Shell script for parasitic extraction using Magic VLSI
- **`evaluator_box/run_pex.sh`** - Backup PEX script
- **`run_full_pipeline.sh`** - Complete pipeline execution script

### Output Directories
- **`sweep_outputs/`** - Results from parallel sweep operations
- **`sequential_outputs/`** - Results from sequential processing (created during execution)
- **`__pycache__/`** - Python bytecode cache

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

# Activate environment and set PDK
conda activate GLdev
export PDK_ROOT=/opt/conda/envs/GLdev/share/pdk

# Test small subset (2 samples per circuit)
python simple_test.py

# Generate full dataset - Sequential approach (recommended)
python sequential_sweeper.py

# Generate full dataset - Parallel approach (may have file conflicts)
python sweeper.py

# Convert to different formats
python assemble_dataset.py     # Convert to JSONL and CSV formats
python dataset_curator.py      # Quality control and validation
python data_diagnostics.py     # Analyze parameter space coverage
```

## Current Dataset Generation Status (July 2025)

**✅ Successfully Running Sequential Dataset Generation**

**Progress:** 17/465 samples completed (3.7%) as of latest check
- Currently processing FVF block (17/60 samples completed)
- Processing rate: ~12 seconds per sample
- Estimated completion time: ~90 minutes total

**Working Features:**
- ✅ Sequential processing eliminates file conflicts
- ✅ GDS file generation for all circuit types
- ✅ Geometric feature extraction (area, symmetry scores)
- ✅ PEX (parasitic extraction) using Magic VLSI
- ✅ Environment setup with Magic and Netgen tools

**Known Issues:**
- ❌ DRC/LVS verification fails after first sample due to PDK path reset
  - First sample (fvf_0) contains complete DRC/LVS data
  - Subsequent samples collect geometric + PEX data only
  - Can be addressed later if comprehensive verification data needed

**Sample Distribution:**
- **fvf**: 60 samples (currently processing)
- **txgate**: 60 samples  
- **current_mirror**: 30 samples
- **diff_pair**: 30 samples
- **lvcm**: 45 samples
- **opamp**: 240 samples (prepared but disabled)
- **Total Active**: 225 samples
- **Total Planned**: 465 samples (when opamp is enabled)

## Pipeline Workflow

1. **Parameter Generation** (`elhs.py`)
   - Latin Hypercube Sampling with maximin optimization
   - Circuit-specific parameter specifications
   - Mixed continuous/discrete parameter handling

2. **Circuit Instantiation** (circuit-specific `.py` files)
   - Generate GDS layouts using glayout library
   - Apply proper labeling for verification

3. **Comprehensive Evaluation** (`evaluator_wrapper.py`)
   - DRC verification using Magic VLSI
   - LVS verification using Netgen
   - PEX extraction for parasitics
   - Geometric analysis (area, symmetry)

4. **Data Assembly** (`assemble_dataset.py`)
   - Collect all JSON results
   - Convert to structured formats (JSONL, CSV)
   - Organize by circuit type

5. **Quality Control** (`dataset_curator.py`)
   - Validate data completeness
   - Check for anomalies
   - Generate quality reports

6. **Analysis** (`data_diagnostics.py`)
   - Parameter space coverage analysis
   - Statistical summaries
   - Visualization of dataset characteristics

## Dataset Structure and Metrics

Each generated sample contains comprehensive evaluation data:

### Core Identification
- **component_name**: Unique identifier (e.g., "fvf_0", "txgate_15")
- **timestamp**: Generation timestamp
- **parameters**: Circuit-specific parameter values used

### Design Rule Check (DRC)
- **status**: "pass"/"fail"/"error"
- **is_pass**: Boolean DRC result
- **report_path**: Path to detailed DRC report
- **summary**: Parsed violation details with rule names and coordinates

### Layout vs Schematic (LVS)
- **status**: "pass"/"fail"/"error"  
- **is_pass**: Boolean LVS result
- **report_path**: Path to detailed LVS report
- **summary**: Net/device mismatch analysis and comparison results

### Parasitic Extraction (PEX)
- **status**: "PEX Complete"/"PEX Error"
- **total_resistance_ohms**: Cumulative parasitic resistance
- **total_capacitance_farads**: Cumulative parasitic capacitance

### Geometric Features
- **raw_area_um2**: Total layout area in square micrometers
- **symmetry_score_horizontal**: Horizontal symmetry metric (0-1, 1=perfect)
- **symmetry_score_vertical**: Vertical symmetry metric (0-1, 1=perfect)

### Processing Metadata
- **evaluation_time**: Processing time in seconds
- **gds_path**: Path to generated GDS file
- **drc_lvs_fail**: Combined DRC/LVS failure flag

## Sample JSON Structure
```json
{
    "component_name": "fvf_0",
    "timestamp": "2025-07-01T21:12:22.624098",
    "drc_lvs_fail": true,
    "drc": {
        "status": "fail",
        "is_pass": false,
        "report_path": "/.../fvf_0.drc.rpt",
        "summary": {
            "is_pass": false,
            "total_errors": 27,
            "error_details": [...]
        }
    },
    "lvs": {
        "status": "fail", 
        "is_pass": false,
        "report_path": "/.../fvf_0.lvs.rpt",
        "summary": {...}
    },
    "pex": {
        "status": "PEX Complete",
        "total_resistance_ohms": 245.7,
        "total_capacitance_farads": 1.23e-14
    },
    "geometric": {
        "raw_area_um2": 5550.78,
        "symmetry_score_horizontal": 0.679,
        "symmetry_score_vertical": 0.986
    }
}
