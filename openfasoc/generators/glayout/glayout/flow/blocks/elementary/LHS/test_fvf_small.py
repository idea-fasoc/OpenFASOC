#!/usr/bin/env python3
"""
Small FVF Test Script
Tests the full pipeline with 10 samples from the 34,995 parameter file
to verify everything works before running the full dataset.
"""

import logging
import sys
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import the functions from the main script
# We need to add the current directory to the path to import the module
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from generate_fvf_360_robust_fixed import (
    setup_environment, 
    load_fvf_parameters, 
    run_dataset_generation
)

def main():
    """Test the FVF pipeline with 10 samples"""
    print("🧪 FVF Dataset Generation - Small Test (10 samples)")
    print("=" * 60)
    
    # Setup environment
    print("🔧 Setting up environment...")
    try:
        setup_environment()
        logger.info("Environment setup completed")
    except Exception as e:
        print(f"❌ Environment setup failed: {e}")
        return False
    
    # Load and verify parameters
    print("📊 Loading parameters...")
    try:
        # Load first 10 parameters from the full file
        parameters = load_fvf_parameters(10)
        print(f"✅ Loaded {len(parameters)} parameter combinations for testing")
    except Exception as e:
        print(f"❌ Failed to load parameters: {e}")
        return False
    
    # Show parameter sample
    print(f"📋 Sample parameter set:")
    if parameters:
        sample_params = parameters[0]
        for key, value in sample_params.items():
            print(f"   {key}: {value}")
    
    # Ask for confirmation
    print(f"\n🤔 This will test the pipeline with 10 samples.")
    print(f"   Expected time: ~2-3 minutes")
    print(f"   Output directory: fvf_test_10_samples")
    
    response = input("\nProceed with test? (y/n): ").lower().strip()
    if response != 'y':
        print("Test cancelled.")
        return True
    
    # Run the test
    print("\n🚀 Starting 10-sample test...")
    try:
        success, passed, total = run_dataset_generation(
            10, 
            "fvf_test_10_samples",
            checkpoint_interval=5,  # Checkpoint every 5 samples for test
            resume_from_checkpoint=True
        )
        
        if success:
            print(f"\n🎉 Test completed successfully!")
            print(f"📊 Results: {passed}/{total} samples successful")
            print(f"📁 Check results in: fvf_test_10_samples/")
            return True
        else:
            print(f"\n⚠️ Test completed with issues")
            print(f"📊 Results: {passed}/{total} samples successful")
            print(f"💡 Review the results before running full dataset")
            return False
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        logger.error(f"Test failed: {e}", exc_info=True)
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Small test completed! Ready for full dataset generation.")
        sys.exit(0)
    else:
        print("\n❌ Test failed. Please fix issues before running full dataset.")
        sys.exit(1) 