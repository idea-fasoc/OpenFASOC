import json
import warnings
from pathlib import Path
from typing import List, Tuple, Union
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


def get_glayout_context() -> str:
    contextmdfile = Path(__file__).resolve().parent / "syntax_data/GlayoutStrictSyntax.md"
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


def load_all_labeled_syntax_data_json() -> List[Tuple[str, str]]:
    """look in syntax_data folder for any json files
    and run load_labeled_syntax_data_json on those files
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
        all_results.extend(load_labeled_syntax_data_json(json_file_path, convo_dir, False))
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
        self.vectordb = Chroma.from_documents(documents=self.documents,embedding=embeddings)


    def query(self, query_text: str, k: int=4):
        """
        Queries the vector database to find the top-k most similar vectors to the given query text.
        Args:
            query_text (str): The text to query.
        Returns:
            List: The list of top-k most similar docs.
        """
        rawdocs =  self.vectordb.similarity_search(query=query_text,k=k)
        rawtxt = list()
        for doc in rawdocs:
            rawtxt.append(doc.page_content)
        return rawtxt

RAGvecdb = RAGdb(Path(__file__).resolve().parent / "rag_data")
#print(vecdb.query("currentmir"))