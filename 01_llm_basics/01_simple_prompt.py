"""
Module 01: LLM Basics
File: 01_simple_prompt.py

Purpose:
Demonstrate the fundamental way to interact with an LLM via raw HTTP:
1. Understanding the stateless request/response model.
2. Using System and User roles.
3. Controlling model creativity with the `temperature` parameter.
4. Inspecting generation metadata (tokens, evaluation speed).
"""

import requests
import json
import sys


def run_llm_prompt(user_question: str, temperature: float = 0.2) -> None:
    # 1. Target endpoint for Ollama's Chat API
    url = "http://localhost:11434/api/chat"

    # 2. System prompt: Sets the behavior, tone, and guardrails for the model
    system_prompt = (
        "You are an encouraging and concise AI tutor. "
        "Answer the question clearly in 2-3 sentences."
    )

    # 3. Request payload: Everything the model needs to generate the next token
    payload = {
        "model": "gemma3:4b",
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_question
            }
        ],
        "stream": False,  # Return the complete response once finished
        "options": {
            "temperature": temperature  # 0.0 = deterministic/focused, 1.0 = creative/random
        }
    }

    print(f"--- Sending Prompt (Temperature: {temperature}) ---")
    print(f"User: {user_question}\n")

    try:
        # 4. Send the HTTP POST request to Ollama
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()

    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to Ollama.")
        print("Make sure Ollama is running (`ollama serve` or open the Ollama app).")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ HTTP Request failed: {e}")
        sys.exit(1)

    # 5. Parse the JSON response
    data = response.json()

    # Extract the assistant's answer text
    assistant_reply = data["message"]["content"]
    print("--- Model Response ---")
    print(assistant_reply.strip())

    # 6. Inspect metadata returned by the local engine
    prompt_tokens = data.get("prompt_eval_count", 0)
    output_tokens = data.get("eval_count", 0)
    total_time_ms = data.get("total_duration", 0) / 1_000_000

    print("\n--- Generation Metadata ---")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Generated tokens: {output_tokens}")
    print(f"Total time: {total_time_ms:.1f} ms")


if __name__ == "__main__":
    sample_question = "What is the difference between a parameter and a hyperparameter in Machine Learning?"
    run_llm_prompt(user_question=sample_question, temperature=0.2)
