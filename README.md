# AI Chatbot (Groq + Streamlit + RAG)

An interactive AI chatbot built using Streamlit and powered by Groq's ultra-fast LLMs. Now supports **PDF-based Retrieval-Augmented Generation (RAG)** — upload a PDF and ask questions grounded in its content, alongside general conversation.


---

## Features

- Ultra-fast responses using the Groq API
- Chat-style UI with message history
- Chat with a PDF — upload a document and ask questions about it
- Local embedding-based retrieval (no external vector DB required)
- Structured, table-formatted answers when summarizing document content
- Secure API key handling using Streamlit Secrets
- Deployed on Streamlit Cloud
- Context-aware conversation (session memory)

---

## Tech Stack

- **Frontend/UI:** Streamlit
- **Backend:** Python
- **LLM API:** Groq (`openai/gpt-oss-20b`)
- **Embeddings:** `sentence-transformers` (`all-MiniLM-L6-v2`)
- **Similarity Search:** `numpy` (cosine similarity, in-memory)
- **PDF Parsing:** `pypdf`
- **Deployment:** Streamlit Cloud

---

## How RAG Works Here

1. **Upload** — a PDF is uploaded via the sidebar.
2. **Extract & Chunk** — text is pulled from the PDF and split into overlapping ~800-character chunks.
3. **Embed** — each chunk is embedded locally using `all-MiniLM-L6-v2` (no external API call needed).
4. **Retrieve** — on every question, the query is embedded and compared against chunk embeddings using cosine similarity to find the most relevant excerpts.
5. **Augment & Generate** — the top matching excerpts are injected into the system prompt sent to Groq, so the model answers using the document's content when relevant, and falls back to general knowledge when it isn't.

This keeps the app lightweight (no external vector database like Pinecone or Chroma) while still providing grounded, document-aware answers.

---

## Screenshots

### Chatting normally (no document loaded)

<img width="1919" height="948" alt="image" src="https://github.com/user-attachments/assets/793c8c2c-b745-4487-b254-84e15f984a92" />


### PDF uploaded and indexed — asking about its content

<img width="1918" height="946" alt="image" src="https://github.com/user-attachments/assets/0798db37-db02-4e91-ac4c-3c3db263f229" />


### Answer generated as a structured table, grounded in the uploaded PDF

<img width="1918" height="938" alt="image" src="https://github.com/user-attachments/assets/d5371611-6d76-4a0f-b2d0-16be6aa816bd" />


### Follow-up question outside the document's scope

The model correctly notes the excerpts don't cover the topic, then answers from general knowledge instead of making something up.

<img width="1919" height="946" alt="image" src="https://github.com/user-attachments/assets/a6e770a8-157b-469a-9cc3-1265a92256be" />


---

## Project Structure

```
AI-ChatBot/
│
├── app.py                # Main Streamlit app (chat + RAG logic)
├── requirements.txt      # Dependencies
├── style.css              # Custom UI styling
├── .gitignore             # Ignore secrets
└── .streamlit/
    └── secrets.toml       # API key (not pushed to GitHub)
```

---

## Installation (Run Locally)

### 1. Clone the repository

```bash
git clone https://github.com/Harshit-0018/AI-ChatBot.git
cd AI-ChatBot
```

### 2. Install dependencies

```bash
py -m pip install -r requirements.txt
```

### 3. Add your API key

Create the folder and file:

```
.streamlit/secrets.toml
```

Add the following line inside it:

```toml
GROQ_API_KEY = "your_api_key_here"
```

Get a free key from [console.groq.com](https://console.groq.com) → API Keys → Create API Key.

### 4. Run the application

```bash
py -m streamlit run app.py
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key |

---

## Notes

- Groq periodically deprecates older models — if you hit a `model_not_found` error, check [console.groq.com/docs/models](https://console.groq.com/docs/models) for the current active model and update the `model=` value in `app.py`.
- `secrets.toml` is intentionally excluded from version control via `.gitignore`. Never commit API keys.
- Retrieval currently returns the top 4 most relevant chunks per query; this can be tuned via the `top_k` parameter inside `app.py`.

---

## Future Improvements

- Long-term memory across sessions
- Multi-document support
- Improved UI/UX
- Multi-language support

---

## Author

**Harshit Singh**
