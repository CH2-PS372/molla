import requests

resp = requests.get("http://127.0.0.1:5000/translate")

print(resp.json())  