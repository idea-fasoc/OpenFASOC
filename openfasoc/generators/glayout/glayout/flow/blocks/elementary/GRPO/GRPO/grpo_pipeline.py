"""
GRPO Error Fixing Pipeline
===========================

This pipeline orchestrates the complete GRPO training and error-fixing workflow:
1. Load evaluation results from output.json
2. Run GRPO training using grpo.py
3. Extract errors and generate error-specific fix prompts
4. Use the trained model to generate fixed code
5. Create an iterative feedback loop

Usage:
------
python grpo_pipeline.py \
    --input_json output.json \
    --base_model "./models/finetuned/codellama-3-8b-instruct" \
    --output_dir grpo_outputs \
    --num_epochs 10 \
    --batch_size 12 \
    --iterations 3
"""

import torch
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import os
import sys
from dataclasses import dataclass

# Import GRPO trainer from existing grpo.py
from grpo import grpo_trainer
from transformers import AutoModelForCausalLM, AutoTokenizer


@dataclass
class ErrorSample:
    """Represents a sample with errors"""
    sample_id: int
    component_name: str
    parameters: Dict
    drc_errors: List[Dict]
    lvs_errors: Dict
    has_critical_errors: bool
    has_reviewable_errors: bool
    has_passable_errors: bool
    original_code: Optional[str] = None


class GRPOPipeline:
    """Orchestrates the complete GRPO training and error-fixing workflow"""
    
    def __init__(self, args):
        self.args = args
        self.root_dir = Path(args.output_dir)
        self.current_iteration = 0
        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create directory structure
        self.iteration_dir = self.root_dir / f"run_{self.run_id}"
        self.iteration_dir.mkdir(parents=True, exist_ok=True)
        
        # Device setup
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        self.log(f"GRPO Pipeline initialized")
        self.log(f"Output directory: {self.iteration_dir}")
        self.log(f"Device: {self.device}")
    
    def log(self, message: str, level: str = "INFO"):
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def load_evaluation_data(self) -> List[Dict]:
        """Load and parse output.json evaluation results"""
        self.log("Loading evaluation data from JSON")
        
        input_path = Path(self.args.input_json)
        if not input_path.exists():
            raise FileNotFoundError(f"Input JSON not found: {input_path}")
        
        with open(input_path, 'r') as f:
            data = json.load(f)
        
        # Handle both list and dict formats
        if isinstance(data, dict):
            data = [data]
        elif isinstance(data, list):
            pass
        else:
            raise ValueError(f"Unexpected JSON format: {type(data)}")
        
        self.log(f"Loaded {len(data)} samples from {input_path}")
        return data
    
    def extract_errors(self, samples: List[Dict]) -> Tuple[List[Dict], List[ErrorSample]]:
        """
        Extract and categorize errors from samples
        Returns: (all_samples, error_samples)
        """
        self.log("Extracting errors from samples")
        
        error_samples = []
        
        for sample in samples:
            # Extract DRC errors
            drc_errors = []
            has_critical = False
            has_reviewable = False
            has_passable = False
            
            if 'drc' in sample and 'summary' in sample['drc']:
                drc_summary = sample['drc']['summary']
                
                # Critical errors
                if drc_summary.get('critical_errors_count', 0) > 0:
                    has_critical = True
                    critical_details = drc_summary.get('critical_error_details', [])
                    for err in critical_details:
                        drc_errors.append({
                            'type': 'critical',
                            'rule': err.get('rule', 'Unknown'),
                            'details': err.get('details', '')
                        })
                
                # Reviewable errors
                if drc_summary.get('reviewable_errors_count', 0) > 0:
                    has_reviewable = True
                    reviewable_details = drc_summary.get('reviewable_error_details', [])
                    for err in reviewable_details:
                        drc_errors.append({
                            'type': 'reviewable',
                            'rule': err.get('rule', 'Unknown'),
                            'details': err.get('details', '')
                        })
                
                # Passable errors
                if drc_summary.get('passable_errors_count', 0) > 0:
                    has_passable = True
                    passable_details = drc_summary.get('passable_error_details', [])
                    for err in passable_details:
                        drc_errors.append({
                            'type': 'passable',
                            'rule': err.get('rule', 'Unknown'),
                            'details': err.get('details', '')
                        })
            
            # Extract LVS errors
            lvs_errors = {}
            if 'lvs' in sample and 'summary' in sample['lvs']:
                lvs_summary = sample['lvs']['summary']
                if not lvs_summary.get('is_pass', True):
                    lvs_errors = {
                        'conclusion': lvs_summary.get('conclusion', ''),
                        'total_mismatches': lvs_summary.get('total_mismatches', 0),
                        'mismatch_details': lvs_summary.get('mismatch_details', {})
                    }
            
            # Only create ErrorSample if there are errors
            if drc_errors or lvs_errors:
                error_sample = ErrorSample(
                    sample_id=sample.get('sample_id', -1),
                    component_name=sample.get('component_name', 'unknown'),
                    parameters=sample.get('parameters', {}),
                    drc_errors=drc_errors,
                    lvs_errors=lvs_errors,
                    has_critical_errors=has_critical,
                    has_reviewable_errors=has_reviewable,
                    has_passable_errors=has_passable
                )
                error_samples.append(error_sample)
        
        self.log(f"Found {len(error_samples)} samples with errors")
        self.log(f"  Critical: {sum(1 for s in error_samples if s.has_critical_errors)}")
        self.log(f"  Reviewable: {sum(1 for s in error_samples if s.has_reviewable_errors)}")
        self.log(f"  Passable: {sum(1 for s in error_samples if s.has_passable_errors)}")
        
        return samples, error_samples
    
    def retrieve_generated_code(self, sample_id: int, component_name: str) -> Optional[str]:
        """
        Retrieve stored Python code for a sample
        This assumes code is stored somewhere - adjust path as needed
        """
        # Check common locations where generated code might be stored
        possible_paths = [
            Path(f"generated_code/{component_name}.py"),
            Path(f"outputs/{component_name}.py"),
            Path(f"predictions/{component_name}.py"),
        ]
        
        for path in possible_paths:
            if path.exists():
                with open(path, 'r') as f:
                    return f.read()
        
        # If no code found, generate placeholder
        self.log(f"Warning: Could not find code for {component_name}, using placeholder", "WARNING")
        return f"# Generated code for {component_name}\n# Code retrieval failed - placeholder"
    
    def generate_error_prompts(self, error_samples: List[ErrorSample]) -> List[Dict]:
        """
        Generate error-specific prompts with original code and error details
        """
        self.log("Generating error-specific prompts")
        
        prompts = []
        
        for sample in error_samples:
            # Retrieve original code
            original_code = self.retrieve_generated_code(
                sample.sample_id,
                sample.component_name
            )
            sample.original_code = original_code
            
            # Generate prompts for DRC errors
            for i, drc_error in enumerate(sample.drc_errors):
                error_type = drc_error['type']
                rule = drc_error['rule']
                details = drc_error['details']
                
                # Create error-specific prompt
                prompt = self._create_drc_fix_prompt(
                    error_type=error_type,
                    rule=rule,
                    details=details,
                    component_name=sample.component_name,
                    original_code=original_code,
                    parameters=sample.parameters
                )
                
                prompts.append({
                    'sample_id': sample.sample_id,
                    'component_name': sample.component_name,
                    'error_type': f'DRC_{error_type}',
                    'error_index': i,
                    'prompt': prompt,
                    'original_code': original_code
                })
            
            # Generate prompts for LVS errors
            if sample.lvs_errors:
                prompt = self._create_lvs_fix_prompt(
                    lvs_errors=sample.lvs_errors,
                    component_name=sample.component_name,
                    original_code=original_code,
                    parameters=sample.parameters
                )
                
                prompts.append({
                    'sample_id': sample.sample_id,
                    'component_name': sample.component_name,
                    'error_type': 'LVS',
                    'error_index': 0,
                    'prompt': prompt,
                    'original_code': original_code
                })
        
        self.log(f"Generated {len(prompts)} error-fixing prompts")
        return prompts
    
    def _create_drc_fix_prompt(
        self,
        error_type: str,
        rule: str,
        details: str,
        component_name: str,
        original_code: str,
        parameters: Dict
    ) -> str:
        """Create DRC error fixing prompt"""
        
        severity_desc = {
            'critical': 'CRITICAL',
            'reviewable': 'REVIEWABLE',
            'passable': 'PASSABLE'
        }
        
        prompt = f"""Fix this {severity_desc.get(error_type, error_type)} DRC error in a VLSI circuit design.

Component: {component_name}
Error Rule: {rule}
Error Details: {details}

Original Python Code:
```python
{original_code}
```

Parameters that led to this error:
{json.dumps(parameters, indent=2)}

Task: Generate corrected Python code that fixes this DRC error while maintaining the circuit functionality.
Focus on adjusting the layout parameters to satisfy the design rule: {rule}

Fixed Python Code:
"""
        return prompt
    
    def _create_lvs_fix_prompt(
        self,
        lvs_errors: Dict,
        component_name: str,
        original_code: str,
        parameters: Dict
    ) -> str:
        """Create LVS error fixing prompt"""
        
        conclusion = lvs_errors.get('conclusion', 'LVS Failed')
        mismatch_details = lvs_errors.get('mismatch_details', {})
        
        prompt = f"""Fix this LVS (Layout vs Schematic) error in a VLSI circuit design.

Component: {component_name}
LVS Result: {conclusion}
Mismatch Details:
{json.dumps(mismatch_details, indent=2)}

Original Python Code:
```python
{original_code}
```

Parameters that led to this error:
{json.dumps(parameters, indent=2)}

Task: Generate corrected Python code that fixes this LVS error.
The layout and schematic must match. Check for missing connections, incorrect device counts, or netlist mismatches.

Fixed Python Code:
"""
        return prompt
    
    def run_grpo_training(self, samples: List[Dict]) -> str:
        """
        Run GRPO training using the existing grpo_trainer
        Returns: path to trained model
        """
        self.log("=== Starting GRPO Training ===")
        
        # Create output directory for this iteration
        model_output_dir = self.iteration_dir / f"iteration_{self.current_iteration}" / "trained_model"
        model_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Convert model path to absolute path if it's a local path
        model_path = self.args.base_model
        if not model_path.startswith(('/', 'http://', 'https://')) and '/' in model_path:
            # This looks like a relative local path, convert to absolute
            model_path = str(Path(model_path).resolve())
            self.log(f"Converted model path to absolute: {model_path}")
            
            # Validate that the model directory exists
            if not Path(model_path).exists():
                raise FileNotFoundError(
                    f"Model directory not found: {model_path}\n"
                    f"Original path: {self.args.base_model}\n"
                    f"Please ensure the model has been downloaded/saved to this location."
                )
        
        # Initialize GRPO trainer with LoRA
        trainer = grpo_trainer(
            model_name=model_path,
            learning_rate=self.args.learning_rate,
            group_size=self.args.batch_size,
            kl_coef=self.args.kl_coef,
            device=self.device,
            use_lora=self.args.use_lora,
            lora_r=self.args.lora_r,
            lora_alpha=self.args.lora_alpha,
            lora_dropout=self.args.lora_dropout,
        )
        
        # Prepare data - save as temporary JSON file
        temp_json = self.iteration_dir / f"temp_training_data_iter_{self.current_iteration}.json"
        with open(temp_json, 'w') as f:
            json.dump(samples, f, indent=2)
        
        self.log(f"Training on {len(samples)} samples")
        
        # Run training
        trainer.train(
            json_files=[str(temp_json)],
            num_epochs=self.args.num_epochs,
            batch_size=self.args.batch_size,
            save_path=str(model_output_dir),
            eval_every=self.args.eval_every
        )
        
        self.log("GRPO training completed")
        self.log(f"Model saved to: {model_output_dir}")
        
        # Clean up temp file
        temp_json.unlink()
        
        return str(model_output_dir)
    
    def generate_fixed_code(
        self,
        model_path: str,
        error_prompts: List[Dict]
    ) -> List[Dict]:
        """
        Generate fixed code using the GRPO-trained model
        """
        self.log("=== Generating Fixed Code ===")
        
        # Load the trained model
        self.log(f"Loading model from {model_path}")
        model = AutoModelForCausalLM.from_pretrained(model_path).to(self.device)
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model.eval()
        
        fixed_codes = []
        output_dir = self.iteration_dir / f"iteration_{self.current_iteration}" / "fixed_code"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for i, prompt_data in enumerate(error_prompts):
            self.log(f"Generating fix {i+1}/{len(error_prompts)}: {prompt_data['component_name']}")
            
            prompt = prompt_data['prompt']
            
            # Tokenize and generate
            inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048).to(self.device)
            
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=self.args.max_new_tokens,
                    temperature=self.args.temperature,
                    do_sample=self.args.temperature > 0,
                    top_k=50,
                    top_p=0.95,
                    repetition_penalty=1.1
                )
            
            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the new generated part (after the prompt)
            if generated_text.startswith(prompt):
                fixed_code = generated_text[len(prompt):].strip()
            else:
                fixed_code = generated_text.strip()
            
            # Save fixed code
            component_name = prompt_data['component_name']
            error_type = prompt_data['error_type']
            error_idx = prompt_data['error_index']
            
            output_file = output_dir / f"{component_name}_{error_type}_{error_idx}_fixed.py"
            with open(output_file, 'w') as f:
                f.write(fixed_code)
            
            fixed_codes.append({
                'sample_id': prompt_data['sample_id'],
                'component_name': component_name,
                'error_type': error_type,
                'error_index': error_idx,
                'original_code': prompt_data['original_code'],
                'fixed_code': fixed_code,
                'output_file': str(output_file)
            })
            
            self.log(f"  Saved to: {output_file.name}")
        
        self.log(f"Generated {len(fixed_codes)} fixed code samples")
        
        # Clean up model from memory
        del model
        torch.cuda.empty_cache()
        
        return fixed_codes
    
    def save_error_analysis(self, error_samples: List[ErrorSample]):
        """Save error analysis to JSON"""
        analysis_file = self.iteration_dir / f"iteration_{self.current_iteration}" / "error_analysis.json"
        analysis_file.parent.mkdir(parents=True, exist_ok=True)
        
        analysis = {
            'total_samples_with_errors': len(error_samples),
            'critical_errors': sum(1 for s in error_samples if s.has_critical_errors),
            'reviewable_errors': sum(1 for s in error_samples if s.has_reviewable_errors),
            'passable_errors': sum(1 for s in error_samples if s.has_passable_errors),
            'samples': [
                {
                    'sample_id': s.sample_id,
                    'component_name': s.component_name,
                    'drc_error_count': len(s.drc_errors),
                    'has_lvs_errors': bool(s.lvs_errors),
                    'drc_errors': s.drc_errors,
                    'lvs_errors': s.lvs_errors
                }
                for s in error_samples
            ]
        }
        
        with open(analysis_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        self.log(f"Error analysis saved to: {analysis_file}")
    
    def save_prompts(self, prompts: List[Dict]):
        """Save generated prompts to JSON"""
        prompts_file = self.iteration_dir / f"iteration_{self.current_iteration}" / "error_prompts.json"
        prompts_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(prompts_file, 'w') as f:
            json.dump(prompts, f, indent=2)
        
        self.log(f"Prompts saved to: {prompts_file}")
    
    def save_fixed_codes_summary(self, fixed_codes: List[Dict]):
        """Save fixed codes summary to JSON"""
        summary_file = self.iteration_dir / f"iteration_{self.current_iteration}" / "fixed_codes_summary.json"
        
        with open(summary_file, 'w') as f:
            json.dump(fixed_codes, f, indent=2)
        
        self.log(f"Fixed codes summary saved to: {summary_file}")
    
    def run_iteration(self, iteration: int) -> bool:
        """Run a single iteration of the pipeline"""
        self.current_iteration = iteration
        self.log(f"\n{'='*60}")
        self.log(f"Starting Iteration {iteration + 1}")
        self.log(f"{'='*60}\n")
        
        try:
            # Step 1: Load evaluation data
            samples = self.load_evaluation_data()
            
            # Step 2: Run GRPO training on all samples
            trained_model_path = self.run_grpo_training(samples)
            
            # Step 3: Extract errors
            all_samples, error_samples = self.extract_errors(samples)
            
            if not error_samples:
                self.log("No errors found in samples. Skipping error-fixing step.")
                return True
            
            # Step 4: Save error analysis
            self.save_error_analysis(error_samples)
            
            # Step 5: Generate error-specific prompts
            error_prompts = self.generate_error_prompts(error_samples)
            self.save_prompts(error_prompts)
            
            # Step 6: Generate fixed code
            fixed_codes = self.generate_fixed_code(trained_model_path, error_prompts)
            self.save_fixed_codes_summary(fixed_codes)
            
            self.log(f"\n{'='*60}")
            self.log(f"Iteration {iteration + 1} completed successfully")
            self.log(f"{'='*60}\n")
            
            return True
            
        except Exception as e:
            self.log(f"Iteration {iteration + 1} failed: {str(e)}", "ERROR")
            import traceback
            traceback.print_exc()
            return False
    
    def run_pipeline(self):
        """Run the complete pipeline"""
        self.log("🚀 Starting GRPO Error Fixing Pipeline")
        self.log(f"Configuration:")
        self.log(f"  Input JSON: {self.args.input_json}")
        self.log(f"  Base Model: {self.args.base_model}")
        self.log(f"  Output Directory: {self.iteration_dir}")
        self.log(f"  Iterations: {self.args.iterations}")
        self.log(f"  GRPO Epochs: {self.args.num_epochs}")
        self.log(f"  Batch Size: {self.args.batch_size}")
        
        try:
            for iteration in range(self.args.iterations):
                success = self.run_iteration(iteration)
                if not success:
                    self.log(f"Pipeline failed at iteration {iteration + 1}", "ERROR")
                    return False
            
            self.log("\n" + "="*60)
            self.log("✅ Pipeline completed successfully!")
            self.log(f"Results saved in: {self.iteration_dir}")
            self.log("="*60)
            return True
            
        except KeyboardInterrupt:
            self.log("Pipeline interrupted by user", "ERROR")
            return False
        except Exception as e:
            self.log(f"Pipeline failed: {str(e)}", "ERROR")
            import traceback
            traceback.print_exc()
            return False


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="GRPO Error Fixing Pipeline",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Input/Output
    parser.add_argument("--input_json", type=str, required=True,
                       help="Path to output.json with evaluation results")
    parser.add_argument("--output_dir", type=str, default="grpo_outputs",
                       help="Output directory for pipeline results")
    
    # Model configuration
    parser.add_argument("--base_model", type=str, required=True,
                       help="Path to base model or HuggingFace model ID")
    
    # GRPO training parameters
    parser.add_argument("--num_epochs", type=int, default=10,
                       help="Number of GRPO training epochs")
    parser.add_argument("--batch_size", type=int, default=12,
                       help="Batch size for GRPO training (increased from 4 for better reward diversity)")
    parser.add_argument("--learning_rate", type=float, default=1e-5,
                       help="Learning rate for GRPO training")
    parser.add_argument("--kl_coef", type=float, default=0.1,
                       help="KL divergence coefficient")
    parser.add_argument("--eval_every", type=int, default=100,
                       help="Evaluation frequency (steps)")
    
    # LoRA Configuration (for memory-efficient GRPO training)
    parser.add_argument("--use_lora", action="store_true", default=True,
                       help="Use LoRA for memory-efficient GRPO training (default: True)")
    parser.add_argument("--lora_r", type=int, default=16,
                       help="LoRA rank for GRPO training")
    parser.add_argument("--lora_alpha", type=int, default=32,
                       help="LoRA alpha scaling")
    parser.add_argument("--lora_dropout", type=float, default=0.05,
                       help="LoRA dropout rate")
    
    # Code generation parameters
    parser.add_argument("--max_new_tokens", type=int, default=2048,
                       help="Maximum new tokens for code generation")
    parser.add_argument("--temperature", type=float, default=0.1,
                       help="Temperature for code generation")
    
    # Pipeline configuration
    parser.add_argument("--iterations", type=int, default=1,
                       help="Number of pipeline iterations")
    
    args = parser.parse_args()
    
    # Validation
    if not Path(args.input_json).exists():
        parser.error(f"Input JSON not found: {args.input_json}")
    
    return args


def main():
    """Main entry point"""
    args = parse_args()
    
    pipeline = GRPOPipeline(args)
    success = pipeline.run_pipeline()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

