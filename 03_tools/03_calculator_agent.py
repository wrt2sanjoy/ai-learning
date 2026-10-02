import ast
import json
import operator
import requests


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "gemma3:4b"


# ---------------------------------------------------------
# Tool: Safe calculator
# ---------------------------------------------------------

def calculator(expression: str) -> float:
    """
    Safely evaluate basic arithmetic expressions.
    Supported operators:
    +, -, *, /, %, **
    """

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

            # Prevent extremely large exponent calculations.
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


# ---------------------------------------------------------
# Step 1: Ask LLM what action to take
# ---------------------------------------------------------

question = "What is 1578 multiplied by 239?"

prompt = f"""
You are an AI assistant that can use tools.

Available tool:
- calculator(expression)

User question:
{question}

Decide whether a calculator is required.

Return ONLY valid JSON:

{{
    "action": "calculator" or "none",
    "input": "mathematical expression or empty string"
}}
"""

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
    print("LLM error:", response.status_code)
    raise SystemExit


# ---------------------------------------------------------
# Step 2: Read LLM decision
# ---------------------------------------------------------

result = response.json()

llm_response = result["message"]["content"]

print("LLM decision:")
print(llm_response)

cleaned_response = (
    llm_response
    .replace("```json", "")
    .replace("```", "")
    .strip()
)

decision = json.loads(cleaned_response)

action = decision["action"]
tool_input = decision["input"]


# ---------------------------------------------------------
# Step 3: Execute the tool
# ---------------------------------------------------------

if action == "calculator":

    print("\nAgent selected: calculator")
    print("Calculator input:", tool_input)

    tool_result = calculator(tool_input)

    print("Calculator result:", tool_result)


# ---------------------------------------------------------
# Step 4: Send tool result back to the LLM
# ---------------------------------------------------------

    final_prompt = f"""
User question:
{question}

The calculator tool returned:
{tool_result}

Answer the user's question using the tool result.
Give only the final answer.
"""

    final_data = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": final_prompt
            }
        ],
        "stream": False
    }

    final_response = requests.post(
        OLLAMA_URL,
        json=final_data
    )

    if final_response.status_code == 200:

        final_result = final_response.json()

        final_answer = final_result["message"]["content"]

        print("\nFinal answer:")
        print(final_answer)

    else:
        print("Final LLM call failed:", final_response.status_code)


elif action == "none":

    print("\nNo tool required.")

else:

    print("\nUnknown action:", action)