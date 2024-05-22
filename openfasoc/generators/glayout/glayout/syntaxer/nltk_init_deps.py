import nltk


def check_and_download_nltk_data(data_name):
    """
    Check if an NLTK dataset is downloaded, and download it if it is not.

    Args:
        data_name (str): The name of the NLTK dataset to check and download.
    """
    try:
        nltk.data.find(f"tokenizers/{data_name}")
    except LookupError:
        print(f"{data_name} is not downloaded. Downloading now...")
        nltk.download(data_name)
        print(f"{data_name} has been downloaded.")


check_and_download_nltk_data("punkt")
