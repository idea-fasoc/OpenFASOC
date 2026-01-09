"""
End-to-End LLM Fine-tuning Pipeline
===================================

This script performs the complete iterative fine-tuning workflow, end to end:

Step 1: Generic code finetuning
1. Base model inference → generates predictions on OpenFASOC prompts
2. Domain adaptation → Model learns OpenFASOC code patterns from raw files
3. Model inference → Generates initial predictions

Step 2: Self-code fixing 
1. Previous model inference → generates predictions
2. Save inference as Python files
3. Compile Python files and save compiler output
4. Pass files + output to master model → analyzes code quality
5. Model + Master model output learns from structured issue/fix data
6. Use master model output as SFT dataset for next iteration
7. Fine-tuned model inference → generates new predictions

FINAL STEP: Metrics Generation
8. Generate metrics and plots from all iterations


Usage:
------
python end_to_end.py \
    --run_both \
    --iterations 4 \
    --epochs_per_iteration 1 \
    --learning_rate 1e-6 \
    --train_last_n_layers 6 \
    --weight_decay 0.001 \
    --warmup_ratio 0.05 \
    --max_grad_norm 2.0 \
    --google_api_key AIzaSyB1lnuPg-kvpK9ysRGOkQfQb1oW70EFe_Q \
    --prompt_file scripts/utils/prompt.txt
"""


import argparse
import subprocess
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import os
import time


class EndToEndPipeline:
    """Orchestrates the complete fine-tuning pipeline."""
    
    def __init__(self, args):
        self.args = args
        self.repo_root = Path(__file__).resolve().parent
        self.current_iteration = 0
        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        self.pipeline_dir = self.repo_root / "pipeline_runs" / self.run_id
        self.models_dir = self.pipeline_dir / "models"
        self.data_dir = self.pipeline_dir / "data" 
        self.outputs_dir = self.pipeline_dir / "outputs"
        self.compile_dir = self.pipeline_dir / "compile_results"
        self.master_predictions_dir = self.pipeline_dir / "master_predictions"
        self.training_data_dir = self.pipeline_dir / "training_data"
        
        for dir_path in [self.models_dir, self.data_dir, self.outputs_dir, 
                        self.compile_dir, self.master_predictions_dir, self.training_data_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        os.environ.setdefault('WANDB_DIR', str(self.pipeline_dir / 'wandb'))
            
        self.current_model_path = args.base_model  
        
        print(f"Starting End-to-End Pipeline")
        print(f"Pipeline directory: {self.pipeline_dir}")
        print(f"Iterations: {args.iterations}")
        print(f"Model size: {args.model_size}")
        print(f"Inferences per iteration: {args.inferences_per_iteration}")

    def log(self, message: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")

    def run_command(self, cmd: List[str], description: str, cwd: Optional[Path] = None) -> bool:
        self.log(f"Running: {description}")
        self.log(f"Command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd, 
                cwd=cwd or self.repo_root,
                check=True,
                capture_output=True,
                text=True
            )
            self.log(f"{description} completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"{description} failed with return code {e.returncode}", "ERROR")
            self.log(f"STDOUT: {e.stdout}", "ERROR")
            self.log(f"STDERR: {e.stderr}", "ERROR")
            return False

    def step_1_base_inference(self) -> bool:
        """Step 1: Run inference with base HF model."""
        self.log("=== STEP 1: Base Model Inference ===")
        
        output_dir = self.outputs_dir / f"iteration_{self.current_iteration}" / "base"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            sys.executable, "scripts/inference/run_base_inferences.py",
            "--model_size", self.args.model_size,
            "--num_inferences", str(self.args.inferences_per_iteration),
            "--prompt_file", str(self.args.prompt_file),
            "--max_new_tokens", str(self.args.max_new_tokens),
            "--top_k", str(self.args.top_k),
            "--repetition_penalty", str(self.args.repetition_penalty),
            "--output_dir", str(output_dir),
        ]
        
        if self.current_iteration == 0:
            #base model from HF
            cmd.extend(["--use_base_api"])
        else:
            #subsequently: use previously fine-tuned model
            cmd.extend(["--model_dir", str(self.current_model_path)])
            
        if self.args.instruction_file:
            cmd.extend(["--instruction_file", str(self.args.instruction_file)])
            
        return self.run_command(cmd, "Base model inference")

    def step_2_finetune_model(self) -> bool:
        """Step 2: Fine-tune model on OpenFASOC data."""
        self.log("=== STEP 2: Fine-tune Model ===")
        if self.current_iteration == 0:
            self.log("🔧 Stage 1: Domain adaptation on raw OpenFASOC files")
            
            base_model = self.args.base_model
            if "7b" in base_model.lower():
                model_key = "7b"
            elif "13b" in base_model.lower():
                model_key = "13b"
            else:
                model_key = base_model
                            
            self.log("Processing OpenFASOC data...")
            processed_data_dir = self.data_dir / f"processed_iteration_{self.current_iteration}"
            process_cmd = [
                sys.executable, "scripts/others/process_data.py",
                "--model", model_key,
                "--openfasoc_path", "external/OpenFASOC/", 
                "--output_dir", str(processed_data_dir),  
            ]
            
            process_success = self.run_command(process_cmd, "OpenFASOC data processing")
            if not process_success:
                self.log("Failed to process OpenFASOC data", "ERROR")
                return False
            
            self.log("Running domain adaptation fine-tuning...")
            model_output_dir = self.models_dir / f"iteration_{self.current_iteration}"
            
            finetune_cmd = [
                sys.executable, "scripts/others/gpu_finetune.py",
                "--model", model_key,
                "--output_dir", str(model_output_dir),
                "--checkpoint_dir", str(model_output_dir / "checkpoints"),
                "--training_data_dir", str(processed_data_dir),
                "--num_train_epochs", str(self.args.epochs_per_iteration),
                "--train_last_n_layers", str(self.args.train_last_n_layers),  # Freeze lower layers to preserve base abilities
            ]
            
            success = self.run_command(finetune_cmd, "Running initial finetuning on code files.")
            
            if success:
                # Use adapter path (not merged model path) - saves 99.7% space
                self.current_model_path = str(model_output_dir)
                self.log(f"Initial finetuning complete! Using LoRA adapter at: {model_output_dir}")                
            return success
            
        else:
            
            #get training data from previous iteration's master model output
            training_data = self.training_data_dir / f"iteration_{self.current_iteration-1}_training.jsonl"
                
            if not training_data.exists():
                self.log(f"Training data not found: {training_data}", "ERROR")
                return False
                
            # Output path for fine-tuned model
            model_output_dir = self.models_dir / f"iteration_{self.current_iteration}"
            
            # Build command for train.py (structured training with LoRA)
            cmd = [
                sys.executable, "scripts/training/train.py",
                "--train_file", str(training_data),
                "--output_dir", str(model_output_dir),
                "--model_paths", self.current_model_path,
                "--use_lora",  # Enable LoRA
                "--lora_r", str(self.args.lora_r),
                "--lora_alpha", str(self.args.lora_alpha),
                "--lora_dropout", str(self.args.lora_dropout),
                "--num_train_epochs", str(self.args.epochs_per_iteration),
                "--learning_rate", str(self.args.learning_rate),
                "--max_length", str(self.args.max_length),
                "--logging_steps", "10",
                "--save_total_limit", "2",
                "--weight_decay", str(self.args.weight_decay),
                "--warmup_ratio", str(self.args.warmup_ratio),
                "--max_grad_norm", str(self.args.max_grad_norm),
            ]
            
            # Add 8-bit quantization if requested
            if self.args.use_8bit:
                cmd.append("--use_8bit")
            
            success = self.run_command(cmd, "Running second iteration of finetuning with LoRA")
            
            if success:
                # Use adapter path directly (no merged model) - saves 99.7% space
                model_name = Path(self.current_model_path).name.replace("/", "_")
                self.current_model_path = str(model_output_dir / model_name)
                self.log(f"LoRA training complete. Using adapter at: {self.current_model_path}")
                
            return success

# ============================================ ignore this codeblock. this is currently not useful
        
        # if self.current_iteration == 0:
        #     # First iteration: use external OpenFASOC data
        #     training_data = self.get_initial_training_data()
        # else:
        #     # Subsequent iterations: use master model output from previous iteration
        #     training_data = self.training_data_dir / f"iteration_{self.current_iteration-1}_training.jsonl"
        #     
        # if not training_data.exists():
        #     self.log(f"Training data not found: {training_data}", "ERROR")
        #     return False
        #     
        # # Output path for fine-tuned model
        # model_output_dir = self.models_dir / f"iteration_{self.current_iteration}"
        # 
        # cmd = [
        #     sys.executable, "scripts/training/train.py",
        #     "--train_file", str(training_data),
        #     "--output_dir", str(model_output_dir),
        #     "--model_paths", self.current_model_path,
        #     "--full_weight_training",
        #     "--train_last_n_layers", str(self.args.train_last_n_layers),
        #     "--num_train_epochs", str(self.args.epochs_per_iteration),
        #     "--learning_rate", str(self.args.learning_rate),
        #     "--max_length", str(self.args.max_length),
        #     "--logging_steps", "10",
        #     "--save_total_limit", "2",
        #     "--weight_decay", str(self.args.weight_decay),
        #     "--warmup_ratio", str(self.args.warmup_ratio),
        #     "--max_grad_norm", str(self.args.max_grad_norm),
        # ]
        # 
        # success = self.run_command(cmd, "Model fine-tuning")
        # 
        # if success:
        #     # Update current model path to the newly fine-tuned model
        #     # The training script creates a subdirectory with the model name
        #     model_name = Path(self.current_model_path).name.replace("/", "_")
        #     self.current_model_path = str(model_output_dir / model_name)
        #     self.log(f"Updated model path: {self.current_model_path}")
        #     
        # return success

    def step_3_finetuned_inference(self) -> bool:
        self.log("=== STEP 3: Fine-tuned Model Inference ===")
        
        output_dir = self.outputs_dir / f"iteration_{self.current_iteration}" / "finetuned"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            sys.executable, "scripts/inference/run_base_inferences.py",
            "--model_size", self.args.model_size,
            "--num_inferences", str(self.args.inferences_per_iteration),
            "--prompt_file", str(self.args.prompt_file),
            "--model_dir", str(self.current_model_path),
            "--max_new_tokens", str(self.args.max_new_tokens),
            "--top_k", str(self.args.top_k),
            "--repetition_penalty", str(self.args.repetition_penalty),
            "--output_dir", str(output_dir),  # Add output directory
        ]
        
        if self.args.instruction_file:
            cmd.extend(["--instruction_file", str(self.args.instruction_file)])
            
        return self.run_command(cmd, "Fine-tuned model inference")

    def step_4_5_compile_outputs(self) -> bool:
        """Steps 4-5: Compile Python files and save compiler output."""
        self.log("=== STEPS 4-5: Compile Generated Python Files ===")
        
        output_dir = self.outputs_dir / f"iteration_{self.current_iteration}" / "finetuned"
        compile_output_dir = self.compile_dir / f"iteration_{self.current_iteration}"
        compile_output_dir.mkdir(parents=True, exist_ok=True)
        
        py_files = list(output_dir.rglob("*.py"))
        txt_files = list(output_dir.rglob("*.txt")) 
        all_code_files = py_files + txt_files
        
        if not all_code_files:
            self.log(f"No code files found in {output_dir}", "ERROR")
            return False
            
        self.log(f"Found {len(all_code_files)} code files to compile (.py: {len(py_files)}, .txt: {len(txt_files)})")
        
        # compile each file and save results
        for code_file in all_code_files:
            # for .txt files, create a temporary .py file for compilation
            if code_file.suffix == ".txt":
                temp_py_file = code_file.with_suffix(".py")
                temp_py_file.write_text(code_file.read_text())
                compile_target = temp_py_file
                cleanup_temp = True
            else:
                compile_target = code_file
                cleanup_temp = False
                
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "py_compile", str(compile_target)],
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
                status = "compiled" if result.returncode == 0 else "not compiled"
                output = (result.stdout or "") + (result.stderr or "")
            except Exception as exc:
                status = "not compiled"
                output = str(exc)
            finally:
                #clean up temporary file if created
                if cleanup_temp and temp_py_file.exists():
                    temp_py_file.unlink()
            
            # save compilation result
            rel_path = code_file.relative_to(output_dir)
            log_path = compile_output_dir / rel_path.with_suffix(".log")
            log_path.parent.mkdir(parents=True, exist_ok=True)
            log_path.write_text(
                f"file: {rel_path}\nstatus: {status}\n\n{output}",
                encoding="utf-8",
            )
            self.log(f"Compiled {rel_path} → {status}")
            
        return True

    def step_6_master_model_inference(self) -> bool:
        self.log("=== STEP 6: Master Model Inference ===")
        
        code_dir = self.outputs_dir / f"iteration_{self.current_iteration}" / "finetuned"
        compile_results_dir = self.compile_dir / f"iteration_{self.current_iteration}"
        master_output_dir = self.master_predictions_dir / f"iteration_{self.current_iteration}"
        
        # Set up environment for Google API
        env = os.environ.copy()
        if self.args.google_api_key:
            env["GOOGLE_API_KEY"] = self.args.google_api_key
            
        # Create a temporary dataset structure that master_inference expects
        temp_dataset_root = master_output_dir.parent / "temp_dataset"
        temp_outputs_dir = temp_dataset_root / "outputs" / self.args.model_size
        temp_compile_dir = temp_dataset_root / "compile_results" / self.args.model_size
        
        temp_outputs_dir.mkdir(parents=True, exist_ok=True)
        temp_compile_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy Python files to the structured outputs directory
        import shutil
        for py_file in code_dir.glob("*.py"):
            shutil.copy2(py_file, temp_outputs_dir)
            
        # Copy compilation logs to the structured compile directory
        for log_file in compile_results_dir.glob("*.log"):
            shutil.copy2(log_file, temp_compile_dir)
            
        cmd = [
            sys.executable, "scripts/inference/master_inference.py",
            "--model", self.args.master_model,
            "--dataset_root", str(temp_dataset_root),
            "--output_dir", str(master_output_dir),
            "--max_tokens", str(self.args.master_max_tokens),
            "--overwrite",
        ]
        
        if self.args.finetuned_prompt:
            cmd.append("--finetuned")
            
        try:
            result = subprocess.run(
                cmd,
                cwd=self.repo_root,
                check=True,
                capture_output=True,
                text=True,
                env=env
            )
            self.log("Master model inference completed successfully")
            
            # Clean up temporary directory
            shutil.rmtree(temp_dataset_root, ignore_errors=True)
            return True
            
        except subprocess.CalledProcessError as e:
            self.log(f"Master model inference failed with return code {e.returncode}", "ERROR")
            self.log(f"STDOUT: {e.stdout}", "ERROR") 
            self.log(f"STDERR: {e.stderr}", "ERROR")
            
            # Clean up temporary directory on error too
            shutil.rmtree(temp_dataset_root, ignore_errors=True)
            return False

    def step_7_convert_to_training_data(self) -> bool:
        """Step 7: Convert master model output to SFT training data."""
        self.log("=== STEP 7: Convert Master Output to Training Data ===")
        
        master_output_dir = self.master_predictions_dir / f"iteration_{self.current_iteration}"
        
        cmd = [
            sys.executable, "scripts/utils/convert_training_data.py",
            "--in_dir", str(master_output_dir),
            "--tag", f"iteration_{self.current_iteration}",
        ]
        
        success = self.run_command(cmd, "Convert master output to training data")
        
        if success:
            # Move the generated training data to our pipeline directory
            processed_dir = self.repo_root / "data" / "processed"
            target_file = self.training_data_dir / f"iteration_{self.current_iteration}_training.jsonl"
            
            # Find the generated file (could be 7b or 13b)
            source_pattern = f"train_data_{self.args.model_size}_iteration_{self.current_iteration}_clean.jsonl"
            source_file = processed_dir / source_pattern
            
            if source_file.exists():
                shutil.move(str(source_file), str(target_file))
                self.log(f"Moved training data to {target_file}")
            else:
                self.log(f"Training data file not found: {source_file}", "ERROR")
                return False
                
        return success

    def get_initial_training_data(self) -> Path:
        """Get initial training data from external OpenFASOC."""
        
        # =================================================================
        # MODIFICATION NOTE: This function is no longer used for iteration 0
        # since gpu_finetune.py now handles domain adaptation directly on
        # raw OpenFASOC files via process_data.py. This function is kept
        # for potential future use or debugging purposes.
        # =================================================================
        
        self.log("Warning: get_initial_training_data() called but iteration 0 now uses gpu_finetune.py")
        
        # Check if there's existing processed data we can use (legacy support)
        existing_data = self.repo_root / "data" / "processed"
        if existing_data.exists():
            for jsonl_file in existing_data.glob(f"*{self.args.model_size}*.jsonl"):
                self.log(f"Using existing training data: {jsonl_file}")
                return jsonl_file
                
        # Fallback to bootstrap data if needed
        bootstrap_file = self.training_data_dir / "bootstrap_training.jsonl"
        self.create_bootstrap_training_data(bootstrap_file)
        return bootstrap_file

        # =================================================================
        # ORIGINAL CODE (COMMENTED OUT)
        # This was the original implementation before two-stage training
        # =================================================================
        
        # # This would need to be implemented based on how the external data is structured
        # # For now, create a placeholder
        # external_data = self.repo_root / "external" / "OpenFASOC"
        # 
        # # Check if there's existing processed data we can use
        # existing_data = self.repo_root / "data" / "processed"
        # if existing_data.exists():
        #     for jsonl_file in existing_data.glob(f"*{self.args.model_size}*.jsonl"):
        #         self.log(f"Using existing training data: {jsonl_file}")
        #         return jsonl_file
        #         
        # # If no existing data, create minimal training data for bootstrapping
        # bootstrap_file = self.training_data_dir / "bootstrap_training.jsonl"
        # self.create_bootstrap_training_data(bootstrap_file)
        # return bootstrap_file

    # def create_bootstrap_training_data(self, output_file: Path):
    #     """Create minimal bootstrap training data."""
        
    #     # =================================================================
    #     # MODIFICATION NOTE: This bootstrap data is now only used as a fallback.
    #     # Iteration 0 uses gpu_finetune.py for domain adaptation on raw OpenFASOC files.
    #     # This function remains for legacy support or emergency fallback scenarios.
    #     # =================================================================
        
    #     self.log("Creating minimal bootstrap training data (fallback mode)")
        
    #     bootstrap_samples = [
    #         {
    #             "filename": "voltage_follower.py",
    #             "analysis": [{
    #                 "issue": "Missing import statements",
    #                 "explanation": {
    #                     "problem": "Code lacks necessary gdsfactory/glayout imports",
    #                     "reason": "Required for component creation and routing",
    #                     "fix": "Add proper import statements"
    #                 }
    #             }],
    #             "fixed_code": "import gdsfactory as gf\nfrom glayout.flow.primitives.fet import pmos, nmos\n\ndef voltage_follower():\n    # Basic voltage follower implementation\n    pass"
    #         }
    #     ]
        
    #     with output_file.open("w") as f:
    #         for sample in bootstrap_samples:
    #             f.write(json.dumps(sample) + "\n")
                
    #     self.log(f"Created bootstrap training data with {len(bootstrap_samples)} samples")

    def run_iteration(self, iteration: int) -> bool:
        """Run a single iteration of the pipeline."""
        self.current_iteration = iteration
        self.log(f"Starting Iteration {iteration + 1}/{self.args.iterations}")
        
        steps = [
            ("Base Inference", self.step_1_base_inference),
            ("Fine-tune Model", self.step_2_finetune_model), 
            ("Fine-tuned Inference", self.step_3_finetuned_inference),
            ("Compile Outputs", self.step_4_5_compile_outputs),
            ("Master Model Inference", self.step_6_master_model_inference),
            ("Convert to Training Data", self.step_7_convert_to_training_data),
        ]
        
        for step_name, step_func in steps:
            self.log(f"⚡ {step_name}")
            start_time = time.time()
            
            if not step_func():
                self.log(f"Iteration {iteration + 1} failed at step: {step_name}", "ERROR")
                return False
                
            elapsed = time.time() - start_time
            self.log(f"{step_name} completed in {elapsed:.1f}s")
            
        self.log(f"Iteration {iteration + 1} completed successfully")
        return True

    def step_8_generate_metrics(self) -> bool:
        self.log("=== STEP 8: Generate Metrics and Plots ===")
        
        # Create plots directory inside pipeline run for better organization
        plots_dir = self.pipeline_dir / "plots"
        plots_dir.mkdir(exist_ok=True)
        
        # Set environment variable for metrics script to save plots in pipeline directory
        env = os.environ.copy()
        env["PIPELINE_PLOTS_DIR"] = str(plots_dir)
        env["MODEL_SIZE"] = self.args.model_size
        
        cmd = [
            sys.executable, "scripts/utils/metrics_output.py"
        ]
        
        self.log(f"Running: Generate metrics and plots")
        self.log(f"Command: {' '.join(cmd)}")
        self.log(f"Plots will be saved to: {plots_dir}")
        
        try:
            result = subprocess.run(
                cmd, 
                cwd=self.repo_root,
                check=True,
                capture_output=True,
                text=True,
                env=env  # Pass environment variables
            )
            self.log(f"Generate metrics and plots completed successfully")
            self.log(f"Plots saved in: {plots_dir}")
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"Generate metrics and plots failed with return code {e.returncode}", "ERROR")
            self.log(f"STDOUT: {e.stdout}", "ERROR")
            self.log(f"STDERR: {e.stderr}", "ERROR")
            return False

    def run_pipeline(self):
        """Run the complete pipeline."""
        self.log("🚀 Starting End-to-End Pipeline")
        
        try:
            for iteration in range(self.args.iterations):
                if not self.run_iteration(iteration):
                    self.log(f"Pipeline failed at iteration {iteration + 1}", "ERROR")
                    return False
            
            # Generate final metrics and plots
            self.log("Generating final metrics and plots...")
            start_time = time.time()
            if not self.step_8_generate_metrics():
                self.log("Metrics generation failed, but pipeline completed successfully", "WARNING")
            else:
                elapsed = time.time() - start_time
                self.log(f"Metrics and plots generated in {elapsed:.1f}s")
                self.log(f"Plots saved in: plots/ directory")
                    
            self.log("Complete pipeline finished successfully!")
            self.log(f"Results saved in: {self.pipeline_dir}")
            return True
            
        except KeyboardInterrupt:
            self.log("Pipeline interrupted by user", "ERROR")
            return False
        except Exception as e:
            self.log(f"Pipeline failed with exception: {e}", "ERROR")
            return False


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="End-to-End LLM Fine-tuning Pipeline",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Model configuration
    parser.add_argument("--model_size", choices=["7b", "13b"], required=True,
                       help="Size of the model to fine-tune")
    parser.add_argument("--base_model", type=str, 
                       default="codellama/CodeLlama-7b-Instruct-hf",
                       help="Base model from HuggingFace")
    parser.add_argument("--master_model", type=str, 
                       default="gemini-2.5-pro",
                       help="Master model for generating training data")
    
    # API configuration  
    parser.add_argument("--google_api_key", type=str,
                       help="Google API key for Gemini (or set GOOGLE_API_KEY env var)")
    
    # Input files
    parser.add_argument("--prompt_file", type=Path, required=True,
                       help="Path to prompt file for inference")
    parser.add_argument("--instruction_file", type=Path,
                       help="Optional instruction file to prepend to prompts")
    
    # Pipeline configuration
    parser.add_argument("--iterations", type=int, default=3,
                       help="Number of fine-tuning iterations")
    parser.add_argument("--run_both", action="store_true",
                       help="Run the full pipeline sequentially for both 7b and 13b models")
    parser.add_argument("--inferences_per_iteration", type=int, default=10,
                       help="Number of inferences per iteration")
    
    # Training parameters
    parser.add_argument("--epochs_per_iteration", type=int, default=3,
                       help="Training epochs per iteration")
    parser.add_argument("--learning_rate", type=float, default=3e-5,
                       help="Learning rate for fine-tuning")
    parser.add_argument("--train_last_n_layers", type=int, default=8,
                       help="Number of last layers to train")
    parser.add_argument("--max_length", type=int, default=1024,
                       help="Maximum sequence length for training")
    parser.add_argument("--weight_decay", type=float, default=0.01,
                       help="Weight decay for optimization")
    parser.add_argument("--warmup_ratio", type=float, default=0.1,
                       help="Warmup ratio for learning rate schedule")
    parser.add_argument("--max_grad_norm", type=float, default=1.0,
                       help="Maximum gradient norm for clipping")
    
    # LoRA Configuration (for memory-efficient training)
    parser.add_argument("--use_lora", action="store_true", default=True,
                       help="Use LoRA for memory-efficient fine-tuning (default: True)")
    parser.add_argument("--lora_r", type=int, default=16,
                       help="LoRA rank (8-64, higher = more capacity but more memory)")
    parser.add_argument("--lora_alpha", type=int, default=32,
                       help="LoRA alpha scaling (typically 2x lora_r)")
    parser.add_argument("--lora_dropout", type=float, default=0.05,
                       help="LoRA dropout rate")
    parser.add_argument("--use_8bit", action="store_true", default=False,
                       help="Use 8-bit quantization for even lower memory usage")
    
    # Inference parameters
    parser.add_argument("--max_new_tokens", type=int, default=2048,
                       help="Maximum new tokens for inference")
    parser.add_argument("--top_k", type=int, default=50,
                       help="Top-k sampling parameter")
    parser.add_argument("--repetition_penalty", type=float, default=1.1,
                       help="Repetition penalty for generation")
    parser.add_argument("--master_max_tokens", type=int, default=8192,
                       help="Maximum tokens for master model")
    parser.add_argument("--finetuned_prompt", action="store_true",
                       help="Use fine-tuned prompt variant for master model")
    
    args = parser.parse_args()
    
    # Validation
    if not args.prompt_file.exists():
        parser.error(f"Prompt file not found: {args.prompt_file}")
    if args.instruction_file and not args.instruction_file.exists():
        parser.error(f"Instruction file not found: {args.instruction_file}")
    if not args.google_api_key and not os.getenv("GOOGLE_API_KEY"):
        parser.error("Google API key required (--google_api_key or GOOGLE_API_KEY env var)")
        
    return args


def main():
    """Main entry point."""
    args = parse_args()

    # Decide which model sizes to run
    model_sizes = ["7b", "13b"] if args.run_both else [args.model_size]

    overall_success = True
    for sz in model_sizes:
        print("\n==============================")
        print(f"Launching pipeline for model size: {sz}")
        print("==============================\n")

        # Update args for this run
        args.model_size = sz
        # Adjust base model path only if user kept the default 7b path
        if args.base_model == "codellama/CodeLlama-7b-Instruct-hf" and sz == "13b":
            args.base_model = "codellama/CodeLlama-13b-Instruct-hf"
        elif args.base_model == "codellama/CodeLlama-13b-Instruct-hf" and sz == "7b":
            args.base_model = "codellama/CodeLlama-7b-Instruct-hf"

        pipeline = EndToEndPipeline(args)
        run_ok = pipeline.run_pipeline()
        overall_success = overall_success and run_ok

    sys.exit(0 if overall_success else 1)


if __name__ == "__main__":
    main()


"""
current command i'm using to run pipeline:


python end_to_end.py   --run_both   --model_size 7b   --prompt_file scripts/utils/prompt.txt   --iterations 4   --epochs_per_iteration 1   --learning_rate 1e-6   --train_last_n_layers 6   --weight_decay 0.001   --warmup_ratio 0.05   --max_grad_norm 2.0   --google_api_key AIzaSyB1lnuPg-kvpK9ysRGOkQfQb1oW70EFe_Q
"""