# 🛠️ Module 03: Tools & Function Calling — Revision Notes

> **The 10-Second Mental Model:**  
> LLMs are reasoning engines, not calculation engines. They are terrible at multi-digit arithmetic, real-time data, and database lookups. "Tool Use" means having the LLM **decide what to call** (as structured JSON), having **Python execute the function**, and optionally feeding the result back to the LLM to format the final answer.

---

## 🔄 The 4-Step Tool Lifecycle

```
[User Question] 
       │
       ▼
[Pass 1: Decision Prompt]  ──> LLM outputs JSON: {"action": "calculator", "input": "1578 * 239"}
       │
       ▼
[Python Parses JSON]       ──> Extracts action & input (strips markdown code fences)
       │
       ▼
[Python Executes Tool]     ──> calculator("1578 * 239") returns 377142
       │
       ▼
[Pass 2: Synthesis Prompt] ──> Prompt: "The calculator returned 377142. Answer user concisely."
       │
       ▼
[Final Answer to User]     ──> "1578 multiplied by 239 is 377,142."
```

---

## 🔑 The Core Code Patterns

### 1. Constraining the Model to JSON
```python
prompt = f"""
You are an AI assistant that can use tools.
Available tool: calculator(expression)
User question: {question}

Decide whether a calculator is required.
Return ONLY valid JSON in this exact structure:
{{
    "action": "calculator" or "none",
    "input": "mathematical expression or empty string"
}}
"""
```

### 2. Cleaning & Parsing Markdown Fences
LLMs frequently wrap JSON in markdown blocks (` ```json ... ``` `). Always sanitize before parsing:
```python
cleaned = (
    raw_llm_response
    .replace("```json", "")
    .replace("```", "")
    .strip()
)
decision = json.loads(cleaned)
action = decision["action"]
tool_input = decision["input"]
```

### 3. Safe Execution with `ast.parse` (Never use `eval()`)
```python
import ast, operator

allowed_operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

def safe_calculator(expr: str):
    tree = ast.parse(expr, mode="eval")
    # Recursively traverse tree and only allow numbers + whitelisted operators
    ...
```

---

## 💡 Critical Concepts & "Aha!" Moments

### 1. Why `ast.parse` instead of Python's built-in `eval()`?
- `eval("__import__('os').system('rm -rf /')")` can destroy your computer!
- If an LLM hallucinates or a malicious user injects malicious Python code through the prompt, `eval()` executes arbitrary code.
- `ast.parse` builds an Abstract Syntax Tree, allowing you to whitelist *only* math operators and numeric constants. Any variable name, import, or function call raises an error before execution.

### 2. Why Two LLM Passes?
- **Pass 1 (Brain / Decider)**: Fast, structured extraction. Determines *what* tool to run and with *what* arguments.
- **Python (Muscle / Tool)**: Deterministic, flawless computation (e.g. calculator, database query, API fetch).
- **Pass 2 (Speaker / Synthesizer)**: Converts the raw tool output into a polite, natural language response for the user.

### 3. Native Function Calling vs. Prompt-based JSON
- In `03_tools`, we used **prompt-based JSON** (specifying schema in the prompt text).
- Major APIs (OpenAI, Anthropic, and newer Ollama versions) also support **native tool schemas** (`tools=[{"type": "function", ...}]`), but under the hood, the principle is identical: the model generates structured arguments for your code to run.

---

## ⚠️ Top Pitfalls & Gotchas

1. **`json.decoder.JSONDecodeError`**:
   - The model prepends commentary like *"Sure! Here is the JSON you requested:"* before the curly braces `{`.
   - **Fix**: Instruct the model strictly (`"Return ONLY valid JSON with no introductory text"`), use Ollama's `"format": "json"`, or use a regex to extract the substring between `{` and `}`.
2. **Hallucinated Tool Inputs**:
   - If the user asks *"What is the square root of banana?"*, the model might output `"input": "sqrt(banana)"`. Your tool must validate input and raise friendly errors instead of crashing.
3. **Infinite Loops or Exponents**:
   - Evaluating `999 ** 999999` can freeze your CPU. Always cap exponents (`abs(right) <= 10`) and set calculation timeouts.

---

## ⚡ Quick Revision Self-Check

1. *Why should you never use `eval(expression)` when running tool inputs from an LLM?*
2. *What is the difference in purpose between Pass 1 and Pass 2 in `03_calculator_agent.py`?*
3. *What happens in `04_interactive_agent.py` if the user asks "What is the capital of Japan?"* *(Hint: Trace the `if action == "calculator"` vs `else` branch)*
