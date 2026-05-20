from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
    table_name: str