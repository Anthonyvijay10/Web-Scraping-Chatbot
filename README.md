Milvus Wikipedia QA System
This project implements a question-answering system using Wikipedia content, Milvus vector database, and the Gemini AI model.
Prerequisites

Docker and Docker Compose
Python 3.8+
Google Cloud account with Gemini API access

Setup

Clone the repository:
Copygit clone https://github.com/yourusername/milvus-wiki-qa.git
cd milvus-wiki-qa

Create a virtual environment and activate it:
Copypython -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install the required packages:
Copypip install -r requirements.txt

Create a .env file in the project root and add your Google API key:
CopyGOOGLE_API_KEY=your_google_api_key_here

Start the Milvus services using Docker Compose:
Copydocker-compose up -d

Wait for a few minutes to ensure all services are up and running.

Running the Application

Start the FastAPI application:
Copyuvicorn app.main:app --reload

The API will be available at http://localhost:8000.

API Endpoints
Load Data

URL: /load
Method: POST
Body: {"url": "https://en.wikipedia.org/wiki/Artificial_intelligence"}

Query Data

URL: /query
Method: POST
Body: {"query": "What is artificial intelligence?"}

Usage Example

Load data from a Wikipedia page:
Copycurl -X POST "http://localhost:8000/load" -H "Content-Type: application/json" -d '{"url": "https://en.wikipedia.org/wiki/Artificial_intelligence"}'

Query the loaded data:
Copycurl -X POST "http://localhost:8000/query" -H "Content-Type: application/json" -d '{"query": "What is artificial intelligence?"}'


Shutting Down
To stop the Milvus services:
Copydocker-compose down
Troubleshooting

If you encounter issues connecting to Milvus, ensure that all services are running:
Copydocker-compose ps

Check the logs of individual services:
Copydocker-compose logs milvus-standalone


Contributing
Feel free to submit issues or pull requests if you have suggestions for improvements or encounter any problems.
License
This project is licensed under the MIT License.
