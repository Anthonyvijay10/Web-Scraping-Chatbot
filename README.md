# Wikipedia QA System

A QA system that utilizes Wikipedia data, Milvus for vector storage, and Gemini AI for generating answers to user queries.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Docker Setup](#docker-setup)
- [Environment Variables](#environment-variables)
- [Contributing](#contributing)
- [License](#license)

## Features

- Load Wikipedia page data and store it in Milvus.
- Query the loaded data to get answers using Gemini AI.
- FastAPI-based RESTful API for easy interaction.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher
- Docker and Docker Compose (for running Milvus)
- An active Google API key for Gemini AI

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/wikipedia-qa-system.git
   cd wikipedia-qa-system
   ```

2. **Install the required Python packages:**

   You can create a virtual environment and install the dependencies listed in `requirements.txt`:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Set up the environment variables:**

   Create a `.env` file in the `app` directory and add your Milvus and Google API key:

   ```plaintext
   MILVUS_HOST=localhost
   MILVUS_PORT=19530
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## Usage

1. **Start the Milvus service using Docker:**

   ```bash
   docker-compose up -d
   ```

2. **Run the FastAPI application:**

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

3. **Access the API documentation:**

   Open your browser and navigate to `http://localhost:8000/docs` to view the interactive API documentation.

## API Endpoints

- **Load Wikipedia Page Data**
  - **Endpoint:** `POST /load`
  - **Request Body:**
    ```json
    {
      "url": "https://en.wikipedia.org/wiki/Lionel_Messi"
    }
    ```

- **Query the Loaded Data**
  - **Endpoint:** `POST /query`
  - **Request Body:**
    ```json
    {
      "query": "What is the name of the club Lionel Messi currently plays for?"
    }
    ```

- **Root Endpoint**
  - **Endpoint:** `GET /`
  - **Response:** Welcome message.

## Docker Setup

This project uses Docker to run Milvus. The `docker-compose.yml` file is included to set up the necessary services. To start the services, run:
