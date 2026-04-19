import requests

url = "http://localhost:11434/api/generate"

data = {
    "model": "llama3.1:8b",
    "prompt": "Who are you?",
    "stream": False
}

response = requests.post(url, json=data)

print(response.json()["response"])