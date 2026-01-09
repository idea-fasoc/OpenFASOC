"""
GRPO Training with Unsloth + TRL
=================================

This module provides GRPO (Group Relative Policy Optimization) training using
Unsloth's FastLanguageModel for fast inference and TRL's GRPOTrainer.

Based on the Unsloth GRPO notebook approach, adapted for VLSI circuit design tasks.

This is Stage 3 of the pipeline as defined in PIPELINE_FLOW.md:
- Input: LoRA adapter from Stage 2 (self-improvement) OR base model
- Training: GRPO with DRC/LVS metrics as rewards
- Output: GRPO-optimized LoRA adapter

Usage (via grpo_pipeline.py):
-----------------------------
    python grpo_pipeline.py \
        --input_json output.json \
        --base_model "./pipeline_runs/<run_id>/models/iteration_2" \
        --output_dir grpo_outputs \
        --num_epochs 10 \
        --batch_size 12
"""

import os
import re
import json
import torch
import numpy as np
from typing import Dict, List, Optional, Callable, Tuple
from dataclasses import dataclass
from pathlib import Path
from torch.utils.data import Dataset, DataLoader
from datasets import Dataset as HFDataset

# Set up environment for Unsloth
os.environ.setdefault("UNSLOTH_VLLM_STANDBY", "1")


# ==============================================================================
# Format Configuration (from notebook)
# ==============================================================================

REASONING_START = "<start_working_out>"
REASONING_END = "<end_working_out>"
SOLUTION_START = "<SOLUTION>"
SOLUTION_END = "</SOLUTION>"

SYSTEM_PROMPT = f"""You are a VLSI circuit design expert.
Think about the problem and provide your working out.
Place it between {REASONING_START} and {REASONING_END}.
Then, provide your solution between {SOLUTION_START}{SOLUTION_END}"""

# Regex pattern for format matching
MATCH_FORMAT = re.compile(
    rf"^[\s]{{0,}}"
    rf"{REASONING_START}.+?{REASONING_END}.*?"
    rf"{SOLUTION_START}(.+?){SOLUTION_END}"
    rf"[\s]{{0,}}$",
    flags=re.MULTILINE | re.DOTALL
)

# Pattern to extract numbers from solution
MATCH_NUMBERS = re.compile(
    SOLUTION_START + r".*?([\d\.\,]{1,})",
    flags=re.MULTILINE | re.DOTALL
)


# ==============================================================================
# VLSI Metrics Configuration
# ==============================================================================

@dataclass
class VLSIMetrics:
    """Metrics from VLSI evaluation (output.json format)"""
    symmetry_horizontal: float = 0.0
    symmetry_vertical: float = 0.0
    area_um2: float = 0.0
    drc_pass: bool = False
    lvs_pass: bool = False
    passable_errors_count: int = 0
    reviewable_errors_count: int = 0
    critical_errors_count: int = 0
    total_resistance_ohms: float = 0.0
    total_capacitance_farads: float = 0.0


# ==============================================================================
# Reward Functions (TRL GRPOTrainer Format)
# ==============================================================================

def match_format_exactly(completions: List, **kwargs) -> List[float]:
    """
    Reward function that checks if the response matches the expected format exactly.
    Returns 3.0 points if format matches exactly.
    """
    scores = []
    for completion in completions:
        score = 0.0
        response = completion[0]["content"] if isinstance(completion, list) else str(completion)
        if MATCH_FORMAT.search(response) is not None:
            score += 3.0
        scores.append(score)
    return scores


def match_format_approximately(completions: List, **kwargs) -> List[float]:
    """
    Reward function that gives partial credit for format elements.
    +0.5 for each correct marker, -1.0 if marker appears more than once.
    """
    scores = []
    for completion in completions:
        score = 0.0
        response = completion[0]["content"] if isinstance(completion, list) else str(completion)
        score += 0.5 if response.count(REASONING_START) == 1 else -1.0
        score += 0.5 if response.count(REASONING_END) == 1 else -1.0
        score += 0.5 if response.count(SOLUTION_START) == 1 else -1.0
        score += 0.5 if response.count(SOLUTION_END) == 1 else -1.0
        scores.append(score)
    return scores


def check_code_syntax(completions: List, **kwargs) -> List[float]:
    """
    Reward function that checks if generated code has valid Python syntax.
    """
    scores = []
    for completion in completions:
        score = 0.0
        response = completion[0]["content"] if isinstance(completion, list) else str(completion)
        
        # Try to extract code block
        code_match = re.search(r"```python\s*(.+?)```", response, re.DOTALL)
        if code_match:
            code = code_match.group(1).strip()
            try:
                compile(code, '<string>', 'exec')
                score += 2.0  # Valid Python syntax
            except SyntaxError:
                score -= 0.5
        else:
            # Try to extract JSON
            json_match = re.search(r"\{[^{}]+\}", response, re.DOTALL)
            if json_match:
                try:
                    json.loads(json_match.group(0))
                    score += 1.5  # Valid JSON
                except json.JSONDecodeError:
                    score -= 0.5
        
        scores.append(score)
    return scores


# Global counter for logging
_PRINT_COUNTER = 0
_PRINT_EVERY = 5


def check_with_logging(prompts: List, completions: List, **kwargs) -> List[float]:
    """
    Reward function with logging for debugging.
    """
    global _PRINT_COUNTER, _PRINT_EVERY
    
    scores = []
    
    if _PRINT_COUNTER % _PRINT_EVERY == 0:
        if prompts and len(prompts) > 0:
            question = prompts[0][-1]["content"] if isinstance(prompts[0], list) else str(prompts[0])
            response = completions[0][0]["content"] if isinstance(completions[0], list) else str(completions[0])
            print('*' * 20)
            print(f"Question:\n{question[:300]}...")
            print(f"\nResponse:\n{response[:500]}...")
    
    _PRINT_COUNTER += 1
    
    for completion in completions:
        response = completion[0]["content"] if isinstance(completion, list) else str(completion)
        length_score = min(len(response) / 1000, 0.5)
        scores.append(length_score)
    
    return scores


# ==============================================================================
# VLSI-Aware Reward Functions
# ==============================================================================

def extract_json_params(response: str) -> Optional[Dict]:
    """Extract JSON parameters from model response."""
    # Try to find JSON in SOLUTION tags first
    solution_match = re.search(
        rf"{SOLUTION_START}(.*?){SOLUTION_END}",
        response, re.DOTALL
    )
    if solution_match:
        text = solution_match.group(1)
    else:
        text = response
    
    # Find JSON object with nested structures
    json_patterns = [
        r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',  # Nested JSON
        r'\{[^{}]+\}',  # Simple JSON
    ]
    
    for pattern in json_patterns:
        matches = re.findall(pattern, text, re.DOTALL)
        for match in matches:
            try:
                parsed = json.loads(match)
                # Check if it looks like VLSI parameters
                if any(k in parsed for k in ['width', 'length', 'fingers', 'multipliers', 'Width', 'Length']):
                    return parsed
            except json.JSONDecodeError:
                continue
    
    return None


def vlsi_parameter_validity(completions: List, **kwargs) -> List[float]:
    """
    Reward function that checks if generated parameters are valid VLSI parameters.
    
    Rewards:
    - +2.0 for valid JSON with VLSI parameters
    - +1.0 for each valid parameter type (width, length, fingers, multipliers)
    - +0.5 for reasonable parameter values
    - -1.0 for invalid JSON or missing required parameters
    """
    scores = []
    for completion in completions:
        score = 0.0
        response = completion[0]["content"] if isinstance(completion, list) else str(completion)
        
        params = extract_json_params(response)
        if params is None:
            scores.append(-1.0)
            continue
        
        # Base reward for valid JSON with parameters
        score += 2.0
        
        # Check for required VLSI parameters (case-insensitive)
        param_keys = {k.lower(): k for k in params.keys()}
        
        required_params = ['width', 'length', 'fingers', 'multipliers']
        for req_param in required_params:
            if req_param in param_keys:
                score += 1.0
                
                # Check if values are reasonable
                val = params[param_keys[req_param]]
                if isinstance(val, list) and len(val) > 0:
                    if req_param in ['width', 'length']:
                        # Width/length should be positive floats
                        if all(isinstance(v, (int, float)) and v > 0 for v in val):
                            score += 0.5
                    elif req_param in ['fingers', 'multipliers']:
                        # Fingers/multipliers should be positive integers
                        if all(isinstance(v, (int, float)) and v >= 1 for v in val):
                            score += 0.5
        
        scores.append(score)
    return scores


def vlsi_optimization_understanding(prompts: List, completions: List, **kwargs) -> List[float]:
    """
    Reward function that checks if the model understands VLSI optimization goals.
    
    Rewards for mentioning key optimization concepts:
    - DRC/LVS compliance understanding
    - Symmetry optimization
    - Area minimization
    - Trade-off awareness
    """
    scores = []
    
    # Keywords that indicate understanding of VLSI optimization
    optimization_keywords = {
        'drc': 1.0,
        'lvs': 1.0,
        'symmetry': 1.5,
        'symmetric': 1.0,
        'area': 0.5,
        'minimize': 0.5,
        'maximize': 0.5,
        'optimize': 0.5,
        'trade-off': 1.0,
        'tradeoff': 1.0,
        'balance': 0.5,
        'compliance': 0.5,
        'layout': 0.5,
        'design rule': 1.0,
        'parasitic': 1.0,
        'resistance': 0.5,
        'capacitance': 0.5,
    }
    
    for completion in completions:
        score = 0.0
        response = completion[0]["content"] if isinstance(completion, list) else str(completion)
        response_lower = response.lower()
        
        found_keywords = set()
        for keyword, reward in optimization_keywords.items():
            if keyword in response_lower and keyword not in found_keywords:
                score += reward
                found_keywords.add(keyword)
        
        # Cap the keyword reward
        score = min(score, 5.0)
        
        # Bonus for mentioning optimization as a SET (holistic approach)
        holistic_phrases = [
            'together', 'combined', 'holistic', 'overall', 
            'all parameters', 'set of', 'parameter set',
            'jointly', 'simultaneously', 'as a whole'
        ]
        if any(phrase in response_lower for phrase in holistic_phrases):
            score += 2.0
        
        scores.append(score)
    return scores


def vlsi_parameter_reasoning(completions: List, **kwargs) -> List[float]:
    """
    Reward function that checks if the model shows proper reasoning about 
    how parameters affect VLSI metrics.
    
    Key understanding the model should demonstrate:
    - Width/Length affect transistor characteristics and area
    - Fingers affect current handling and layout
    - Multipliers affect matching and symmetry
    - These parameters interact and should be optimized together
    """
    scores = []
    
    # Reasoning patterns that show understanding
    reasoning_patterns = [
        (r'width.*(?:area|current|resistance)', 1.0),
        (r'length.*(?:area|current|channel)', 1.0),
        (r'finger.*(?:current|parallel|layout)', 1.0),
        (r'multiplier.*(?:match|symmetr|balance)', 1.0),
        (r'increas.*width.*(?:current|resistance)', 1.5),
        (r'decreas.*length.*(?:speed|area)', 1.5),
        (r'(?:trade-?off|balance).*(?:area|performance)', 2.0),
        (r'parameter.*(?:together|combined|set)', 2.0),
    ]
    
    for completion in completions:
        score = 0.0
        response = completion[0]["content"] if isinstance(completion, list) else str(completion)
        response_lower = response.lower()
        
        for pattern, reward in reasoning_patterns:
            if re.search(pattern, response_lower):
                score += reward
        
        # Cap the score
        score = min(score, 8.0)
        scores.append(score)
    
    return scores


def vlsi_metrics_reward(prompts: List, completions: List, **kwargs) -> List[float]:
    """
    Main VLSI reward that combines parameter validity with optimization understanding.
    Provides a comprehensive score for VLSI-aware responses.
    """
    global _PRINT_COUNTER, _PRINT_EVERY
    
    scores = []
    should_log = _PRINT_COUNTER % _PRINT_EVERY == 0
    _PRINT_COUNTER += 1
    
    for i, completion in enumerate(completions):
        score = 0.0
        response = completion[0]["content"] if isinstance(completion, list) else str(completion)
        response_lower = response.lower()
        
        # 1. Check for valid parameter output
        params = extract_json_params(response)
        if params:
            score += 3.0  # Valid parameter JSON
            
            # Check all 4 required parameters present
            param_keys = {k.lower() for k in params.keys()}
            required = {'width', 'length', 'fingers', 'multipliers'}
            found = required.intersection(param_keys)
            score += len(found) * 0.5
        
        # 2. Reward holistic optimization understanding
        holistic_terms = ['together', 'combined', 'set', 'overall', 'balance', 'jointly']
        if any(term in response_lower for term in holistic_terms):
            score += 2.0
        
        # 3. Reward mentioning key VLSI concepts
        vlsi_concepts = ['drc', 'lvs', 'symmetry', 'area', 'parasitic']
        concepts_mentioned = sum(1 for c in vlsi_concepts if c in response_lower)
        score += concepts_mentioned * 0.5
        
        # 4. Penalty for not providing any parameters
        if params is None and '<solution>' not in response_lower:
            score -= 2.0
        
        # Log sample
        if should_log and i == 0 and prompts:
            prompt = prompts[0][-1]["content"] if isinstance(prompts[0], list) else str(prompts[0])
            print('*' * 20)
            print(f"Question:\n{prompt[:300]}...")
            print(f"\nResponse:\n{response[:500]}...")
            print(f"\nVLSI Score: {score:.2f}")
        
        scores.append(score)
    
    return scores


# ==============================================================================
# VLSI Dataset for Legacy Interface
# ==============================================================================

class VLSIDataset(Dataset):
    """Dataset for VLSI samples with metrics (legacy PyTorch format)"""
    
    def __init__(self, json_data: List[Dict], tokenizer):
        self.data = json_data
        self.tokenizer = tokenizer
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        sample = self.data[idx]
        
        # Create prompt
        prompt = self._create_prompt(sample)
        target = self._create_target(sample)
        
        # Extract metrics
        metrics = self._extract_metrics(sample)
        
        return {
            'prompt': prompt,
            'target': target,
            'parameters': sample.get('parameters', {}),
            'metrics': metrics,
            'sample_id': sample.get('sample_id', idx),
            'component_name': sample.get('component_name', 'unknown')
        }
    
    def _create_prompt(self, sample: Dict) -> str:
        component_name = sample.get('component_name', 'unknown')
        return f"""Design VLSI circuit: {component_name}

Task: Generate optimal parameters for the circuit design.

Provide parameters in JSON format:
"""
    
    def _create_target(self, sample: Dict) -> str:
        params = sample.get('parameters', {})
        return json.dumps(params, indent=2)
    
    def _extract_metrics(self, sample: Dict) -> VLSIMetrics:
        # Extract error counts from DRC structure
        passable = reviewable = critical = 0
        if 'drc' in sample and 'summary' in sample['drc']:
            drc_summary = sample['drc']['summary']
            passable = drc_summary.get('passable_errors_count', 0)
            reviewable = drc_summary.get('reviewable_errors_count', 0)
            critical = drc_summary.get('critical_errors_count', 0)
        
        return VLSIMetrics(
            symmetry_horizontal=sample.get('symmetry_horizontal', 0.0),
            symmetry_vertical=sample.get('symmetry_vertical', 0.0),
            area_um2=sample.get('area_um2', 0.0),
            drc_pass=sample.get('drc_pass', False),
            lvs_pass=sample.get('lvs_pass', False),
            passable_errors_count=passable,
            reviewable_errors_count=reviewable,
            critical_errors_count=critical,
            total_resistance_ohms=sample.get('total_resistance_ohms', 0.0),
            total_capacitance_farads=sample.get('total_capacitance_farads', 0.0)
        )


# ==============================================================================
# GRPO Trainer Class (Interface for grpo_pipeline.py)
# ==============================================================================

class grpo_trainer:
    """
    GRPO Trainer using Unsloth + TRL.
    
    This class provides the interface expected by grpo_pipeline.py while using
    Unsloth's FastLanguageModel and TRL's GRPOTrainer internally.
    
    Pipeline Stage 3: GRPO Optimization on DRC/LVS metrics.
    """
    
    def __init__(
        self,
        model_name: str = "codellama/CodeLlama-7b-Instruct-hf",
        learning_rate: float = 5e-6,
        gamma: float = 0.99,
        group_size: int = 4,
        kl_coef: float = 0.1,
        device: str = "cuda" if torch.cuda.is_available() else "cpu",
        use_lora: bool = True,
        lora_r: int = 64,
        lora_alpha: int = 64,
        lora_dropout: float = 0.05,
        lora_target_modules: List[str] = None,
        max_seq_length: int = 2048,
        gpu_memory_utilization: float = 0.9,
    ):
        """
        Initialize GRPO trainer.
        
        Args:
            model_name: Model path or HuggingFace model ID (can be LoRA adapter path)
            learning_rate: Learning rate for training
            gamma: Discount factor (unused in TRL GRPO, kept for compatibility)
            group_size: Number of generations per prompt for GRPO
            kl_coef: KL divergence coefficient
            device: Device to use
            use_lora: Whether to use LoRA (always True with Unsloth)
            lora_r: LoRA rank
            lora_alpha: LoRA alpha
            lora_dropout: LoRA dropout
            lora_target_modules: Target modules for LoRA
            max_seq_length: Maximum sequence length
            gpu_memory_utilization: GPU memory utilization for vLLM
        """
        self.device = device
        self.learning_rate = learning_rate
        self.group_size = group_size
        self.kl_coef = kl_coef
        self.use_lora = use_lora
        self.lora_r = lora_r
        self.lora_alpha = lora_alpha
        self.lora_dropout = lora_dropout
        self.max_seq_length = max_seq_length
        self.gpu_memory_utilization = gpu_memory_utilization
        
        if lora_target_modules is None:
            self.lora_target_modules = [
                "q_proj", "k_proj", "v_proj", "o_proj",
                "gate_proj", "up_proj", "down_proj",
            ]
        else:
            self.lora_target_modules = lora_target_modules
        
        # VLSI metric weights for reward calculation
        self.metric_weights = {
            'symmetry_horizontal': 2.0,
            'symmetry_vertical': 2.0,
            'resistance_weight': 3.0,
            'capacitance_weight': 3.0,
            'area_penalty': 0.5,
            'drc_pass_bonus': 10.0,
            'lvs_pass_bonus': 8.0,
            'passable_error_penalty': 0.2,
            'reviewable_error_penalty': 1.5,
            'critical_error_penalty': 8.0
        }
        
        # Target values
        self.target_resistance_ohms = 100.0
        self.target_capacitance_farads = 1e-12
        self.target_area_um2 = 5000.0
        
        # Load model
        self._load_model(model_name)
    
    def _load_model(self, model_name: str):
        """Load model with Unsloth, handling LoRA adapters from previous stages."""
        from unsloth import FastLanguageModel
        
        model_path = Path(model_name)
        is_lora_adapter = model_path.is_dir() and (model_path / "adapter_config.json").exists()
        
        if is_lora_adapter:
            print(f"🔧 Loading existing LoRA adapter from: {model_name}")
            
            # Read base model from adapter config
            with open(model_path / "adapter_config.json", 'r') as f:
                adapter_config = json.load(f)
                base_model_name = adapter_config.get(
                    "base_model_name_or_path",
                    "codellama/CodeLlama-7b-Instruct-hf"
                )
            
            self.base_model_name = base_model_name
            print(f"  Base model: {base_model_name}")
            
            # Load base model with Unsloth
            self.model, self.tokenizer = FastLanguageModel.from_pretrained(
                model_name=base_model_name,
                max_seq_length=self.max_seq_length,
                load_in_4bit=True,
                fast_inference=False,
                max_lora_rank=self.lora_r,
            )
            
            # Apply LoRA (this will create new LoRA layers)
            self.model = FastLanguageModel.get_peft_model(
                self.model,
                r=self.lora_r,
                target_modules=self.lora_target_modules,
                lora_alpha=self.lora_alpha,
                lora_dropout=self.lora_dropout,
                use_gradient_checkpointing="unsloth",
                random_state=3407,
            )
            
            # Load the weights from the existing adapter
            print(f"  Loading adapter weights...")
            from peft import PeftModel
            # We need to load the adapter weights into the model
            # First, get the state dict from the adapter
            from safetensors.torch import load_file
            adapter_file = model_path / "adapter_model.safetensors"
            if adapter_file.exists():
                adapter_weights = load_file(str(adapter_file))
                # Load weights into model
                model_state = self.model.state_dict()
                for key, value in adapter_weights.items():
                    if key in model_state:
                        model_state[key].copy_(value)
                print(f"  ✅ Loaded adapter weights from {adapter_file}")
            else:
                print(f"  ⚠️ No safetensors found, using fresh LoRA weights")
        else:
            print(f"🔧 Loading base model: {model_name}")
            self.base_model_name = model_name
            
            # Load with Unsloth
            self.model, self.tokenizer = FastLanguageModel.from_pretrained(
                model_name=model_name,
                max_seq_length=self.max_seq_length,
                load_in_4bit=True,
                fast_inference=False,
                max_lora_rank=self.lora_r,
            )
            
            # Apply LoRA
            self.model = FastLanguageModel.get_peft_model(
                self.model,
                r=self.lora_r,
                target_modules=self.lora_target_modules,
                lora_alpha=self.lora_alpha,
                lora_dropout=self.lora_dropout,
                use_gradient_checkpointing="unsloth",
                random_state=3407,
            )
        
        # Ensure pad token
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Print trainable parameters
        trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        total_params = sum(p.numel() for p in self.model.parameters())
        print(f"✅ Model loaded: {trainable_params:,} / {total_params:,} trainable params "
              f"({100 * trainable_params / total_params:.2f}%)")
    
    def compute_reward(self, metrics: VLSIMetrics) -> float:
        """
        Compute VLSI-specific reward from metrics.
        Higher is better.
        """
        w = self.metric_weights
        reward = 0.0
        
        # Symmetry (0-1 normalized)
        reward += w['symmetry_horizontal'] * metrics.symmetry_horizontal
        reward += w['symmetry_vertical'] * metrics.symmetry_vertical
        
        # Resistance score
        if metrics.total_resistance_ohms > 0:
            error = abs(metrics.total_resistance_ohms - self.target_resistance_ohms)
            normalized_error = error / self.target_resistance_ohms
            score = np.exp(-2.0 * normalized_error)
            reward += w['resistance_weight'] * score
        
        # Capacitance score
        if metrics.total_capacitance_farads > 0:
            error = abs(metrics.total_capacitance_farads - self.target_capacitance_farads)
            normalized_error = error / self.target_capacitance_farads
            score = np.exp(-2.0 * normalized_error)
            reward += w['capacitance_weight'] * score
        
        # DRC/LVS bonuses
        if metrics.drc_pass:
            reward += w['drc_pass_bonus']
        if metrics.lvs_pass:
            reward += w['lvs_pass_bonus']
        
        # Error penalties (quadratic for discrimination)
        if metrics.passable_errors_count > 0:
            reward -= w['passable_error_penalty'] * (metrics.passable_errors_count ** 1.5)
        if metrics.reviewable_errors_count > 0:
            reward -= w['reviewable_error_penalty'] * (metrics.reviewable_errors_count ** 1.8)
        if metrics.critical_errors_count > 0:
            reward -= w['critical_error_penalty'] * (metrics.critical_errors_count ** 2.0)
        
        # Area penalty
        if metrics.area_um2 > 0:
            normalized_area = metrics.area_um2 / self.target_area_um2
            if normalized_area > 1.0:
                excess = normalized_area - 1.0
                reward -= w['area_penalty'] * (excess ** 1.5)
        
        return reward
    
    def _prepare_dataset(self, json_data: List[Dict]) -> HFDataset:
        """Convert JSON data to HuggingFace Dataset for GRPOTrainer."""
        processed = []
        
        for sample in json_data:
            component_name = sample.get('component_name', 'unknown')
            parameters = sample.get('parameters', {})
            
            # Create prompt in chat format
            user_content = f"""Design VLSI circuit: {component_name}

Task: Generate optimal parameters for the circuit design.
Current parameters:
{json.dumps(parameters, indent=2)}

Analyze the design and suggest improvements to optimize for:
- DRC compliance (Design Rule Check)
- LVS compliance (Layout vs Schematic)
- Symmetry (horizontal and vertical)
- Minimal area

Provide your analysis and optimized parameters."""

            prompt = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ]
            
            # Extract answer (for reference during training)
            answer = "DRC: " + ("Pass" if sample.get('drc_pass') else "Fail")
            answer += ", LVS: " + ("Pass" if sample.get('lvs_pass') else "Fail")
            
            processed.append({
                "prompt": prompt,
                "answer": answer,
                "vlsi_sample": sample,  # Keep full sample for metrics
            })
        
        return HFDataset.from_list(processed)
    
    def _get_reward_functions(self) -> List[Callable]:
        """Get reward functions for GRPOTrainer.
        
        Now includes VLSI-aware reward functions that teach the model to:
        1. Output valid VLSI parameters in JSON format
        2. Understand VLSI optimization concepts (DRC, LVS, symmetry, area)
        3. Reason about parameter trade-offs holistically
        """
        return [
            # Format rewards (keep for structure)
            match_format_exactly,
            match_format_approximately,
            # VLSI-specific rewards (main learning signal)
            vlsi_parameter_validity,         # +8 max for valid params
            vlsi_optimization_understanding,  # +7 max for VLSI concepts
            vlsi_parameter_reasoning,         # +8 max for reasoning
            vlsi_metrics_reward,              # +8 max comprehensive VLSI score
        ]
    
    def train(
        self,
        json_files: List[str],
        num_epochs: int = 10,
        batch_size: int = 4,
        save_path: str = "grpo_vlsi_model",
        eval_every: int = 100
    ):
        """
        Run GRPO training.
        
        Args:
            json_files: List of JSON files with VLSI evaluation data
            num_epochs: Number of training epochs (converted to max_steps)
            batch_size: Batch size (used as gradient accumulation steps)
            save_path: Path to save the trained model
            eval_every: Evaluation frequency (unused with TRL, kept for compatibility)
        """
        from trl import GRPOConfig, GRPOTrainer
        
        print("=" * 60)
        print("Starting GRPO Training with Unsloth + TRL")
        print("=" * 60)
        
        # Load all data
        all_data = []
        for json_file in json_files:
            print(f"Loading data from {json_file}")
            with open(json_file, 'r') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    all_data.append(data)
                elif isinstance(data, list):
                    all_data.extend(data)
        
        print(f"Loaded {len(all_data)} samples from {len(json_files)} file(s)")
        
        # Prepare dataset
        dataset = self._prepare_dataset(all_data)
        
        # Calculate max prompt length
        max_prompt_length = 0
        for sample in dataset:
            tokens = self.tokenizer.apply_chat_template(
                sample["prompt"],
                add_generation_prompt=True,
                tokenize=True
            )
            max_prompt_length = max(max_prompt_length, len(tokens))
        
        max_prompt_length = min(max_prompt_length + 10, self.max_seq_length // 2)
        max_completion_length = self.max_seq_length - max_prompt_length
        
        print(f"Max prompt length: {max_prompt_length}")
        print(f"Max completion length: {max_completion_length}")
        
        # Calculate max_steps from epochs
        samples_per_step = batch_size * self.group_size
        steps_per_epoch = max(1, len(dataset) // samples_per_step)
        max_steps = num_epochs * steps_per_epoch
        
        print(f"Training for {max_steps} steps ({num_epochs} epochs)")
        
        # Create training config
        training_args = GRPOConfig(
            learning_rate=self.learning_rate,
            weight_decay=0.1,
            warmup_ratio=0.1,
            lr_scheduler_type="cosine",
            optim="adamw_8bit",
            logging_steps=1,
            per_device_train_batch_size=1,
            gradient_accumulation_steps=batch_size,
            num_generations=self.group_size,
            max_prompt_length=max_prompt_length,
            max_completion_length=max_completion_length,
            max_steps=max_steps,
            save_steps=max(1, max_steps // 4),
            max_grad_norm=1.0,
            report_to="none",
            output_dir=save_path,
        )
        
        # Get reward functions
        reward_funcs = self._get_reward_functions()
        print(f"\nUsing {len(reward_funcs)} reward functions:")
        for func in reward_funcs:
            print(f"  - {func.__name__}")
        
        # Create trainer
        print("\nInitializing GRPOTrainer...")
        trainer = GRPOTrainer(
            model=self.model,
            processing_class=self.tokenizer,
            reward_funcs=reward_funcs,
            args=training_args,
            train_dataset=dataset,
        )
        
        # Train
        print("\n" + "=" * 60)
        print("Starting training...")
        print("Note: Rewards may start at 0 for first ~100 steps. Be patient!")
        print("=" * 60 + "\n")
        
        trainer.train()
        
        print("\n✅ GRPO Training completed!")
        
        # Save the model
        self.save_model(save_path)
    
    def save_model(self, path: str, merge_weights: bool = True):
        """
        Save the trained LoRA adapter.
        
        Args:
            path: Output path
            merge_weights: Whether to also save merged model (16-bit)
        """
        os.makedirs(path, exist_ok=True)
        
        print(f"💾 Saving GRPO-trained model to {path}")
        
        # Save LoRA adapter
        lora_path = os.path.join(path, "lora_adapter")
        # Try Unsloth's save_lora first, fall back to PEFT's save_pretrained
        if hasattr(self.model, 'save_lora'):
            self.model.save_lora(lora_path)
        else:
            # Standard PEFT model
            self.model.save_pretrained(lora_path)
        self.tokenizer.save_pretrained(lora_path)
        print(f"✅ LoRA adapter saved to {lora_path}")
        
        if merge_weights:
            merged_path = os.path.join(path, "merged")
            try:
                print(f"🔄 Saving merged model to {merged_path}")
                self.model.save_pretrained_merged(
                    merged_path,
                    self.tokenizer,
                    save_method="merged_16bit"
                )
                print(f"✅ Merged model saved to {merged_path}")
            except Exception as e:
                print(f"⚠️ Could not save merged model: {e}")
        
        # Save training config
        config = {
            'base_model_name': self.base_model_name,
            'learning_rate': self.learning_rate,
            'group_size': self.group_size,
            'kl_coef': self.kl_coef,
            'lora_r': self.lora_r,
            'lora_alpha': self.lora_alpha,
            'metric_weights': self.metric_weights,
        }
        with open(os.path.join(path, "training_config.json"), "w") as f:
            json.dump(config, f, indent=2)
        
        print("✅ Training config saved")
    
    def validate(self, val_loader: DataLoader) -> Dict[str, float]:
        """Validate on held-out data (legacy interface)."""
        val_rewards = []
        
        for batch in val_loader:
            metrics_list = batch.get('metrics', [])
            for m in metrics_list:
                if isinstance(m, VLSIMetrics):
                    val_rewards.append(self.compute_reward(m))
        
        return {
            'mean_reward': np.mean(val_rewards) if val_rewards else 0.0,
            'mean_loss': 0.0  # Not computed in this mode
        }
    
    def collate_fn(self, batch_list):
        """Collate function for DataLoader (legacy interface)."""
        return {
            'prompt': [b['prompt'] for b in batch_list],
            'target': [b['target'] for b in batch_list],
            'parameters': [b['parameters'] for b in batch_list],
            'metrics': [b['metrics'] for b in batch_list],
            'sample_id': [b['sample_id'] for b in batch_list],
            'component_name': [b['component_name'] for b in batch_list]
        }


# ==============================================================================
# Convenience Functions
# ==============================================================================

def run_inference(
    model,
    tokenizer,
    prompt: str,
    lora_path: Optional[str] = None,
    temperature: float = 0.8,
    top_p: float = 0.95,
    max_tokens: int = 1024,
) -> str:
    """
    Run inference with the trained model using vLLM.
    
    Args:
        model: Unsloth model
        tokenizer: Tokenizer
        prompt: User prompt
        lora_path: Path to LoRA adapter (optional)
        temperature: Sampling temperature
        top_p: Top-p sampling
        max_tokens: Maximum tokens to generate
    
    Returns:
        Generated text
    """
    from vllm import SamplingParams
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
    
    text = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=False,
    )
    
    sampling_params = SamplingParams(
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )
    
    lora_request = None
    if lora_path:
        lora_request = model.load_lora(lora_path)
    
    output = model.fast_generate(
        [text],
        sampling_params=sampling_params,
        lora_request=lora_request,
    )[0].outputs[0].text
    
    return output


# ==============================================================================
# Main Entry Point
# ==============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="GRPO Training with Unsloth + TRL")
    parser.add_argument("--model_name", type=str, 
                       default="codellama/CodeLlama-7b-Instruct-hf",
                       help="Model name or path (can be LoRA adapter)")
    parser.add_argument("--dataset_path", type=str, default="output.json",
                       help="Path to VLSI evaluation JSON")
    parser.add_argument("--output_dir", type=str, default="grpo_outputs",
                       help="Output directory")
    parser.add_argument("--num_epochs", type=int, default=10,
                       help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=4,
                       help="Batch size (gradient accumulation)")
    parser.add_argument("--learning_rate", type=float, default=5e-6,
                       help="Learning rate")
    parser.add_argument("--lora_r", type=int, default=64,
                       help="LoRA rank")
    parser.add_argument("--lora_alpha", type=int, default=64,
                       help="LoRA alpha")
    parser.add_argument("--group_size", type=int, default=4,
                       help="Number of generations for GRPO")
    parser.add_argument("--kl_coef", type=float, default=0.1,
                       help="KL divergence coefficient")
    
    args = parser.parse_args()
    
    # Initialize trainer
    trainer = grpo_trainer(
        model_name=args.model_name,
        learning_rate=args.learning_rate,
        group_size=args.group_size,
        kl_coef=args.kl_coef,
        lora_r=args.lora_r,
        lora_alpha=args.lora_alpha,
    )
    
    # Train
    trainer.train(
        json_files=[args.dataset_path],
        num_epochs=args.num_epochs,
        batch_size=args.batch_size,
        save_path=args.output_dir,
    )
