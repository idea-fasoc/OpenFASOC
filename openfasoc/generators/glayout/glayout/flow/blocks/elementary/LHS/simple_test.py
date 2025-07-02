#!/usr/bin/env python3

import os
import sys
import time
import json
import logging
from datetime import datetime

# Add the parent directories to the Python path
sys.path.append('/home/arnavshukla/OpenFASOC/openfasoc/generators/glayout')

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('simple_sweep.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def test_single_block():
    """Test processing a single FVF sample"""
    logger.info("Testing single block processing")
    
    # Create output directory
    output_dir = "test_output"
    if os.path.exists(output_dir):
        import shutil
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    
    try:
        # Import FVF module and PDK
        from fvf import flipped_voltage_follower
        from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk
        
        pdk = sky130_mapped_pdk
        
        # Test parameters
        params = {
            'pdk': pdk,
            'width': (5.0, 10.0),
            'length': (1.0, 2.0), 
            'fingers': (2, 2),
            'multipliers': (1, 1)
        }
        
        logger.info(f"Testing FVF with params: {params}")
        
        # Generate component
        comp = flipped_voltage_follower(**params)
        
        # Save GDS
        gds_path = os.path.join(output_dir, "test_fvf.gds")
        comp.write_gds(gds_path)
        logger.info(f"GDS saved: {gds_path}")
        
        # Run evaluation
        logger.info("Running evaluation...")
        import fvf
        comp.name = "test_fvf"
        result = fvf.run_evaluation(gds_path, comp.name, comp)
        
        # Save result
        result_path = os.path.join(output_dir, "test_fvf_result.json")
        with open(result_path, 'w') as f:
            json.dump(result, f, indent=2)
        
        logger.info("✅ Test successful!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_single_block()
