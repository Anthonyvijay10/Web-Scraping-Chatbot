import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer

class WikiExtractor:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def extract_content(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        content = [p.get_text().strip() for p in paragraphs if p.get_text().strip()]
        return content

    def embed_text(self, text):
        return self.model.encode(text).tolist()

    def process_wikipedia_page(self, url):
        content = self.extract_content(url)
        embeddings = [self.embed_text(paragraph) for paragraph in content]
        return list(zip(content, embeddings))