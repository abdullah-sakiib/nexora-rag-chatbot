from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from config import VECTORSTORE_DIR, EMBEDDING_MODEL

# SCORE_THRESHOLD = 0.75  # lower distance = more similar; tune after testing
K = 6                    # fetch more, then filter down


def load_vectordb():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return Chroma(persist_directory=VECTORSTORE_DIR, embedding_function=embeddings)


def retrieve_relevant(vectordb, question, k=4, fetch_k=15, lambda_mult=0.5):
    """
    k: number of chunks to return
    fetch_k: pool size to select from before diversifying
    lambda_mult: 0 = max diversity, 1 = max relevance (0.5 = balanced)
    """
    docs = vectordb.max_marginal_relevance_search(
        question,
        k=k,
        fetch_k=fetch_k,
        lambda_mult=lambda_mult
    )
    return docs