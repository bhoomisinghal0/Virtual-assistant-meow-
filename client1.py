import requests
import json
OPENROUTER_API_KEY="ai_api_key"
response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  
  headers={
    "Authorization": (f"Bearer {OPENROUTER_API_KEY}"),
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:ffhffff", # Optional. Site URL for rankings on openrouter.ai.
    "X-OpenRouter-Title": "Local Debug Script", # Optional. Site title for rankings on openrouter.ai.
  },
  data=json.dumps({
    "model": "openrouter/free",
    "messages": [
      {
        "role": "user",
        "content": "What is the meaning of life?"
      }
    ]
  })
)

print(response.json()["choices"][0]["message"]["content"])

