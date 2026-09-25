# 🤖 Nexora RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers questions using a company's internal knowledge base (15 PDF documents covering products, pricing, policies, support, and more). Built with LangChain, ChromaDB, and Claude (Anthropic), served through a Streamlit UI.

## Features

- **Retrieval-Augmented Generation** — answers grounded in your own PDFs, not the model's general knowledge
- **MMR (Maximal Marginal Relevance) retrieval** — reduces redundant/overlapping context chunks
- **Conversational memory** — follow-up questions ("does that include support?") are automatically contextualized against prior turns before retrieval
- **Source citations** — every answer shows which PDF(s) and page(s) it drew from
- **Simple, public-friendly UI** — no login required; single ongoing conversation with a "Start over" reset

## Project Structure

```
rag_chatbot/
├── data/
│   └── pdfs/                  # company knowledge base (15 PDFs)
├── src/
│   ├── ingest.py               # load PDFs, chunk, embed, store in vector DB
│   ├── retriever.py            # MMR-based retrieval from the vector store
│   ├── llm.py                  # Claude API wrapper
│   ├── chatbot.py               # RAG pipeline: contextualize → retrieve → generate
│   └── config.py                # paths, model names, chunk size, etc.
├── vectorstore/                 # persisted Chroma vector DB (generated, gitignored)
├── app.py                       # Streamlit chat UI
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/abdullah-sakiib/nexora-rag-chatbot.git
   cd nexora-rag-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   Copy `.env.example` to `.env` and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_key_here
   ```

4. **Add your PDFs**

   Place your PDF files in `data/pdfs/`.

5. **Build the vector store**
   ```bash
   python src/ingest.py
   ```
   Re-run this any time PDFs are added, removed, or edited.

6. **Run the app**
   ```bash
   streamlit run app.py
   ```

## How it works

1. **Ingestion** (`ingest.py`) — PDFs are loaded, split into overlapping chunks, embedded with a local HuggingFace model (`all-MiniLM-L6-v2`), and stored in a local ChromaDB vector store.
2. **Query contextualization** (`chatbot.py`) — follow-up questions are rewritten into standalone questions using conversation history before retrieval, so the vector search understands what "that" or "it" refers to.
3. **Retrieval** (`retriever.py`) — relevant chunks are pulled from the vector store using MMR search, balancing relevance and diversity.
4. **Generation** (`llm.py`, `chatbot.py`) — Claude generates an answer strictly from the retrieved context, with source citations returned separately from the answer text.

## Tech Stack

- [LangChain](https://www.langchain.com/) — orchestration
- [ChromaDB](https://www.trychroma.com/) — vector store
- [Claude (Anthropic)](https://www.anthropic.com/) — generation
- [Sentence-Transformers](https://www.sbert.net/) — embeddings
- [Streamlit](https://streamlit.io/) — UI

## Notes

- This app does not require user login — it's designed for public-facing support use, with a single in-memory conversation per browser session.
- The vector store is excluded from version control; run `ingest.py` locally to regenerate it after cloning.
