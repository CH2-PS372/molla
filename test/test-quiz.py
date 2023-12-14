import requests

# Create JSON data
data = {
    language: "indonesia"
}

# Send GET request with JSON content type
response = requests.get("https://get-quiz-mf5fjq4ezq-et.a.run.app/quiz, headers={"Content-Type": "application/json"}, json=data)


print(response.json())
