# Wikipedia QA System

This project is a QA system that utilizes Wikipedia data, Milvus for vector storage, and Gemini AI for generating answers. 

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Docker Setup](#docker-setup)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.7 or higher
- pip (Python package installer)
- Docker (for running Milvus)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Anthonyvijay10/Wikipedia-Scraping-Chatbot.git
   cd Wikipedia-Scraping-Chatbot
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Environment Setup

1. **`.env` file:**

   Make sure to set the `GOOGLE_API_KEY` with your actual Google API key.

## Running the Application

1. **Start the Docker containers:**
   Make sure Docker is running, then execute:
   ```bash
   docker-compose up -d
   ```

2. **Run the FastAPI application:**
   In a new terminal (with the virtual environment activated), run:
   ```bash
   cd app
   uvicorn main:app --reload
   ```

3. **Access the API:**
   Open your browser and go to `http://localhost:8000/docs` to view the API documentation and test the endpoints.

## API Endpoints

- **Load Wikipedia Page Data**
  - `POST /load`
  - Request Body: `{ "url": "http://example.com" }`
  
- **Query the Loaded Data**
  - `POST /query`
  - Request Body: `{ "query": "Your question here" }`

- **Root Endpoint**
  - `GET /`
  - Returns a welcome message.

 ### Stopping the Application

 1. **Stop the Docker Containers**:
   ```bash
   docker-compose down
   ```

2. **Ctrl+C to stop the FastAPI and to deactivate the Virtual Environment**:
   ```bash
   deactivate
   ```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
