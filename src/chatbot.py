from retriever import load_vectordb, retrieve_relevant
from llm import get_llm

SYSTEM_PROMPT = """You are a helpful support assistant for our company.At first of the conversation if the user greets then greet back.
Answer using the provided context below.

Rules:
- Be direct and concise. Do not add disclaimers unless the context truly lacks the answer.
- If the context fully answers the question, answer confidently without hedging.
- If the context partially answers it, answer what you can and note only the specific gap.
- If the context has nothing relevant, say so and suggest contacting support.
- Do NOT include inline "Source:" citations in your answer — sources are shown separately.

Context:
{context}
"""

MAX_HISTORY_TURNS = 5


def build_chain():
    vectordb = load_vectordb()
    llm = get_llm()
    return vectordb, llm


def format_context(docs):
    parts = []
    for d in docs:
        src = d.metadata.get("source")
        page = d.metadata.get("page", "?")
        parts.append(f"[{src}, page {page}]\n{d.page_content}")
    return "\n\n---\n\n".join(parts)


def format_sources(docs):
    seen = set()
    sources = []
    for d in docs:
        src = d.metadata.get("source")
        page = d.metadata.get("page", "?")
        key = (src, page)
        if key not in seen:
            seen.add(key)
            sources.append(f"{src} (p.{page})")
    return sources

CONTEXTUALIZE_PROMPT = """Given the conversation history and a follow-up question,
rewrite the follow-up into a standalone question that includes all necessary context.
If the follow-up is already standalone, return it unchanged.
Only output the rewritten question, nothing else.

History:
{history}

Follow-up question: {question}
Standalone question:"""


def contextualize_question(question, history, llm):
    if not history:
        return question
    hist_text = "\n".join(f"Q: {h['question']}\nA: {h['answer']}" for h in history[-3:])
    prompt = CONTEXTUALIZE_PROMPT.format(history=hist_text, question=question)
    response = llm.invoke([("human", prompt)])
    return response.content.strip()


def ask(question, vectordb, llm, history=None):
    search_query = contextualize_question(question, history, llm)
    docs = retrieve_relevant(vectordb, search_query)
    context = format_context(docs)
    prompt = SYSTEM_PROMPT.format(context=context)

    messages = [("system", prompt)]
    if history:
        for turn in history[-MAX_HISTORY_TURNS:]:
            messages.append(("human", turn["question"]))
            messages.append(("ai", turn["answer"]))
    messages.append(("human", question))  # original question, not rewritten, for natural reply

    response = llm.invoke(messages)
    sources = format_sources(docs)
    return response.content, sources

# def ask(question, vectordb, llm, history=None):
#     docs = retrieve_relevant(vectordb, question)
#     context = format_context(docs)
#     prompt = SYSTEM_PROMPT.format(context=context)

#     messages = [("system", prompt)]
#     if history:
#         for turn in history[-MAX_HISTORY_TURNS:]:
#             messages.append(("human", turn["question"]))
#             messages.append(("ai", turn["answer"]))
#     messages.append(("human", question))

#     response = llm.invoke(messages)
#     sources = format_sources(docs)
#     return response.content, sources