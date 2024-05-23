import json
import warnings
from pathlib import Path
from typing import List, Tuple, Union
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from datasets import Dataset


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
                nlp_text = nlp_file.read()
            results.append((llm_prompt, nlp_text))
        except (FileNotFoundError, KeyError) as faulty_example_error:
            if fail_on_error:
                raise faulty_example_error
            print(f"\n\nan exception was encounterd when processing {example}\n")
            warnings.warn(f"{faulty_example_error}")
    return results


def load_all_labeled_syntax_data_json(test: bool = False) -> List[Tuple[str, str]]:
    """look in syntax_data folder for any json files
    and run load_labeled_syntax_data_json on those files
    Args:
        test (bool, Optional): if True, only load json files containing keyword "test", default False
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
        test_in_name = "test" in json_file_path.name
        if test and test_in_name:  # load test data and test is in name of this json
            all_results.extend(
                load_labeled_syntax_data_json(json_file_path, convo_dir, False)
            )
        elif not (
            test or test_in_name
        ):  # dont load test data and test is not in name of this json
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

    def query(self, query_text: str, k: int = 4):
        """
        Queries the vector database to find the top-k most similar vectors to the given query text.
        Args:
            query_text (str): The text to query.
        Returns:
            List: The list of top-k most similar docs.
        """
        rawdocs = self.vectordb.similarity_search(query=query_text, k=k)
        rawtxt = list()
        for doc in rawdocs:
            rawtxt.append(doc.page_content)
        return rawtxt


RAGvecdb = RAGdb(Path(__file__).resolve().parent / "rag_data")


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


def pre_tokenize_dataset(tokenizer, data: list) -> dict:
    """tokenize both the prompts and expected responses
    Args:
        tokenizer (_type_): LM tokenizer which follows hugging face tokenizer model
        data (list): A list of tuples, where each tuple is (prompt (str), result (str))
    Returns:
        dict: {"prompt": list of tokenized prompts, "strictsyntax": list of tokenized responses}
    """
    tokenized_prompts = list()
    tokenized_responses = list()
    for prompt, response in data:
        tokenized_prompt = tokenizer(prompt, return_tensors="pt")
        tokenized_response = tokenizer(response, return_tensors="pt")
        tokenized_prompts.append(tokenized_prompt)
        tokenized_responses.append(tokenized_response)
    return {"prompt": tokenized_prompts, "strictsyntax": tokenized_responses}


def load_preprocessed_pretokenized_data(tokenizer):
    """Wrapper function for full retrival and preprocessing of dataset
    1- Loads raw data from files
    2- adds RAG context to the LLM prompts
    3- converts the dataset to Arrow
    Args:
        tokenizer: LM tokenizer which follows hugging face tokenizer model
    Returns:
        dataset in the exact format needed for training
    """
    # get train and testing data in dictionary {prompt: list, strictsyntax: list} form
    train_data = pre_tokenize_dataset(
        tokenizer, add_context_to_data(load_all_labeled_syntax_data_json())
    )
    test_data = pre_tokenize_dataset(
        tokenizer, add_context_to_data(load_all_labeled_syntax_data_json(True))
    )
    # use from dict method to convert to hugging face dataset
    train_data = Dataset.from_dict(train_data)
    test_data = Dataset.from_dict(test_data)
    # combine to create the final dataset
    return {"train": train_data, "test": test_data}
