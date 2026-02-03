import requests
import os


class OllamaService:
    """Service to interact with Ollama AI."""

    def __init__(self):
        self.base_url = os.environ.get('OLLAMA_URL', 'http://ollama:11434')

    def generate(self, prompt, model='llama2'):
        """Generate a response from Ollama."""
        try:
            response = requests.post(
                f'{self.base_url}/api/generate',
                json={
                    'model': model,
                    'prompt': prompt,
                    'stream': False
                },
                timeout=120
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}

    def chat(self, messages, model='llama2'):
        """Chat with Ollama."""
        try:
            response = requests.post(
                f'{self.base_url}/api/chat',
                json={
                    'model': model,
                    'messages': messages,
                    'stream': False
                },
                timeout=120
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}

    def list_models(self):
        """List available models."""
        try:
            response = requests.get(
                f'{self.base_url}/api/tags',
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}

    def pull_model(self, model_name):
        """Pull a model from Ollama library."""
        try:
            response = requests.post(
                f'{self.base_url}/api/pull',
                json={'name': model_name},
                timeout=600
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
