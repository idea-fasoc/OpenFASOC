#!/usr/bin/env python3
"""
Generate comprehensive statistics for the LHS dataset
"""

import json
from pathlib import Path

def analyze_dataset():
    """Analyze the complete LHS dataset"""
    results_file = Path("lhs_dataset_robust/lhs_results.json")
    
    with open(results_file, 'r') as f:
        results = json.load(f)
    
    total_samples = len(results)
    successful_samples = [r for r in results if r["success"]]
    failed_samples = [r for r in results if not r["success"]]
    
    drc_passes = [r for r in successful_samples if r["drc_pass"]]
    drc_failures = [r for r in successful_samples if not r["drc_pass"]]
    
    lvs_passes = [r for r in successful_samples if r["lvs_pass"]]
    lvs_failures = [r for r in successful_samples if not r["lvs_pass"]]
    
    execution_times = [r["execution_time"] for r in successful_samples]
    avg_time = sum(execution_times) / len(execution_times) if execution_times else 0
    min_time = min(execution_times) if execution_times else 0
    max_time = max(execution_times) if execution_times else 0
    
    print("🎉 LHS Dataset Analysis Report")
    print("=" * 50)
    print(f"📊 Dataset Overview:")
    print(f"   Total samples: {total_samples}")
    print(f"   Successful completions: {len(successful_samples)} ({len(successful_samples)/total_samples*100:.1f}%)")
    print(f"   Pipeline failures: {len(failed_samples)} ({len(failed_samples)/total_samples*100:.1f}%)")
    
    print(f"\n🔍 Quality Analysis (among successful samples):")
    print(f"   DRC passes: {len(drc_passes)}/{len(successful_samples)} ({len(drc_passes)/len(successful_samples)*100:.1f}%)")
    print(f"   DRC failures: {len(drc_failures)}/{len(successful_samples)} ({len(drc_failures)/len(successful_samples)*100:.1f}%)")
    print(f"   LVS passes: {len(lvs_passes)}/{len(successful_samples)} ({len(lvs_passes)/len(successful_samples)*100:.1f}%)")
    print(f"   LVS failures: {len(lvs_failures)}/{len(successful_samples)} ({len(lvs_failures)/len(successful_samples)*100:.1f}%)")
    
    print(f"\n⏱️  Performance Analysis:")
    print(f"   Average execution time: {avg_time:.1f}s")
    print(f"   Fastest sample: {min_time:.1f}s")
    print(f"   Slowest sample: {max_time:.1f}s")
    
    # Identify any failed samples
    if failed_samples:
        print(f"\n❌ Failed Samples:")
        for sample in failed_samples:
            print(f"   Sample {sample['sample_id']:04d}: {sample.get('error', 'Unknown error')}")
    
    # Identify DRC failures
    if drc_failures:
        print(f"\n🔍 DRC Failure Details:")
        for sample in drc_failures:
            print(f"   Sample {sample['sample_id']:04d}: {sample['component_name']}")
    
    # Identify LVS failures  
    if lvs_failures:
        print(f"\n🔍 LVS Failure Details:")
        for sample in lvs_failures:
            print(f"   Sample {sample['sample_id']:04d}: {sample['component_name']}")
    
    # Overall assessment
    success_rate = len(successful_samples) / total_samples * 100
    drc_rate = len(drc_passes) / len(successful_samples) * 100 if successful_samples else 0
    lvs_rate = len(lvs_passes) / len(successful_samples) * 100 if successful_samples else 0
    
    print(f"\n🏆 Overall Assessment:")
    if success_rate == 100:
        print(f"   ✅ EXCELLENT: 100% pipeline completion rate")
    elif success_rate >= 95:
        print(f"   ✅ VERY GOOD: {success_rate:.1f}% pipeline completion rate")
    elif success_rate >= 90:
        print(f"   ⚠️  GOOD: {success_rate:.1f}% pipeline completion rate")
    else:
        print(f"   ❌ NEEDS IMPROVEMENT: {success_rate:.1f}% pipeline completion rate")
    
    if drc_rate == 100:
        print(f"   ✅ PERFECT: 100% DRC pass rate")
    elif drc_rate >= 95:
        print(f"   ✅ EXCELLENT: {drc_rate:.1f}% DRC pass rate")
    elif drc_rate >= 90:
        print(f"   ✅ VERY GOOD: {drc_rate:.1f}% DRC pass rate")
    else:
        print(f"   ⚠️  NEEDS REVIEW: {drc_rate:.1f}% DRC pass rate")
    
    if lvs_rate == 100:
        print(f"   ✅ PERFECT: 100% LVS pass rate")
    elif lvs_rate >= 95:
        print(f"   ✅ EXCELLENT: {lvs_rate:.1f}% LVS pass rate")
    elif lvs_rate >= 90:
        print(f"   ✅ VERY GOOD: {lvs_rate:.1f}% LVS pass rate")
    else:
        print(f"   ⚠️  NEEDS REVIEW: {lvs_rate:.1f}% LVS pass rate")
    
    print(f"\n🎯 Dataset Status:")
    if success_rate == 100 and drc_rate >= 95 and lvs_rate >= 95:
        print(f"   🎉 PRODUCTION READY: Dataset meets all quality thresholds")
        print(f"   🚀 Ready for machine learning training and analysis")
    else:
        print(f"   ⚠️  REVIEW NEEDED: Some quality metrics below optimal")
    
    return {
        "total_samples": total_samples,
        "success_rate": success_rate,
        "drc_rate": drc_rate,
        "lvs_rate": lvs_rate,
        "avg_time": avg_time
    }

if __name__ == "__main__":
    stats = analyze_dataset()
    
    # Generate a brief summary
    print(f"\n📋 Brief Summary:")
    print(f"   {stats['total_samples']} samples, {stats['success_rate']:.0f}% success")
    print(f"   DRC: {stats['drc_rate']:.0f}%, LVS: {stats['lvs_rate']:.0f}%")
    print(f"   Avg time: {stats['avg_time']:.1f}s per sample")
