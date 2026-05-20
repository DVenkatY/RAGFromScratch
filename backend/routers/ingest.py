import os
import re
import time
from fastapi import APIRouter, UploadFile, File, HTTPException
from fitz import open as open_pdf
from services import embedding, database

router = APIRouter()

@router.post("/ingest")
async def ingest_file(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only standard PDF files are supported.")
    
    base_name = os.path.splitext(file.filename)[0]
    table_name = re.sub(r'[^a-zA-Z0-9_]', '_', base_name).lower()
    doc_id = f"web_upload_{base_name}"

    try:
        if database.check_table_exists(table_name):
            return {"status": "exists", "table_name": table_name, "filename": file.filename}

        print(f"Creating dynamic table: {table_name}...")
        database.create_dynamic_table(table_name)

        # Timer 1: Parsing
        t0_chunk = time.time()
        pdf_bytes = await file.read()
        doc = open_pdf(stream=pdf_bytes, filetype="pdf")
        
        all_sentences = []
        for page_num, page in enumerate(doc):
            cleaned = embedding.clean_text(page.get_text())
            if cleaned:
                for sent in embedding.split_into_sentences(cleaned):
                    all_sentences.append((sent, page_num + 1))

        chunks_data = embedding.create_overlapping_chunks_with_pages(all_sentences)
        t1_chunk = time.time()

        # Timer 2: Embedding
        t0_embed = time.time()
        chunk_texts = [item[0] for item in chunks_data]
        embeddings_list = embedding.generate_embeddings(chunk_texts)
        t1_embed = time.time()

        # Timer 3: Upload
        t0_db = time.time()
        payload = []
        for chunk_idx, (chunk_text, start_page) in enumerate(chunks_data):
            payload.append({
                "doc_id": doc_id,
                "chunk_index": chunk_idx,
                "content": chunk_text,
                "metadata": {"original_filename": file.filename, "page_number": start_page},
                "embedding": embeddings_list[chunk_idx].tolist()
            })

        database.upload_chunks(table_name, payload)
        t1_db = time.time()

        return {
            "status": "success",
            "table_name": table_name,
            "chunks_created": len(payload),
            "message": "Ingestion completed successfully!",
            "metrics": {
                "chunking_seconds": round(t1_chunk - t0_chunk, 2),
                "embedding_seconds": round(t1_embed - t0_embed, 2),
                "database_upload_seconds": round(t1_db - t0_db, 2),
                "total_processing_seconds": round(t1_db - t0_chunk, 2)
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))