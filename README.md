# Technical Interview Preparation Assistant

A fully local RAG (Retrieval-Augmented Generation) system for technical interview preparation. This system answers questions using only your course materials, provides explicit citations, and includes a verification layer to ensure answer faithfulness.

## ✨ Features

- **Fully Local**: No cloud APIs, no external dependencies, complete privacy
- **Multi-Format Support**: PDF, DOCX, TXT, MD files
- **Smart Retrieval**: FAISS vector search with metadata filtering
- **Citation Required**: Every answer includes explicit source citations
- **Verification Layer**: Faithfulness checking with configurable thresholds
- **Refusal When Uncertain**: System refuses to answer when information isn't in materials
- **Evaluation Tools**: Recall@K and citation accuracy scripts included

## 🏗️ Architecture

```
Backend (Python/FastAPI)
├── Document Ingestion (PDF, DOCX, TXT, MD)
├── Intelligent Chunking (section-aware, configurable)
├── Embedding Generation (SentenceTransformers)
├── Vector Search (FAISS)
├── LLM Generation (Ollama - local)
├── Verification Layer (faithfulness checking)
└── SQLite Database (metadata & logs)

Frontend (React/Vite)
├── Ask Page (query with filters)
├── Materials Browser (upload/manage)
└── Verification View (detailed reports)
```

## 📋 Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **OpenRouter API Key** (get one at https://openrouter.ai/)
- 4GB+ RAM recommended

## 🚀 Installation

### 1. Get OpenRouter API Key

1. Sign up at https://openrouter.ai/
2. Get your API key from the dashboard
3. Add credits to your account (pay-as-you-go)

### 2. Configure API Key

Edit `backend/config.py`:

```python
OPENROUTER_API_KEY = "your-api-key-here"
OPENROUTER_MODEL = "anthropic/claude-3.5-sonnet"  # or another model
```

### 3. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

## ▶️ Running the Application

### Start Backend

```bash
cd backend
source venv/bin/activate
python main.py
```

Backend will run on `http://localhost:8000`

### Start Frontend

```bash
cd frontend
npm run dev
```

Frontend will run on `http://localhost:5173`

## 📖 Usage

### 1. Upload Materials

1. Navigate to the **Materials** tab
2. Click **Upload Material**
3. Select your file (PDF, DOCX, TXT, or MD)
4. Enter material type (lecture, textbook, notes, assignment, lab, exam)
5. Optionally enter course name
6. Wait for processing (chunking + embedding generation)

### 2. Ask Questions

1. Navigate to the **Ask Question** tab
2. Type your technical interview question
3. Optionally apply filters:
   - Material Type
   - Lecture Number
   - Topic
4. Click **Ask Question**
5. Review answer with sources and verification status

### 3. Verification

1. After asking a question, navigate to **Verification** tab
2. Review:
   - Faithfulness score
   - Verification status
   - Source details
3. Export results as JSON for grading/evaluation

## ⚙️ Configuration

Edit `backend/config.py` to adjust:

```python
# Chunking
CHUNK_SIZE = 500  # tokens (400-600 recommended)
CHUNK_OVERLAP = 100  # 20% overlap

# Retrieval
TOP_K = 12  # number of chunks to retrieve

# LLM - OpenRouter API
OPENROUTER_API_KEY = "your-api-key"
OPENROUTER_MODEL = "anthropic/claude-3.5-sonnet"  # Best for RAG
# Other good options:
# - "google/gemini-pro-1.5" (fast, cost-effective)
# - "openai/gpt-4-turbo" (excellent quality)
# - "meta-llama/llama-3.1-70b-instruct" (open-source)

LLM_TEMPERATURE = 0.1  # low for factual responses

# Verification
FAITHFULNESS_THRESHOLD = 0.8  # minimum score to pass
```

## 🔌 API Endpoints

### Query
- `POST /ask` - Submit question with optional filters

### Materials Management
- `GET /materials` - List all materials
- `POST /ingest` - Upload and process new material
- `DELETE /materials/{id}` - Delete material

### Utilities
- `GET /source/{chunk_id}` - Get chunk details
- `GET /logs/{id}` - Get query log
- `POST /admin/reindex` - Rebuild vector index

## 📊 Metadata Schema

Each chunk includes comprehensive metadata:

```json
{
  "chunk_id": "uuid",
  "course": "Machine Intelligence",
  "material_type": "lecture",
  "material_title": "Lecture 5 – RNN",
  "material_file": "data/lectures/Lecture_05_RNN.pdf",
  "lecture_number": 5,
  "chapter": "7",
  "topic": "Recurrent Neural Networks",
  "section": "Teacher Forcing",
  "page": 12,
  "text": "..."
}
```

## 🧪 Evaluation

### Recall@K Testing

```bash
cd backend
python evaluation/recall_at_k.py
```

### Citation Accuracy

```bash
cd backend
python evaluation/citation_accuracy.py
```

Results are saved to `logs/` directory.

## 🎯 Behavior Rules

The system enforces strict rules:

1. **No Relevant Chunks** → Refuse to answer
2. **Conflicting Sources** → Show both with citations
3. **Never Hallucinate** → Citations must be real
4. **No General Knowledge** → Only use provided materials
5. **Always Log** → All queries logged for evaluation

## 🗂️ Project Structure

```
Technical-Interview-Prep-Assistant/
├── backend/
│   ├── api/endpoints/          # API routes
│   ├── ingestion/              # Document processing
│   ├── retrieval/              # Embeddings & FAISS
│   ├── llm/                    # Ollama integration
│   ├── verification/           # Faithfulness checking
│   ├── db/                     # Database models
│   ├── evaluation/             # Evaluation scripts
│   └── config.py               # Configuration
├── frontend/
│   ├── src/
│   │   ├── pages/              # React pages
│   │   ├── components/         # React components
│   │   └── styles/             # CSS
│   └── package.json
├── data/                       # Uploaded materials
├── index/                      # FAISS index & metadata
└── logs/                       # Query logs
```

## 🔧 Troubleshooting

### API Key Issues
```bash
# Verify your API key is set correctly in backend/config.py
# Check your OpenRouter dashboard for credits and usage
```

### Embedding Model Download
First run will download the SentenceTransformers model (~90MB). This is automatic.

### FAISS Index Issues
```bash
# Rebuild index via API
curl -X POST http://localhost:8000/admin/reindex

# Or delete and re-upload materials
rm -rf index/*
```

### Frontend Can't Connect to Backend
- Ensure backend is running on port 8000
- Check Vite proxy configuration in `vite.config.js`

### Rate Limiting
If you hit rate limits, consider:
- Using a different model (e.g., Gemini Pro 1.5)
- Adding delays between requests
- Upgrading your OpenRouter plan

## 📝 Development

### Backend Development

```bash
cd backend
source venv/bin/activate

# Run with auto-reload
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend

# Development server with hot reload
npm run dev

# Build for production
npm run build
```

## 🌟 Key Technologies

- **Backend**: FastAPI, SentenceTransformers, FAISS, OpenRouter API, SQLAlchemy
- **Frontend**: React, Vite
- **Embedding**: all-MiniLM-L6-v2 (384 dimensions, CPU-friendly)
- **LLM**: Claude 3.5 Sonnet via OpenRouter (or other models)
- **Vector Store**: FAISS (exact cosine similarity)

## 📄 License

This project is for educational purposes.

## 🤝 Contributing

This is a local-only system. Contributions welcome for:
- Additional file format support
- Improved chunking strategies
- Better verification methods
- UI/UX enhancements

## 📧 Support

For issues or questions, please check:
1. Ollama is running and model is downloaded
2. Backend and frontend are both running
3. Materials are properly uploaded
4. Configuration is correct

---

**Built with ❤️ for local-first, privacy-preserving AI**