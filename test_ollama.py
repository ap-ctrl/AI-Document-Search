import requests

try:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "tinyllama",
            "prompt": "Who are you?",
            "stream": False
        }
        timeout=60
    )

    response.raise_for_status()

    print(response.json()["response"])

except Exception as e:
    print("Error:", e)
# import requests

# try:
#     response = requests.post(
#         "http://localhost:11434/api/generate",
#         json={
#             "model": "phi3",
#             "prompt": "Who are you?",
#             "stream": False
#         },
#         timeout=30
#     )

#     response.raise_for_status()

#     print("\nOllama Response:\n")
#     print(response.json()["response"])

# except Exception as e:
#     print("Error:", e)
