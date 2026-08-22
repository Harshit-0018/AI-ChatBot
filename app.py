import streamlit as st
from groq import Groq
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AskAI", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main { background-color: #0e1117; }
section[data-testid="stSidebar"] { background-color: #161b22; }
.block-container {
    padding-top: 3rem !important;
    padding-left: 3rem !important;
    max-width: 100% !important;
}
.stChatMessage p { font-size: 1.15rem !important; }
.stChatMessage { border-radius: 16px; padding: 12px; margin-bottom: 10px; }
div[data-testid="stChatInput"] { margin-bottom: 20px; }
.user-profile {
    position: fixed; bottom: 20px; left: 20px; width: 280px;
    border-top: 1px solid #30363d; padding-top: 15px; z-index: 99;
    background-color: #161b22;
}
.model-card {
    background-color: #21262d; border: 1px solid #30363d;
    border-radius: 8px; padding: 15px; margin-top: 20px;
}
.rag-badge {
    background-color: #1f6feb22; border: 1px solid #1f6feb;
    border-radius: 8px; padding: 8px 12px; margin-top: 10px;
    font-size: 0.85rem; color: #58a6ff;
}
</style>
""", unsafe_allow_html=True)

# ---------------- EMBEDDING MODEL (cached, loads once) ----------------
@st.cache_resource
def load_embedder():
    return SentenceTransformer("all-MiniLM-L6-v2")

embedder = load_embedder()

# ---------------- RAG HELPERS ----------------
def extract_text_from_pdf(file) -> str:
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text + "\n"
    return text

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150):
    """Simple character-based chunking with overlap."""
    chunks = []
    start = 0
    text = text.strip()
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def build_index(chunks):
    """Embed all chunks and store as a numpy matrix."""
    embeddings = embedder.encode(chunks, normalize_embeddings=True)
    return np.array(embeddings)

def retrieve_relevant_chunks(query: str, chunks, embeddings, top_k: int = 4):
    if embeddings is None or len(chunks) == 0:
        return []
    query_emb = embedder.encode([query], normalize_embeddings=True)[0]
    scores = embeddings @ query_emb  # cosine similarity (vectors are normalized)
    top_idx = np.argsort(scores)[::-1][:top_k]
    return [chunks[i] for i in top_idx if scores[i] > 0.2]  # basic relevance floor

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your AI assistant. How can I help you today? 🚀"}
    ]

if "doc_chunks" not in st.session_state:
    st.session_state.doc_chunks = []

if "doc_embeddings" not in st.session_state:
    st.session_state.doc_embeddings = None

if "doc_name" not in st.session_state:
    st.session_state.doc_name = None

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## 🤖 AskAI")

    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your AI assistant. How can I help you today? 🚀"}
        ]
        st.rerun()

    st.markdown("---")
    st.markdown("### 📄 Chat with a PDF")
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

    if uploaded_file is not None and uploaded_file.name != st.session_state.doc_name:
        with st.spinner("Reading and indexing PDF..."):
            raw_text = extract_text_from_pdf(uploaded_file)
            chunks = chunk_text(raw_text)
            embeddings = build_index(chunks) if chunks else None
            st.session_state.doc_chunks = chunks
            st.session_state.doc_embeddings = embeddings
            st.session_state.doc_name = uploaded_file.name
        st.success(f"Indexed {len(chunks)} chunks from {uploaded_file.name}")

    if st.session_state.doc_name:
        st.markdown(
            f"""<div class="rag-badge">📎 Using: <b>{st.session_state.doc_name}</b></div>""",
            unsafe_allow_html=True
        )
        if st.button("🗑️ Remove document", use_container_width=True):
            st.session_state.doc_chunks = []
            st.session_state.doc_embeddings = None
            st.session_state.doc_name = None
            st.rerun()

    # Model Information
    st.markdown("""
    <div class="model-card">
        <p style="margin: 0; font-size: 0.9rem; color: #8b949e;">Active Model</p>
        <h4 style="margin: 5px 0 0 0; color: #58a6ff;">openai/gpt-oss-20b</h4>
        <p style="margin: 5px 0 0 0; font-size: 0.8rem; color: #8b949e;">Powered by Groq ⚡</p>
    </div>
    """, unsafe_allow_html=True)

    # BOTTOM SECTION
    st.markdown("""
    <div class="user-profile">
        <div style="font-weight: bold; font-size: 1rem; color: #ffffff;">👤 Harshit Singh</div>
        <div style="font-size: 0.85rem; color: #8b949e;">Free plan</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- MAIN SCREEN TITLE ----------------
st.markdown("<h2 style='text-align: left;'>🤖 AI Chatbot</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: left; color: #8b949e;'>Powered by Groq ⚡ &nbsp;|&nbsp; RAG-enabled 📄</p>", unsafe_allow_html=True)

# ---------------- CLIENT ----------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:
    avatar = "🧑" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ---------------- INPUT & LOGIC ----------------
user_input = st.chat_input("💬 Ask a follow-up...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):

            # --- RAG retrieval step ---
            context_blurb = ""
            if st.session_state.doc_chunks:
                relevant_chunks = retrieve_relevant_chunks(
                    user_input,
                    st.session_state.doc_chunks,
                    st.session_state.doc_embeddings,
                    top_k=4,
                )
                if relevant_chunks:
                    context_blurb = "\n\n".join(relevant_chunks)

            # Build the messages sent to Groq: system prompt (+ context) + chat history
            api_messages = []
            if context_blurb:
                api_messages.append({
                    "role": "system",
                    "content": (
                        "You are a helpful assistant. Use the following document excerpts "
                        "to answer the user's question when relevant. If the answer isn't "
                        "in the excerpts, say so and answer from general knowledge.\n\n"
                        f"--- DOCUMENT EXCERPTS ---\n{context_blurb}\n--- END EXCERPTS ---"
                    )
                })
            api_messages.extend(st.session_state.messages)

            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=api_messages
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})