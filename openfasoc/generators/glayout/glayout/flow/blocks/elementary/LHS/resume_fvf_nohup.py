#!/usr/bin/env python3
"""Resume the FVF generation non-interactively and exit with status.

This script imports the updated generator and calls run_dataset_generation
directly. It's intended to be launched under nohup or a systemd service so it
continues after SSH disconnects.
"""
import logging
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from generate_fvf_8h_runtime_aware import load_fvf_parameters, run_dataset_generation
except Exception as e:
    logger.error(f"Failed to import generator module: {e}")
    sys.exit(2)


def main():
    try:
        params = load_fvf_parameters(None)
        n = len(params)
        logger.info(f"Resuming generation for {n} samples (checkpoint-aware)")

        # Run dataset generation; it will load and resume from checkpoint.json
        success, passed, total = run_dataset_generation(n, "fvf_dataset_8h_runtime_aware", checkpoint_interval=100, resume_from_checkpoint=True)

        logger.info(f"Finished. success={success}, passed={passed}, total={total}")
        return 0 if success else 1
    except Exception as e:
        logger.exception(f"Unexpected error during resume: {e}")
        return 3


if __name__ == '__main__':
    rc = main()
    sys.exit(rc)
