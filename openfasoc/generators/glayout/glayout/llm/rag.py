from pathlib import Path
from typing import List, Tuple, Union
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import Chroma
#from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
#from sentence_transformers import SentenceTransformer
from langchain_core.documents import Document
import glayout.syntaxer.nltk_init_deps
from typing import Callable


class RAGdb:
    """
    A class to create and manage a vector database for the RAG data using ChromaDB.

    Attributes:
        chroma_client (Client): The ChromaDB client used for managing the vector database.
        collection_name (str): The name of the collection used in ChromaDB.
        collection (Collection): The vector database
    """

    def __init__(self, rag_data_dir: Union[str, Path], minimum_similarity: float=1.35):
        """Initializes the RAGdb instance with a ChromaDB collection
        takes a rag_data_dir (to read documents from) and a minimum_similarity value
        documents with similarities below minimum_similarity will be ignored
        """
        self.summarizer: Callable[[str], str] = lambda query : query
        self.minimum_similarity = float(minimum_similarity)
        # error checking
        rag_data_dir = Path(rag_data_dir).resolve()
        if not rag_data_dir.is_dir():
            raise FileNotFoundError(f"could not find RAG data directory {rag_data_dir}")
        # load RAG data
        langchain_documents = DirectoryLoader(str(rag_data_dir), glob="*.md").load()
        document_labels = [self._get_document_label(lddoc) for lddoc in langchain_documents]
        self.documents = dict(zip(document_labels, langchain_documents))
        # create vector db and set collection_metadata to configure the distance similarity metric
        # the default similarity metric is l2 norm
        embeddings_model_name = "sentence-transformers/all-MiniLM-L6-v2"
        #embeddings_model_name = "PotatoOff/mxbai-embed-large-safetensors"
        embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
        #embeddings_model_name = "Alibaba-NLP/gte-large-en-v1.5"
        #embeddings = SentenceTransformer(embeddings_model_name,trust_remote_code=True)
        #collection_metadata = {"hnsw:space": "cosine"}
        collection_metadata = {"hnsw:space": "l2"}# lower is better
        #self.vectordb = Chroma.from_documents(
        #    documents=document_labels, embedding=embeddings, collection_metadata=collection_metadata
        #)
        self.vectordb = Chroma.from_texts(
            texts=document_labels, embedding=embeddings, collection_metadata=collection_metadata
        )

    def _get_document_label(self, langchain_doc: Document) -> str:
        """returns the document label given an input langchain document
        Args:
            langchain_doc (langchain_core.documents.base.Document): A langchain document type
                this should contain the document text and a metadata attribute with a source
        Returns:
            str: the document label for this document (used to search for this doc in rag)
        """
        # returns the first line of the document
        # if the first line is empty, returns the document name
        label = str(langchain_doc.page_content.split('\n')[0])
        label = label.strip().strip("#").strip()
        if len(label)==0 or label.isspace():
            label = Path(langchain_doc.metadata["source"]).resolve().stem
        return label

    def query(self, query_text: str, k: int = 1) -> list:
        """
        Queries the vector database to find the top-k most similar vectors to the given query text.
        Args:
            query_text (str): The text to query.
            k (int): number of documents to query
        Returns:
            List: The list of at most top-k most similar docs. (always returns a list even if k=1)
                    NOTE: if similarity is below a threshold, it will ignore documents
                    NOTE: if final list is length 0, it will return a list with "None" as the only element
        Raises
            ValueError: less than one document queried (k<1)
        """
        # error checking
        k = int(k)
        if k<1:
            raise ValueError("you must query for at least one document")
        # preprocess the query
        preproc_query = self.summarizer(query_text)
        # query the vec db
        #dbresult_doc_labels = self.vectordb.similarity_search(query=query_text, k=k)
        #import pdb; pdb.set_trace()
        dbresult_doc_labels = self.vectordb.similarity_search_with_score(query=preproc_query, k=k)
        rawtxt = list()
        for i, (doc,similarity) in enumerate(dbresult_doc_labels):
            if similarity < self.minimum_similarity:# for l2 lower is better, if similarity is cosine then higher is better
                rawtxt.append(self.documents[doc.page_content].page_content)
                with open("RAGoutputs_example_dumpfile.txt", "a") as afile:
                    text_to_append = "\n\nquery_text: "+query_text
                    text_to_append += "\nprocessed query_text: "+preproc_query
                    text_to_append += "\nsimilarity: "+str(similarity)+"\n"
                    text_to_append += f"choosen file: {doc.page_content}"
                    #text_to_append += f"content: {rawtxt[-1]}\n"
                    #afile.write(text_to_append)
        # if no results then return a list with "None" as the only element
        if len(rawtxt)==0:
            return [None]
        else:
            return rawtxt

