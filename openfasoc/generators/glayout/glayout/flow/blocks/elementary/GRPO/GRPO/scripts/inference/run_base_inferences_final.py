import argparse
from pathlib import Path
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import time
from datasets import Dataset
from typing import Dict, List, Optional
import os


def clear_gpu_memory():
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()


def run_model_inference(model_source, combined_prompt, args, model_name=""):

    print(f"Loading {model_name} model from {model_source}...")
    
    try:
        start_load_time = time.time()
        model = AutoModelForCausalLM.from_pretrained(
            model_source,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            trust_remote_code=True,
        )
        tokenizer = AutoTokenizer.from_pretrained(model_source, trust_remote_code=True)
        load_time = time.time() - start_load_time
        print(f"{model_name} model loaded. ({load_time:.2f}s)")
    except Exception as e:
        print(f"Error loading {model_name}: {e}")
        return None
    
    # Run inference
    generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
    
    print(f"Running {args.num_inferences} inference(s) for {model_name} model...")
    start_time = time.time()
    
    # inferencing serially
    outputs = []
    for i in range(args.num_inferences):
        print(f"  Running inference {i+1}/{args.num_inferences}...")
        single_output = generator(
            combined_prompt,
            max_new_tokens=args.max_new_tokens,
            pad_token_id=tokenizer.eos_token_id,
            batch_size=1,  
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            top_k=args.top_k,
            repetition_penalty=args.repetition_penalty,
            return_full_text=False,
        )
        outputs.append(single_output)
    
    # ORIGINAL BATCHING CODE (commented out due to pad_token issues):
    # batch_prompts = [combined_prompt] * args.num_inferences
    # outputs = generator(
    #     batch_prompts,
    #     max_new_tokens=args.max_new_tokens,
    #     pad_token_id=tokenizer.eos_token_id,
    #     batch_size=8,
    #     do_sample=True,
    #     temperature=0.7,
    #     top_p=0.9,
    #     top_k=args.top_k,
    #     repetition_penalty=args.repetition_penalty,
    #     return_full_text=False,
    # )
    
    inference_time = time.time() - start_time
    
    #clearing memory, to prevent Cuda OOM issues
    del model, tokenizer, generator
    clear_gpu_memory()
    
    return outputs, inference_time, load_time


def clean_generated_code(text: str) -> str:
    # removal of opening code block markers (```python, ```py, ```), as they cause compilation issues
    text = text.strip()
    
    patterns_to_remove = [
        "```python\n",
        "```py\n", 
        "```\n"
    ]
    
    for pattern in patterns_to_remove:
        if text.startswith(pattern):
            text = text[len(pattern):].lstrip()
            break
    
    if text.endswith("\n```"):
        text = text[:-4].rstrip()
    elif text.endswith("```"):
        text = text[:-3].rstrip()
    
    return text


def main() -> None:
    parser = argparse.ArgumentParser(description="Run inference on a model")
    parser.add_argument("--model_size", choices=["7b", "13b"], help="Model size to use")
    parser.add_argument("--model_dir", type=Path, help="Path to model directory")
    parser.add_argument("--use_base_api", action="store_true", help="Use base HuggingFace model instead of local")
    parser.add_argument("--prompt_file", type=Path, required=True, help="Path to prompt file")
    parser.add_argument("--instruction_file", type=Path, help="Path to instruction file to prepend")
    parser.add_argument("--num_inferences", type=int, default=10, help="Number of inferences to run")
    parser.add_argument("--compare_models", action="store_true", help="Compare 7b and 13b models")
    parser.add_argument("--model_13b_dir", type=Path, help="Path to 13b model for comparison")
    parser.add_argument("--verbose", action="store_true", help="Display generated responses")
    parser.add_argument("--max_new_tokens", type=int, default=2048, help="Maximum new tokens to generate")
    parser.add_argument("--top_k", type=int, default=50, help="Top-k sampling parameter")
    parser.add_argument("--repetition_penalty", type=float, default=1.1, help="Repetition penalty parameter")
    parser.add_argument("--output_dir", type=Path, help="Custom output directory for results")
    args = parser.parse_args()
    

    if args.compare_models:
        if not args.model_size:
            args.model_size = "7b"  # default for comparision
        if not args.model_13b_dir and not args.use_base_api:
            repo_root = Path(__file__).resolve().parent.parent.parent
            args.model_13b_dir = repo_root / "models" / "run-2" / "finetuned" / "13b" / "final_model"
    elif not args.model_size:
        parser.error("--model_size is required when not using --compare_models")

    # resolve repo root (three levels up from this script)
    repo_root = Path(__file__).resolve().parent.parent.parent

    # setup paths
    if args.model_dir is not None:
        model_source = args.model_dir
    elif args.use_base_api:
        # hard-coded CodeLlama Instruct ids
        hf_map = {
            "7b": "codellama/CodeLlama-7b-Instruct-hf",
            "13b": "codellama/CodeLlama-13b-Instruct-hf",
        }
        model_source = hf_map[args.model_size]
    else:
        model_source = repo_root / "models" / "run-2" / "finetuned" / args.model_size / "final_model"

    if "run-3" in str(model_source):
        run_tag = "run-3"
    elif "run-2" in str(model_source):
        run_tag = "run-2"
    elif "run-1" in str(model_source):
        run_tag = "run-1"
    else:
        run_tag = "run-custom"
    
    # custom output directory if provided, otherwise use default
    if args.output_dir:
        output_dir = args.output_dir
    else:
        output_dir = repo_root / "predictions" / run_tag / args.model_size
    output_dir.mkdir(parents=True, exist_ok=True)

    if not args.use_base_api and isinstance(model_source, Path) and not model_source.exists():
        print(f"Error: Local model path not found at {model_source}. Use --use_base_api to load the CodeLlama HF model instead.")
        return


    try:
        prompt_text = args.prompt_file.read_text()

        # building the final prompt
        if args.instruction_file is not None:
            if not args.instruction_file.exists():
                print(f"Error: instruction file {args.instruction_file} not found!")
                return
            instruction_text = args.instruction_file.read_text()
            combined_prompt = instruction_text.rstrip() + "\n\n" + prompt_text.lstrip()
        else:
            combined_prompt = prompt_text
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    if args.compare_models:
        # for comparision
        print("=" * 60)
        print("Comparision Mode: Testing 7B vs 13B models")
        print("=" * 60)
        
        if args.use_base_api:
            model_13b_source = "codellama/CodeLlama-13b-Instruct-hf"
        else:
            model_13b_source = args.model_13b_dir
        
        print("\nTesting 7B Model:")
        print("-" * 40)
        result_7b = run_model_inference(model_source, combined_prompt, args, "7B")
        
        print("\nTesting 13B Model:")
        print("-" * 40)
        result_13b = run_model_inference(model_13b_source, combined_prompt, args, "13B")
        
        print("\n" + "=" * 60)
        print("Comparision Results")
        print("=" * 60)
        
        if result_7b:
            outputs_7b, inference_time_7b, load_time_7b = result_7b
            print(f"\n7B Model:")
            print(f"  Load Time: {load_time_7b:.2f}s")
            print(f"  Inference Time: {inference_time_7b:.2f}s")
            print(f"  Responses: {len(outputs_7b)}")
            if args.verbose and outputs_7b:
                print(f"  First Response:\n{outputs_7b[0][0]['generated_text'][:200]}...")
        
        if result_13b:
            outputs_13b, inference_time_13b, load_time_13b = result_13b
            print(f"\n13B Model:")
            print(f"  Load Time: {load_time_13b:.2f}s") 
            print(f"  Inference Time: {inference_time_13b:.2f}s")
            print(f"  Responses: {len(outputs_13b)}")
            if args.verbose and outputs_13b:
                print(f"  First Response:\n{outputs_13b[0][0]['generated_text'][:200]}...")
        
        print(f"\nComparison completed!")
        
    else:
        # single model mode
        result = run_model_inference(model_source, combined_prompt, args, f"{args.model_size}")
        
        if not result:
            return
            
        outputs, inference_time, load_time = result
        
        for i, output_list in enumerate(outputs):
            generated_text = output_list[0]["generated_text"]
            
            cleaned_code = clean_generated_code(generated_text)
            
            output_file = output_dir / f"prediction_{i + 1}.py"  
            output_file.write_text(cleaned_code)
            
            # verbose output in terminal
            if args.verbose:
                print(f"\nResponse {i + 1}:")
                print("-" * 40)
                print(cleaned_code)
                print("-" * 40)
        
        total_time = inference_time + load_time
        print(f"All {args.num_inferences} outputs saved to {output_dir}")
        print(f"Total time: {total_time:.2f}s .")


if __name__ == "__main__":
    main() 