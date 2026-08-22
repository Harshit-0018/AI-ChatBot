# AI Chatbot (Groq + Streamlit)

An interactive AI chatbot built using Streamlit and powered by Groq’s ultra-fast LLMs (LLaMA 3.1).  
This application provides real-time conversational responses with a clean and modern chat interface.

---

## Live Demo

https://simple-chatbot-hwmg7tbp4vxr5mhfhjmfbk.streamlit.app/

---

## Features

- Ultra-fast responses using Groq API  
- Chat-style UI with message history  
- Secure API key handling using Streamlit Secrets  
- Deployed on Streamlit Cloud  
- Context-aware conversation (session memory)  

---

## Tech Stack

- Frontend/UI: Streamlit  
- Backend: Python  
- LLM API: Groq (LLaMA 3.1)  
- Deployment: Streamlit Cloud  

---

## Project Structure

```
simple-chatbot/
│
├── app.py                # Main Streamlit app
├── requirements.txt     # Dependencies
├── .gitignore           # Ignore secrets
└── .streamlit/
    └── secrets.toml     # API key (not pushed to GitHub)
```
## Architecture and Workflow

<img width="1536" height="1024" alt="ChatGPT Image Apr 23, 2026, 01_54_53 PM" src="https://github.com/user-attachments/assets/b9a7779a-e685-4558-b917-b9d1b3f1f176" />

---

## Installation (Run Locally)

### 1. Clone the repository

```
git clone https://github.com/YOUR_USERNAME/Simple-chatbot.git
cd Simple-chatbot
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Add your API key

Create the file:

```
.streamlit/secrets.toml
```

Add:

```
GROQ_API_KEY = "your_api_key_here"
```

### 4. Run the application

```
streamlit run app.py
```

---

## Environment Variables

| Variable     | Description       |
|--------------|------------------|
| GROQ_API_KEY | Your Groq API key |

---

## Future Improvements

- PDF-based Q&A (RAG system)  
- Long-term memory  
- Improved UI/UX  
- Multi-language support  

---

## Author

Harshit Singh
