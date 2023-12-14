import requests

# Create JSON data
#data = {
#    "language": "indonesia"
#}

# Send GET request with JSON content type
response = requests.get("https://get-quiz-mf5fjq4ezq-et.a.run.app/quiz", headers={"Content-type": "application/json"}, json={"language": "indonesia"})


print(response.json())
