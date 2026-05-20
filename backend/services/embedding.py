import re
from sentence_transformers import SentenceTransformer

print("Loading 1024-Dimension Embedding Model into Memory...")
model = SentenceTransformer("mixedbread-ai/mxbai-embed-large-v1")

def clean_text(text: str) -> str:
    if not text: return ""
    text = re.sub(r'[\r\n\t]+', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

def split_into_sentences(text: str) -> list:
    sentence_end = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')
    return [s.strip() for s in sentence_end.split(text) if len(s.strip()) > 5]

def create_overlapping_chunks_with_pages(sentences_with_pages: list, chunk_size=10, overlap=2) -> list:
    if not sentences_with_pages: return []
    chunks = []
    stride = chunk_size - overlap
    for i in range(0, len(sentences_with_pages), stride):
        chunk_group = sentences_with_pages[i:i + chunk_size]
        combined_text = " ".join([item[0] for item in chunk_group])
        start_page = chunk_group[0][1]
        chunks.append((combined_text, start_page))
        if i + chunk_size >= len(sentences_with_pages):
            break
    return chunks

def generate_embeddings(text_list: list) -> list:
    """Generates embeddings for a batch of chunks"""
    return model.encode(text_list, batch_size=32, show_progress_bar=False, normalize_embeddings=True)

def embed_single_query(query: str) -> list:
    """Generates an embedding for a single user question"""
    return model.encode(query, normalize_embeddings=True).tolist()