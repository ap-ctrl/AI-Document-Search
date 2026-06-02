import streamlit as st
import pickle
from sentence_transformers import SentenceTransformer
from search import search
from rag import generate_answer
from rewrite import rewrite_query

# ---------------- PAGE SETUP ----------------

st.set_page_config(
    page_title="AI Document Chat",
    page_icon="📄",
    layout="wide"
)

# ---------------- TITLE ----------------

st.title("📄 AI Document Chat")
st.write("Chat with your PDF using local AI (Ollama)")

# ---------------- LOAD DATA ----------------

with open("data.pkl", "rb") as f:
    chunks, embeddings = pickle.load(f)

# ---------------- LOAD EMBEDDING MODEL ----------------

model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------- CHAT MEMORY ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- DISPLAY OLD CHAT ----------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- CHAT INPUT ----------------

user_question = st.chat_input(
    "Ask anything from your PDF..."
)

# ---------------- WHEN USER ASKS QUESTION ----------------

if user_question:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_question)

    # Assistant response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            # -------- QUERY REWRITING --------

            rewritten_question = rewrite_query(
                user_question,
                st.session_state.messages
            )

            # Show rewritten query
            st.write(
                "### Rewritten Query:"
            )

            st.info(rewritten_question)

            # -------- SEMANTIC SEARCH --------

            results = search(
                rewritten_question,
                model,
                chunks,
                embeddings
            )

            # -------- SHOW RETRIEVED CHUNKS --------

            st.write(
                "### Retrieved Chunks:"
            )

            st.write(results)

            # -------- GENERATE FINAL ANSWER --------

            answer = generate_answer(
                user_question,
                results
            )

            # -------- SHOW ANSWER --------

            st.markdown(answer)

    # Save assistant reply
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
# import streamlit as st
# import pickle
# from sentence_transformers import SentenceTransformer
# from search import search
# from rag import generate_answer
# from rewrite import rewrite_query

# # Page setup
# st.set_page_config(
#     page_title="AI Document Chat",
#     page_icon="📄",
#     layout="wide"
# )

# # Title
# st.title("📄 AI Document Chat")
# st.write("Chat with your PDF using local AI (Ollama)")

# # Load PDF knowledge
# with open("data.pkl", "rb") as f:
#     chunks, embeddings = pickle.load(f)

# # Load embedding model
# model = SentenceTransformer("all-MiniLM-L6-v2")

# # Create chat memory
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Show old chat messages
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # Chat input
# user_question = st.chat_input("Ask anything from your PDF...")

# # When user sends message
# if user_question:

#     # Save user message
#     st.session_state.messages.append(
#         {"role": "user", "content": user_question}
#     )

#     # Show user message
#     with st.chat_message("user"):
#         st.markdown(user_question)

#     # Assistant response
#     with st.chat_message("assistant"):

#         with st.spinner("Thinking..."):

#             # Build conversation memory
#             conversation_context = ""

#             # Take recent messages
#             for msg in st.session_state.messages[-4:]:
#                 conversation_context += msg["content"] + " "

#             # Add latest question
#             conversation_context += user_question

#             # Semantic search
#             results = search(
#                 conversation_context,
#                 model,
#                 chunks,
#                 embeddings
#             )

#             # Debug retrieved chunks
#             st.write(results)

#             # Generate answer
#             answer = generate_answer(
#                 user_question,
#                 results
#             )

#             # Show answer
#             st.markdown(answer)

#     # Save assistant reply
#     st.session_state.messages.append(
#         {"role": "assistant", "content": answer}
#     )

