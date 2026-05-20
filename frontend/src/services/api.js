const BASE_URL = "http://localhost:8000/api";

export const api = {
    // 1. Send PDF to backend for ingestion
    ingestDocument: async (file) => {
        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch(`${BASE_URL}/ingest`, {
            method: "POST",
            body: formData,
        });
        
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || "Ingestion failed");
        return data;
    },

    // 2. Send query and table name to search/LLM endpoint
    searchAndChat: async (query, tableName) => {
        const response = await fetch(`${BASE_URL}/search`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ 
                query: query, 
                table_name: tableName 
            }),
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || "Search failed");
        return data;
    }
};