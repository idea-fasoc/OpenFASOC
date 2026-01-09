#!/bin/bash

# Complete GRPO Training Pipeline
# ================================
# This script runs the complete training pipeline from base models:
# 1. Initial finetuning on OpenFASOC data
# 2. Self-improvement with master model evaluation
# 3. GRPO optimization on DRC/LVS metrics
#
# Usage:
#   ./run_pipeline.sh <model_size> [options]

# Setup CUDA environment for flashinfer JIT compilation
if [ -n "$CONDA_PREFIX" ]; then
    export CUDA_HOME=$CONDA_PREFIX
    export CUDA_PATH=$CONDA_PREFIX
    # CUDA headers
    export CPATH=$CONDA_PREFIX/targets/x86_64-linux/include:$CPATH
    # CCCL (CUB, Thrust, etc.) headers for flashinfer
    export CPATH=$CONDA_PREFIX/targets/x86_64-linux/include/cccl:$CPATH
    # CUDA libraries
    export LIBRARY_PATH=$CONDA_PREFIX/targets/x86_64-linux/lib:$LIBRARY_PATH
    export LD_LIBRARY_PATH=$CONDA_PREFIX/targets/x86_64-linux/lib:$LD_LIBRARY_PATH
fi
#
# Model sizes: 7b | 13b | both

set -e  # Exit on error

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Default configuration
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GOOGLE_API_KEY="${GOOGLE_API_KEY:-}"
MASTER_MODEL=""
SELF_IMPROVEMENT_ITERS=3
GRPO_ITERS=3

# Available Master Models (updated model names without -latest suffix)
declare -A MASTER_MODELS
MASTER_MODELS=(
    ["1"]="gemini-2.0-flash"
    ["2"]="gemini-1.5-pro"
    ["3"]="gemini-1.5-flash"
    ["4"]="gemini-1.5-flash-8b"
    ["5"]="gemini-1.0-pro"
)

declare -A MASTER_MODEL_DESCRIPTIONS
MASTER_MODEL_DESCRIPTIONS=(
    ["1"]="Fast 2.0 model, good balance (recommended)"
    ["2"]="Best quality 1.5 Pro, slower"
    ["3"]="Fast 1.5 Flash production model"
    ["4"]="Lightweight 1.5 Flash 8B, fastest"
    ["5"]="Legacy 1.0 Pro stable model"
)

# Model paths (always start from base)
BASE_7B="codellama/CodeLlama-7b-Instruct-hf"
BASE_13B="codellama/CodeLlama-13b-Instruct-hf"

# Files
PROMPT_FILE="scripts/utils/prompt.txt"
INSTRUCTION_FILE="scripts/utils/instruction.txt"
DRC_LVS_DATA="output.json"

# Print functions
print_header() {
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}" >&2
    echo -e "${BLUE}║${NC}  $1" >&2
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}" >&2
}

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1" >&2
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" >&2
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

# Validation
validate_environment() {
    print_info "Validating environment..."
    
    if [ ! -f "end_to_end.py" ] || [ ! -f "grpo_pipeline.py" ]; then
        print_error "Must be run from llm-finetuning-folder directory"
        exit 1
    fi
    
    if [ ! -f "$PROMPT_FILE" ]; then
        print_error "Prompt file not found: $PROMPT_FILE"
        exit 1
    fi
    
    if [ ! -f "$DRC_LVS_DATA" ]; then
        print_error "DRC/LVS data not found: $DRC_LVS_DATA"
        exit 1
    fi
    
    if ! command -v python &> /dev/null; then
        print_error "Python not found"
        exit 1
    fi
    
    # Check for training scripts
    if [ ! -f "scripts/training/train.py" ]; then
        print_error "Training script not found: scripts/training/train.py"
        exit 1
    fi
    
    if [ ! -f "scripts/others/process_data.py" ]; then
        print_error "Data processing script not found: scripts/others/process_data.py"
        exit 1
    fi
    
    print_info "Environment validation passed ✓"
}

# Prompt for master model selection
prompt_master_model() {
    print_header "Select Master Model for Code Evaluation"
    
    echo ""
    echo "Available Gemini Models:"
    echo ""
    for key in $(echo "${!MASTER_MODELS[@]}" | tr ' ' '\n' | sort -n); do
        echo "  [$key] ${MASTER_MODELS[$key]}"
        echo "      ${MASTER_MODEL_DESCRIPTIONS[$key]}"
        echo ""
    done
    
    while true; do
        read -p "Enter your choice [1-5] (default: 1): " choice
        choice=${choice:-1}
        
        if [[ -n "${MASTER_MODELS[$choice]}" ]]; then
            MASTER_MODEL="${MASTER_MODELS[$choice]}"
            print_info "Selected master model: $MASTER_MODEL"
            break
        else
            print_error "Invalid choice. Please enter a number between 1 and 5."
        fi
    done
    
    echo ""
}

# Prompt for Google API key
prompt_api_key() {
    print_header "Google API Key Configuration"
    
    if [ -n "$GOOGLE_API_KEY" ]; then
        print_info "Google API key found in environment variable"
        local masked_key="${GOOGLE_API_KEY:0:8}...${GOOGLE_API_KEY: -4}"
        echo "Current key: $masked_key"
        echo ""
        read -p "Use this key? [Y/n]: " use_existing
        use_existing=${use_existing:-Y}
        
        if [[ "$use_existing" =~ ^[Yy]$ ]]; then
            print_info "Using existing API key from environment"
            return 0
        fi
    fi
    
    echo ""
    echo "You need a Google API key to use Gemini models."
    echo "Get your API key from: https://makersuite.google.com/app/apikey"
    echo ""
    
    while true; do
        read -sp "Enter your Google API key: " api_key
        echo ""
        
        if [ -z "$api_key" ]; then
            print_error "API key cannot be empty"
            continue
        fi
        
        if [[ "$api_key" =~ ^AIza ]]; then
            GOOGLE_API_KEY="$api_key"
            export GOOGLE_API_KEY
            print_info "API key set successfully ✓"
            break
        else
            print_warning "API key doesn't look valid (should start with 'AIza')"
            read -p "Use it anyway? [y/N]: " use_anyway
            use_anyway=${use_anyway:-N}
            
            if [[ "$use_anyway" =~ ^[Yy]$ ]]; then
                GOOGLE_API_KEY="$api_key"
                export GOOGLE_API_KEY
                print_info "API key set"
                break
            fi
        fi
    done
    
    echo ""
}

# Setup configuration
setup_config() {
    if [ -z "$GOOGLE_API_KEY" ]; then
        prompt_api_key
    fi
    
    if [ -z "$MASTER_MODEL" ]; then
        prompt_master_model
    fi
}

get_timestamp() {
    date '+%Y%m%d_%H%M%S'
}

# Step 1: Initial finetuning on OpenFASOC data
run_initial_finetuning() {
    local model_size=$1
    local timestamp=$2
    
    print_header "Step 1: Initial Finetuning on OpenFASOC Data"
    
    local base_model="$([[ $model_size == "7b" ]] && echo "$BASE_7B" || echo "$BASE_13B")"
    local output_dir="initial_finetuned_models/${model_size}_${timestamp}"
    
    print_info "Base model: $base_model"
    print_info "Output directory: $output_dir"
    
    # Process OpenFASOC data
    print_info "Processing OpenFASOC data for $model_size model..."
    local processed_data_dir="data/processed_initial_ft_${timestamp}/${model_size}"
    
    python scripts/others/process_data.py \
        --model "$model_size" \
        --openfasoc_path "./external/OpenFASOC/" \
        --output_dir "$processed_data_dir"
    
    if [ ! -d "$processed_data_dir" ]; then
        print_error "Data processing failed - output directory not created"
        return 1
    fi
    
    # Run initial finetuning with LoRA
    print_info "Running initial LoRA finetuning..."
    
    python scripts/training/train.py \
        --train_file "$processed_data_dir/train_data_${model_size}.jsonl" \
        --output_dir "$output_dir" \
        --model_paths "$base_model" \
        --use_lora \
        --lora_r 16 \
        --lora_alpha 32 \
        --lora_dropout 0.05 \
        --num_train_epochs 3 \
        --learning_rate 2e-4 \
        --max_length 1024 \
        --logging_steps 10 \
        --save_total_limit 2 \
        --weight_decay 0.01 \
        --warmup_ratio 0.1 \
        --max_grad_norm 1.0
    
    # Find the LoRA adapter (not merged model) - saves 99.7% space
    local adapter_dir=$(find "$output_dir" -type f -name "adapter_config.json" | head -1 | xargs dirname)
    
    if [ -z "$adapter_dir" ]; then
        print_error "Initial finetuning completed but LoRA adapter not found"
        return 1
    fi
    
    print_info "Initial finetuning completed ✓"
    print_info "LoRA adapter: $adapter_dir (~40MB vs 13GB for merged model)"
    
    # Return the path to the LoRA adapter
    echo "$adapter_dir"
}

# Step 2: Self-improvement with master model evaluation
run_self_improvement() {
    local model_size=$1
    local finetuned_model=$2
    local timestamp=$3
    local iterations=$4
    
    print_header "Step 2: Self-Improvement with Master Model Evaluation"
    
    print_info "Starting model: $finetuned_model"
    print_info "Master model: $MASTER_MODEL"
    print_info "Iterations: $iterations"
    
    # Redirect verbose output to stderr so only the final model path is captured
    python end_to_end.py \
        --model_size "$model_size" \
        --base_model "$finetuned_model" \
        --master_model "$MASTER_MODEL" \
        --prompt_file "$PROMPT_FILE" \
        --instruction_file "$INSTRUCTION_FILE" \
        --google_api_key "$GOOGLE_API_KEY" \
        --iterations "$iterations" \
        --inferences_per_iteration 10 \
        --epochs_per_iteration 1 \
        --learning_rate 1e-6 \
        --train_last_n_layers 6 \
        --weight_decay 0.001 \
        --warmup_ratio 0.05 \
        --max_grad_norm 2.0 \
        --use_lora \
        --lora_r 16 \
        --lora_alpha 32 >&2
    
    # Find the latest pipeline run
    local latest_run=$(ls -td pipeline_runs/*/ | head -1)
    print_info "Self-improvement completed: $latest_run"
    
    # Find the final iteration LoRA adapter
    local final_iter=$((iterations - 1))
    local self_improved_model=$(find "$latest_run/models/iteration_${final_iter}" -type f -name "adapter_config.json" | head -1 | xargs dirname)
    
    if [ -z "$self_improved_model" ]; then
        print_warning "Expected adapter at iteration_${final_iter} not found, searching for latest adapter..."
        self_improved_model=$(find "$latest_run/models" -type f -name "adapter_config.json" | tail -1 | xargs dirname)
    fi
    
    if [ -z "$self_improved_model" ]; then
        print_error "Self-improvement completed but final adapter not found"
        return 1
    fi
    
    print_info "Self-improved model: $self_improved_model"
    
    # Return the path to the self-improved model
    echo "$self_improved_model"
}

# Step 3: GRPO optimization
run_grpo() {
    local model_size=$1
    local self_improved_model=$2
    local timestamp=$3
    local iterations=$4
    
    print_header "Step 3: GRPO Optimization on DRC/LVS Metrics"
    
    print_info "Starting model: $self_improved_model"
    print_info "Iterations: $iterations"
    
    python grpo_pipeline.py \
        --input_json "$DRC_LVS_DATA" \
        --base_model "$self_improved_model" \
        --output_dir "grpo_outputs/${model_size}_complete_${timestamp}" \
        --num_epochs 10 \
        --batch_size 12 \
        --learning_rate 1e-4 \
        --kl_coef 0.1 \
        --use_lora \
        --lora_r 16 \
        --lora_alpha 32 \
        --iterations "$iterations"
    
    local final_iter=$((iterations - 1))
    print_info "GRPO optimization completed ✓"
    print_info "Final LoRA adapter: grpo_outputs/${model_size}_complete_${timestamp}/iteration_${final_iter}/trained_model"
    print_info "💡 To merge adapter to full model for deployment, use: scripts/utils/lora_loader.py --merge"
}

# Run complete pipeline for single model
run_complete_pipeline() {
    local model_size=$1
    local timestamp=$(get_timestamp)
    
    print_header "Starting Complete Pipeline for ${model_size^^} Model"
    print_info "Timestamp: $timestamp"
    print_info "Self-improvement iterations: $SELF_IMPROVEMENT_ITERS"
    print_info "GRPO iterations: $GRPO_ITERS"
    
    # Step 1: Initial finetuning
    local finetuned_model=$(run_initial_finetuning "$model_size" "$timestamp")
    if [ $? -ne 0 ] || [ -z "$finetuned_model" ]; then
        print_error "Initial finetuning failed"
        return 1
    fi
    
    # Step 2: Self-improvement
    local self_improved_model=$(run_self_improvement "$model_size" "$finetuned_model" "$timestamp" "$SELF_IMPROVEMENT_ITERS")
    if [ $? -ne 0 ] || [ -z "$self_improved_model" ]; then
        print_error "Self-improvement failed"
        return 1
    fi
    
    # Step 3: GRPO
    run_grpo "$model_size" "$self_improved_model" "$timestamp" "$GRPO_ITERS"
    if [ $? -ne 0 ]; then
        print_error "GRPO optimization failed"
        return 1
    fi
    
    print_header "✓ Complete Pipeline Finished for ${model_size^^} Model"
    print_info "Results saved in:"
    print_info "  - Initial finetuned: initial_finetuned_models/${model_size}_${timestamp}"
    print_info "  - Self-improvement: $(dirname $(dirname "$self_improved_model"))"
    print_info "  - GRPO outputs: grpo_outputs/${model_size}_complete_${timestamp}"
}

# Run both models sequentially
run_both_models() {
    print_header "Running Complete Pipeline for Both Models"
    
    # Run 7B
    print_info "=== Starting 7B Model Pipeline ==="
    run_complete_pipeline "7b"
    local status_7b=$?
    
    # Run 13B
    print_info "=== Starting 13B Model Pipeline ==="
    run_complete_pipeline "13b"
    local status_13b=$?
    
    if [ $status_7b -eq 0 ] && [ $status_13b -eq 0 ]; then
        print_header "✓ Both Models Completed Successfully!"
    else
        print_error "One or more pipelines failed"
        print_info "7B status: $([[ $status_7b -eq 0 ]] && echo "✓ Success" || echo "✗ Failed")"
        print_info "13B status: $([[ $status_13b -eq 0 ]] && echo "✓ Success" || echo "✗ Failed")"
        return 1
    fi
}

# Print usage
print_usage() {
    cat << EOF
Complete GRPO Training Pipeline
================================

This pipeline starts from base CodeLlama models and runs:
  1. Initial finetuning on OpenFASOC data (LoRA)
  2. Self-improvement with master model evaluation (Gemini)
  3. GRPO optimization on DRC/LVS metrics

Usage:
  $0 <model_size> [options]

Model Sizes:
  7b          - Run 7B model only
  13b         - Run 13B model only
  both        - Run both 7B and 13B models sequentially

Options:
  --self-improvement-iters <N>    Number of self-improvement iterations (default: 3)
  --grpo-iters <N>                Number of GRPO iterations (default: 3)

Examples:
  $0 7b                                           # Default: 3 self-improvement, 3 GRPO
  $0 13b --self-improvement-iters 5               # 5 self-improvement, 3 GRPO
  $0 both --grpo-iters 5                          # 3 self-improvement, 5 GRPO
  $0 7b --self-improvement-iters 2 --grpo-iters 2 # 2 self-improvement, 2 GRPO

Interactive Prompts:
  • Master model selection (Gemini variants)
  • Google API key (if not set in environment)

Available Master Models:
  1. gemini-2.0-flash     - Fast, recommended (default)
  2. gemini-1.5-pro       - Best quality, slower
  3. gemini-1.5-flash     - Fast production
  4. gemini-1.5-flash-8b  - Lightweight, fast
  5. gemini-1.0-pro       - Legacy stable

Environment Variables (Optional):
  GOOGLE_API_KEY            - Pre-set to skip API key prompt

Expected Time per Iteration:
  Initial finetuning:    ~2-4 hours
  Self-improvement:      ~1-3 hours per iteration
  GRPO:                  ~2-4 hours per iteration

Total (default 3+3):
  7B model:  ~12-18 hours
  13B model: ~18-28 hours

EOF
}

# Parse command-line arguments
parse_args() {
    if [ $# -lt 1 ]; then
        print_usage
        exit 1
    fi
    
    MODEL_SIZE=$1
    shift
    
    # Parse options
    while [[ $# -gt 0 ]]; do
        case $1 in
            --self-improvement-iters)
                SELF_IMPROVEMENT_ITERS="$2"
                shift 2
                ;;
            --grpo-iters)
                GRPO_ITERS="$2"
                shift 2
                ;;
            *)
                print_error "Unknown option: $1"
                print_usage
                exit 1
                ;;
        esac
    done
    
    # Validate model size
    if [[ ! "$MODEL_SIZE" =~ ^(7b|13b|both)$ ]]; then
        print_error "Invalid model size: $MODEL_SIZE"
        print_usage
        exit 1
    fi
    
    # Validate iteration counts
    if ! [[ "$SELF_IMPROVEMENT_ITERS" =~ ^[0-9]+$ ]] || [ "$SELF_IMPROVEMENT_ITERS" -lt 1 ]; then
        print_error "Invalid self-improvement iterations: $SELF_IMPROVEMENT_ITERS (must be >= 1)"
        exit 1
    fi
    
    if ! [[ "$GRPO_ITERS" =~ ^[0-9]+$ ]] || [ "$GRPO_ITERS" -lt 1 ]; then
        print_error "Invalid GRPO iterations: $GRPO_ITERS (must be >= 1)"
        exit 1
    fi
}

# Main script
main() {
    cd "$REPO_ROOT"
    
    # Parse arguments
    parse_args "$@"
    
    # Validate environment
    validate_environment
    
    # Setup configuration (prompts for API key and master model)
    setup_config
    
    # Show pipeline summary
    print_header "Pipeline Configuration"
    print_info "Model size: $MODEL_SIZE"
    print_info "Master model: $MASTER_MODEL"
    print_info "Starting from: Base CodeLlama models"
    print_info "Self-improvement iterations: $SELF_IMPROVEMENT_ITERS"
    print_info "GRPO iterations: $GRPO_ITERS"
    echo ""
    read -p "Press Enter to start the pipeline or Ctrl+C to cancel..."
    
    # Run pipeline
    if [ "$MODEL_SIZE" == "both" ]; then
        run_both_models
    else
        run_complete_pipeline "$MODEL_SIZE"
    fi
}

# Run main
main "$@"
