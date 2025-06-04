# OpenFASoC LLM

An LLM-powered system for translating natural language prompts into Glayout strict syntax for electronic circuit layout generation. This repository implements a fine-tuned language model with Retrieval Augmented Generation (RAG) capabilities for analog circuit design automation.

## Overview

The OpenFASoC LLM system trains language models to understand analog design concepts and generate precise layout commands. The system combines two key learning approaches:

1. **In-Context Learning via RAG**: Understanding layout strategies and analog design terminology through retrieval of relevant documentation
2. **Supervised Fine-Tuning**: Learning to generate Glayout strict syntax through paired examples of natural language prompts and their corresponding layout commands

## Architecture

### Core Components

The system consists of several interconnected modules that handle data processing, model training, and inference:

- **Data Management**: Preprocessing and loading of training data with RAG context integration
- **RAG System**: Vector-based document retrieval for analog design knowledge
- **Model Training**: Fine-tuning pipeline using LoRA and Supervised Fine-Tuning
- **Validation**: Testing framework for synthetic data and conversation parsing
- **Session Management**: Interactive interface for LLM-powered layout generation

## Repository Structure

### Core Python Package (`LLM/`)

#### Data Management (`manage_data.py`)
Handles loading, preprocessing, and structuring of training data for the LLM.

**Key Functions:**
- `remove_comments_and_empty_lines(input_string: str) -> str`: Cleans text input by removing comments and empty lines
- `load_labeled_syntax_data_json(json_file_path, convo_dir_path, fail_on_error=True) -> List[Tuple[str, str]]`: Loads paired prompt-syntax examples from JSON files and .convo files
- `load_all_labeled_syntax_data_json(evaluation=False) -> List[Tuple[str, str]]`: Aggregates all labeled training/evaluation data from the syntax_data directory
- `get_glayout_context() -> str`: Retrieves Glayout syntax reference documentation from Markdown files
- `get_prompt_from_template(tokenizer, prompt, ragcontext=None, strictsyntax=None, return_message=False) -> str`: Constructs structured prompts with RAG context and syntax examples
- `unify_prompt_and_add_context_to_data(tokenizer, data, no_label=False) -> list`: Enhances prompts with RAG-retrieved context and combines with target syntax
- `load_preprocessed_data_in_messages_format()`: Prepares data in conversational format for SFTTrainer
- `load_preprocessed_pretokenized_data(tokenizer)`: **[Deprecated]** Pre-tokenizes data for training

#### RAG Implementation (`rag.py`)
Implements Retrieval Augmented Generation for incorporating analog design knowledge.

**RAGdb Class:**
- `__init__(rag_data_dir, minimum_similarity=1.35)`: Initializes vector database with document embeddings using sentence transformers (all-MiniLM-L6-v2)
- `query(query_text: str, k=1) -> list`: Retrieves k most similar documents based on vector similarity
- `_get_document_label(langchain_doc: Document) -> str`: Extracts document identifiers for retrieval

**Key Features:**
- Vector embeddings using HuggingFace sentence transformers
- Chroma vector database for efficient similarity search
- Configurable similarity thresholds for relevance filtering

#### Training and Inference (`train_and_run.py`)
Main training pipeline and model session management for Glayout LLM.

**Training Functions:**
- `load_model_and_tokenizer(model: str, accesstoken: str, device: str, lora=True) -> tuple`: Loads pre-trained models with optional LoRA and quantization
- `run_full_SFT_training(model: str, accesstoken: str) -> tuple`: Implements Supervised Fine-Tuning using SFTTrainer
- `train(model, tokenizer, data, qlora=True)`: **[Deprecated]** Legacy training loop implementation

**GlayoutLLMSessionHandler Class:**
- `__init__(model: str, accesstoken: str, converse_mode=False)`: Initializes model session with RAG integration
- `generate(user_input: str) -> str`: Core inference method with prompt engineering and RAG context
- `clear_history()`: Resets conversation history with Glayout-specific context
- `load_model_from_checkpoint(checkpoint_dir)`: Loads fine-tuned models from saved checkpoints

**Supported Models:**
- Microsoft Phi-3 series
- Mistral models
- Custom model configurations with LoRA adaptation

#### Validation (`validate_synthetic_data.py`)
Testing framework for validating .convo files and synthetic training data.

**Key Functions:**
- `instantiate_convo(pdk: MappedPDK, convo_file) -> bool`: Validates .convo files by attempting layout generation
- `run_all_tests(test_cases_dir="./syntax_data/convos")`: Batch validation of all conversation files

#### Parser Testing (`parser_test.py`)
Test script for .convo file parsing functionality using the convo_parser module.

### Supporting Directories

#### `convo_parser/`
Contains Python modules for parsing .convo files that represent conversational data or command sequences for Glayout. Defines classes like `Convo` and `ConvoParser` for interpreting and transforming .convo file content.

#### `rag_data/`
Knowledge base directory containing Markdown documents with analog design information, layout strategies, and domain-specific knowledge. These documents form the corpus for RAG retrieval during training and inference.

#### `syntax_data/`
Training and evaluation data repository containing:
- **JSON files**: Labeled examples mapping natural language prompts to Glayout strict syntax
- **`convos/` subdirectory**: Collection of .convo files with valid Glayout command sequences and test cases

## Training Process

### Data Preprocessing
1. **Context Integration**: RAG system retrieves relevant analog design information based on user prompts
2. **Prompt Engineering**: Structured prompts combine user input, RAG context, and syntax reference guides
3. **Data Formatting**: Examples are formatted for SFTTrainer with proper message structure

### Fine-Tuning Pipeline
1. **Model Loading**: Pre-trained language models loaded with LoRA configuration and 8-bit quantization
2. **Supervised Fine-Tuning**: Training focuses on completion generation using SFTTrainer from the `trl` library
3. **Loss Computation**: Training loss computed only on generated completions, not input prompts

### RAG Integration
1. **Vector Embedding**: Documents processed using sentence transformers to create vector representations
2. **Similarity Search**: Query-based retrieval of most relevant documents using Chroma vector database
3. **Context Injection**: Retrieved information integrated into training prompts and inference queries

## Usage

### Training a New Model
```python
from train_and_run import run_full_SFT_training

# Fine-tune model with Glayout-specific data
model, tokenizer = run_full_SFT_training(
    model="microsoft/Phi-3-mini-4k-instruct",
    accesstoken="your_hf_token"
)
```

### Running Inference
```python
from train_and_run import GlayoutLLMSessionHandler

# Initialize session handler
handler = GlayoutLLMSessionHandler(
    model="microsoft/Phi-3-mini-4k-instruct",
    accesstoken="your_hf_token"
)

# Generate Glayout syntax from natural language
response = handler.generate("Create a current mirror with NMOS transistors")
```

### Validating Training Data
```python
from validate_synthetic_data import run_all_tests

# Validate all .convo files in syntax_data
run_all_tests("./syntax_data/convos")
```

## Key Features

- **Dual Learning Approach**: Combines RAG-based knowledge retrieval with supervised fine-tuning
- **Efficient Training**: Uses LoRA adaptation and 8-bit quantization for resource-efficient fine-tuning
- **Vector-Based Retrieval**: Semantic search through analog design documentation
- **Conversational Interface**: Interactive session management with history tracking
- **Comprehensive Validation**: Testing framework for synthetic data and model outputs
- **Flexible Model Support**: Compatible with various pre-trained language models

## Dependencies

- **Core ML**: Transformers, Torch, TRL (SFTTrainer)
- **RAG Components**: LangChain, Chroma, Sentence Transformers
- **Data Processing**: Pandas, JSON handling libraries
- **Model Optimization**: PEFT (LoRA), BitsAndBytesConfig
- **Glayout Integration**: Custom Glayout modules for syntax parsing and validation

## Model Architecture Details

The system supports multiple base model architectures with specific optimizations:

- **Quantization**: 8-bit quantization using BitsAndBytesConfig for memory efficiency
- **LoRA Adaptation**: Low-rank adaptation for parameter-efficient fine-tuning
- **Context Management**: Structured prompt templates with RAG context integration
- **Conversation Handling**: Multi-turn conversation support with history management

## Data Flow

1. **Training Data**: Natural language prompts paired with Glayout strict syntax examples
2. **RAG Enhancement**: Prompts augmented with retrieved analog design knowledge
3. **Model Training**: Supervised fine-tuning on enhanced prompt-syntax pairs
4. **Inference**: User queries processed through RAG retrieval and model generation
5. **Validation**: Generated syntax validated through Glayout instantiation

This system enables natural language interaction with electronic circuit layout tools, bridging the gap between design intent and precise layout specifications through advanced language model capabilities.
