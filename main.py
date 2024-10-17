import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig, get_peft_model  # Import LoRA components
import torch
import re

# Initialize FastAPI app
app = FastAPI(title="Wikipedia QA API", version="1.0")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Model configurations
embedding_model_name = 'sentence-transformers/all-MiniLM-L6-v2'  # Lightweight embedding model
gpt2_model_name = 'distilgpt2'  # Using DistilGPT-2 for efficiency

# Load SentenceTransformer model for embeddings
try:
    logger.info(f"Loading embedding model: {embedding_model_name}")
    embedder = SentenceTransformer(embedding_model_name)
except Exception as e:
    logger.error(f"Failed to load embedding model: {e}")
    raise RuntimeError(f"Failed to load embedding model: {e}")

# Load DistilGPT-2 with LoRA configuration
try:
    logger.info(f"Loading DistilGPT-2 model: {gpt2_model_name}")
    model = AutoModelForCausalLM.from_pretrained(gpt2_model_name)
    tokenizer = AutoTokenizer.from_pretrained(gpt2_model_name)

    # Set up LoRA configuration
    lora_config = LoraConfig(
        r=16,  # Rank of the low-rank adaptation
        lora_alpha=32,  # Scaling factor
        lora_dropout=0.1,  # Dropout rate
    )

    # Apply LoRA to the model
    qa_pipeline_instance = get_peft_model(model, lora_config)

    # Switch the model to evaluation mode
    qa_pipeline_instance.eval()
except Exception as e:
    logger.error(f"Failed to load DistilGPT-2 model with LoRA: {e}")
    raise RuntimeError(f"Failed to load DistilGPT-2 model with LoRA: {e}")

# Initialize FAISS index
embedding_dim = embedder.get_sentence_embedding_dimension()
faiss_index = faiss.IndexFlatL2(embedding_dim)
documents = []
embeddings = None

# Define Pydantic models for request bodies
class LoadRequest(BaseModel):
    url: str

class QueryRequest(BaseModel):
    query: str

def scrape_wikipedia(url: str) -> str:
    """
    Scrapes the content of a Wikipedia page.
    """
    try:
        logger.info(f"Scraping Wikipedia page: {url}")
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"Failed to retrieve page. Status code: {response.status_code}")
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract all paragraph texts
        paragraphs = soup.find_all('p')
        content = ' '.join([para.get_text() for para in paragraphs])
        logger.info(f"Scraped content length: {len(content)} characters")
        return content
    except Exception as e:
        logger.error(f"Error scraping Wikipedia page: {e}")
        raise ValueError(f"Error scraping Wikipedia page: {e}")

def preprocess_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    """
    Splits text into chunks of specified size with overlap.
    """
    logger.info(f"Preprocessing text into chunks of size {chunk_size} with overlap {overlap}")
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = ' '.join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    logger.info(f"Created {len(chunks)} chunks")
    return chunks

def embed_text(chunks: list) -> np.ndarray:
    """
    Embeds text chunks using the SentenceTransformer model.
    """
    try:
        logger.info("Embedding text chunks")
        embeddings = embedder.encode(chunks, convert_to_numpy=True)
        logger.info(f"Generated embeddings shape: {embeddings.shape}")
        return embeddings
    except Exception as e:
        logger.error(f"Error embedding text: {e}")
        raise ValueError(f"Error embedding text: {e}")

@app.post("/load", summary="Load data from a Wikipedia page")
def load_data(request: LoadRequest):
    global faiss_index, documents, embeddings
    url = request.url
    if not url.startswith("https://en.wikipedia.org/wiki/"):
        logger.error("Invalid URL provided. Must be a Wikipedia page.")
        raise HTTPException(status_code=400, detail="URL must be a Wikipedia page.")
    try:
        content = scrape_wikipedia(url)
        chunks = preprocess_text(content)
        embeddings = embed_text(chunks)
        faiss_index = faiss.IndexFlatL2(embedding_dim)  # Reset index
        faiss_index.add(embeddings)
        documents = chunks
        logger.info("Data loaded and indexed successfully")
        return {"message": "Data loaded successfully.", "number_of_chunks": len(documents)}
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", summary="Query the loaded data")
def query_data(request: QueryRequest):
    query = request.query
    if not documents:
        logger.error("No data loaded. Please load data first using /load.")
        raise HTTPException(status_code=400, detail="No data loaded. Please load data first using /load.")
    try:
        logger.info(f"Received query: {query}")
        query_embedding = embedder.encode([query], convert_to_numpy=True)
        k = 5  # Number of nearest neighbors
        logger.info(f"Searching for the top {k} nearest neighbors")
        D, I = faiss_index.search(query_embedding, k)
        retrieved_chunks = [documents[idx] for idx in I[0]]
        context = " ".join(retrieved_chunks)
        
        # Tokenize context to limit length
        tokenized_context = tokenizer(context, return_tensors="pt")
        max_context_length = 512  # Define a maximum length for the context
        if tokenized_context["input_ids"].size(1) > max_context_length:
            context = tokenizer.decode(tokenized_context["input_ids"][0, :max_context_length], skip_special_tokens=True)

        logger.info(f"Retrieved context: {context[:500]}...")  # Log first 500 chars
        
        # Prepare input for DistilGPT-2
        input_text = f"Question: {query}\nContext: {context}\nAnswer:"
        inputs = tokenizer(input_text, return_tensors="pt").to(qa_pipeline_instance.device)
        
        # Generate answer using the DistilGPT-2 model
        logger.info("Generating answer using the DistilGPT-2 model")
        output_sequences = qa_pipeline_instance.generate(
            inputs["input_ids"],
            max_new_tokens=100,  # Limit the number of tokens to generate
            num_return_sequences=1,
            early_stopping=True,
        )

        # Decode the generated answer
        answer = tokenizer.decode(output_sequences[0], skip_special_tokens=True)
        answer_part = answer.split("Context:")[-1].strip()  # Extract the context part
        
        # Clean the context to remove unwanted characters
        cleaned_context = re.sub(r'[^a-zA-Z,; ]+', '', answer_part)  # Keep only alphabets, commas, and semicolons

        if not cleaned_context:
            logger.warning("Model returned an empty cleaned context")
            cleaned_context = "I'm sorry, I couldn't find an answer to your question based on the provided context."
        
        return {"answer": cleaned_context}
    
    except Exception as e:
        logger.error(f"Error during query processing: {e}")
        raise HTTPException(status_code=500, detail=str(e))
