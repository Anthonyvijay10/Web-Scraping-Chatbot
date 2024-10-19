import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, HttpUrl
from dotenv import load_dotenv

from wiki_extractor import WikiExtractor
from milvus_handler import MilvusHandler
from gemini_handler import GeminiHandler

load_dotenv()

app = FastAPI(title="Wikipedia QA System", description="A QA system using Wikipedia, Milvus, and Gemini AI")

wiki_extractor = WikiExtractor()
milvus_handler = MilvusHandler()
gemini_handler = GeminiHandler()

class LoadRequest(BaseModel):
    url: HttpUrl

class QueryRequest(BaseModel):
    query: str

@app.post("/load", summary="Load Wikipedia page data")
async def load_data(request: LoadRequest):
    try:
        data = wiki_extractor.process_wikipedia_page(str(request.url))
        milvus_handler.insert_data(data)
        return {"message": f"Data from {request.url} loaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading data: {str(e)}")

@app.post("/query", summary="Query the loaded data")
async def query_data(request: QueryRequest):
    try:
        query_embedding = wiki_extractor.embed_text(request.query)
        search_results = milvus_handler.search(query_embedding)
        context = " ".join([result[0] for result in search_results])
        answer = gemini_handler.generate_answer(request.query, context)
        return {"query": request.query, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/", summary="Root endpoint")
async def root():
    return {"message": "Welcome to the Wikipedia QA System API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)