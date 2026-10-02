import requests


def main() -> None:
    url = "http://localhost:11434/api/chat"
    # This list will store the conversation history.
    messages = []
    while True:
        question = input("\nYou:")

        if question.lower() == "exit":
            print("Goodbye...")
            break
        # Add the user's message to the conversation.
        messages.append({
            "role": "user",
            "content": question
        })

        data = {
            "model": "Gemma3:4b",
            "messages": messages,
            "stream": False
        }
        print("\nDEBUG - Messages being sent to Gemma:")
        print(messages)
        response = requests.post(url, json= data)

        if response.status_code == 200:
            result = response.json()

            answer = result["message"]["content"]
            print("\nGemma:", answer)

           # Add Gemma's response to the conversation history.
            messages.append({
                "role": "assistant",
                "content": answer
            })

        else:
            print("Error:", response.status_code)


if __name__ == "__main__":
    main()
