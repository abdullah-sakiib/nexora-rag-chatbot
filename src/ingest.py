import os
from langchain_community.document_loaders import PyPDFLoader
# Use this instead
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from config import PDF_DIR, VECTORSTORE_DIR, EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP


def load_documents():
    docs = []
    for fname in os.listdir(PDF_DIR):
        if fname.endswith(".pdf"):
            path = os.path.join(PDF_DIR, fname)
            loader = PyPDFLoader(path)
            pages = loader.load()
            for p in pages:
                p.metadata["source"] = fname
            docs.extend(pages)
    return docs


def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""]  # respects paragraphs/sentences first
    )
    return splitter.split_documents(docs)


def build_vectorstore():
    docs = load_documents()
    chunks = split_documents(docs)
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectordb = Chroma.from_documents(
        chunks,
        embedding=embeddings,
        persist_directory=VECTORSTORE_DIR
    )
    vectordb.persist()
    print(f"Ingested {len(chunks)} chunks from {len(set(d.metadata['source'] for d in docs))} PDFs.")
    return vectordb


if __name__ == "__main__":
    build_vectorstore()