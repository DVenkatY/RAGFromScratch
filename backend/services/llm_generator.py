import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

# We use the Serverless Inference API so you don't need 16GB of local RAM to run this!
# We are using Microsoft's incredibly fast Phi-3.5 model for RAG.
client = InferenceClient(
    model="microsoft/Phi-3.5-mini-instruct",
    token=HF_TOKEN
)

def generate_rag_answer(query: str, retrieved_chunks: list) -> str:
    """Takes retrieved chunks and asks the LLM to formulate an answer."""
    
    # 1. Combine all the chunk text into a single context block
    context = "\n\n".join([f"Chunk {i+1}:\n{chunk['content']}" for i, chunk in enumerate(retrieved_chunks)])
    
    # 2. Build the strict RAG prompt
    prompt = f"""You are a helpful AI assistant. Use the following pieces of retrieved context to answer the user's question. 
    If you don't know the answer based ONLY on the context, just say that you don't know. Do not make up information.

    Context:
    {context}

    User Question: {query}
    
    Answer:"""

    # 3. Request generation from the LLM
    try:
        response = client.text_generation(
            prompt,
            max_new_tokens=400,
            temperature=0.3, # Low temperature keeps it factual
            return_full_text=False
        )
        return response.strip()
    except Exception as e:
        print(f"LLM Generation Error: {e}")
        return "I found the relevant chunks, but the AI model encountered an error generating the final response."