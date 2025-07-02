#!/bin/bash

# Master dataset generation pipeline
# This script runs the complete LHS dataset generation process

set -e  # Exit on any error

echo "=============================================="
echo "LHS DATASET GENERATION PIPELINE"
echo "=============================================="
echo "Start time: $(date)"
echo ""

# Ensure we're in the right directory
cd /home/arnavshukla/OpenFASOC/openfasoc/generators/glayout/glayout/flow/blocks/elementary/LHS

# Activate conda environment and set PDK_ROOT
echo "Setting up environment..."
source /opt/conda/etc/profile.d/conda.sh
conda activate GLdev
export PDK_ROOT=/opt/conda/envs/GLdev/share/pdk

echo "✓ Conda environment activated: $CONDA_DEFAULT_ENV"
echo "✓ PDK_ROOT set: $PDK_ROOT"
echo ""

# Check if sweep_outputs exists, if not create it
mkdir -p sweep_outputs

# Step 1: Generate LHS samples
echo "Step 1: Generating LHS parameter samples..."
python -c "
from elhs import all_samples
print('LHS sample generation completed!')
print('Sample counts:')
for pcell, samples in all_samples.items():
    print(f'  {pcell}: {len(samples)} samples')
total = sum(len(samples) for samples in all_samples.values())
print(f'Total samples: {total}')
"
echo ""

# Step 2: Run enhanced sweeper with logging and checkpointing
echo "Step 2: Running enhanced sweeper (main dataset generation)..."
echo "This is the longest step - generating GDS files and running evaluations"
echo "Progress will be logged to sweep_outputs/dataset_generation.log"
echo ""

python enhanced_sweeper.py

# Check if sweeper completed successfully
if [ $? -eq 0 ]; then
    echo "✓ Enhanced sweeper completed successfully"
else
    echo "✗ Enhanced sweeper failed"
    exit 1
fi

# Step 3: Assemble dataset into different formats
echo ""
echo "Step 3: Assembling dataset into JSONL and CSV formats..."
python assemble_dataset.py

if [ $? -eq 0 ]; then
    echo "✓ Dataset assembly completed"
else
    echo "✗ Dataset assembly failed"
    exit 1
fi

# Step 4: Run data diagnostics
echo ""
echo "Step 4: Running data quality diagnostics..."
python data_diagnostics.py

if [ $? -eq 0 ]; then
    echo "✓ Data diagnostics completed"
else
    echo "✗ Data diagnostics failed"
    exit 1
fi

# Step 5: Generate final summary
echo ""
echo "Step 5: Generating final summary..."
python -c "
import json
import os
from datetime import datetime

# Load final results
results_file = 'sweep_outputs/sweep_results.json'
if os.path.exists(results_file):
    with open(results_file, 'r') as f:
        results = json.load(f)
    
    print('FINAL DATASET SUMMARY')
    print('='*50)
    print(f'Generation completed: {datetime.now().strftime(\"%Y-%m-%d %H:%M:%S\")}')
    print(f'Total samples: {len(results)}')
    
    # Success statistics
    successful = [r for r in results if r.get('success', False)]
    failed = [r for r in results if not r.get('success', False)]
    
    print(f'Successful: {len(successful)}')
    print(f'Failed: {len(failed)}')
    print(f'Success rate: {len(successful)/len(results)*100:.1f}%')
    
    # Breakdown by circuit
    print('')
    print('Breakdown by circuit:')
    circuit_stats = {}
    for result in results:
        circuit = result['pcell']
        if circuit not in circuit_stats:
            circuit_stats[circuit] = {'success': 0, 'fail': 0}
        if result.get('success', False):
            circuit_stats[circuit]['success'] += 1
        else:
            circuit_stats[circuit]['fail'] += 1
    
    for circuit, stats in sorted(circuit_stats.items()):
        total = stats['success'] + stats['fail']
        rate = stats['success'] / total * 100 if total > 0 else 0
        print(f'  {circuit}: {stats[\"success\"]}/{total} ({rate:.1f}%)')
    
    # File sizes
    print('')
    print('Generated files:')
    files_to_check = [
        'sweep_outputs/sweep_results.json',
        'sweep_outputs/sweep_results.jsonl', 
        'sweep_outputs/sweep_results.csv'
    ]
    
    for filepath in files_to_check:
        if os.path.exists(filepath):
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f'  {filepath}: {size_mb:.1f} MB')
        else:
            print(f'  {filepath}: NOT FOUND')
            
else:
    print('ERROR: Results file not found!')
"

echo ""
echo "=============================================="
echo "PIPELINE COMPLETION"
echo "=============================================="
echo "End time: $(date)"

# Display final file listing
echo ""
echo "Generated files in sweep_outputs/:"
ls -lh sweep_outputs/ | grep -v "^total"

echo ""
echo "Dataset generation pipeline completed successfully! 🎉"
echo ""
echo "Next steps:"
echo "1. Review sweep_outputs/dataset_generation.log for detailed logs"
echo "2. Examine sweep_outputs/sweep_results.csv for the tabular dataset"
echo "3. Use sweep_outputs/sweep_results.jsonl for streaming processing"
echo "4. Check data_diagnostics output for parameter space coverage analysis"
