import requests

# Ollama automatically runs a local API server on port 11434
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2" # The model we just downloaded!

print(f"✅ Configured to use Local Ollama Model: {MODEL_NAME}")

def generate_rag_answer(query: str, retrieved_chunks: list) -> str:
    # 1. Combine the chunks into our context string
    context = "\n\n".join([f"Chunk {i+1}:\n{chunk['content']}" for i, chunk in enumerate(retrieved_chunks)])
    
    # 2. Build the strict RAG prompt
    prompt = f"""You are a helpful AI assistant. Use the following pieces of retrieved context to answer the user's question. 
    If you don't know the answer based ONLY on the context, just say that you don't know. Do not make up information.

    Context:
    {context}

    User Question: {query}
    
    Answer:"""

    # 3. Format the payload for Ollama's local API
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False, # Tell it to send the whole answer at once, not word-by-word
        "options": {
            "temperature": 0.3 # Keep it factual
        }
    }

    try:
        # 4. Send the request to your local computer
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status() # Check for HTTP errors
        
        data = response.json()
        return data.get("response", "").strip()
        
    except requests.exceptions.ConnectionError:
        return "❌ Error: Could not connect to Ollama. Is the Ollama app running in the background?"
    except Exception as e:
        error_msg = repr(e) 
        print(f"❌ Local LLM Generation Error: {error_msg}")
        return f"I found the relevant chunks, but the local model encountered an error: {error_msg}"