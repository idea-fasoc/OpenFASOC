#!/usr/bin/env python3
"""
Smoke test for Current Mirror Dataset Generator
Tests 5 samples to ensure the pipeline works correctly.
"""

import logging
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Run smoke test with 5 samples."""
    print("🔥 Current Mirror Smoke Test - 5 Samples")
    print("=" * 50)
    
    try:
        # Import the main generator
        from generate_current_mirror_360_robust_fixed import run_dataset_generation
        
        # Run with 5 samples
        logger.info("Starting smoke test with 5 samples...")
        success, passed, total = run_dataset_generation(
            n_samples=5,
            output_dir="cm_smoke_test",
            checkpoint_interval=2,  # Checkpoint every 2 samples for testing
            resume_from_checkpoint=False  # Start fresh
        )
        
        print(f"\n🎯 Smoke Test Results:")
        print(f"   Success: {success}")
        print(f"   Passed: {passed}/{total}")
        print(f"   Success Rate: {(passed/total)*100:.1f}%")
        
        if passed >= 3:  # At least 60% success rate
            print("\n✅ Smoke test PASSED! Pipeline is working correctly.")
            return True
        else:
            print("\n❌ Smoke test FAILED! Check logs for issues.")
            return False
            
    except Exception as e:
        logger.error(f"Smoke test failed with error: {e}")
        print(f"\n❌ Smoke test FAILED with exception: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 