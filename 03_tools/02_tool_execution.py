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

    llm_response = result["message"]["content"]
    print("Raw LLM response")
    print(llm_response)

    # Remove Markdown code fences if the model added them.
    cleaned_response = llm_response.replace("```json", "").replace("```", "").strip()
    
    # Convert JSON text into a Python dictionary.
    decision = json.loads(cleaned_response)
    print("\nParsed decision")
    print(decision)

    print("\nAction:", decision["action"])
    print("\nInput:", decision["input"])

else:
    print(f"Request failed: {response.status_code}")
