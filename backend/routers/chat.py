from fastapi import APIRouter, HTTPException
from models.schemas import QueryRequest
from services import embedding, database, llm_generator

router = APIRouter()

@router.post("/search")
async def search_and_generate(request: QueryRequest):
    try:
        # 1. Embed user query
        query_embedding = embedding.embed_single_query(request.query)
        
        # 2. Retrieve top 5 matching chunks from Supabase
        raw_chunks = database.search_chunks(request.table_name, query_embedding, match_count=5)
        
        # 3. THRESHOLD FILTER: Keep only chunks with > 50% match score (0.50)
        valid_chunks = [chunk for chunk in raw_chunks if chunk.get("similarity", 0) > 0.50]
        
        # 4. If no chunks passed the threshold, stop early!
        if not valid_chunks:
            return {
                "status": "success", 
                "answer": "I couldn't find any relevant information in the document for that query.",
                "sources": [] # Passing an empty list ensures the frontend skips printing page numbers
            }

        # 5. Pass ONLY the highly-relevant chunks to the LLM to combine and read
        generated_answer = llm_generator.generate_rag_answer(request.query, valid_chunks)

        # 6. Return both the AI answer AND the valid sources for citation
        return {
            "status": "success", 
            "answer": generated_answer,
            "sources": valid_chunks
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")