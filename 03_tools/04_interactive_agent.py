import ast
import json
import operator
import requests


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "gemma3:4b"


def calculator(expression: str) -> float:
    """Safely evaluate basic arithmetic expressions."""

    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def evaluate(node):

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Only numbers are allowed.")

        if isinstance(node, ast.BinOp):
            left = evaluate(node.left)
            right = evaluate(node.right)

            operation = allowed_operators.get(type(node.op))

            if operation is None:
                raise ValueError("Operator not supported.")

            if isinstance(node.op, ast.Pow) and abs(right) > 10:
                raise ValueError("Exponent too large.")

            return operation(left, right)

        if isinstance(node, ast.UnaryOp):
            operand = evaluate(node.operand)

            operation = allowed_operators.get(type(node.op))

            if operation is None:
                raise ValueError("Unary operator not supported.")

            return operation(operand)

        raise ValueError("Invalid mathematical expression.")

    tree = ast.parse(expression, mode="eval")

    return evaluate(tree.body)


def ask_llm(prompt: str) -> str:

    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=data)

    if response.status_code != 200:
        raise RuntimeError(
            f"Ollama request failed: {response.status_code}"
        )

    result = response.json()

    return result["message"]["content"]


while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        print("Goodbye...")
        break

    prompt = f"""
You are an AI assistant with access to a calculator tool.

User question:
{question}

Decide whether a calculator is required.

Return ONLY valid JSON:

{{
    "action": "calculator" or "none",
    "input": "mathematical expression or empty string"
}}
"""

    llm_response = ask_llm(prompt)

    print("\nLLM decision:")
    print(llm_response)

    cleaned_response = (
        llm_response
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    decision = json.loads(cleaned_response)

    action = decision["action"]

    if action == "calculator":

        expression = decision["input"]

        print("Tool selected: calculator")
        print("Tool input:", expression)

        result = calculator(expression)

        print("Tool result:", result)

        final_prompt = f"""
User question:
{question}

Calculator result:
{result}

Answer the user using this result.
Give a clear, concise answer.
"""

        final_answer = ask_llm(final_prompt)

        print("\nGemma:", final_answer)

    else:

        final_prompt = f"""
Answer this user question clearly:

{question}
"""

        final_answer = ask_llm(final_prompt)

        print("\nGemma:", final_answer)