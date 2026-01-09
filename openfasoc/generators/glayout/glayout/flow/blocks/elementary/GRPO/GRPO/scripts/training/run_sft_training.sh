#!/bin/bash

# Supervised Fine-Tuning Script for Local Checkpoints
# Uses the enhanced train.py with full weight training and robust JSON parsing

echo " Starting Supervised Fine-Tuning with Local Checkpoints"

# Check if robust training data exists, if not create it
if [ ! -f "train_data_7b_robust.jsonl" ] || [ ! -f "train_data_13b_robust.jsonl" ]; then
    echo " Creating robust training data with improved JSON parsing..."
    python fix_json_parsing.py
    if [ $? -ne 0 ]; then
        echo " Failed to create robust training data!"
        exit 1
    fi
fi

# Verify training data
echo " Training data summary:"
echo "  7B samples: $(wc -l < train_data_7b_robust.jsonl)"
echo "  13B samples: $(wc -l < train_data_13b_robust.jsonl)"

# Training configuration
OUTPUT_DIR="./supervised_finetuned_models"
EPOCHS=3
LEARNING_RATE=3e-5

echo "========================="
echo " Training Configuration:"
echo "  Output Directory: $OUTPUT_DIR"
echo "  Epochs: $EPOCHS"
echo "  Learning Rate: $LEARNING_RATE"
echo "  Full Weight Training: Yes"
echo "  GPU Memory Optimization: Yes"
echo "  Robust JSON Parsing: Yes"
echo "========================="

# Function to run training for a model
run_training() {
    local model_path=$1
    local train_file=$2
    local model_name=$3
    local train_last_layers=$4
    local model_output_dir=$5
    
    echo ""
    echo " Training $model_name model..."
    echo "  Model Path: $model_path"
    echo "  Training Data: $train_file"
    echo "  Train Last N Layers: $train_last_layers"
    echo "  Output Directory: $model_output_dir"
    
    # Create model-specific output directory
    mkdir -p "$model_output_dir"
    
    python finetuning/train.py \
        --train_file "$train_file" \
        --output_dir "$model_output_dir" \
        --model_paths "$model_path" \
        --full_weight_training \
        --train_last_n_layers $train_last_layers \
        --num_train_epochs $EPOCHS \
        --learning_rate $LEARNING_RATE \
        --max_length 1024 \
        --logging_steps 10 \
        --save_total_limit 2 \
        --weight_decay 0.01 \
        --warmup_ratio 0.1 \
        --max_grad_norm 1.0
    
    if [ $? -eq 0 ]; then
        echo " $model_name training completed successfully!"
        echo " Model saved to: $model_output_dir"
    else
        echo " $model_name training failed!"
        return 1
    fi
}

# Check if models exist
if [ ! -d "7b/final_model" ]; then
    echo " Error: 7b/final_model directory not found!"
    exit 1
fi

if [ ! -d "13b/final_model" ]; then
    echo " Error: 13b/final_model directory not found!"
    exit 1
fi

# Create base output directory
mkdir -p "$OUTPUT_DIR"

# Train 7B model (train last 8 layers to prevent overfitting)
run_training "./7b/final_model" "train_data_7b_robust.jsonl" "7B" 8 "$OUTPUT_DIR/7b"

# Train 13B model (train last 12 layers)
run_training "./13b/final_model" "train_data_13b_robust.jsonl" "13B" 12 "$OUTPUT_DIR/13b"

echo ""
echo " All training completed!"
echo " Models saved in: $OUTPUT_DIR"
echo ""
echo " Training Summary:"
ls -la "$OUTPUT_DIR"/ 2>/dev/null || echo "No output directory created (training may have failed)"

# Optional: Show GPU memory usage
if command -v nvidia-smi &> /dev/null; then
    echo ""
    echo " Final GPU Memory Status:"
    nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader,nounits
fi 