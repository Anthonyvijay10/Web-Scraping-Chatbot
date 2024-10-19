import google.generativeai as genai
import os

class GeminiHandler:
    def __init__(self):
        api_key = os.getenv("AIzaSyDHI0LNxREeOS8wKN40SVc1wERTFT4cqcM")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_answer(self, query, context):
        prompt = f"answer the question and answer as whole sentence: '{query}'\n\nContext: {context}"
        response = self.model.generate_content(prompt)
        # Filter the response to only include alphanumeric characters, apostrophes, and spaces
        filtered_response = ''.join(char for char in response.text if char.isalnum() or char == "'" or char.isspace())
        return filtered_response
