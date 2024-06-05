import json
import warnings
from pathlib import Path
from typing import List, Tuple, Union
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import Chroma
#from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from datasets import Dataset
from typing import Optional


def remove_comments_and_empty_lines(input_string: str) -> str:
    """
    Removes all lines starting with a '#' or any empty lines from the input string.
    Args:
        input_string (str): The input string containing multiple lines.
    Returns:
        str: The modified string with comments and empty lines removed.
    """
    # Split the input string into individual lines
    lines = input_string.split('\n')
    # Filter out lines that start with # or are empty
    filtered_lines = str()
    for line in lines:
        remove = line.strip().startswith('#') or line.strip() == ''
        if not remove:
            filtered_lines += line + "\n"
    return filtered_lines


def load_labeled_syntax_data_json(
    json_file_path: Union[str, Path],
    convo_dir_path: Union[str, Path],
    fail_on_error: bool = True,
) -> List[Tuple[str, str]]:
    """Load all labeled data examples from a JSON file by reading LLM prompt
    and extracting strict syntax from corresponding '.convo' files.
    Args:
        json_file_path (str or Path): The path to the JSON file.
        convo_dir_path (str or Path): The path to the directory containing convo files for training
        fail_on_error (bool): if False, issue warnings if an individual example raises an Exception
    Raises:
        FileNotFoundError: If a '.convo' file, the convo_dir_path or json_file_path do not exist
        KeyError: if the JSON file does not correspond to the expected form
            jsonfile[data] must be a list of examples containing an LLMprompt and NLPfilename
    Returns:
        list of tuple: A list of tuples containing information about each example.
            Each tuple consists of:
                - str: The LLM prompt.
                - str: The text found in the NLP file.
    """
    # process the convo dir path
    convo_dir_path = Path(convo_dir_path).resolve()
    if not convo_dir_path.is_dir():
        raise FileNotFoundError(f"convo directory not found {convo_dir_path}")
    # this requires manage_data.py to be in the llm folder
    # Load JSON data
    json_file_path = Path(json_file_path).resolve()
    if not json_file_path.is_file():
        raise FileNotFoundError(f"could not find JSON file {json_file_path}")
    with open(json_file_path, "r") as file:
        data = json.load(file)
    examples = data.get("data")
    if examples is None:
        raise KeyError(
            f"data not found in JSON file {json_file_path}, ensure 'data' keyword is used"
        )
    # loop through examples and append to results
    results = list()
    for example in examples:
        try:
            llm_prompt = example.get("LLMprompt")
            if llm_prompt is None:
                raise KeyError(f"LLMprompt not found in JSON data {example}")
            # get the name of the strict syntax convo corresponding to this example
            nlp_filename = example.get("NLPfilename")
            if nlp_filename is None:
                raise KeyError(f"NLPfilename not found in JSON data {example}")
            convo_filename = f"{nlp_filename.strip()}"
            if not convo_filename.endswith(".convo"):
                convo_filename += ".convo"
            # get the .convo file path and check that it exists
            convo_file_path = Path(convo_dir_path).resolve() / convo_filename
            if not convo_file_path.is_file():
                raise FileNotFoundError(f"Convo file '{convo_file_path}' not found.")
            # Read text from convo file
            with convo_file_path.open("r") as nlp_file:
                nlp_text = remove_comments_and_empty_lines(nlp_file.read())
            results.append((llm_prompt, nlp_text))
        except (FileNotFoundError, KeyError) as faulty_example_error:
            if fail_on_error:
                raise faulty_example_error
            print(f"\n\nan exception was encounterd when processing {example}\n")
            warnings.warn(f"{faulty_example_error}")
    return results


def load_all_labeled_syntax_data_json(
    evaluation: bool = False,
) -> List[Tuple[str, str]]:
    """look in syntax_data folder for any json files
    and run load_labeled_syntax_data_json on those files
    Args:
        evaluation (bool, Optional): if True, only load json files containing keyword "eval", default False
    Returns:
        list[tuple]: all results from running load_labeled_syntax_data_json on all json files
    """
    # Path to the directory containing JSON files
    llm_dir = Path(__file__).resolve().parent
    json_dir = llm_dir / "syntax_data"
    convo_dir = json_dir / "convos"
    if not json_dir.is_dir():
        raise FileNotFoundError(
            "Could not find syntax_data directory within llm subpackage of glayout"
        )
    # Iterate over all JSON files in the directory
    all_results = list()
    for json_file_path in json_dir.glob("*.json"):
        eval_in_name = "eval" in json_file_path.name
        # load evaluation data and evaluation is in name of this json
        if evaluation and eval_in_name:
            all_results.extend(
                load_labeled_syntax_data_json(json_file_path, convo_dir, False)
            )
        # dont load evaluation data and evaluation is not in name of this json
        elif not (evaluation or eval_in_name):
            all_results.extend(
                load_labeled_syntax_data_json(json_file_path, convo_dir, False)
            )
    return all_results


class RAGdb:
    """
    A class to create and manage a vector database for the RAG data using ChromaDB.

    Attributes:
        chroma_client (Client): The ChromaDB client used for managing the vector database.
        collection_name (str): The name of the collection used in ChromaDB.
        collection (Collection): The vector database
    """

    def __init__(self, rag_data_dir: Union[str, Path]):
        """Initializes the RAGdb instance with a ChromaDB collection"""
        # error checking
        rag_data_dir = Path(rag_data_dir).resolve()
        if not rag_data_dir.is_dir():
            raise FileNotFoundError(f"could not find RAG data directory {rag_data_dir}")
        # load RAG data
        self.documents = DirectoryLoader(str(rag_data_dir), glob="*.md").load()
        # create vector db
        embeddings_model_name = "sentence-transformers/all-MiniLM-L6-v2"
        embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
        self.vectordb = Chroma.from_documents(
            documents=self.documents, embedding=embeddings
        )

    def query(self, query_text: str, k: int = 1) -> list:
        """
        Queries the vector database to find the top-k most similar vectors to the given query text.
        Args:
            query_text (str): The text to query.
        Returns:
            List: The list of top-k most similar docs.
        """
        kact = k if k>1 else 2
        rawdocs = self.vectordb.similarity_search(query=query_text, k=kact)
        rawtxt = list()
        for i, doc in enumerate(rawdocs):
            rawtxt.append(doc.page_content)
            if i == kact-1:
                break
        return rawtxt


RAGvecdb = RAGdb(Path(__file__).resolve().parent / "rag_data")


def get_glayout_context() -> str:
    """retrieve the context of syntax_data/GlayoutStrictSyntax.md
    to provide context of Glayout strictsyntax inserted in the prompt

    Returns:
        str: string content of GlayoutStrictSyntax.md
    """
    contextmdfile = (
        Path(__file__).resolve().parent / "syntax_data/GlayoutStrictSyntax.md"
    )
    loader = TextLoader(contextmdfile)
    return loader.load()[0].page_content


def get_prompt_from_template(
    tokenizer,
    ragcontext: str,
    prompt: str,
    strictsyntax: Optional[str] = None,
    return_message: bool=False
) -> str:
    """Generate a structured prompt for translating input text to Glayout strictsyntax.
    Will extract glayout NLPcontext from the get_glayout_context function.

    Args:
        tokenizer: a tokenizer compatible with huggingface, transformers tokenizer class
        ragcontext (str): Contextual information about analog circuit design to aid in translation.
        prompt (str): The input prompt that needs to be converted to Glayout strictsyntax.
        strictsyntax (str, Optional): The strictsyntax command language template to be used.
            if None (default), then only format the prompt (no labeled output strictsyntax)
        return_message (bool, Optional): if True, will not combine the prompt, rather it will return messages format

    Returns:
        str: The generated prompt formatted with the provided context and input data.
    """
    inst_prompt = str()
    glayout_nlp_context = get_glayout_context()
    inst_prompt += f"Below is some context on Glayout strictsyntax:\n{glayout_nlp_context}\n\n"
    #inst_prompt += "Below is context on the circuit"
    #inst_prompt += "convert an example prompt to Glayout strictsyntax\n"
    #inst_prompt += f"{ragcontext}\n\n----\nTRANSLATION TASK\n"
    #inst_prompt += f"Do NOT include the context in your response. Convert the following prompt to Glayout strictsyntax:\n{prompt}"
    inst_prompt += f"Glayout strictsyntax is a electronic circuit layout command language. Convert the following prompt to Glayout strictsyntax:\n{prompt}"
    # unify prompt and return
    messages = [{"role": "user", "content": inst_prompt}]
    # conditionally add label (expected strict syntax output)
    if strictsyntax is not None:
        messages.append({"role": "assistant", "content": strictsyntax})
    if return_message:
        return messages
    return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

# pass all prompts through rag before handing training data to llm
def unify_prompt_and_add_context_to_data(tokenizer, data: list, no_label: bool=False) -> list:
    """Enhance prmopts with vectordb contextual information
    constructs a new prompt incorporating this contextual information according to a specified template
    Args:
        tokenizer: a tokenizer compatible with huggingface, transformers tokenizer class
        data (list): A list of tuples, where each tuple is (prompt (str), result (str)) (or a list of prompts (str))
        no_label (bool): set this to true if you pass data in with JUST the prompt (no strictsyntax label)
    Returns:
        list[str]: A list of strings (prompt and strictsyntax have been combined)
    """
    glayout_context = get_glayout_context()
    if no_label:
        data = [(prompt, None) for prompt in data]
    contextualized_prompts = list()
    for prompt, result in data:
        docs = RAGvecdb.query(prompt, 1)
        ragdata = str()
        for doc in docs:
            # ragdata += f"[CONTEXT DOCUMENT NUMBER {i}]\n"
            ragdata += "\n" + doc + "\n"
            # ragdata += f"[/CONTEXT DOCUMENT NUMBER {i}]\n"
        newprompt = get_prompt_from_template(
            tokenizer=tokenizer,
            ragcontext=ragdata,
            prompt=prompt,
            strictsyntax=result
        )
        contextualized_prompts.append(newprompt)
    return contextualized_prompts


def load_preprocessed_data_in_messages_format():
    # get train and evaluation data in a single unified prompt format
    train_examples = load_all_labeled_syntax_data_json()
    eval_examples = load_all_labeled_syntax_data_json(True)
    # train
    train_messages = list()
    for prompt, result in train_examples:
        train_messages.append(get_prompt_from_template(None,None,prompt,result,True))
    train_data = Dataset.from_dict({"messages":train_messages})
    # eval
    eval_messages = list()
    for prompt, result in eval_examples:
        eval_messages.append(get_prompt_from_template(None,None,prompt,result,True))
    eval_data = Dataset.from_dict({"messages":eval_messages})
    return {"train": train_data, "evaluation": eval_data}




def load_preprocessed_pretokenized_data(tokenizer):
    """Wrapper function for full retrival and preprocessing of dataset
    1- Loads raw data from files
    2- adds RAG context to the LLM prompts
    3- unifies the prompt and strictsyntax output
    4- converts the dataset to Dataset type with example, input_ids, and attention_mask
    Args:
        tokenizer: LM tokenizer which follows hugging face tokenizer model
    Returns:
        dataset in the exact format needed for training
    """
    # get train and evaluation data in a single unified prompt format
    train_examples = unify_prompt_and_add_context_to_data(tokenizer, load_all_labeled_syntax_data_json())
    eval_examples = unify_prompt_and_add_context_to_data(tokenizer, load_all_labeled_syntax_data_json(True))
    # tokenize the prompts
    train_data = tokenizer(train_examples, padding=True)
    eval_data = tokenizer(eval_examples, padding=True)
    # use from dict method to convert to hugging face dataset
    train_data = Dataset.from_dict(
        {
            "example": train_examples,
            "input_ids": train_data.input_ids,
            "attention_mask": train_data.attention_mask,
        }
    )
    eval_data = Dataset.from_dict(
        {
            "example": eval_examples,
            "input_ids": eval_data.input_ids,
            "attention_mask": eval_data.attention_mask,
        }
    )
    # combine to create the final dataset
    return {"train": train_data, "evaluation": eval_data}
