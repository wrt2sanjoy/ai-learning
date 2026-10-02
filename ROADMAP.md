# 🗺️ AI Learning Roadmap: From First Principles to Autonomous Systems

Welcome to the **AI Learning Roadmap**! This repository is designed to teach you applied AI and Large Language Model (LLM) engineering from the ground up.

Rather than jumping directly into high-level abstractions like LangChain or CrewAI, this curriculum follows a **bottom-up, first-principles** methodology:

1. **Pure Python & HTTP first**: Understand the raw mechanics (JSON payloads, stateless APIs, token streams).
2. **Patterns from scratch**: Build memory, tools, and agents with standard Python while loops and lists.
3. **Frameworks later**: Adopt frameworks like LangChain and LangGraph only after you know exactly what problems they solve.

---

## 🧭 Curriculum Overview

```
Phase 1: LLM Basics & Prompting (01_llm_basics)
   │
Phase 2: Conversation & Context Memory (02_context_memory)
   │
Phase 3: Structured Output & Tool Calling (03_tools)
   │
Phase 4: Autonomous Agents (04_agents)
   │
Phase 5: Retrieval-Augmented Generation (05_rag)
   │
Phase 6: Production Frameworks with LangChain (06_langchain)
   │
Phase 7: Multi-Agent Graphs with LangGraph (07_langgraph)
   │
Phase 8: Capstone Projects (projects)
```

---

## 📚 Phase-by-Phase Roadmap

### Phase 1: LLM Basics & Prompting (`01_llm_basics/`)
*Understand what an LLM actually is: a stateless next-token predictor.*

- **Core Concepts:**
  - Tokenization, context window limits, and generation parameters (`temperature`, `top_p`, `max_tokens`).
  - Roles in chat APIs: `system`, `user`, `assistant`.
  - Zero-shot, few-shot prompting, and Chain-of-Thought (CoT).
- **Hands-on Exercises:**
  - `01_basics.ipynb`: Sending raw chat requests to local models (Ollama / `gemma3:4b`).
  - Experiment with temperature (0.0 for deterministic code/math, 0.8+ for creative tasks).
- **Milestone:** You can write clear prompts and understand how hyperparameters change the response.

---

### Phase 2: Context Window & Memory (`02_context_memory/`)
*LLMs have no memory. Discover how multi-turn conversation actually works.*

- **Core Concepts:**
  - The stateless nature of LLMs: each request must send previous messages to maintain context.
  - Message buffer: managing the `messages` list in Python.
  - Context limits: what happens when conversations grow too long (context overflow).
  - Memory strategies: sliding window (keeping last $N$ turns) vs. summarization memory.
- **Hands-on Exercises:**
  - `01_conversation_memory.py`: Building an interactive CLI chat loop that preserves conversation history.
  - `02_sliding_window_memory.py`: Implementing a token/turn cap to prevent context window overflow.
  - `03_persisted_chat.py`: Saving and restoring conversation history from a local JSON file.
- **Milestone:** You can build a conversational chatbot with bounded memory and persistence.

---

### Phase 3: Structured Output & Tool Calling (`03_tools/`)
*LLMs output freeform text. Learn how to constrain them to valid JSON and run Python code.*

- **Core Concepts:**
  - The challenge of unstructured text vs. deterministic software systems.
  - Prompting for JSON schemas and validating with `pydantic` or `json.loads`.
  - Ollama's `format: "json"` mode.
  - Function calling lifecycle:
    1. Send user prompt + tool description to model.
    2. Model decides whether to call a tool and outputs JSON arguments.
    3. Python executes the matching Python function.
    4. Python feeds the function result back to the model.
- **Hands-on Exercises:**
  - `01_structured_output.py`: Asking the model to decide if a calculator is required and output JSON.
  - `02_execute_tool.py`: Writing a Python dispatcher that parses the JSON and actually runs `calculator(expression)`.
  - `03_multi_tools.py`: Supporting multiple tools (calculator, current time, weather simulator).
- **Milestone:** You can have an LLM trigger deterministic Python functions reliably.

---

### Phase 4: Autonomous Agents (`04_agents/`)
*An agent is simply an LLM in a loop with tools and a stopping condition.*

- **Core Concepts:**
  - The **ReAct** pattern: Reason $\to$ Act $\to$ Observe $\to$ Repeat.
  - The Agent Loop: `while not done and iterations < max_iterations:`.
  - Handling failures: what to do if a tool throws an error or if the model hallucinates an invalid action.
  - Stopping conditions and final answer extraction.
- **Hands-on Exercises:**
  - `01_simple_react_agent.py`: A 60-line pure-Python ReAct agent loop solving multi-step questions.
  - `02_agent_with_memory.py`: Giving the agent long-term scratchpad memory.
- **Milestone:** You can build an agent from scratch without any third-party agent framework.

---

### Phase 5: Retrieval-Augmented Generation (`05_rag/`)
*Connect your LLM to private knowledge bases and external documents.*

- **Core Concepts:**
  - Embeddings: converting text into numerical vectors that capture semantic meaning.
  - Cosine similarity: measuring distance between text queries and documents.
  - The RAG pipeline:
    1. Ingestion: Loading and chunking text documents.
    2. Indexing: Creating embeddings and storing them.
    3. Retrieval: Finding the top-$K$ most relevant chunks.
    4. Generation: Injecting retrieved chunks into the LLM prompt as context.
- **Hands-on Exercises:**
  - `01_embeddings_basics.py`: Generating embeddings with Ollama (`nomic-embed-text` or similar).
  - `02_vector_similarity.py`: Building a pure-Python / NumPy vector search without external vector DBs.
  - `03_document_qa.py`: End-to-end RAG over a local markdown/PDF file.
- **Milestone:** You understand how vector search works under the hood and how to ground LLM answers in facts.

---

### Phase 6: Production Frameworks: LangChain (`06_langchain/`)
*Now that you know the fundamentals, use modern abstractions to move faster.*

- **Core Concepts:**
  - LangChain Expression Language (LCEL): `prompt | model | parser`.
  - Unified model interfaces (`ChatOllama`, `ChatOpenAI`).
  - Standardized document loaders, text splitters, and vector stores (`Chroma`, `FAISS`).
  - Output parsers and schema validation.
- **Hands-on Exercises:**
  - `01_lcel_basics.py`: Building composable chains with LCEL.
  - `02_langchain_rag.py`: Implementing RAG with LangChain's document loaders and retriever chains.
- **Milestone:** You can leverage LangChain without getting trapped by its abstractions because you understand the underlying HTTP calls.

---

### Phase 7: State Graphs: LangGraph (`07_langgraph/`)
*Build robust, cyclical, multi-actor workflows and state machines.*

- **Core Concepts:**
  - Why DAGs aren't enough: real-world agentic workflows require cycles, human review, and persistent checkpoints.
  - LangGraph components:
    - **State**: The shared dictionary/dataclass passed across the graph.
    - **Nodes**: Python functions that take state and return state updates.
    - **Edges & Conditional Edges**: Determining what node runs next.
- **Hands-on Exercises:**
  - `01_simple_graph.py`: A cyclic agent loop with a validation check.
  - `02_human_in_the_loop.py`: Pausing graph execution for user confirmation before executing a tool.
  - `03_multi_agent_workflow.py`: Supervisor agent delegating work to researcher and writer agents.
- **Milestone:** You can design production-grade, fault-tolerant AI agent architectures.

---

### Phase 8: Capstone Projects (`projects/`)
*Put everything together into full-featured applications.*

1. **`01_cli_research_assistant/`**: An interactive CLI assistant that searches local docs, runs Python code, and writes a synthesized report.
2. **`02_local_code_reviewer/`**: A git pre-commit hook that analyzes git diffs, checks for bugs, and outputs review feedback in structured JSON.
3. **`03_autonomous_support_agent/`**: A LangGraph-powered customer support bot with database lookup, escalation routing, and human handoff.

---

## 🛠️ Recommended Setup & Local Stack

- **Model Runner**: [Ollama](https://ollama.com/)
- **Recommended Models**:
  - Chat/Reasoning: `gemma3:4b`, `llama3.2:3b`, or `qwen2.5:7b`
  - Embeddings: `nomic-embed-text`
- **Environment**: Python 3.10+ in `.venv`

---

## 💡 Golden Rules for Learning
1. **Always inspect the prompt**: If something fails, print the exact text being sent to the model.
2. **Test failure cases**: What happens when the model hallucinates or the tool returns an error?
3. **Write code before copying templates**: You learn 10x faster by writing the 30 lines of code yourself.
