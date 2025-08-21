#!/usr/bin/env python3
"""Run and time LHS generator files once and emit a JSON array of results.

This script will attempt to execute the following files (located in the same
directory) once each and measure wall-clock time for the run:

- current_mirror.py
- diff_pair.py
- fvf.py
- transmission_gate.py
- lvcm.py

It records start/stop times, exit codes, elapsed seconds and any stderr output
into a JSON file named `run_lhs_results.json` and prints the JSON array to
stdout.
"""
import json
import os
import sys
import time
import subprocess


FILES = [
    "current_mirror.py",
    "diff_pair.py",
    "fvf.py",
    "transmission_gate.py",
    "lvcm.py",
]


def run_file(path, timeout=120):
    """Run a python file and time the execution. Returns a dict with results."""
    start = time.perf_counter()
    try:
        completed = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=timeout)
        end = time.perf_counter()
        return {
            "file": os.path.basename(path),
            "elapsed_seconds": end - start,
            "returncode": completed.returncode,
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
        }
    except subprocess.TimeoutExpired as e:
        end = time.perf_counter()
        return {
            "file": os.path.basename(path),
            "elapsed_seconds": end - start,
            "returncode": None,
            "stdout": "",
            "stderr": f"Timeout after {timeout}s",
        }
    except Exception as e:
        end = time.perf_counter()
        return {
            "file": os.path.basename(path),
            "elapsed_seconds": end - start,
            "returncode": None,
            "stdout": "",
            "stderr": f"Exception: {e}",
        }


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    results = []
    for fname in FILES:
        fpath = os.path.join(base, fname)
        if not os.path.exists(fpath):
            results.append({
                "file": fname,
                "elapsed_seconds": None,
                "returncode": None,
                "stdout": "",
                "stderr": "File not found",
            })
            continue
        print(f"Running {fname}...")
        res = run_file(fpath)
        print(f" -> {fname}: {res['elapsed_seconds']:.4f}s, returncode={res['returncode']}")
        results.append(res)

    out_path = os.path.join(base, "run_lhs_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    # Print only the array of elapsed_seconds for quick consumption, then full JSON
    elapsed_array = [r["elapsed_seconds"] for r in results]
    print("\nElapsed seconds array:")
    print(json.dumps(elapsed_array))
    print("\nFull results saved to:", out_path)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
