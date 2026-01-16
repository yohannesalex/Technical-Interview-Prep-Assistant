# Ollama API Configuration Guide

## Using External Ollama API

To use an external Ollama API instead of running Ollama locally:

### 1. Update Configuration

Edit `backend/config.py`:

```python
# Change this line to your Ollama API endpoint
OLLAMA_URL = "https://your-ollama-api.com"  # Your API endpoint

# If your API requires authentication, set the API key
OLLAMA_API_KEY = "your-api-key-here"  # Or None if no auth needed

# Model name (check what models your API supports)
OLLAMA_MODEL = "mistral:7b-instruct"
```

### 2. Examples

**Local Ollama (default):**
```python
OLLAMA_URL = "http://localhost:11434"
OLLAMA_API_KEY = None
```

**Remote Ollama API:**
```python
OLLAMA_URL = "https://api.example.com/ollama"
OLLAMA_API_KEY = "sk-your-api-key-here"
```

**Cloud-hosted Ollama:**
```python
OLLAMA_URL = "https://your-instance.cloud-provider.com"
OLLAMA_API_KEY = "your-token"
```

### 3. No Other Changes Needed

The system automatically uses the configured endpoint. Just:
1. Update `config.py`
2. Restart the backend: `python backend/main.py`

### 4. Verify Connection

Check the health endpoint:
```bash
curl http://localhost:8000/health
```

Should return:
```json
{
  "status": "healthy",
  "vector_store_size": 0,
  "ollama_available": true
}
```

## Benefits of External API

✅ No need to run Ollama locally
✅ No model downloads required
✅ Can use more powerful hardware
✅ Easier deployment
✅ Shared infrastructure

## Privacy Note

⚠️ When using an external API, your queries and course materials will be sent to that API endpoint. Make sure you trust the API provider or use your own hosted instance.
