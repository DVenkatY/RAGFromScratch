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
        retrieved_chunks = database.search_chunks(request.table_name, query_embedding, match_count=5)
        
        if not retrieved_chunks:
            return {
                "status": "success", 
                "answer": "I couldn't find any relevant information in the document.",
                "sources": []
            }

        # 3. Pass chunks to the LLM to generate a natural response
        generated_answer = llm_generator.generate_rag_answer(request.query, retrieved_chunks)

        # 4. Return both the AI answer AND the sources for citation
        return {
            "status": "success", 
            "answer": generated_answer,
            "sources": retrieved_chunks
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")