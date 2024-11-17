import requests
import json

url = 'http://localhost/v1/chat-messages'
headers = {
    'Authorization': 'Bearer app-OWwrLKVDT5aSRRIFyVFwgDsd',
    'Content-Type': 'application/json',
}
data = {
    "inputs": {},
    "query": "can you introduce yourself?",
    "response_mode": "blocking",
    "conversation_id": "",
    "user": "user-123"
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print(response.json())  # Use response.json() to parse the JSON content
