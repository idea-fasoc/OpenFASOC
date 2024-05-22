#from glayout.llm.manage_data import load_all_labeled_syntax_data_json


PROMPT_TEMPLATE = """
Below is some context on Glayout strictsyntax:
{glayout_NLPcontext}

Below is context on analog circuit design which will help you convert an example prompt to Glayout strictsyntax
{context}

----
Convert the following prompt to Glayout strictsyntax:
{prompt}
"""

# PROMPT_TEMPLATE.replace({glayout_NLPcontext},glayout_NLPcontext).replace("{context}",context).replace("{prompt}",prompt)

#labeled_data = load_all_labeled_syntax_data_json()




from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "mistralai/Mistral-7B-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_id)

model = AutoModelForCausalLM.from_pretrained(model_id)

text = "Hello my name is"
inputs = tokenizer(text, return_tensors="pt")

outputs = model.generate(**inputs, max_new_tokens=20)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))


