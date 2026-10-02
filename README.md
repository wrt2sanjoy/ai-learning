# AI Learning

A step-by-step, hands-on learning roadmap for building with Large Language Models (LLMs), tools, memory, agents, retrieval-augmented generation (RAG), and modern orchestration frameworks.

> 📖 **Full Curriculum**: See [ROADMAP.md](file:///Users/ajayhalder/Documents/Codex/ai-learning/ROADMAP.md) for the detailed, phase-by-phase learning path and exercises.

---

## 📂 Project Structure

```text
ai-learning/
│
├── .venv/
│
├── 01_llm_basics/          # Prompting fundamentals, tokenization, API basics
├── 02_context_memory/       # Multi-turn conversation history & memory management
├── 03_tools/                # Structured output, function calling, tool use
├── 04_agents/               # ReAct agents, goal planning, autonomous loops
├── 05_rag/                  # Embeddings, vector databases, document retrieval
├── 06_langchain/            # LangChain abstractions, prompt templates, chains
├── 07_langgraph/            # State graphs, cycles, multi-agent workflows
│
├── projects/                # End-to-end practical AI applications
│
├── requirements.txt         # Project dependencies
├── ROADMAP.md               # Step-by-step curriculum & milestones
└── README.md                # Project overview & quickstart
```

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python 3.10+**
- **Ollama** running locally on `http://localhost:11434` with the models you plan to use (e.g., `gemma3:4b`):
  ```bash
  ollama run gemma3:4b
  ```

### 2. Environment Setup

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install project dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🧪 Running Examples

### 01. LLM Basics
Stateless API call with system prompt, temperature control, and token statistics:
```bash
python 01_llm_basics/01_simple_prompt.py
```

### 02. Context & Memory
Interactive multi-turn conversation with memory maintained across turns:
```bash
python 02_context_memory/01_conversation_memory.py
```

### 03. Tools & Structured Output
Safe calculator execution and two-pass tool response synthesis:
```bash
python 03_tools/04_interactive_agent.py
```

---

## 🎓 How to Learn with This Repo

1. Follow the phases sequentially in [ROADMAP.md](file:///Users/ajayhalder/Documents/Codex/ai-learning/ROADMAP.md).
2. Write each Python script by hand rather than copy-pasting.
3. Review the `NOTES.md` file in each folder for quick mental models, diagrams, and gotchas.
