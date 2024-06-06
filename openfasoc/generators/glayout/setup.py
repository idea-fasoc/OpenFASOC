from setuptools import setup, find_packages


setup(
    name="glayout",
    version="0.0.7",
    author="Ali Hammoud, Harsh Khandeparkar, Vijay Shankar, Chetanya Goyal, Sakib Pathen, Arlene Dai, Ryan Wans, Mehdi Saligane",
    author_email="alibilal@umich.edu, Harsh, vijayshankar.renganathan@analog.com, Chetanya, spathen@umich.edu, arlendai@umich.edu, Ryan, mehdi@umich.edu",
    description="A human language to analog layout API with support for different technologies.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/idea-fasoc/OpenFASOC/tree/main/openfasoc/generators/glayout",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "gdsfactory==7.7.0",
        "prettyprint",
        "prettyprinttree",
        "nltk"
    ],
    extras_require={
        "llm": [
            "torch",
            "transformers",
            "langchain",
            "langchain_community",
            "chromadb",
            "ollama",
            "unstructured",
            "unstructured[md]",
            "sentence-transformers",
            "peft",
            "accelerate",
            "bitsandbytes",
            "safetensors",
            "datasets",
            "auto-gptq",
            "optimum",
            "trl",
            "langchain_huggingface",
            "tensorboard"
        ]
    },
    entry_points={
        "console_scripts": [
            # "glayout = something:run"# Define any command line scripts here
        ],
    },
)
