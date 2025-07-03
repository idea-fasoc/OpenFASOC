#!/usr/bin/env python3

"""Sequential sweeper for dataset generation - processes one block at a time"""

import os
import sys
import json
import time
import logging
import shutil
import subprocess
from datetime import datetime

def setup_environment():
    """Setup the conda environment and PDK paths"""
    # Check if we're in the GLdev environment
    conda_env = os.environ.get('CONDA_DEFAULT_ENV', '')
    print(f"Current conda environment: {conda_env}")
    
     # 1. Handle PDK_ROOT existence and value
    pdk_root = os.environ.get('PDK_ROOT')
    default_path = '/opt/conda/envs/GLdev/share/pdk'
    
    # Case 1: Missing or literal 'None'
    if not pdk_root or str(pdk_root).strip().lower() == 'none':
        logging.warning(f"Invalid PDK_ROOT: '{pdk_root}'. Setting to default: {default_path}")
        os.environ['PDK_ROOT'] = default_path
        pdk_root = default_path
    
    # 2. Verify directory structure
    required_files = {
        'magic': 'sky130A/libs.tech/magic/sky130A.tech',
        'netgen': 'sky130A/libs.tech/netgen/setup.tcl'
    }
    
    missing_files = []
    for tool, rel_path in required_files.items():
        abs_path = os.path.join(pdk_root, rel_path)
        if not os.path.exists(abs_path):
            missing_files.append(abs_path)
    
    if missing_files:
        logging.error(f"Missing critical PDK files:\n- " + "\n- ".join(missing_files))
        if pdk_root != default_path:
            logging.info(f"Attempting fallback to default PDK: {default_path}")
            os.environ['PDK_ROOT'] = default_path
            return setup_pdk_environment()  # Recursively verify default path
        raise FileNotFoundError(f"PDK files missing in both {pdk_root} and default location")
    
    # Check if tools are available
    magic_path = subprocess.run(['which', 'magic'], capture_output=True, text=True)
    netgen_path = subprocess.run(['which', 'netgen'], capture_output=True, text=True)
    
    print(f"Magic path: {magic_path.stdout.strip() if magic_path.returncode == 0 else 'NOT FOUND'}")
    print(f"Netgen path: {netgen_path.stdout.strip() if netgen_path.returncode == 0 else 'NOT FOUND'}")
    
    return magic_path.returncode == 0 and netgen_path.returncode == 0

# Import circuit functions and data
from elhs import all_samples
from sweeper import PCELL_FUNCS, sky130_mapped_pdk, run_evaluation

# Configuration
OUTPUT_DIR = "sequential_outputs"
LOG_FILE = os.path.join(OUTPUT_DIR, "sequential_generation.log")
RESULTS_FILE = os.path.join(OUTPUT_DIR, "all_results.json")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

def cleanup_temp_files():
    """Clean up temporary files between evaluations"""
    temp_extensions = ['.gds', '.mag', '.drc.rpt', '.lvs.rpt', '.nodes', '.res.ext', '.sim']
    current_dir = os.getcwd()
    
    for file in os.listdir(current_dir):
        if any(file.endswith(ext) for ext in temp_extensions):
            try:
                os.remove(file)
                logging.debug(f"Cleaned up temp file: {file}")
            except Exception as e:
                logging.warning(f"Could not remove {file}: {e}")

def run_single_evaluation(pcell, idx, params):
    """Run a single evaluation with proper cleanup"""
    comp_name = f"{pcell}_{idx}"
    task_start = time.time()
    
    try:
        # Clean up before starting
        cleanup_temp_files()
        
        # Create component
        logging.info(f"Creating component {comp_name}")
        comp = PCELL_FUNCS[pcell](sky130_mapped_pdk, **params)
        comp.name = comp_name
        
        # Write GDS
        gds_path = os.path.join(OUTPUT_DIR, f"{comp_name}.gds")
        comp.write_gds(gds_path)
        logging.info(f"GDS written to {gds_path}")
        
        # Run evaluation
        logging.info(f"Running evaluation for {comp_name}")
        report = run_evaluation(gds_path, comp_name, comp)
        
        # Calculate timing
        task_time = time.time() - task_start
        
        # Prepare result
        result = {
            "pcell": pcell,
            "index": idx,
            "component_name": comp_name,
            "parameters": params,
            "report": report,
            "evaluation_time": round(task_time, 2),
            "timestamp": datetime.now().isoformat(),
            "gds_path": gds_path
        }
        
        logging.info(f"✅ {comp_name} completed in {task_time:.2f}s")
        return result
        
    except Exception as e:
        logging.error(f"❌ {comp_name} failed: {str(e)}")
        return {
            "pcell": pcell,
            "index": idx,
            "component_name": comp_name,
            "parameters": params,
            "report": None,
            "error": str(e),
            "evaluation_time": time.time() - task_start,
            "timestamp": datetime.now().isoformat()
        }
    finally:
        # Clean up temp files after each evaluation
        cleanup_temp_files()

def save_results(results, pcell_name=None):
    """Save results to file"""
    if pcell_name:
        pcell_file = os.path.join(OUTPUT_DIR, f"{pcell_name}_results.json")
        with open(pcell_file, "w") as f:
            json.dump(results, f, indent=2)
        logging.info(f"Saved {len(results)} results for {pcell_name}")
    
    # Also append to master results file
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "r") as f:
            all_results = json.load(f)
    else:
        all_results = []
    
    all_results.extend(results)
    with open(RESULTS_FILE, "w") as f:
        json.dump(all_results, f, indent=2)

def process_pcell_sequentially(pcell, samples):
    """Process all samples for one pcell sequentially"""
    logging.info(f"\n🔄 Starting {pcell} - {len(samples)} samples")
    pcell_start = time.time()
    
    results = []
    successful = 0
    failed = 0
    
    for idx, params in enumerate(samples):
        logging.info(f"Progress: {idx+1}/{len(samples)} for {pcell}")
        
        result = run_single_evaluation(pcell, idx, params)
        results.append(result)
        
        if result.get("report") is not None:
            successful += 1
        else:
            failed += 1
        
        # Save intermediate results every 10 samples
        if (idx + 1) % 10 == 0:
            save_results(results, pcell)
    
    # Final save for this pcell
    save_results(results, pcell)
    
    pcell_time = time.time() - pcell_start
    logging.info(f"✅ {pcell} completed: {successful} successful, {failed} failed in {pcell_time/60:.1f} minutes")
    
    return results

def main():
    """Main sequential processing function"""
    logging.info("🚀 Starting Sequential Dataset Generation")
    
    # Setup environment first
    if not setup_environment():
        logging.error("❌ Environment setup failed. Make sure Magic and Netgen are available.")
        logging.error("Try: conda activate GLdev")
        sys.exit(1)
    
    logging.info(f"Output directory: {OUTPUT_DIR}")
    
    total_start = time.time()
    all_results = []
    
    # Process blocks in order of complexity (simplest first)
    processing_order = ['fvf', 'txgate', 'current_mirror', 'diff_pair', 'lvcm', 'opamp']
    
    for pcell in processing_order:
        if pcell in all_samples:
            samples = all_samples[pcell]
            logging.info(f"\n📊 Processing {pcell}: {len(samples)} samples")
            
            pcell_results = process_pcell_sequentially(pcell, samples)
            all_results.extend(pcell_results)
        else:
            logging.warning(f"⚠️  No samples found for {pcell}")
    
    # Final cleanup and summary
    total_time = time.time() - total_start
    total_successful = sum(1 for r in all_results if r.get("report") is not None)
    total_failed = len(all_results) - total_successful
    
    summary = {
        "total_samples": len(all_results),
        "successful": total_successful,
        "failed": total_failed,
        "success_rate": round((total_successful / len(all_results)) * 100, 2) if all_results else 0,
        "total_time_minutes": round(total_time / 60, 2),
        "timestamp": datetime.now().isoformat(),
        "by_pcell": {}
    }
    
    # Calculate per-pcell statistics
    for pcell in processing_order:
        pcell_results = [r for r in all_results if r["pcell"] == pcell]
        if pcell_results:
            pcell_successful = sum(1 for r in pcell_results if r.get("report") is not None)
            summary["by_pcell"][pcell] = {
                "total": len(pcell_results),
                "successful": pcell_successful,
                "failed": len(pcell_results) - pcell_successful,
                "success_rate": round((pcell_successful / len(pcell_results)) * 100, 2)
            }
    
    # Save final summary
    summary_file = os.path.join(OUTPUT_DIR, "generation_summary.json")
    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=2)
    
    logging.info(f"\n🎉 Dataset Generation Complete!")
    logging.info(f"📈 Summary: {total_successful}/{len(all_results)} successful ({summary['success_rate']}%)")
    logging.info(f"⏱️  Total time: {total_time/60:.1f} minutes")
    logging.info(f"📄 Results saved to: {RESULTS_FILE}")
    logging.info(f"📊 Summary saved to: {summary_file}")

if __name__ == "__main__":
    main()
