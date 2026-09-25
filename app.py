# import sys
# sys.path.append("src")

# import streamlit as st
# from chatbot import build_chain, ask



# def escape_dollars(text):
#     return text.replace("$", "\\$")


# st.set_page_config(
#     page_title="Company RAG Chatbot",
#     page_icon="🤖"
# )

# st.title("🤖 Company Support Chatbot")


# @st.cache_resource
# def load_chain():
#     return build_chain()


# # Load RAG components
# vectordb, llm = load_chain()


# # Initialize session state
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "history" not in st.session_state:
#     st.session_state.history = []


# # Render chat history
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(escape_dollars(msg["content"]))

#         if msg["role"] == "assistant" and msg.get("sources"):
#             st.caption(
#                 f"📄 Sources: {', '.join(msg['sources'])}"
#             )


# # Chat input
# if question := st.chat_input(
#     "Ask about our products, pricing, policies..."
# ):

#     # Add user message
#     st.session_state.messages.append({
#         "role": "user",
#         "content": question
#     })

#     with st.chat_message("user"):
#         st.markdown(question)


#     # Generate answer
#     with st.chat_message("assistant"):
#         with st.spinner("Thinking..."):

#             answer, sources = ask(
#                 question,
#                 vectordb,
#                 llm,
#                 history=st.session_state.history
#             )

#             st.markdown(escape_dollars(answer))

#             if sources:
#                 st.caption(
#                     f"📄 Sources: {', '.join(sources)}"
#                 )


#     # Add assistant message
#     st.session_state.messages.append({
#         "role": "assistant",
#         "content": answer,
#         "sources": sources
#     })


#     # Add conversation to history
#     st.session_state.history.append({
#         "question": question,
#         "answer": answer
#     })


# # Sidebar
# with st.sidebar:

#     st.header("About")

#     st.write(
#         "RAG chatbot answering from 15 internal company PDFs."
#     )

#     if st.button("Clear chat"):

#         st.session_state.messages = []
#         st.session_state.history = []

#         st.rerun()


# ###################################################################################
########################################################################################
########################################################################################


# Multi Session

# import sys
# sys.path.append("src")

# import uuid
# import streamlit as st
# from chatbot import build_chain, ask

# st.set_page_config(page_title="Company RAG Chatbot", page_icon="🤖")


# def escape_dollars(text):
#     return text.replace("$", "\\$")


# @st.cache_resource
# def load_chain():
#     return build_chain()


# vectordb, llm = load_chain()

# # ---- Session state setup ----
# if "chats" not in st.session_state:
#     st.session_state.chats = {}  # {chat_id: {"title": str, "messages": [], "history": []}}
# if "active_chat" not in st.session_state:
#     st.session_state.active_chat = None


# def new_chat():
#     chat_id = str(uuid.uuid4())
#     st.session_state.chats[chat_id] = {
#         "title": "New Chat",
#         "messages": [],
#         "history": []
#     }
#     st.session_state.active_chat = chat_id


# def delete_chat(chat_id):
#     del st.session_state.chats[chat_id]
#     if st.session_state.active_chat == chat_id:
#         st.session_state.active_chat = next(iter(st.session_state.chats), None)


# # create a first chat if none exist
# if not st.session_state.chats:
#     new_chat()

# # ---- Sidebar ----
# with st.sidebar:
#     st.header("Chats")
#     if st.button("➕ New chat", use_container_width=True):
#         new_chat()
#         st.rerun()

#     st.divider()

#     for chat_id, chat in list(st.session_state.chats.items()):
#         col1, col2 = st.columns([4, 1])
#         with col1:
#             if st.button(chat["title"], key=f"select_{chat_id}", use_container_width=True):
#                 st.session_state.active_chat = chat_id
#                 st.rerun()
#         with col2:
#             if st.button("🗑", key=f"delete_{chat_id}"):
#                 delete_chat(chat_id)
#                 st.rerun()

#     st.divider()
#     st.caption("RAG chatbot answering from 15 internal company PDFs.")

# # ---- Main chat area ----
# active_id = st.session_state.active_chat
# chat = st.session_state.chats[active_id]

# st.title("🤖 Company Support Chatbot")

# for msg in chat["messages"]:
#     with st.chat_message(msg["role"]):
#         st.markdown(escape_dollars(msg["content"]))
#         if msg["role"] == "assistant" and msg.get("sources"):
#             st.caption(f"📄 Sources: {', '.join(msg['sources'])}")

# if question := st.chat_input("Ask about our products, pricing, policies..."):
#     chat["messages"].append({"role": "user", "content": question})
#     with st.chat_message("user"):
#         st.markdown(question)

#     with st.chat_message("assistant"):
#         with st.spinner("Thinking..."):
#             answer, sources = ask(question, vectordb, llm, history=chat["history"])
#             st.markdown(escape_dollars(answer))
#             if sources:
#                 st.caption(f"📄 Sources: {', '.join(sources)}")

#     chat["messages"].append({
#         "role": "assistant",
#         "content": answer,
#         "sources": sources
#     })
#     chat["history"].append({"question": question, "answer": answer})

#     # auto-title the chat from the first question
#     if chat["title"] == "New Chat":
#         chat["title"] = question[:40] + ("..." if len(question) > 40 else "")

#     st.rerun()

import sys
sys.path.append("src")

import streamlit as st
from chatbot import build_chain, ask

st.set_page_config(page_title="Company Support Chatbot", page_icon="🤖")
st.title("🤖 Company Support Chatbot")


def escape_dollars(text):
    return text.replace("$", "\\$")


@st.cache_resource
def load_chain():
    return build_chain()


vectordb, llm = load_chain()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []

# ---- Sidebar: just a reset button ----
with st.sidebar:
    st.caption("RAG chatbot answering from 15 internal company PDFs.")
    if st.button("🔄 Start over", use_container_width=True):
        st.session_state.messages = []
        st.session_state.history = []
        st.rerun()

# ---- Render conversation ----
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(escape_dollars(msg["content"]))
        if msg["role"] == "assistant" and msg.get("sources"):
            st.caption(f"📄 Sources: {', '.join(msg['sources'])}")

# ---- Chat input ----
if question := st.chat_input("Ask about our products, pricing, policies..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer, sources = ask(question, vectordb, llm, history=st.session_state.history)
            st.markdown(escape_dollars(answer))
            if sources:
                st.caption(f"📄 Sources: {', '.join(sources)}")

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources
    })
    st.session_state.history.append({"question": question, "answer": answer})