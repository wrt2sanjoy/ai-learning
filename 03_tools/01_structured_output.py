import requests
import json

url = "http://localhost:11434/api/chat"

question = "What is 1578 multiplied by 239?"

prompt = f"""
You are an AI assistant that can use tools.

User question:
{question}

Decide whether a calculator is required.

Return ONLY valid JSON in this exact structure:

{{
    "action": "calculator" or "none",
    "input": "mathematical expression or empty string"
}}
"""

data = {
    "model": "gemma3:4b",
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ],
    "stream": False
}

response = requests.post(url, json=data)

if response.status_code == 200:

    result = response.json()

    answer = result["message"]["content"]

    print("LLM Response:")
    print(answer)

else:
    print("Error:", response.status_code)