import streamlit as st
from sentence_transformers import SentenceTransformer

from search import search
from rag import generate_answer
from rewrite import rewrite_query
from pdf_processor import process_pdf
from embeddings import create_embeddings


# ---------------- PAGE SETUP ----------------

st.set_page_config(
    page_title="AI Document Chat",
    page_icon="📄",
    layout="wide"
)

# ---------------- TITLE ----------------

st.title("📄 AI Document Chat")
st.write("Chat with your PDF using local AI (Ollama)")

# ---------------- PDF UPLOAD ----------------

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

# ---------------- PROCESS PDF ----------------

if uploaded_file:

    with st.spinner("Processing PDF..."):

        chunks = process_pdf(uploaded_file)

        embeddings = create_embeddings(chunks)

    st.success("PDF processed successfully!")

else:

    st.warning("Please upload a PDF first.")
    st.stop()

# ---------------- LOAD EMBEDDING MODEL ----------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

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

# ---------------- USER ASKED QUESTION ----------------

if user_question:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    # Display user message
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

            # -------- SEARCH --------

            results = search(
                rewritten_question,
                model,
                chunks,
                embeddings
            )

            # -------- GENERATE ANSWER --------

            answer = generate_answer(
                user_question,
                results
            )

            # -------- SHOW ANSWER --------

            st.markdown(answer)

    # Save assistant message

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
# from pdf_processor import process_pdf
# from embeddings import create_embeddings

# # ---------------- PAGE SETUP ----------------

# st.set_page_config(
#     page_title="AI Document Chat",
#     page_icon="📄",
#     layout="wide"
# )

# # ---------------- TITLE ----------------

# st.title("📄 AI Document Chat")
# st.write("Chat with your PDF using local AI (Ollama)")
# uploaded_file = st.file_uploader(
#     "Upload a PDF",
#     type=["pdf"]
# )

# # ---------------- LOAD DATA ----------------

# # with open("data.pkl", "rb") as f: old
# #     chunks, embeddings = pickle.load(f)old


# if uploaded_file:

#     with st.spinner("Processing PDF..."):

#         chunks = process_pdf(uploaded_file)

#         embeddings = create_embeddings(chunks)

#     st.success("PDF processed successfully!")

# # ---------------- LOAD EMBEDDING MODEL ----------------

# model = SentenceTransformer("all-MiniLM-L6-v2")

# # ---------------- CHAT MEMORY ----------------

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # ---------------- DISPLAY OLD CHAT ----------------

# for message in st.session_state.messages:

#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # ---------------- CHAT INPUT ----------------

# user_question = st.chat_input(
#     "Ask anything from your PDF..."
# )

# # ---------------- WHEN USER ASKS QUESTION ----------------

# if user_question:

#     # Save user message
#     st.session_state.messages.append(
#         {
#             "role": "user",
#             "content": user_question
#         }
#     )

#     # Show user message
#     with st.chat_message("user"):
#         st.markdown(user_question)

#     # Assistant response
#     with st.chat_message("assistant"):

#         with st.spinner("Thinking..."):

#             # -------- QUERY REWRITING --------

#             rewritten_question = rewrite_query(
#                 user_question,
#                 st.session_state.messages
#             )

#             # Show rewritten query
#             st.write(
#                 "### Rewritten Query:"
#             )

#             st.info(rewritten_question)

#             # -------- SEMANTIC SEARCH --------

#             results = search(
#                 rewritten_question,
#                 model,
#                 chunks,
#                 embeddings
#             )

#             # -------- SHOW RETRIEVED CHUNKS --------

#             st.write(
#                 "### Retrieved Chunks:"
#             )

#             st.write(results)

#             # -------- GENERATE FINAL ANSWER --------

#             answer = generate_answer(
#                 user_question,
#                 results
#             )

#             # -------- SHOW ANSWER --------

#             st.markdown(answer)

#     # Save assistant reply
#     st.session_state.messages.append(
#         {
#             "role": "assistant",
#             "content": answer
#         }
#     )
