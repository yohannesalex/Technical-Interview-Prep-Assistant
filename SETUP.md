# Quick Setup Guide

## Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/Mac
# OR
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

## Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

## Configuration

1. Copy the example config:
```bash
cp backend/config.py.example backend/config.py
```

2. Edit `backend/config.py` and add your OpenRouter API key:
```python
OPENROUTER_API_KEY = "your-actual-api-key-here"
```

## Running

### Start Backend (Terminal 1)
```bash
cd backend
source venv/bin/activate
python main.py
```
Backend runs on: http://localhost:8000

### Start Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```
Frontend runs on: http://localhost:5173

## First Time Setup Checklist

- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] OpenRouter API key obtained from https://openrouter.ai/
- [ ] Virtual environment created
- [ ] Dependencies installed (backend)
- [ ] Dependencies installed (frontend)
- [ ] config.py created with API key
- [ ] Both servers running

## Troubleshooting

**Virtual environment not activating?**
```bash
# Make sure you're in the backend directory
cd backend
python3 -m venv venv
source venv/bin/activate
```

**FAISS installation fails?**
```bash
# Try installing with pip upgrade
pip install --upgrade pip
pip install -r requirements.txt
```

**Frontend won't start?**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**API key not working?**
- Check that config.py exists (not config.py.example)
- Verify API key is in quotes
- Check OpenRouter dashboard for credits
