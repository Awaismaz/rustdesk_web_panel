import requests
import json

data = {
    "clients": [
        {"id": 112321, "OS":"Windows", "name": "Awais", "status": "connected", "last_domain_accessed": "www.google.com"},
        {"id": 232132, "name": "Moeez", "status": "connected", "last_domain_accessed": "www.google.com"},
    ]
}
response = requests.post('http://127.0.0.1:8000/api/receive_clients/', json=data)

# response = requests.post('https://awaismaz.pythonanywhere.com/api/receive_clients/', json=data)

if response.status_code == 200:
    print("Data sent successfully")
else:
    print(f"Failed to send data: {response.content}")
