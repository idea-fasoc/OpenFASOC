import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent 
OUTPUT_DIR = ROOT / "dataset_for_sft" / "outputs"
RESULTS_DIR = ROOT / "dataset_for_sft" / "compile_results"


def compile_file(py_file: Path) -> tuple[str, str]:
    # Use `python -m py_compile`
    try:
        proc = subprocess.run(
            ["python", "-m", "py_compile", str(py_file)],
            capture_output=True,
            text=True,
            timeout=60,  # prevent hanging scripts
        )
        status = "compiled" if proc.returncode == 0 else "not compiled"
        output = (proc.stdout or "") + (proc.stderr or "")
    except Exception as exc:
        status = "not compiled"
        output = str(exc)
    return status, output


def save_result(py_file: Path, status: str, output: str) -> None:
    """Save compilation result to a sibling .log file inside RESULTS_DIR."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    result_file = RESULTS_DIR / f"{py_file.stem}.log"
    with result_file.open("w", encoding="utf-8") as f:
        f.write(f"file: {py_file.name}\n")
        f.write(f"status: {status}\n\n")
        f.write(output)


def main():
    if not OUTPUT_DIR.exists():
        print(f"Output directory '{OUTPUT_DIR}' does not exist.")
        return

    py_files = sorted(OUTPUT_DIR.glob("*.py"))
    if not py_files:
        print(f"No Python files found in '{OUTPUT_DIR}'.")
        return

    for py_file in py_files:
        status, output = compile_file(py_file)
        save_result(py_file, status, output)
        print(f"{py_file.name}: {status}")


if __name__ == "__main__":
    main() 