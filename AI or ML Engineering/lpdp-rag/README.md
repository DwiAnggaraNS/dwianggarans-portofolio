## LPDP Scholarship RAG Assistant

Flask-based RAG (Retrieval Augmented Generation) assistant for LPDP scholarship information. Uses LangChain + ChromaDB for retrieval and Groq LLM for answer generation, with optional LangSmith monitoring.

## Features
- Simple RAG pipeline with Chroma vector store
- Groq LLM integration with graceful fallback when unavailable
- Chat UI with session-based history and rate limiting
- Admin endpoints: document upload and collection stats

## Project Structure

```
lpdp-rag/
├── app.py                 # Flask app factory + routes
├── config.py              # .env-backed configuration
├── core/                  # RAG chain and helpers
├── services/              # LLM + RAG service + monitoring
├── scripts/               # populate/depopulate utilities
├── data/
│   ├── documents/         # place PDFs/Docs here
│   └── chroma_db/         # vector DB storage
├── templates/             # Jinja templates (index, chat, errors)
├── static/                # CSS/JS assets
└── requirements.txt
```

## Requirements
- Python 3.10+
- Groq API key (for best answers). Works without it using simple text fallback.

## Setup (Windows PowerShell)
1) Create venv and install deps
```
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
```
2) Configure environment
```
Copy-Item .env.example .env
# Edit .env and set at least:
# GROQ_API_KEY=your_key_here            # optional but recommended
# CHROMA_DB_PATH=./data/chroma_db
# DOCUMENTS_PATH=./data/documents
```
3) Populate the knowledge base
```
python scripts/simple_populate.py
```
4) Run the app
```
python app.py
```
Open http://localhost:5000

## Core Routes
- GET `/` → landing page
- GET `/chat` → chat UI (initializes a session)
- POST `/chat` → ask a question; body: `{ "question": "..." }`
- GET `/chat/history` → session chat history
- POST `/chat/clear` → clear current session history
- GET `/about` → about page
- GET `/admin` → admin dashboard (template)
- GET `/admin/stats` → collection stats JSON
- POST `/admin/upload` → upload `.pdf|.txt|.docx` to index (multipart field `documents`)

Response payload example (POST /chat):
```
{
   "answer": "markdown text...",
   "sources": [{"title": "...", "url": "..."}],
   "confidence": 0.82,
   "needs_continuation": false,
   "session_id": "uuid",
   "metadata": {}
}
```

## Configuration (.env)
- GROQ_API_KEY: Groq API key (optional)
- GROQ_MODEL: default `llama3-8b-8192`
- CHROMA_DB_PATH: default `./data/chroma_db`
- CHROMA_COLLECTION_NAME: default `lpdp_docs`
- DOCUMENTS_PATH: default `./data/documents`
- MAX_INPUT_TOKENS, CHUNK_SIZE, CHUNK_OVERLAP: text splitting controls
- LANGCHAIN_API_KEY, LANGCHAIN_TRACING_V2, LANGCHAIN_PROJECT: optional LangSmith

## Data Sources
- Local PDFs/Docs: put files in `data/documents/` then run populate script
- Web pages: can be crawled by custom scripts (see services and scripts)

## Troubleshooting
- Chroma not found: `pip install chromadb --upgrade`
- Deep translator missing: `pip install deep-translator`
- Empty answers: check GROQ_API_KEY and ensure `data/chroma_db` is populated
- Rate limit message: wait 2 seconds between questions per session

## License
MIT