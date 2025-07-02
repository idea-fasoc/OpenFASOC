#!/usr/bin/env python3

"""Enhanced sweeper with checkpointing and detailed logging"""

import os
import sys
import json
import time
import logging
import random
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime

# Import circuit functions and data
from elhs import all_samples
from sweeper import PCELL_FUNCS, sky130_mapped_pdk, run_evaluation

# Enhanced configuration
OUTPUT_DIR = "sweep_outputs"
CHECKPOINT_FILE = os.path.join(OUTPUT_DIR, "checkpoint.json")
LOG_FILE = os.path.join(OUTPUT_DIR, "dataset_generation.log")
PROGRESS_FILE = os.path.join(OUTPUT_DIR, "progress.json")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Configure enhanced logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

def save_checkpoint(results, completed_tasks, total_tasks):
    """Save current progress to checkpoint file"""
    checkpoint_data = {
        "timestamp": datetime.now().isoformat(),
        "completed_tasks": completed_tasks,
        "total_tasks": total_tasks,
        "completion_percentage": (completed_tasks / total_tasks) * 100,
        "results": results
    }
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump(checkpoint_data, f, indent=2)
    
    # Also save progress summary
    progress_data = {
        "timestamp": datetime.now().isoformat(),
        "completed": completed_tasks,
        "total": total_tasks,
        "percentage": round((completed_tasks / total_tasks) * 100, 2),
        "by_pcell": {}
    }
    
    # Count by pcell
    for result in results:
        pcell = result.get("pcell", "unknown")
        if pcell not in progress_data["by_pcell"]:
            progress_data["by_pcell"][pcell] = {"completed": 0, "failed": 0, "total": 0}
        progress_data["by_pcell"][pcell]["total"] += 1
        if result.get("report") is not None:
            progress_data["by_pcell"][pcell]["completed"] += 1
        else:
            progress_data["by_pcell"][pcell]["failed"] += 1
    
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress_data, f, indent=2)

def load_checkpoint():
    """Load previous checkpoint if exists"""
    if os.path.exists(CHECKPOINT_FILE):
        try:
            with open(CHECKPOINT_FILE, "r") as f:
                data = json.load(f)
            logging.info(f"Loaded checkpoint: {data['completed_tasks']}/{data['total_tasks']} tasks completed")
            return data.get("results", [])
        except Exception as e:
            logging.warning(f"Failed to load checkpoint: {e}")
    return []

def run_task_enhanced(pcell, idx, params, retry=2):
    """Enhanced task runner with better error handling and timing"""
    comp_name = f"{pcell}_{idx}"
    task_start = time.time()
    
    for attempt in range(1, retry + 2):
        try:
            # Create component
            comp_start = time.time()
            comp = PCELL_FUNCS[pcell](sky130_mapped_pdk, **params)
            comp.name = comp_name
            comp_time = time.time() - comp_start
            
            # Write GDS
            gds_start = time.time()
            gds_path = os.path.join(OUTPUT_DIR, f"{comp_name}.gds")
            comp.write_gds(gds_path)
            gds_time = time.time() - gds_start
            
            # Run evaluation
            eval_start = time.time()
            report = run_evaluation(gds_path, comp_name, comp)
            eval_time = time.time() - eval_start
            
            total_time = time.time() - task_start
            
            logging.info(f"✓ {comp_name} SUCCESS (attempt {attempt}) - "
                        f"Total: {total_time:.1f}s (Comp: {comp_time:.1f}s, GDS: {gds_time:.1f}s, Eval: {eval_time:.1f}s)")
            
            return {
                "pcell": pcell,
                "index": idx,
                "params": params,
                "report": report,
                "timing": {
                    "total": total_time,
                    "component": comp_time,
                    "gds": gds_time,
                    "evaluation": eval_time
                },
                "attempts": attempt,
                "success": True
            }
            
        except Exception as e:
            attempt_time = time.time() - task_start
            logging.error(f"✗ {comp_name} FAILED (attempt {attempt}) after {attempt_time:.1f}s: {e}")
            
            if attempt <= retry:
                logging.info(f"↻ Retrying {comp_name} (attempt {attempt + 1})")
                time.sleep(1)  # Brief delay before retry
            else:
                total_time = time.time() - task_start
                logging.error(f"✗ {comp_name} FINAL FAILURE after {retry + 1} attempts ({total_time:.1f}s)")
                return {
                    "pcell": pcell,
                    "index": idx,
                    "params": params,
                    "report": None,
                    "error": str(e),
                    "timing": {"total": total_time},
                    "attempts": retry + 1,
                    "success": False
                }

def estimate_runtime():
    """Estimate total runtime based on sample counts"""
    total_samples = sum(len(samples) for samples in all_samples.values())
    
    # Rough estimates based on test runs (in seconds per sample)
    time_estimates = {
        'fvf': 10,
        'txgate': 120,  # Slowest from our tests
        'current_mirror': 8,
        'diff_pair': 5,
        'opamp': 15,  # Conservative estimate
        'lvcm': 60
    }
    
    total_estimated_time = 0
    for pcell, samples in all_samples.items():
        estimated_time = len(samples) * time_estimates.get(pcell, 30)
        total_estimated_time += estimated_time
        logging.info(f"  {pcell}: {len(samples)} samples × {time_estimates.get(pcell, 30)}s = {estimated_time/60:.1f} min")
    
    # Account for parallelization (assuming 26 workers)
    parallel_time = total_estimated_time / 26
    
    logging.info(f"Total estimated sequential time: {total_estimated_time/3600:.1f} hours")
    logging.info(f"Total estimated parallel time (26 workers): {parallel_time/3600:.1f} hours")
    
    return parallel_time

def main():
    """Main dataset generation function"""
    logging.info("="*80)
    logging.info("STARTING DATASET GENERATION")
    logging.info("="*80)
    
    # Log sample counts and estimate runtime
    logging.info("Sample counts by PCell:")
    for pcell, samples in all_samples.items():
        logging.info(f"  {pcell}: {len(samples)} samples")
    
    total_samples = sum(len(samples) for samples in all_samples.values())
    logging.info(f"Total samples to generate: {total_samples}")
    
    # Estimate runtime
    logging.info("\nRuntime estimation:")
    estimated_time = estimate_runtime()
    
    # Load any existing checkpoint
    existing_results = load_checkpoint()
    completed_task_ids = {(r["pcell"], r["index"]) for r in existing_results}
    
    # Build task list
    tasks = []
    for pcell, samples in all_samples.items():
        for idx, params in enumerate(samples):
            if (pcell, idx) not in completed_task_ids:
                tasks.append((pcell, idx, params))
    
    if existing_results:
        logging.info(f"Resuming from checkpoint: {len(existing_results)} tasks already completed")
        logging.info(f"Remaining tasks: {len(tasks)}")
    
    # Shuffle for load balancing
    random.seed(42)  # Reproducible shuffle
    random.shuffle(tasks)
    
    results = existing_results.copy()
    start_time = time.time()
    
    logging.info(f"\nStarting parallel execution with {min(26, len(tasks))} workers...")
    
    # Execute tasks in parallel
    with ProcessPoolExecutor(max_workers=26) as executor:
        futures = {
            executor.submit(run_task_enhanced, pcell, idx, params): (pcell, idx)
            for pcell, idx, params in tasks
        }
        
        completed_count = len(existing_results)
        total_count = total_samples
        
        for fut in as_completed(futures):
            try:
                result = fut.result()
                results.append(result)
                completed_count += 1
                
                # Log progress every 10 completions
                if completed_count % 10 == 0:
                    elapsed = time.time() - start_time
                    rate = completed_count / elapsed if elapsed > 0 else 0
                    eta = (total_count - completed_count) / rate if rate > 0 else 0
                    
                    logging.info(f"Progress: {completed_count}/{total_count} ({completed_count/total_count*100:.1f}%) - "
                               f"Rate: {rate:.1f} tasks/min - ETA: {eta/60:.1f} min")
                
                # Save checkpoint every 25 completions
                if completed_count % 25 == 0:
                    save_checkpoint(results, completed_count, total_count)
                    logging.info(f"Checkpoint saved at {completed_count} completed tasks")
                    
            except Exception as e:
                logging.error(f"Future failed: {e}")
                pcell, idx = futures[fut]
                results.append({
                    "pcell": pcell,
                    "index": idx,
                    "error": f"Future failed: {e}",
                    "success": False
                })
                completed_count += 1
    
    # Final save
    total_time = time.time() - start_time
    save_checkpoint(results, completed_count, total_count)
    
    # Save final results
    final_results_file = os.path.join(OUTPUT_DIR, "sweep_results.json")
    with open(final_results_file, "w") as f:
        json.dump(results, f, indent=2)
    
    # Generate summary statistics
    successful = sum(1 for r in results if r.get("success", False))
    failed = len(results) - successful
    
    logging.info("="*80)
    logging.info("DATASET GENERATION COMPLETED")
    logging.info("="*80)
    logging.info(f"Total time: {total_time/3600:.2f} hours")
    logging.info(f"Total samples: {len(results)}")
    logging.info(f"Successful: {successful}")
    logging.info(f"Failed: {failed}")
    logging.info(f"Success rate: {successful/len(results)*100:.1f}%")
    logging.info(f"Results saved to: {final_results_file}")
    
    # Success breakdown by PCell
    logging.info("\nSuccess breakdown by PCell:")
    pcell_stats = {}
    for result in results:
        pcell = result["pcell"]
        if pcell not in pcell_stats:
            pcell_stats[pcell] = {"success": 0, "fail": 0}
        if result.get("success", False):
            pcell_stats[pcell]["success"] += 1
        else:
            pcell_stats[pcell]["fail"] += 1
    
    for pcell, stats in pcell_stats.items():
        total = stats["success"] + stats["fail"]
        success_rate = stats["success"] / total * 100 if total > 0 else 0
        logging.info(f"  {pcell}: {stats['success']}/{total} ({success_rate:.1f}%)")

if __name__ == "__main__":
    # Seed for reproducibility
    random.seed(42)
    main()
