import requests

resp = requests.get("http://127.0.0.1:5000/quiz", params={'language': 'indonesia'})

print(resp.json())