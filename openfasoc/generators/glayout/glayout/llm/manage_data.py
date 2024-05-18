import json
from pathlib import Path
from typing import Union


def load_labeled_syntax_data_json(json_file_path: Union[str, Path]) -> list[tuple]:
    """Load all labeled data examples from a JSON file by reading LLM prompt
    and extracting strict syntax from corresponding '.convo' files.
    Args:
        json_file_path (str or Path): The path to the JSON file.
    Raises:
        FileNotFoundError: If a '.convo' file corresponding to an example is not found.
    Returns:
        list of tuple: A list of tuples containing information about each example.
            Each tuple consists of:
                - str: The LLM prompt.
                - str: The text found in the NLP file.
    """
    # this requires manage_data.py to be in the llm folder
    # Load JSON data
    json_file_path = Path(json_file_path).resolve()
    if not json_file_path.is_file():
        raise FileNotFoundError(f"could not find JSON file {json_file_path}")
    with open(json_file_path, "r") as file:
        data = json.load(file)
    examples = data.get("data")
    if examples is None:
        raise KeyError(f"data not found in JSON file {json_file_path}, ensure 'data' keyword is used")
    # loop through examples and append to results
    results = list()
    for example in examples:
        llm_prompt = example.get("LLMprompt")
        if llm_prompt is None:
            raise KeyError(f"LLMprompt not found in JSON data {example}")
        # get the strict syntax convo corresponding to this example
        nlp_filename = example.get("NLPfilename")
        if nlp_filename is None:
            raise KeyError(f"NLPfilename not found in JSON data {example}")
        convo_filename = f"{nlp_filename.strip()}.convo"
        # Check if the .convo file exists
        convo_file_path = Path(convo_filename).resolve()
        if not convo_file_path.is_file():
            raise FileNotFoundError(f"Convo file '{convo_file_path}' not found.")
        # Read text from convo file
        with convo_file_path.open("r") as nlp_file:
            nlp_text = nlp_file.read()
        results.append((llm_prompt, nlp_text))
    return results

def load_all_labeled_syntax_data_json() -> list[tuple]:
    """look in syntax_data/llm folder for any json files
    and run load_labeled_syntax_data_json on those files
    Returns:
        list[tuple]: all results from running load_labeled_syntax_data_json on all json files
    """
    # Path to the directory containing JSON files
    llm_dir = Path(__file__).resolve()
    json_dir = llm_dir / "syntax_data/llm"
    if not json_dir.is_dir():
        raise FileNotFoundError("Could not find syntax_data/llm directory within llm subpackage of glayout")
    # Iterate over all JSON files in the directory
    all_results = list()
    for json_file_path in json_dir.glob("*.json"):
        all_results.extend(load_labeled_syntax_data_json(json_file_path))
    return all_results

# Example usage:
print(*load_all_labeled_syntax_data_json(),sep="\n")

# def create_RAG_db():
#
