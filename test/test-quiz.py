import requests

# Create JSON data
data = {
}

# Send GET request with JSON content type
response = requests.get("http://127.0.0.1:5000/quiz", headers={"Content-Type": "application/json"}, json=data)


print(response.json())