from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import ingest, chat
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="RAG Ingestion & Chat Engine")

# Enable CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include our modular API routes
app.include_router(ingest.router, prefix="/api", tags=["Ingestion"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)