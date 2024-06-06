from pathlib import Path
import json
from typing import Union
import time
import argparse

from glayout.llm.manage_data import (
    load_preprocessed_pretokenized_data,
    unify_prompt_and_add_context_to_data,
    get_glayout_context,
    get_prompt_from_template,
    load_preprocessed_data_in_messages_format,
    load_all_labeled_syntax_data_json,
)

import torch
from peft import (
    get_peft_config,
    get_peft_model,
    LoraConfig,
    prepare_model_for_kbit_training,
    AutoPeftModelForCausalLM,
)
from datasets import Dataset
from auto_gptq import AutoGPTQForCausalLM

from transformers import (
    AutoModelForCausalLM,
    AutoModel,
    AutoTokenizer,
    TrainingArguments,
    BitsAndBytesConfig,
)
import transformers
from trl import DataCollatorForCompletionOnlyLM, SFTTrainer


def get_huggingface_token():
    """Parse the command-line arguments to retrieve the Hugging Face access token.
    This function uses argparse to handle command-line arguments and specifically looks for an 
    access token required to download models and tokenizers from Hugging Face. If the token is 
    not provided, it raises an EnvironmentError with instructions on how to obtain one.
    Returns:
        str: The Hugging Face access token.
    Raises:
        EnvironmentError: If the access token is not provided in the command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Manage, interact, and run the Glayout LLM")
    parser.add_argument(
        "-t",
        "--token",
        type=str,
        help="Specify the access token you are using to download the model and tokenizer from huggingface",
    )
    args = parser.parse_args()
    if args.token is None:
        errstring = "To download models from huggingface you need a hugging face account and an access token"
        errstring += "\nYou can create a hugging face account here: https://huggingface.co/join\n"
        errstring += "Once you have an account and sign in, you can create an access token (need read access) here:\n"
        errstring += "https://huggingface.co/settings/tokens\n"
        errstring += "pass the access token in the command line with the option --token=[insert token here]"
        raise EnvironmentError(errstring)
    return args.token
#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
accesstoken = get_huggingface_token()


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
    qlora = True
    # load modela
    # modelname = "mistralai/Mistral-7B-v0.1"
    modelname = "mistralai/Mistral-7B-Instruct-v0.3"
    if not qlora:
        model = AutoModelForCausalLM.from_pretrained(modelname, token=accesstoken)
    else:
        # modelname = "TheBloke/Mistral-7B-Instruct-v0.2-GPTQ"
        # model = AutoModelForCausalLM.from_pretrained(modelname, token=accesstoken, device_map="auto", load_in_8bit=True)
        model = AutoModelForCausalLM.from_pretrained(
            modelname,
            token=accesstoken,
            quantization_config=BitsAndBytesConfig(load_in_8bit=True)
        )
        # model = AutoModelForCausalLM.from_pretrained(modelname, token=accesstoken, device_map="auto", trust_remote_code=False, revision="main")
        model.train()
        model.gradient_checkpointing_enable()
        model = prepare_model_for_kbit_training(model)
    tokenizer = AutoTokenizer.from_pretrained(
        modelname, use_fast=True, token=accesstoken
    )
    # configure lora
    if lora:
        peft_config = LoraConfig(
            task_type="CAUSAL_LM",
            r=8,
            lora_alpha=16,
            lora_dropout=0.05,
            bias="none",
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        )
        model = get_peft_model(model, peft_config)
        model.print_trainable_parameters()
    if not qlora:  # the model loaded by qlora is prequantized
        model.half()
        model.to(device)
    tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    return model, tokenizer


def run_llm_normal(
    model, tokenizer, device: str, prompt: str, max_new_tokens: int = 1000
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
    inputs = tokenizer.apply_chat_template(
        [{"role": "user", "content": prompt}],
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt",
    )
    inputs = inputs.to(device)
    outputs = model.generate(input_ids=inputs, max_new_tokens=max_new_tokens)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def train(model, tokenizer, data, qlora: bool = True):
    if not qlora:
        raise NotImplementedError("currently only support qlora")
    # model.train()
    # hyperparameters
    lr = 1e-4
    batch_size = 1  # 2 #4
    num_epochs = 2
    # define training arguments
    output_dir = Path(__file__).resolve().parent / "glayout_llm_checkpoints"
    training_args = TrainingArguments(
        output_dir=str(output_dir),
        learning_rate=lr,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        num_train_epochs=num_epochs,
        weight_decay=0.01,
        logging_strategy="epoch",
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        gradient_accumulation_steps=1,
        warmup_steps=0,
        bf16=True,
        optim="paged_adamw_8bit",
    )
    # inlcude in the prompt do not repeat the context
    # try to see Mistral 7b docs if there is another label
    # try to only train on the response
    # experiment with these results include prompts or not
    # check the context length for Mistral
    # code distral, try to directly create from the python code.
    data_collator = transformers.DataCollatorForLanguageModeling(tokenizer, mlm=False)
    # data_collator = DataCollatorForCompletionOnlyLM(response_template="[/INST]",tokenizer=tokenizer,mlm=False)
    # configure trainer
    trainer = transformers.Trainer(
        model=model,
        train_dataset=data["train"],
        eval_dataset=data["evaluation"],
        args=training_args,
        data_collator=data_collator,
    )
    # train model
    model.config.use_cache = False  # silence warnings
    trainer.train()
    model.config.use_cache = True  # reenable warnings
    # model.to("cuda")
    model.save_pretrained(output_dir / "checkpoint-bestperf")
    model.eval()
    return model


def run_full_training() -> tuple:
    """returns model (and tokenizer) resulting from training LLM
    Returns:
        tuple: model, tokenizer
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, tokenizer = load_model_and_tokenizer(device)
    # load fine tuning data
    data = load_preprocessed_pretokenized_data(tokenizer)
    return train(model, tokenizer, data), tokenizer


def run_full_SFT_training() -> tuple:
    # load model, tokenizer
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, tokenizer = load_model_and_tokenizer(device)
    # load data
    data = load_preprocessed_data_in_messages_format()
    # train
    # hyperparameters
    lr = 5e-5
    batch_size = 1  # 2 #4
    num_epochs = 4
    # define training arguments
    output_dir = Path(__file__).resolve().parent / "glayout_llm_checkpoints"
    training_args = TrainingArguments(
        output_dir=str(output_dir),
        learning_rate=lr,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        num_train_epochs=num_epochs,
        weight_decay=0.01,
        logging_strategy="epoch",
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        gradient_accumulation_steps=1,
        warmup_steps=1,
        bf16=True,
        optim="paged_adamw_8bit",
    )
    #training_args = TrainingArguments(output_dir=str(output_dir))
    data_collator = DataCollatorForCompletionOnlyLM(response_template="[/INST]",instruction_template="[INST]",tokenizer=tokenizer,mlm=False)
    #import pdb; pdb.set_trace()
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        args=training_args,
        train_dataset=data["train"],
        eval_dataset=data["evaluation"],
        max_seq_length=4096,
        data_collator=data_collator
    )# add context to all glayout prompts
    trainer.train()
    model.save_pretrained(output_dir / "checkpoint-bestperf")
    model.eval()
    return model, tokenizer


class GlayoutLLMSessionHandler:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # look for an existing model
        base_path = Path(__file__).resolve().parent
        checkpoint_dirs = list(base_path.glob("**/*checkpoint-bestperf*"))
        checkpoint_dir = None
        if len(checkpoint_dirs) > 0 and checkpoint_dirs[-1].is_dir():
            checkpoint_dir = checkpoint_dirs[-1]
        # if no existing model then run training
        if checkpoint_dir:
            print(f"Found checkpoint directory: {checkpoint_dir}")
            model, tokenizer = self.load_model_from_checkpoint(checkpoint_dir)
            # model.to(self.device)
            print("Model and tokenizer loaded successfully.")
        else:
            # model, tokenizer = run_full_training()
            model, tokenizer = run_full_SFT_training()
        # set self attributes
        #self.promptexamples = "the following are several labeled examples of converting prompts to strict syntax.\n"
        #promptexamples = load_all_labeled_syntax_data_json()
        #for prompt, result in promptexamples[::25]:
        #    self.promptexamples += prompt + "\n" + result + "\n\n"
        self.model = model
        self.tokenizer = tokenizer
        self.chat_history = []
        self.chat_history.append({"role": "user", "content": get_glayout_context()})
        self.chat_history.append({"role": "assistant", "content": RESPONSE})
        #print(self.generate(self.promptexamples, clear=False))
        #print(self.generate(user_input="summarize the following:\n" + get_glayout_context(), clear=False))

    def load_model_from_checkpoint(self, checkpoint_dir):
        # helper function
        def get_base_model_name_or_path(file_path: Union[str, Path]) -> str:
            file_path = Path(file_path)
            with file_path.open("r") as file:
                data = json.load(file)
            return data.get("base_model_name_or_path")

        # load model
        model = AutoPeftModelForCausalLM.from_pretrained(
            checkpoint_dir, device_map=self.device
        )
        model_id = get_base_model_name_or_path(checkpoint_dir / "adapter_config.json")
        # basemodel = AutoModelForCausalLM.from_pretrained(model_id, device_map=self.device)
        # model = AutoGPTQForCausalLM.from_quantized(checkpoint_dir)
        # model = model.merge_and_unload()
        # load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True, token=accesstoken)
        return model, tokenizer

    def generate(self, user_input: str, clear: bool = False) -> str:
        """provide LLM output from user input
        by default will keep appending to the previous prompts in a conversation.
        Args:
            user_input (str): general user prompt
            clear (bool, Optional): reset the chat history. Default False
        Returns:
            str: strictsyntax output
        """
        self.model.eval()
        user_input = f"Glayout strictsyntax is a electronic circuit layout command language. Convert the following prompt to Glayout strictsyntax:\n{user_input}"
        if clear:
            self.chat_history = []
            self.generate(
                user_input="summarize the following:\n" + get_glayout_context(),
                clear=False,
            )
        self.chat_history.append({"role": "user", "content": user_input})
        inputs = self.tokenizer.apply_chat_template(
            self.chat_history,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt",
        )
        inputs = inputs.to(self.device)
        outputs = self.model.generate(input_ids=inputs, max_new_tokens=4096)
        response = self.tokenizer.decode(
            outputs[0][len(inputs[0]) : -1], skip_special_tokens=False
        )
        self.chat_history.append({"role": "assistant", "content": response})
        return response
        # prompt = unify_prompt_and_add_context_to_data(self.tokenizer, input_list, no_label=True)[0]
        # return run_llm_normal(model=self.model, tokenizer=self.tokenizer, device=self.device, prompt=prompt)

    def __call__(self, user_input: str) -> str:
        return self.generate(user_input=user_input)


RESPONSE = """Example Syntax:
Importing: import CrossCoupledInverters
Creating Parameters: create a float parameter called device_width
Placing Components: place a nmos called m1 with width 1.0, length 2.0, fingers 2
Moving Components: move m1 below m2
Routing: route between m1_source_E and m2_source_E using smart_route
This structured approach ensures clarity and modularity, making it easier to design complex analog circuits efficiently."""
