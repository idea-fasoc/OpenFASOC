import requests
from pathlib import Path

from glayout.llm.manage_data import load_all_labeled_syntax_data_json, RAGdb
# from manage_data import load_all_labeled_syntax_data_json, RAGvecdb, get_glayout_context
import torch
import time
from peft import get_peft_config, get_peft_model, LoraConfig
from datasets import Dataset

# from transformers import AutoModelForCausalLM, AutoTokenizer, Conv1D, TrainingArguments
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
import transformers

def get_prompt_from_template(
    glayout_NLPcontext: str, ragcontext: str, prompt: str, instruct: bool = False
) -> str:
    prompt = f"""
[CONTEXT]
[EXPLAINING STRICT SYNTAX]
Below is some context on Glayout strictsyntax:
{glayout_NLPcontext}
[/EXPLAINING STRICT SYNTAX]
Below is context on analog circuit design which will help you convert an example prompt to Glayout strictsyntax
{ragcontext}
[/CONTEXT]
----
[TRANSLATION_TASK]
Convert the following prompt to Glayout strictsyntax:
{prompt}
[/TRANSLATION_TASK]
"""
    if instruct:
        prompt = f"[INST] {prompt} [/INST]"
    return prompt


# pass all prompts through rag before handing training data to llm
def add_context_to_data(data: list) -> list:
    """Enhance a list of data pairs (prompt and result) with contextual information from external documents.
    This function takes each prompt-result pair in the input data, queries an vector database for relevant documents,
    constructs a new prompt incorporating this contextual information according to a specified template, and returns the modified
    list of prompt-result pairs with added context.

    Args:
        data (list): A list of tuples, where each tuple is (prompt (str), result (str))

    Returns:
        list: same format as input but the prompt has additional context and is correctly formated
    """
    glayout_context = get_glayout_context()
    contextualized_prompts = list()
    for prompt, result in data:
        docs = RAGvecdb.query(prompt, 2)
        ragdata = str()
        for i, doc in enumerate(docs):
            ragdata += f"[CONTEXT DOCUMENT NUMBER {i}]\n"
            ragdata += doc + "\n"
            ragdata += f"[/CONTEXT DOCUMENT NUMBER {i}]\n"
        newprompt = get_prompt_from_template(glayout_context, ragdata, prompt)
        contextualized_prompts.append((newprompt, result))
    return contextualized_prompts


# credit
# https://stackoverflow.com/questions/76768226/target-modules-for-applying-peft-lora-on-different-models
def get_lora_supported_layer_names(model) -> list:
    """create a list of lora supported layers in a particular model
    This allows for easy setting of layers when creating a lora config
    only use this if you want to use lora with all the layers

    Args:
        model (huggingface model): any model compatible with hugging face

    Returns:
        list: list of strings (layer names)
    """
    # Create a list to store the layer names
    layer_names = list()
    # Recursively visit all modules and submodules
    for name, module in model.named_modules():
        # Check if the module is an instance of the specified layers
        # if isinstance(module, (torch.nn.Linear, torch.nn.Embedding, torch.nn.Conv2d, Conv1D)):
        if isinstance(module, (torch.nn.Linear, torch.nn.Embedding, torch.nn.Conv2d)):
            layer_names.append(".".join(name.split(".")[4:]).split(".")[0])
    layer_names = list(set(layer_names))
    return [name for name in layer_names if not (name.isspace() or len(name) == 0)]


# returns model, tokenizer
def load_model_and_tokenizer(device: str, lora: bool = True) -> tuple:
    """Downloads or restores model and tokenizer
    converts the model to half precision
    moves tokenizer and model to the specified device

    Args:
        device (str): move model to device (tokenizer always runs on CPU)
                      (e.g., 'cpu', 'cuda').

    Returns:
        tuple: first element is model and second is tokenizer.

    Raises:
        ValueError: If there is an error in loading the model or tokenizer.
        RuntimeError: If there is an error moving the model to the specified device.
    """
    accesstoken = "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"
    modelname = "mistralai/Mistral-7B-v0.1"
    modelname = "mistralai/Mistral-7B-Instruct-v0.2"
    model = AutoModelForCausalLM.from_pretrained(modelname, token=accesstoken)
    tokenizer = AutoTokenizer.from_pretrained(modelname, use_fast=True)
    if lora:
        peft_config = LoraConfig(
            task_type="CAUSAL_LM",
            r=8,
            lora_alpha=32,
            lora_dropout=0.1,
            target_modules=get_lora_supported_layer_names(model),
        )
        model = get_peft_model(model, peft_config)
        model.print_trainable_parameters()
    model.half()
    model.to(device)
    tokenizer.pad_token = tokenizer.eos_token
    return model, tokenizer


def run_llm_normal(
    model, tokenizer, device: str, prompt: str, max_new_tokens: int = 500
) -> str:
    """Generate a text completion for a given prompt using a provided language model.

    Args:
        model: The language model to use, should be compatible with huggingfaceinterface
        device (str): The device where the model is currently located
        prompt (str): The initial text to prompt the language model with.
        max_new_tokens (int, optional): maximum number of new tokens to generate. Defaults to 500.

    Returns:
        str: The text generated by the language model as a continuation of the prompt.
    """
    model.eval()
    inputs = tokenizer(prompt, return_tensors="pt")
    inputs.to(device)
    outputs = model.generate(**inputs, max_new_tokens=max_new_tokens)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


# tokenize both the prompts and expected responses
def pre_tokenize_and_convert_dataset_to_arrow(tokenizer, data: list) -> list:
    tokenized_prompts = list()
    tokenized_responses = list()
    for prompt, response in data:
        tokenized_prompt = tokenizer(prompt, return_tensors="pt")
        tokenized_response = tokenizer(response, return_tensors="pt")
        tokenized_prompts.append(tokenized_prompt)
        tokenized_responses.append(tokenized_response)
    dictionary_data = {"prompt": tokenized_prompts, "strictsyntax": tokenized_responses}
    return tokenized_data


def train(model, tokenizer, data):
    data = pre_tokenize_dataset(tokenizer, data)
    model.train()
    # hyperparameters
    lr = 2e-4
    batch_size = 4
    num_epochs = 10
    # define training arguments
    training_args = TrainingArguments(
        output_dir="glayout_llm_checkpoints",
        learning_rate=lr,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        num_train_epochs=num_epochs,
        weight_decay=0.01,
        logging_strategy="epoch",
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        gradient_accumulation_steps=4,
        warmup_steps=2,
        fp16=True,
        # optim="paged_adamw_8bit",
    )
    # configure trainer
    trainer = transformers.Trainer(
        model=model,
        train_dataset=tokenized_data["train"],
        eval_dataset=tokenized_data["test"],
        args=training_args,
        data_collator=data_collator,
    )
    # train model
    model.config.use_cache = False  # silence warnings
    trainer.train()
    model.config.use_cache = True  # reenable warnings
    return model


def run_full_training():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, tokenizer = load_model_and_tokenizer(device)
    # load fine tuning data
    labeled_data = add_context_to_data(load_all_labeled_syntax_data_json())
    return train(model, tokenizer, labeled_data)


run_full_training()
# # time was 28.69 seconds for CPU
# # time on GPU including transfering to and from GPU 19.33 seconds
# # raw GPU compute time 1.31 seconds
# # time if you do not move the model back to the cpu 9.67 seconds

# text = "Hello my name is"

# print(run_llm_normal(model, tokenizer, DEVICE, text))


# data["train"] and data["test"]
# each is 