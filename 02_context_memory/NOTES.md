# 🧠 Module 02: Context & Memory — Revision Notes

> **The 10-Second Mental Model:**  
> LLMs have **zero memory**. Every HTTP request is completely forgotten the moment it finishes. "Chat memory" is an illusion maintained entirely by Python storing a list of past messages and re-sending the whole history on every turn.

---

## 🔄 How Memory Works Under the Hood

```
Turn 1: Python sends [User: "Hi"]                     --> LLM generates "Hello!"
Turn 2: Python sends [User: "Hi", Bot: "Hello!",      --> LLM generates "Paris!"
                      User: "Capital of France?"]
Turn 3: Python sends [User: "Hi", Bot: "Hello!",      --> LLM knows the context!
                      User: "Capital of France?", 
                      Bot: "Paris!", 
                      User: "What was my first question?"]
```

---

## 🔑 The Core Code Pattern

```python
messages = []  # The conversation memory buffer

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    # 1. Append user turn
    messages.append({"role": "user", "content": user_input})

    # 2. Send the ENTIRE message history to the model
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={"model": "gemma3:4b", "messages": messages, "stream": False}
    )

    reply = response.json()["message"]["content"]
    print("AI:", reply)

    # 3. Append assistant turn so the next turn remembers it
    messages.append({"role": "assistant", "content": reply})
```

---

## 💡 Critical Concepts & "Aha!" Moments

### 1. The Cost of Memory: Quadratic Token Growth
- On turn 1, you send 10 tokens.
- On turn 10, you are re-sending the tokens from turns 1 through 9 plus the new turn!
- Every conversation turn gets progressively slower and consumes more context window space.

### 2. Context Window Overflow
- Models have a fixed context window (e.g. 4k, 8k, 32k tokens).
- If your `messages` list exceeds this limit, the model will either crash or silently truncate/forget earlier messages.

### 3. Production Memory Strategies
| Strategy | How it works | Pros & Cons |
| :--- | :--- | :--- |
| **Buffer (What we built)** | Append every turn forever | Simple, but overflows eventually |
| **Sliding Window** | Keep only the last $N$ messages (e.g., `messages[-10:]`) | Never overflows, but forgets old facts |
| **Summary Memory** | Ask LLM to summarize turns 1-10 into 2 sentences, keep recent turns | Keeps key facts, costs an extra LLM call |
| **Vector / Long-term** | Store facts in a database and retrieve when relevant | Unlimited history, requires RAG pipeline |

---

## ⚠️ Top Pitfalls & Gotchas

1. **Forgetting to append the `assistant` reply**: If you only append `user` messages, the model won't know what it said, leading to disjointed or repeating answers.
2. **Role confusion**: Stick to valid role names (`system`, `user`, `assistant`). Sending unsupported role strings will trigger a `400 Bad Request`.
3. **Restarting the Python process wipes memory**: Because `messages` is an in-memory Python list, restarting the script resets history. For persistence, save `messages` to a JSON file or SQLite DB.

---

## ⚡ Quick Revision Self-Check

1. *If you close your terminal and run `python 01_conversation_memory.py` again, does Gemma remember who you are? Why or why not?*
2. *Why do API costs/latency increase as a conversation gets longer?*
3. *How would you implement a simple sliding window that only keeps the last 6 messages?* *(Hint: `messages = messages[-6:]`)*
