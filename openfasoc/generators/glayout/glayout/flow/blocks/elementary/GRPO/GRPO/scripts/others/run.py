#!/usr/bin/env python3
"""Run the full 13-Billion model pipeline (data → train)."""

import subprocess
import sys
from pathlib import Path

THIS_DIR = Path(__file__).parent.resolve()


def run(cmd: str, desc: str):
    print(f"🚀 {desc}\n{cmd}\n{'-'*40}")
    if subprocess.call(cmd, shell=True, cwd=THIS_DIR) != 0:
        sys.exit(f"❌ Failed step: {desc}")
    print(f"✅ {desc} complete\n")


def main():
    run("python process_data.py", "Processing dataset (13B)")
    run("python gpu_finetune.py", "13B full-weight fine-tune")
    print("🎉 13B pipeline finished – model saved to 13b/final_model/")


if __name__ == "__main__":
    main() 