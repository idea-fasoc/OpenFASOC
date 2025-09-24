# Dataset Generation Setup Guide

This guide provides step-by-step instructions for setting up the environment and generating datasets for analog circuit components using the Glayout framework.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Installation Steps](#installation-steps)
- [Dataset Generation](#dataset-generation)
- [Available Generators](#available-generators)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before starting, ensure you have:
- Python 3.10 or later
- Conda package manager
- Git
- Access to PDK files (Process Design Kit)

## Environment Setup

### 1. Create and Activate Conda Environment

Create a new conda environment named `GLdev`:

```bash
# Create conda environment
conda create -n GLdev python=3.10

# Activate the environment
conda activate GLdev
```

### 2. Install Glayout Package

Navigate to the glayout directory and install in development mode:

```bash
# Navigate to the glayout directory
cd /path/to/OpenFASOC/openfasoc/generators/glayout

# Install glayout in development mode
pip install -e .
```

### 3. Install Core Dependencies

Install the core requirements:

```bash
# Install core dependencies
pip install -r requirements.txt
```

The core dependencies include:
- `gdsfactory>=7.16.0,<7.17`
- `numpy!=1.24.0,>=1.20`
- `prettyprint`
- `prettyprinttree`
- `gdstk`

### 4. Install ML Dependencies (Optional)

For machine learning features, install additional requirements:

```bash
# Install ML dependencies
pip install -r requirements.ml.txt
```

The ML dependencies include:
- `torch`
- `transformers`
- `langchain`
- `chromadb`
- `sentence-transformers`
- And other ML-related packages

### 5. Setup PDK Environment

Set up the Process Design Kit environment variable:

```bash
# Set PDK_ROOT environment variable
export PDK_ROOT=/opt/conda/envs/GLdev/share/pdk
```

**Note**: Add this line to your `~/.bashrc` or `~/.zshrc` to make it persistent:

```bash
echo "export PDK_ROOT=/opt/conda/envs/GLdev/share/pdk" >> ~/.bashrc
source ~/.bashrc
```

## Installation Steps

### Complete Setup Script

You can run all the setup commands in sequence:

```bash
# 1. Create and activate conda environment
conda create -n GLdev python=3.10
conda activate GLdev

# 2. Navigate to glayout directory
cd /path/to/OpenFASOC/openfasoc/generators/glayout

# 3. Install glayout in development mode
pip install -e .

# 4. Install dependencies
pip install -r requirements.txt
pip install -r requirements.ml.txt  # Optional for ML features

# 5. Set PDK environment
export PDK_ROOT=/opt/conda/envs/GLdev/share/pdk

# 6. Navigate to LHS directory
cd glayout/flow/blocks/elementary/LHS

# 7. Setup execution permissions
chmod +x run_pex.sh
chmod +x getStarted.sh
```

## Dataset Generation

### 1. Navigate to LHS Directory

```bash
cd /path/to/OpenFASOC/openfasoc/generators/glayout/glayout/flow/blocks/elementary/LHS
```

### 2. Run Initial Setup

Execute the startup script:

```bash
# Activate conda environment
conda activate GLdev

# Set PDK_ROOT
export PDK_ROOT=/opt/conda/envs/GLdev/share/pdk

# Make scripts executable
chmod +x run_pex.sh
```

### 3. Generate Datasets

The LHS directory contains pre-generated parameters in the `gen_params_8h_runtime_aware` folder for different circuit components:

- `current_mirror_params.json`
- `diff_pair_params.json`
- `fvf_params.json`
- `lvcm_params.json`
- `opamp_params.json`
- `txgate_params.json`

#### Generate Transmission Gate Dataset

```bash
python generate_tg_1000_dataset.py
# or
python generate_tg_200_dataset.py
# or 
python generate_tg_100_dataset.py
```

#### Generate FVF (Flipped Voltage Follower) Dataset

```bash
python generate_fvf_8h_runtime_aware.py
# or
python generate_fvf_360_robust.py
```

#### Generate Op-Amp Dataset

```bash
python generate_opamp_dataset.py
# or
python generate_opamp_5_samples.py
```

#### Generate Differential Pair Dataset

```bash
python generate_diff_pair_dataset.py
```

#### Generate Current Mirror Dataset

```bash
python generate_current_mirror_3164_dataset.py
```

## Available Generators

The following generator scripts are available in the LHS directory:

| Generator Script | Circuit Type | Parameter File | Output Dataset |
|------------------|--------------|----------------|----------------|
| `generate_tg_1000_dataset.py` | Transmission Gate | `txgate_params.json` | `tg_dataset_1000_lhs/` |
| `generate_fvf_8h_runtime_aware.py` | Flipped Voltage Follower | `fvf_params.json` | `fvf_dataset_8h_runtime_aware/` |
| `generate_opamp_dataset.py` | Operational Amplifier | `opamp_params.json` | `opamp_dataset_250/` |
| `generate_diff_pair_dataset.py` | Differential Pair | `diff_pair_params.json` | `diff_pair_dataset_1800_lhs/` |
| `generate_current_mirror_3164_dataset.py` | Current Mirror | `current_mirror_params.json` | `cm_dataset_3164_lhs/` |

## Usage Example

Here's a complete workflow example:

```bash
# 1. Activate environment
conda activate GLdev

# 2. Set environment variables
export PDK_ROOT=/opt/conda/envs/GLdev/share/pdk

# 3. Navigate to LHS directory
cd /path/to/OpenFASOC/openfasoc/generators/glayout/glayout/flow/blocks/elementary/LHS

# 4. Make scripts executable
chmod +x run_pex.sh

# 5. Generate transmission gate dataset with 1000 samples
python generate_tg_1000_dataset.py

# 6. Generate FVF dataset
python generate_fvf_8h_runtime_aware.py

# 7. Generate op-amp dataset
python generate_opamp_dataset.py
```

## Output Structure

Generated datasets are stored in their respective directories:

```
LHS/
├── tg_dataset_1000_lhs/          # Transmission gate samples
├── fvf_dataset_8h_runtime_aware/ # FVF samples
├── opamp_dataset_250/            # Op-amp samples
├── diff_pair_dataset_1800_lhs/   # Differential pair samples
└── cm_dataset_3164_lhs/          # Current mirror samples
```

Each dataset directory contains:
- Individual JSON parameter files
- Generated layout files (GDS format)
- Simulation results
- Performance metrics

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Make sure you're in the GLdev environment
   conda activate GLdev
   
   # Reinstall dependencies
   pip install -r requirements.txt
   ```

2. **PDK Path Issues**
   ```bash
   # Verify PDK_ROOT is set correctly
   echo $PDK_ROOT
   
   # Reset if needed
   export PDK_ROOT=/opt/conda/envs/GLdev/share/pdk
   ```

3. **Permission Errors**
   ```bash
   # Make scripts executable
   chmod +x run_pex.sh
   chmod +x getStarted.sh
   ```

4. **Memory Issues**
   - For large datasets, consider running smaller batches
   - Monitor system memory usage during generation

### Verification

To verify your setup is working:

```bash
# Test with a small sample
python generate_tg_5_samples.py

# Check if output directory is created
ls -la tg_dataset_*
```

## Notes

- Dataset generation can be time-intensive depending on the number of samples
- Ensure sufficient disk space for large datasets
- The generation process includes layout synthesis and performance extraction
- Parameters are pre-optimized using Latin Hypercube Sampling (LHS) for design space exploration

## Support

For issues or questions:
- Check the main OpenFASOC documentation
- Review the glayout README.md for API details
- Ensure all dependencies are correctly installed
