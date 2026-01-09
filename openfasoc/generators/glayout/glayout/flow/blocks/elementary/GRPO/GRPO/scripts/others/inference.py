#!/usr/bin/env python3
"""Simple inference for 13B fine-tuned checkpoint."""

import argparse, torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model_dir", default="./final_model")
    p.add_argument("--prompt", required=True)
    p.add_argument("--max_new_tokens", type=int, default=1024)
    p.add_argument("--temperature", type=float, default=0.2)
    p.add_argument("--top_p", type=float, default=0.9)
    p.add_argument("--repetition_penalty", type=float, default=1.1)
    p.add_argument("--no_repeat_ngram_size", type=int, default=6)
    a = p.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32

    tok = AutoTokenizer.from_pretrained(a.model_dir)
    tok.pad_token = tok.pad_token or tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(a.model_dir, device_map="auto" if device=="cuda" else None, torch_dtype=dtype)
    model.eval()

    inp = tok(a.prompt, return_tensors="pt").to(device)
    streamer = TextStreamer(tok)
    with torch.no_grad():
        model.generate(
            **inp,
            max_new_tokens=a.max_new_tokens,
            temperature=a.temperature,
            top_p=a.top_p,
            do_sample=a.temperature > 0,
            pad_token_id=tok.eos_token_id,
            eos_token_id=tok.eos_token_id,
            early_stopping=True,
            repetition_penalty=a.repetition_penalty,
            no_repeat_ngram_size=a.no_repeat_ngram_size,
            streamer=streamer,
        )

if __name__ == "__main__":
    main() 