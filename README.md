# Wikipedia QA API

This FastAPI application scrapes Wikipedia pages, processes the content into embeddings using `SentenceTransformer`, indexes it with FAISS, and answers queries based on the indexed content using a lightweight GPT-2 model with LoRA (Low-Rank Adaptation).

## Features

- Scrapes Wikipedia pages for content.
- Embeds Wikipedia content with `sentence-transformers/all-MiniLM-L6-v2`.
- Uses FAISS for fast similarity search of text chunks.
- Provides answers to questions using `distilgpt2` model with LoRA optimization.

## Prerequisites

- Python 3.8 or higher installed on your machine.

## Installation Guide

### 1. Clone the Repository

To get started, clone the repository to your local machine:

```bash
git clone <repository_url>
cd <repository_directory>
