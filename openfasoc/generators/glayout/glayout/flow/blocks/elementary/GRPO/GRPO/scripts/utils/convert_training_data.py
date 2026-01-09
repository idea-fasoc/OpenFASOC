"""
convert_training_data.py – Generic converter for prediction-files -> clean JSONL.

Usage
-----
# Baseline run-3 example
python scripts/utils/convert_training_data.py \
       --in_dir data/dataset_for_sft/data-run-3/predictions_baseline \
       --tag run3

# Fine-tuned run-2 example (old default folders!)
python scripts/utils/convert_training_data.py

The script expects *in_dir* to have **either**:
  • sub-folders `7b` and `13b`, **or**
  • sub-folders `7b-ft` and `13b-ft`  (for finetuned predictions).

It extracts the fenced ```json … ``` block from every `.txt` file and writes
one JSON object per line into:
  data/processed/train_data_{7b,13b}_{tag}_clean.jsonl
"""
from __future__ import annotations

import argparse
import glob
import json
import sys
from pathlib import Path
from typing import List, Dict


def _extract_json_from_file(file_path: Path) -> List[Dict]:
    data: List[Dict] = []
    current_json = ""
    in_block = False

    with file_path.open("r", encoding="utf-8", errors="replace") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue

            # fenced start
            if line.startswith("```json"):
                in_block = True
                current_json = ""
                continue
            # fenced end
            if line.startswith("```") and in_block:
                if current_json.strip():
                    try:
                        data.append(json.loads(current_json.strip()))
                    except json.JSONDecodeError as err:
                        print(f"  {file_path}: JSON decode error -> {err}")
                in_block = False
                current_json = ""
                continue
            # lines inside block
            if in_block:
                current_json += raw
                continue

            # fallback single-line JSON
            if line.startswith("{"):
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError as err:
                    print(f"  {file_path}: JSON decode error (inline) -> {err}")

    # EOF without closing fence
    if in_block and current_json.strip():
        try:
            data.append(json.loads(current_json.strip()))
        except json.JSONDecodeError as err:
            print(f"  {file_path}: JSON decode error (unterminated block) -> {err}")

    return data


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Convert prediction txt files to JSONL dataset")
    p.add_argument("--in_dir", type=str, default=None,
                   help="Directory that holds prediction txt files (must contain sub-dirs 7b/13b or 7b-ft/13b-ft). If omitted, falls back to old finetuned default path.")
    p.add_argument("--tag", type=str, default="clean",
                   help="Tag appended to output jsonl filenames (default: 'clean')")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent.parent.parent  # project root

    if args.in_dir is None:
        pred_root = repo_root / "dataset_for_sft" / "prediction_finetuned"
    else:
        pred_root = Path(args.in_dir).resolve()
        if not pred_root.is_dir():
            sys.exit(f" in_dir not found: {pred_root}")

    possible_subs = ["7b", "13b", "7b-ft", "13b-ft"]
    sub_exists = [s for s in possible_subs if (pred_root / s).is_dir()]
    if not sub_exists:
        sys.exit("No 7b/13b sub-folders found in provided directory")

    out_dir = repo_root / "data" / "processed"
    out_dir.mkdir(parents=True, exist_ok=True)

    total_samples = 0
    for sub in sub_exists:
        model_tag = "7b" if sub.startswith("7") else "13b"
        out_path = out_dir / f"train_data_{model_tag}_{args.tag}_clean.jsonl"

        files = sorted(glob.glob(str(pred_root / sub / "*.txt")))
        all_items: List[Dict] = []
        for fp in files:
            all_items.extend(_extract_json_from_file(Path(fp)))

        with out_path.open("w", encoding="utf-8") as fout:
            for item in all_items:
                fout.write(json.dumps(item, ensure_ascii=False) + "\n")

        print(f" {sub}: {len(all_items)} samples -> {out_path.relative_to(repo_root)}")
        total_samples += len(all_items)

    print(f"Total samples: {total_samples}")


if __name__ == "__main__":
    main() 