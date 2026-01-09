"""master_inference.py – batch inference over a dataset of code + compile logs

Usage example
-------------
python master_inference.py \
  --model gemini-2.0-flash-exp \
  --dataset_root dataset_for_sft \
  --output_dir dataset_for_sft/predictions_baseline

Add `--finetuned` to switch to the prompt variant for the fine-tuned model and
specify a custom `--model` id pointing to your fine-tuned checkpoint.

Environment variable GOOGLE_API_KEY must be set, or pass via --api_key.

Supported Master Models (Google Gemini):
-----------------------------------------
  - gemini-2.0-flash           (Fast 2.0 model, good balance)
  - gemini-1.5-pro-latest      (Best quality, slower)
  - gemini-1.5-flash-latest    (Fast production model)
  - gemini-1.5-flash-8b-latest (Lightweight, fastest)
  - gemini-1.0-pro-latest      (Legacy stable model)
  
Choose based on your needs:
  - For speed: gemini-2.0-flash, gemini-1.5-flash-latest
  - For quality: gemini-1.5-pro-latest
  - For stability: gemini-1.5-flash-latest
"""
from __future__ import annotations
import argparse
import os
import sys
import time
from pathlib import Path
from typing import Optional
import datetime
import google.generativeai as genai


BASE_PROMPT = (
    "You are an expert Python programmer and educator. Your task is to analyze "
    "the provided Python code + its compilation log for errors, explain the "
    "errors clearly and concisely, keep them short but descriptive, as much as possible, and then provide a corrected version of the "
    "code. The files are written in context to this repository: "
    "https://github.com/idea-fasoc/OpenFASOC\n\n"
    "DO NOT RETURN ANY COMMENTS OR LINES THAT YOU MAY HAVE, APART FROM CODE, in the fixed code section."
    "the fixed code should have only python code."
    "**Instructions:**\n\n"
    "1.  **Code Analysis:** Carefully examine the Python code provided below for any "
    "syntax errors, runtime errors, logical errors, or style issues that deviate from best practices (PEP 8).\n\n"
    "2.  **Error Explanation:**  For each identified error or issue, provide a clear and concise explanation of:\n"
    "    *   **The specific problem:**  What is wrong with the code?  Be precise.\n"
    "    *   **Why it is a problem:**  What is the consequence of this error (e.g., \"causes a `TypeError`\", \"leads to incorrect results\", \"violates readability guidelines\")?\n"
    "    *   **How to fix it:** Briefly describe the correction needed.\n\n"
    "3.  **Fixed Code:** After explaining the errors, provide a complete, corrected version of the original code. "
    "This corrected code *must* be valid Python code that runs without errors and addresses the identified issues.\n\n"
    "**Output Format:**\n\n"
    "Your output should be structured in the following way.  *It is crucial that you adhere to this format EXACTLY to enable easy parsing.*\n"
    "{\n"
    "  \"filename\": \"example.py\",\n"
    "  \"analysis\": [\n"
    "    {\n"
    "      \"issue\": \"Brief description of issue #1\",\n"
    "      \"explanation\": {\n"
    "        \"problem\": \"What exactly is wrong? (e.g., 'Uses = instead of == in condition')\",\n"
    "        \"reason\": \"Why it's a problem (e.g., 'Will cause always-true condition and logic error')\",\n"
    "        \"fix\": \"How to fix it (e.g., 'Use == instead of =')\"\n"
    "      }\n"
    "    },\n"
    "    {\n"
    "      \"issue\": \"Brief description of issue #2\",\n"
    "      \"explanation\": {\n"
    "        \"problem\": \"Explain the second problem here...\",\n"
    "        \"reason\": \"Why it causes a bug, bad output, or violates best practices...\",\n"
    "        \"fix\": \"Correction needed...\"\n"
    "      }\n"
    "    }\n"
    "  ],\n"
    "  \"fixed_code\": \"'''Insert the full corrected code as a string here. Use \\n for line breaks and escape characters as needed.'''\"\n"
    "}\n\n"
    "****code****:\n\n"
    ""
)

finetuned_prompt = (
    "\n\nYou have to make sure the model realises that glayout/gdsfactory modules are important, and they should be used in context to the code in the repository and the written code as well:\n"
)


def build_prompt(code: str, compile_log: str, filename: str, finetuned: bool) -> str:
    prompt = BASE_PROMPT
    if finetuned:
        prompt += finetuned_prompt
    
    # adding instruction.txt as extra context
    try:
        instruction_path = Path("instruction.txt")
        if instruction_path.exists():
            instruction_content = instruction_path.read_text()
            prompt += f"\n\n**Additional Context Instructions:**\n{instruction_content}\n\n"
        else:
            print(f"[WARNING] instruction.txt not found at {instruction_path}")
    except Exception as e:
        print(f"[WARNING] Failed to read instruction.txt: {e}")
    
    prompt += "\n\n" + code + "\n\n--- compile log ---\n" + compile_log + "\n"

    prompt = prompt.replace("****code****:", f"****code****:\n{code}\n\n--- compile log ---\n{compile_log}\n")
    prompt = prompt.replace("example.py", filename)
    return prompt


def infer_single(prompt: str, model: str, max_tokens: int = 1024, n_retry: int = 7) -> str:
    """Make a single inference call to Gemini API with exponential backoff retry logic."""
    for attempt in range(1, n_retry + 1):
        try:
            # configuring master model
            model_instance = genai.GenerativeModel(model)
            
            # inferring response from model
            response = model_instance.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=max_tokens,
                )
            )
            return response.text.strip()
        except Exception as e:
            error_str = str(e).lower()
            
            # Check if it's a rate limit error
            if '429' in error_str or 'rate limit' in error_str or 'quota' in error_str:
                # Longer exponential backoff for rate limits: 30s, 60s, 90s, 120s, 180s, 240s, 300s
                wait = min(30 + (30 * (attempt - 1)), 300)
                print(f"⚠️  Rate limit hit (attempt {attempt}/{n_retry}): retrying in {wait}s", file=sys.stderr)
            else:
                # Regular error: shorter wait
                wait = 10 * attempt
                print(f"⚠️  Gemini API error (attempt {attempt}/{n_retry}): {e}; retrying in {wait}s", file=sys.stderr)
            
            time.sleep(wait)
    raise RuntimeError("Inference failed after retries.")



def parse_args():
    p = argparse.ArgumentParser(
        description="Batch inference using Google Gemini API for code analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Supported Gemini Models:
  gemini-2.0-flash-exp    - Fast, experimental (recommended for speed)
  gemini-2.5-pro          - Most capable, best quality (recommended for accuracy)
  gemini-1.5-pro          - Stable production model
  gemini-1.5-flash        - Fast production model
  gemini-pro              - Legacy stable model

Examples:
  # Basic usage with default model
  python master_inference.py --dataset_root ./dataset --api_key YOUR_KEY
  
  # Use fast experimental model
  python master_inference.py --model gemini-2.0-flash-exp --dataset_root ./dataset
  
  # Use highest quality model
  python master_inference.py --model gemini-2.5-pro --dataset_root ./dataset
        """
    )
    p.add_argument("--model", type=str, default="gemini-2.0-flash-exp", 
                   help="Gemini model id (default: gemini-2.0-flash-exp)")
    p.add_argument("--dataset_root", type=str, default="dataset_for_sft", 
                   help="Root folder holding outputs/ compile_results/ etc.")
    p.add_argument("--code_dir", type=str, default=None, 
                   help="Optional explicit code directory (overrides automatic selection)")
    p.add_argument("--compile_dir", type=str, default=None, 
                   help="Optional explicit compile-results directory (overrides automatic selection)")
    p.add_argument("--output_dir", type=str, default=None, 
                   help="Output directory root (auto-set if omitted)")
    p.add_argument("--api_key", type=str, default=None, 
                   help="Google API key (otherwise read from env GOOGLE_API_KEY)")
    p.add_argument("--finetuned", action="store_true", 
                   help="Use the fine-tuned prompt variant")
    p.add_argument("--overwrite", action="store_true", 
                   help="Overwrite existing outputs")
    p.add_argument("--max_tokens", type=int, default=8192, 
                   help="Maximum output tokens (default: 8192)")
    p.add_argument("--limit", type=int, default=None, 
                   help="Limit number of files to process")
    p.add_argument("--api_delay", type=float, default=15.0,
                   help="Delay (seconds) between API calls to avoid rate limits (default: 15.0)")
    return p.parse_args()


def main():
    args = parse_args()

    api_key = args.api_key or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: GOOGLE_API_KEY not provided", file=sys.stderr)
        print("Please either:", file=sys.stderr)
        print("  1. Set environment variable: export GOOGLE_API_KEY='your_key'", file=sys.stderr)
        print("  2. Pass via command line: --api_key YOUR_KEY", file=sys.stderr)
        sys.exit(1)
    
    print(f"[INFO] Using Gemini model: {args.model}")
    genai.configure(api_key=api_key)

    file_limit = None
    if args.limit:
        file_limit = args.limit
    # elif args.smoke_test:
    #     file_limit = 5
    #     print(f"[INFO] Running smoke test - processing only {file_limit} files")

    start_time = datetime.datetime.now()

    dataset_root = Path(args.dataset_root)

    # directory creation
    if args.code_dir is None:
        categories = ["7b-ft", "13b-ft"] if args.finetuned else ["7b", "13b"]
        if args.finetuned:
            code_root = dataset_root  # e.g. dataset_for_sft/7b-ft
        else:
            code_root = dataset_root / "outputs"
    else:
        categories = [None]  # single dir
        code_root = Path(args.code_dir)

    compile_root = Path(args.compile_dir) if args.compile_dir else dataset_root / "compile_results"

    if args.output_dir is None:
        default_out = "predictions_finetuned" if args.finetuned else "predictions_baseline"
        out_root = dataset_root / default_out
    else:
        out_root = Path(args.output_dir)

    total_processed = 0

    for category in categories:
        code_dir = code_root if category is None else code_root / category
        if not code_dir.exists():
            print(f"[warn] code directory not found: {code_dir}, skipping", file=sys.stderr)
            continue

        compile_dir = (
            compile_root if category is None else compile_root / category
        )

        out_dir = out_root if category is None else out_root / category
        out_dir.mkdir(parents=True, exist_ok=True)

        files = sorted(code_dir.glob("*.py"))
        if not files:
            print(f"[warn] No .py files in {code_dir}", file=sys.stderr)
            continue

        print(f"[INFO] Found {len(files)} Python files in {code_dir}")

        # # Apply file limit if specified
        # if file_limit and total_processed >= file_limit:
        #     print(f"[INFO] Reached file limit of {file_limit}, stopping processing")
        #     break

        for code_path in files:
            # # Check file limit
            # if file_limit and total_processed >= file_limit:
            #     print(f"[INFO] Reached file limit of {file_limit}, stopping processing")
            #     break

            fname = code_path.name
            out_path = out_dir / (code_path.stem + ".txt")
            if out_path.exists() and not args.overwrite:
                print(f"[skip] {out_path} exists", file=sys.stderr)
                continue

            compile_log_path_candidates = [
                compile_dir / (code_path.stem + ext) for ext in (".txt", ".log")
            ]
            compile_log_path: Optional[Path] = next(
                (p for p in compile_log_path_candidates if p.exists()), None
            )
            compile_log = (
                compile_log_path.read_text() if compile_log_path else "(compile log missing)"
            )

            code = code_path.read_text()
            prompt = build_prompt(code, compile_log, fname, args.finetuned)

            print(f"Inferencing {fname} [{category or 'custom'}] with model {args.model}... ({total_processed + 1})")
            response = infer_single(prompt, model=args.model, max_tokens=args.max_tokens)

            out_path.write_text(response)
            print(f"[saved] {out_path}")
            total_processed += 1
            
            # Add delay between API calls to avoid rate limiting
            # Gemini free tier has strict limits, default is 15 seconds between calls
            # Adjust with --api_delay if you have different rate limits
            time.sleep(args.api_delay)

            # Calculate and display ETA
            elapsed = datetime.datetime.now() - start_time
            if total_processed > 0:
                avg_time_per_file = elapsed.total_seconds() / total_processed
                if file_limit:
                    remaining = file_limit - total_processed
                    eta = datetime.timedelta(seconds=remaining * avg_time_per_file)
                    print(f"[INFO] ETA: {eta} (avg: {avg_time_per_file:.1f}s per file)")

    elapsed_total = datetime.datetime.now() - start_time
    print(f"Inference complete. Processed {total_processed} files in {elapsed_total}.")


if __name__ == "__main__":
    main()