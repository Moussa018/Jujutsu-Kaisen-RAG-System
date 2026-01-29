# Jujutsu-Kaisen-RAG-System
Architecture RAG (Retrieval-Augmented Generation) locale dédiée à l'univers de Jujutsu Kaisen. Utilise **Llama 3.2 1B** et **ChromaDB** pour fournir des réponses basées sur des sources vérifiées.



## 🛠️ Stack
- **LLM :** Llama 3.2 1B (Ollama)
- **Vector Store :** ChromaDB
- **Framework :** FastAPI
- **Scraping :** Playwright (Chromium)

## 🚀 Installation
```bash
pip install -r requirements.txt
python -m playwright install chromium
ollama pull llama3.2:1b
