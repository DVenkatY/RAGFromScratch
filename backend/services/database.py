import os
import psycopg2
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def check_table_exists(table_name: str) -> bool:
    try:
        supabase.table(table_name).select("id").limit(1).execute()
        return True
    except Exception:
        return False

def create_dynamic_table(table_name: str):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    dynamic_sql = f"""
    CREATE EXTENSION IF NOT EXISTS vector;
    CREATE TABLE public.{table_name} (
        id BIGSERIAL PRIMARY KEY,
        doc_id VARCHAR(255) NOT NULL,
        chunk_index INTEGER NOT NULL,
        content TEXT NOT NULL,
        metadata JSONB DEFAULT '{{}}'::jsonb NOT NULL,
        embedding vector(1024)
    );
    CREATE INDEX idx_{table_name}_doc_id ON public.{table_name}(doc_id);
    CREATE INDEX idx_{table_name}_metadata_gin ON public.{table_name} USING gin (metadata);
    
    CREATE OR REPLACE FUNCTION public.match_{table_name} (
        query_embedding vector(1024), match_count INT, filter_metadata JSONB DEFAULT '{{}}'::jsonb
    ) RETURNS TABLE (
        id BIGINT, doc_id VARCHAR(255), chunk_index INT, content TEXT, metadata JSONB, similarity REAL
    ) LANGUAGE plpgsql AS $$
    BEGIN
        RETURN QUERY
        SELECT c.id, c.doc_id, c.chunk_index, c.content, c.metadata,
            (1 - (c.embedding <=> query_embedding))::REAL AS similarity
        FROM public.{table_name} c
        WHERE c.metadata @> filter_metadata
        ORDER BY c.embedding <=> query_embedding
        LIMIT match_count;
    END;
    $$;
    """
    cur.execute(dynamic_sql)
    conn.commit()
    cur.close()
    conn.close()

def upload_chunks(table_name: str, payload: list):
    batch_size = 100
    for i in range(0, len(payload), batch_size):
        batch = payload[i:i + batch_size]
        supabase.table(table_name).insert(batch).execute()

def search_chunks(table_name: str, query_embedding: list, match_count: int = 5):
    response = supabase.rpc(
        f"match_{table_name}", 
        {"query_embedding": query_embedding, "match_count": match_count, "filter_metadata": {}}
    ).execute()
    return response.data