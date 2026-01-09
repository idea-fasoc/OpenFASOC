"""Batch inference script for strict-syntax .convo files.

This tool reads every .convo file under the `strict-syntax` directory,
feeds the content to a specified language model, and writes the resulting
Python code to a corresponding file in the `outputs` directory.

Usage
-----
$ python -m dataset_for_sft.run_inference --model <model_path_or_hf_repo>

Optional flags:
  --convo_dir PATH    # default: dataset_for_sft/strict-syntax
  --output_dir PATH   # default: dataset_for_sft/outputs
  --max_tokens N      # default: 2048
  --temperature F     # default: 0.1 (0 = greedy)
  --device {cpu,cuda,auto}

The script will automatically create the output directory if it does not
exist.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Iterable

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

PKG_ROOT = Path(__file__).resolve().parent
DEFAULT_CONVO_DIR = PKG_ROOT / "strict-syntax"
DEFAULT_OUTPUT_DIR = PKG_ROOT / "outputs"

def parse_convo_file(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def generate_code(
    model,
    tokenizer,
    prompt: str,
    max_tokens: int = 2048,
    temperature: float = 0.1,
) -> str:
    """Generate Python code from *prompt* using *model*/*tokenizer*."""
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    gen_kwargs = dict(
        **inputs,
        max_new_tokens=max_tokens,
        temperature=temperature,
        do_sample=temperature > 0,
        eos_token_id=tokenizer.eos_token_id,
    )

    with torch.inference_mode():
        output_ids = model.generate(**gen_kwargs)

    generated = tokenizer.decode(
        output_ids[0][inputs["input_ids"].shape[1] :], skip_special_tokens=True
    )
    return generated


def main(argv: Iterable[str] | None = None) -> None:
    p = argparse.ArgumentParser(description="Generate Python code from strict-syntax .convo files with an LLM.")
    p.add_argument(
        "--model",
        dest="models",
        metavar="TAG=PATH",
        action="append",
        help=(
            "Model definition in the form <tag>=<hf_repo_or_local_path>. "
            "Can be supplied multiple times. If omitted, defaults to the four "
            "pre-defined: 7b, 7b-ft, 13b, 13b-ft."
        ),
    )
    p.add_argument(
        "--convo_dir",
        default=str(DEFAULT_CONVO_DIR),
        help="Directory containing .convo files",
    )
    p.add_argument(
        "--output_dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory to write generated .py files",
    )
    p.add_argument(
        "--max_tokens",
        type=int,
        default=2048,
        help="Maximum tokens to generate per file",
    )
    p.add_argument(
        "--temperature",
        type=float,
        default=0.1,
        help="Sampling temperature (0 = greedy)",
    )
    p.add_argument(
        "--device",
        default="auto",
        choices=["auto", "cpu", "cuda"],
        help="Computation device",
    )
    p.add_argument(
        "--prompt_template_file",
        default="",
        help=(
            "Optional file containing an instruction-tuned template. The first line "
            "that starts with 'TASK:' will have its contents replaced by the strict "
            "syntax text from the .convo file. If no 'TASK:' line is found, the text "
            "of the .convo file is appended to the end of the template."
        ),
    )
    args = p.parse_args(argv)

    convo_dir = Path(args.convo_dir)

    template_text: str | None = None
    if args.prompt_template_file:
        template_path = Path(args.prompt_template_file)
        if not template_path.is_file():
            raise SystemExit(f"Prompt template file '{template_path}' not found.")
        template_text = template_path.read_text(encoding="utf-8")

    if not convo_dir.is_dir():
        raise SystemExit(f"Convo directory '{convo_dir}' not found.")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Determine device
    device = (
        "cuda" if (args.device == "auto" and torch.cuda.is_available()) else args.device
    )

    # ------------------------------------------------------------------
    # Determine which models to run
    # ------------------------------------------------------------------
    if args.models:
        model_map: dict[str, str] = {}
        for item in args.models:
            if "=" not in item:
                raise SystemExit(
                    f"Invalid --model format '{item}'. Expected TAG=PATH."
                )
            tag, path = item.split("=", 1)
            model_map[tag.strip()] = path.strip()
    else:
        # Default set (local fine-tunes + HF base repos)
        repo_7b_base = "codellama/CodeLlama-7b-Instruct-hf"
        repo_13b_base = "codellama/CodeLlama-13b-Instruct-hf"
        model_map = {
            "7b": repo_7b_base,
            "7b-ft": str(Path(__file__).resolve().parent.parent / "7b" / "final_model"),
            "13b": repo_13b_base,
            "13b-ft": str(Path(__file__).resolve().parent.parent / "13b" / "final_model"),
        }

    convo_files = sorted(convo_dir.glob("*.convo"))
    if not convo_files:
        raise SystemExit(f"No '.convo' files found in '{convo_dir}'.")

    dtype = torch.float16 if device == "cuda" else torch.float32

    for tag, model_path in model_map.items():
        print("\n==============================================")
        print(f"Tag: {tag}")
        print(f"Loading model: {model_path}")

        tokenizer = AutoTokenizer.from_pretrained(
            model_path,
            local_files_only=os.path.isdir(model_path),
        )
        tokenizer.pad_token = tokenizer.pad_token or tokenizer.eos_token
        # For CUDA we let hf Accelerate shard the model across available GPUs with
        # `device_map="auto"`. In that case the returned model already lives on
        # multiple devices and an additional `.to(device)` would try to move all
        # parameters onto a single GPU, triggering the "expected all tensors on
        # same device" runtime error. Hence we only call `.to(device)` when we
        # did *not* request automatic sharding.

        device_map = "auto" if device == "cuda" else None

        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=dtype,
            device_map=device_map,
            local_files_only=os.path.isdir(model_path),
        )

        if device_map is None:
            # on cpu, the model needs to be moved explicitly, unlike on device_map=auto
            model = model.to(device)
        model.eval()

        tag_output_dir = output_dir / tag
        tag_output_dir.mkdir(parents=True, exist_ok=True)

        for convo_path in convo_files:
            print(f"\n[{tag}] Processing {convo_path.name}")
            prompt_core = parse_convo_file(convo_path)

            if template_text is not None:
                if "TASK:" in template_text:
                    before, _sep, after = template_text.partition("TASK:")
                    after_lines = after.splitlines(keepends=True)
                    after_tail = "".join(after_lines[1:]) if after_lines else ""

                    task_text = (
                        "Return python code for this pcell, described in strict syntax:\n"
                        f"{prompt_core}"
                    )

                    prompt = f"{before}TASK: {task_text}\n{after_tail}"
                else:
                    prompt = template_text + "\n" + prompt_core
            else:
                prompt = prompt_core

            generated_code = generate_code(
                model,
                tokenizer,
                prompt,
                max_tokens=args.max_tokens,
                temperature=args.temperature,
            )

            output_path = tag_output_dir / f"{convo_path.stem}.py"
            output_path.write_text(generated_code, encoding="utf-8")
            print(
                f"Saved -> {output_path.relative_to(Path.cwd())} (chars={len(generated_code)})"
            )

        del model
        torch.cuda.empty_cache()

    print("\nAll models processed.")


if __name__ == "__main__": 
    main() 