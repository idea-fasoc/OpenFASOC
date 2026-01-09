import argparse
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


def generate(model_path: str, prompt: str, device: str, dtype: torch.dtype, max_new: int, temperature: float, top_p: float, repetition_penalty: float, no_repeat_ngram_size: int) -> str:
    tok = AutoTokenizer.from_pretrained(model_path)
    tok.pad_token = tok.pad_token or tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        device_map="auto" if device == "cuda" else None,
        torch_dtype=dtype,
        local_files_only=os.path.isdir(model_path),
    )
    model.eval()
    inputs = tok(prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        out_ids = model.generate(
            **inputs,
            max_new_tokens=max_new,
            temperature=temperature,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
            no_repeat_ngram_size=no_repeat_ngram_size,
            do_sample=temperature > 0,
            pad_token_id=tok.eos_token_id,
            eos_token_id=tok.eos_token_id,
            early_stopping=True,
        )
    txt = tok.decode(out_ids[0, inputs["input_ids"].shape[1]:], skip_special_tokens=True)
    del model
    torch.cuda.empty_cache()
    return txt.strip()


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--prompt", required=True)
    p.add_argument("--finetuned_dir", default="./final_model")
    p.add_argument("--base_repo", default="codellama/CodeLlama-13b-Instruct-hf")
    p.add_argument("--max_new_tokens", type=int, default=2048)
    p.add_argument("--temperature", type=float, default=0.2)
    p.add_argument("--top_p", type=float, default=0.9)
    p.add_argument("--finetuned_output", default="finetuned_output.txt")
    p.add_argument("--base_output", default="base_output.txt")
    p.add_argument("--repetition_penalty", type=float, default=1.1)
    p.add_argument("--no_repeat_ngram_size", type=int, default=6)
    a = p.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32

    tuned = generate(a.finetuned_dir, a.prompt, device, dtype, a.max_new_tokens, a.temperature, a.top_p, a.repetition_penalty, a.no_repeat_ngram_size)
    open(a.finetuned_output, "w", encoding="utf-8").write(tuned + "\n")

    base = generate(a.base_repo, a.prompt, device, dtype, a.max_new_tokens, a.temperature, a.top_p, a.repetition_penalty, a.no_repeat_ngram_size)
    open(a.base_output, "w", encoding="utf-8").write(base + "\n")

    print("--- 13B fine-tuned (trimmed) ---\n", tuned[:300])
    print("\n--- 13B base (trimmed) ---\n", base[:300])


if __name__ == "__main__":
    main()
