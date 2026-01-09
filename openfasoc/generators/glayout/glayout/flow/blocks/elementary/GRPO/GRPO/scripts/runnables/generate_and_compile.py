#!/usr/bin/env python3
"""End-to-end pipeline: Generate code via `scripts/others/run_inference.py` then compile.

Steps
-----
1. Execute `scripts/others/run_inference.py` with the forwarded CLI flags
   to generate Python files under `dataset_for_sft/outputs` (or user-specified dir).
2. Recursively compile every generated `*.py` file using `python -m py_compile`.
3. Save a log per file under a parallel directory (default: `dataset_for_sft/compile_results`).

Example
-------
$ python generate_and_compile.py \
      --model 7b=codellama/CodeLlama-7b-Instruct-hf \
      --temperature 0.0
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent  # Repo root
DEFAULT_OUTPUT_DIR = ROOT / "dataset_for_sft" / "outputs"
DEFAULT_RESULTS_DIR = ROOT / "dataset_for_sft" / "compile_results"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def run(cmd: str | list[str], desc: str) -> None:
    """Run *cmd*. Abort on non-zero exit."""
    print(f"\n🚀 {desc}\nCMD: {cmd}\n{'-'*60}")
    result = subprocess.run(cmd, shell=isinstance(cmd, str))
    if result.returncode != 0:
        sys.exit(f"  Step failed: {desc}")
    print(f" {desc} complete")


def compile_file(py_file: Path) -> tuple[str, str]:
    """Compile *py_file* and return (status, combined_output)."""
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "py_compile", str(py_file)],
            capture_output=True,
            text=True,
            timeout=60,
        )
        status = "compiled" if proc.returncode == 0 else "not compiled"
        output = (proc.stdout or "") + (proc.stderr or "")
    except Exception as exc:  # pragma: no cover – generic catch for robustness
        status = "not compiled"
        output = str(exc)
    return status, output


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate Python code with an LLM then compile it.",
        add_help=False,  # let sub-parser handle duplicates
    )

    # Known wrapper-specific flags
    parser.add_argument(
        "--output_dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory where run_inference writes .py outputs (forwarded).",
    )
    parser.add_argument(
        "--results_dir",
        default=str(DEFAULT_RESULTS_DIR),
        help="Directory to store compilation logs.",
    )

    parser.add_argument(
        "--prompt_template_file",
        default=str(ROOT / "scripts" / "utils" / "prompt.txt"),
        help="Instruction-template file to wrap each strict-syntax prompt.",
    )

    # Collect unknown args to forward to run_inference
    args, unknown = parser.parse_known_args()

    output_dir = Path(args.output_dir)
    results_dir = Path(args.results_dir)

    # ------------------------------------------------------------------
    # 1. Run inference
    # ------------------------------------------------------------------
    # Add the data directory to Python path so dataset_for_sft can be found as a module
    data_dir = str(ROOT / "data")
    env = os.environ.copy()
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] = f"{data_dir}{os.pathsep}{env['PYTHONPATH']}"
    else:
        env["PYTHONPATH"] = data_dir

    inf_cmd = [
        sys.executable,
        str(ROOT / "scripts" / "others" / "run_inference.py"),
        "--output_dir",
        str(output_dir),
        "--prompt_template_file",
        str(args.prompt_template_file),
        *unknown,  # forward remaining CLI options untouched
    ]

    print(f"\n🚀 Generate code via scripts/others/run_inference.py\nCMD: {inf_cmd}\n{'-'*60}")
    result = subprocess.run(inf_cmd, env=env)
    if result.returncode != 0:
        sys.exit(f"  Step failed: Generate code via scripts/others/run_inference.py")
    print(f" Generate code via scripts/others/run_inference.py complete")

    # ------------------------------------------------------------------
    # 2. Compile every produced .py file
    # ------------------------------------------------------------------
    if not output_dir.exists():
        sys.exit(f"  Output directory '{output_dir}' does not exist after inference.")

    py_files = list(output_dir.rglob("*.py"))
    if not py_files:
        sys.exit(f"  No Python files found in '{output_dir}'.")

    for py_file in py_files:
        rel_path = py_file.relative_to(output_dir)
        status, output = compile_file(py_file)

        log_path = results_dir / rel_path.with_suffix(".log")
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text(
            f"file: {rel_path}\nstatus: {status}\n\n{output}",
            encoding="utf-8",
        )
        print(f" {rel_path} → {status}")

    print("\n  Generation + compilation complete!")


if __name__ == "__main__":
    main() 