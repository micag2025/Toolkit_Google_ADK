# Designing a Safe Multi-Agent Developer Assistant with Google ADK  
_An extensible toolkit for AI news, code execution, and MCP-based enrichment_

## Overview

This repository contains the full implementation for the publication **Designing a Safe Multi-Agent Developer Assistant with ADK**, published on the [Ready Tensor](https://www.readytensor.ai/) platform.

This project is built using **Google Agent Development Kit (ADK)** with a clean multi-agent architecture,  giving an example toolkit that demonstrates how to build, orchestrate, and deploy multi-agent systems using Google’s Agent Development Kit (ADK). The project focuses on creating an **AI Developer Agent** capable of discovering real-time AI news, generating Python code, and integrating with developer platforms like Hugging Face and GitHub.  

This project implements a **RootAgent–based multi‑agent system** designed for developers. The RootAgent never answers user queries directly. Instead, it **routes user input** to the most appropriate specialist agent, ensuring a clean separation of responsibilities and predictable behavior.

The system is optimized for:

* AI developer news discovery and summarization
* Safe and deterministic Python code execution
* Clear explanation of Python code
* Transparent use of third‑party developer platforms  

---

## Highlights
- Interactive ADK Web UI for experimenting with agents
- Multi-agent orchestration with a RootAgent that routes to specialist agents
- Real-time web discovery using `google_search`
- Safe Python execution via ADK's sandboxed executor

---

## Core capabilities

- **Real-time text agents**: natural conversational interaction with web access for up-to-date information.
- **Multi-agent orchestration**: coordinated workflows (e.g., researchers, planners, executors).
- **Production readiness**: guardrails, persistent memory, logging, and deployment on Vertex AI Agent Engine.

---

## Architecture overview

High-level flow:
1. **ADK Web UI**: user input, headline selection, and execution requests.
2. **Session state**: tracks mode (news / code), last query, headlines, selections.
3. **RootAgent**: intent detection, context aggregation, and deterministic routing.
4. **Specialist agents**:
   - AIDevSearchAgent (news + google_search)
   - CodeAgent (sandboxed Python execution)
   - CodeExplainAgent   
   - HugginFaceAgent  
   - GitHib Agent    

The application is built using a **state-aware, multi-agent architecture powered by Gemini models and Google ADK Web**, designed specifically for AI developers.     

---

## Core Architecture

### RootAgent

The **RootAgent** acts as the central orchestrator:

* Routes all user input
* Never responds directly to the user
* Ensures correct agent selection
* Enforces separation of concerns between agents

The RootAgent has **direct access** to:

* Gemini‑powered specialist agents
* Third‑party developer APIs (custom tools)

---

## Gemini‑Powered Specialist Agents

### AIDevSearchAgent *(also known as the **AI Developer News Agent**)*  

Responsible for discovering and summarizing AI‑related news relevant to developers.

**Capabilities:**

* Searches AI developer news, articles, platforms, and use cases
* Uses `google_search`
* Manages headline selection and summarization

**Workflow:**

1. Clarify the number of items to retrieve
2. Search and filter AI‑related content
3. Present candidate headlines
4. Summarize selected items

---

### CodeAgent *(also known as the **Python Code Agent**)*

Responsible **only** for executing Python code.

**Constraints:**

* Executes Python code exclusively
* Uses `BuiltInCodeExecutor`
* Returns raw execution output or errors
* No explanations or commentary

---

### CodeExplainAgent

Responsible for **explaining Python code**.

**Constraints:**

* Explains code logic and behavior
* Does **not** execute code

---

## Third‑Party Developer APIs (Custom Tools)

### Hugging Face Hub Agent

Provides access to Hugging Face ecosystem data:

* Model metadata
* Spaces
* Datasets
* Popularity and usage signals

---

### GitHub Agent

Provides insights into open‑source repositories:

* Repository metadata
* Stars, issues, and commits
* Open‑source activity signals

---

## Architecture Diagram (Control Flow vs Data Flow)

This system architecture is intentionally described using **two parallel lanes**:

* a **Control Flow lane**, which defines *who decides* and *who delegates*
* a **Data Flow lane**, which defines *where execution and data actually travel*

Keeping these lanes separate makes authority, responsibility, and trust boundaries explicit.

### Control Flow Lane — *Who decides what happens next?*

The **Control Flow lane** represents **decision‑making and orchestration**, entirely owned by the **RootAgent**.

Key rules:

* **Only the RootAgent decides** what happens next
* All specialist agents are **children** of the RootAgent
* **No agent self‑invokes** or chains other agents
* **No external system** can directly trigger agent logic

This guarantees a single, auditable decision point and prevents hidden agent autonomy.

```text
╔═══════════════════════════════════════════════════════════════════════════════════════════════════╗
║                          CONTROL FLOW                                                             ║
║          (Decision, routing, orchestration – ADK)                                                 ║
╠═══════════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                                   ║
║  ┌─────────────────────────────────────────────────────────────────────────────────────┐          ║
║  │                    ADK Web UI                                                       │          ║
║  │  - User prompts                                                                     │          ║
║  │  - Headline selection                                                               │          ║
║  └──────────────────────────┬──────────────────────────────────────────────────────────┘          ║
║                             ▼                                                                     ║
║  ┌─────────────────────────────────────────────────────────────────────────────────────┐          ║
║  │                    RootAgent                                                        │          ║
║  │        (Gemini 2.5 Flash – Router / Orchestrator)                                   │          ║
║  │                                                                                     │          ║
║  │  - Intent classification                                                            │          ║
║  │  - Delegation (AgentTool)                                                           │          ║
║  │  - Result aggregation                                                               │          ║
║  └───────┬──────────────┬──────────────┬──────────────┬───────────────────────┬────────┘          ║
║          │              │              │              │                       │                   ║
║          ▼              ▼              ▼              ▼                       ▼                   ║
║  ┌──────────────┐ ┌──────────────┐ ┌────────────────┐ ┌────────────────┐    ┌────────────────┐    ║
║  │ AIDevSearch  │ │   CodeAgent  │ │   CodeExplain  │ │ HuggingFace    │    │ GitHub         │    ║
║  │   Agent      │ │              │ │   Agent       │  │ Agent          │    │ Agent          │    ║
║  │ (Gemini Tool)│ │ (Gemini Tool)│ │ (Gemini Tool)  │ │ (Gemini Tool)  │    │ (Gemini Tool)  │    ║
║  └──────────────┘ └──────────────┘ └────────────────┘ └────────────────┘    └────────────────┘    ║
║                                                                                                   ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════╝
```

### Data Flow Lane — *Where does execution and data actually go?*

The **Data Flow lane** represents **execution, transport, and I/O paths**. These flows may:

* remain local
* cross process boundaries
* cross network boundaries

**Important:** transport differences do **not** imply authority. All flows still originate from RootAgent decisions.

```text
╔════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                           DATA FLOW                                                                ║
║            (Execution, transport, external systems)                                                ║
╠════════════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                                    ║
║  ┌─────────────────────┐      ┌──────────────────────────────┐    ┌──────────────────────────────┐ ║
║  │ google_search (ADK) │      │ BuiltInCodeExecutor          │    │ CodeExplain                  │ ║
║  └─────────┬───────────┘      │ (Python sandbox, no net/fs)  │    │ (Python sandbox, no net/fs)  │ ║
║            │                  └─────────┬────────────────────┘    └─────────┬────────────────────┘ ║
║            ▼                            ▼                                   ▼                      ║
║  External search results          Python execution output              Python explanation output   ║
║                                                                                                    ║
║  ┌─────────────────────┐      ┌────────────────────────────────┐                                   ║
║  │ HF MCP Server       │      │ GitHub MCP Server              │                                   ║
║  │ (stdio, local proc) │      │ (HTTP, remote Copilot MCP)     │                                   ║
║  └─────────┬───────────┘      └─────────┬──────────────────────┘                                   ║
║            │                            │                                                          ║
║            ▼                            ▼                                                          ║
║  Hugging Face Hub               GitHub Platform                                                    ║
║  - models                       - repos                                                            ║
║  - datasets                     - issues / PRs                                                     ║
║  - spaces                       - commits / releases                                               ║
║                                                                                                    ║
╚════════════════════════════════════════════════════════════════════════════════════════════════════╝
```

---

## Agents & Tools

This section provides a **concise, authoritative mapping** between agents, tools, and execution backends. It complements the architecture diagrams by making *attachments, responsibilities, and transport mechanisms explicit*.

### Tool Schema

|              Component | Type                             | Attached To        | Purpose                                      |
| ---------------------: | -------------------------------- | ------------------ | -------------------------------------------- |
|   **AIDevSearchAgent** | `AgentTool`                      | RootAgent          | Discover & summarize AI developer news       |
|          **CodeAgent** | `AgentTool`                      | RootAgent          | Execute Python code safely                   |
|   **CodeExplainAgent** | `AgentTool`                      | RootAgent          | Explain Python code safely                   |
| **hugging_face_agent** | `AgentTool` (Gemini + MCP stdio) | RootAgent          | Hugging Face models, datasets, spaces        |
|       **github_agent** | `AgentTool` (Gemini + MCP HTTP)  | RootAgent          | GitHub repositories, issues, PRs (read‑only) |
|        `google_search` | Built‑in ADK Tool                | AIDevSearchAgent   | Web discovery for news                       |
|  `BuiltInCodeExecutor` | ADK Executor                     | CodeAgent          | Deterministic Python sandbox                 |
|      **HF MCP Server** | MCP Backend (stdio)              | hugging_face_agent | Transport to Hugging Face Hub                |
|  **GitHub MCP Server** | MCP Backend (HTTP)               | github_agent       | Transport to GitHub API (Copilot MCP)        |

**Why this matters:**

* Makes **agent–tool attachment explicit**
* Clarifies **execution vs transport vs authority**
* Supports audits, reviews, and future extension
* Prevents accidental agent autonomy or tool misuse

---

## Design Principles

* **Separation of concerns** – RootAgent routes, specialist agents execute
* **Deterministic workflows** – Minimal LLM guesswork for critical steps
* **Tool transparency** – Explicit tool usage and sources
* **Developer‑first UX** – Safe code execution and predictable outputs

---

## Use Cases and Example Prompts by User Type  
This table highlights how different user roles can use the ADK Toolkit, along with example prompts that demonstrate typical interactions and expected value.


| **User Type**           | **Primary Value**                            | **Example Prompts**                                                                                                                 |
| ----------------------- | -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| **ML Engineers**        | Deep technical insight into models & tooling | • “Show popular open-source LLMs for text summarization”<br>• “Which Hugging Face models are state-of-the-art for text generation?” |
| **Backend Engineers**   | AI relevance without ML complexity           | • “Are there AI tools useful for backend search or summarization?”<br>• “Which of these tools are production-ready?”                |
| **MLOps Engineers**     | Deployment & infrastructure signals          | • “Which of these tools are open-source and actively maintained?”<br>• “Are these models deployable on-prem or via containers?”     |
| **Tech Leads**          | High-signal summaries & trend awareness      | • “Summarize the most relevant AI developer news this week”<br>• “Which AI trends could impact backend teams?”                      |
| **Technical Writers** | Structured, reusable technical content       | • “Explain this article for developers new to LLMs”<br>• “Extract the key technical takeaways from this news item”                  |
| **Product Managers**    | Strategic clarity & market signals           | • “Which of these tools are proprietary vs open-source?”<br>• “What AI trends should product teams care about?”                     |
| **Researchers**         | Bridge from research to implementation       | • “Which research projects have working implementations?”<br>• “Are there Hugging Face models implementing this approach?”          |
| **Students & Learners** | Guided learning & exploration                | • “Explain this Python code step by step”<br>• “Which AI tools should I learn first as a beginner?”                                 |
---

## Project Structure

```bash
Toolkit_Google_ADK/                     # Root project directory
├── app_01/                             # Main application module
│   ├── __init__.py                     # Python package marker
│   ├── agent.py                        # Core agent logic (Google ADK integration)
│   └── .env                            # Local environment variables (not committed)
│
├── Notebbook_app_001.ipynb              # Notebook for experiments and demos
├── requirements.txt                    # Python dependencies
├── .env.example                        # Environment variable template
├── LICENSE                             # Project license
├── .gitignore                          # Ignore rules for secrets and artifacts
├── README.md                           # Project documentation
│
├── Screenshots_Examples_Usage/          # UI and agent output examples
│   ├── Screenshot_UI_interface.jpeg
│   ├── Screenshot_AIDevSearchAgent_2.jpeg
│   ├── Screenshot_AIDevSearchAgent_3.jpeg
│   ├── Screenshot_CodeAgent_1.jpeg
│   ├── Screenshot_CodeExplainAgent1.jpeg
│   ├── Screenshot_HuggingFaceAgent1.jpeg
│   ├── Screenshot_GitHubAgent1.jpeg
│   ├── Screenshot_2
│   ├── Screenshot_3
│   └── Screenshot_4
```

---

## Getting Started

This section shows how to install dependencies, configure authentication, and run the full pipeline.  

### Interactive Notebook: Getting Started with ADK  

For hands-on learning and experimentation, [`Notebbook_app_001.ipynb`](https://github.com/micag2025/Toolkit_Google_ADK/blob/96b5476392dc201e4710fbf9aa76c7bb0fa63d99/Notebook_app_01.ipynb)
 demonstrates:

- Setting up a new agent folder (`adk create`)
- Writing the first `agent.py`
- Adding text models and built-in tools (`google_search`, `BuiltInCodeExecutor`)
- Fine-tuning agent instructions and behavior
- Testing valid and invalid prompts

### Prerequisites  

- Python 3.10+
- Google account & Vertex AI / Gemini access (API key)
- Optional: Hugging Face and GitHub API keys for enrichment

### Clone and install:

```bash
git clone https://github.com/micag2025/Toolkit_Google_ADK.git
cd Toolkit_Google_ADK
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Environment variables 
Set environment variables (keys) in `.env` or your environment. See example `.env.example`.  

```env
GEMINI_API_KEY=your_gemini_api_key
HF_API_KEY=your_hf_api_key
GIT_API_KEY=your_github_api_key
ADK_DEV_MODE=true
```

> _Notes:_  
> - The project expects API keys to be correctly provisioned for Vertex AI / Gemini usage.
> - You can create a [Gemini API key](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/quickstart?usertype=apikey#python-gen-ai-sdk). This key is essential for authenticating your requests to the Gemini API. A step-by-step guide can be found on o [Google AI Studio](https://cloud.google.com/free?hl=en)


### Launch the ADK Web App  / Get the app URL  
Start the ADK Web app:

```bash
adk web
```

### Open in  browser  
ADK will provide a local URL. Open it in your browser. From the Google ADK user interface in the left pane, select the `app_01` agent. You can now interact with the ADK AI Developer.    

### Kill ADK process    
Stop the ADK process (if needed):

```bash
pkill -f "adk web"
```
---  

### Testing Instructions  

You can test the enhanced multi-agent system using both **valid** and **invalid** prompts.

The examples below are designed to validate multiple aspects of the system, including:  
- **Routing accuracy** (correct delegation by the RootAgent)  
- **Agent specialization** (each agent handles only its intended scope)  
- **MCP integrations** (GitHub and Hugging Face tool usage)  
- **Safety boundaries** (sandboxing, no guessing, no unauthorized access)  
- **Session state handling** (headline selection and follow-up flows)  
- **Instruction adherence** (strict output formats and guardrails)  
- **Model choice impact** (behavior differences across Gemini models)

Use the valid prompts to confirm expected behavior, and the invalid prompts to verify that the system 
**refuses**, **redirects**, **or safely degrades** as intended.  

- **AIDevSearchAgent**
    
| ✅ Valid prompts (should get a response)                              | ❌ Invalid prompts (should be refused / redirected) |
| -------------------------------------------------------------------- | -------------------------------------------------- |
| **General request**<br>• “Give me AI news for Google”                | “What’s the weather today?”                        |
| **Scoped request**<br>• “Give me 3 top AI news items for developers” | “Give me sports news headlines”                    |
| **Follow-up**<br>• “Tell me more about the first one”                | “Tell me celebrity gossip”                         |
| **Company-focused**<br>• “Recent AI developer news from Meta”        | “Latest stock price of Apple”                      |
| **Technology-focused**<br>• “AI tooling news for Python developers”  | “Movie releases this week”                         |

---

- **CodeAgent (Python Execution)**  

| ✅ Valid prompts                                                          | ❌ Invalid prompts                                      |
| ------------------------------------------------------------------------ | --------------------------------------------------------- |
| **Simple execution**<br>`Execute python code: print(sum(range(10)))`     | `Execute python code: import os; os.listdir()`            |
| **Math operations**<br>`Execute python code: import math; math.sqrt(16)` | `Execute python code: import requests; requests.get(...)` |
| **Computation**<br>`Execute python code: sum(i*i for i in range(10))`    | `Execute python code: while True: pass`                   |
| **Data structures**<br>`Execute python code: [x*2 for x in range(5)]`    | `Execute python code: open("file.txt")`                   |

---

- **CodeExplainAgent**

| ✅ Valid prompts                                                            | ❌ Invalid prompts                |
| -------------------------------------------------------------------------- | ----------------------------------- |
| **Basic explanation**<br>“Explain this Python code:” *(fib example)*       | “Explain this JavaScript code”      |
| **Pedagogical**<br>“Explain this code line by line for a junior developer” | “Optimize this code and rewrite it” |
| **Conceptual**<br>“What does this loop do?”                                | “Execute this code”                 |
| **Edge cases**<br>“Explain possible pitfalls in this Python function”      | “Convert this code to Rust”         |


--- 

- **Hugging_face_agent (Canonical Reference Only)**

| ✅ Valid prompts                                                                                  | ❌ Invalid prompts                                      |
| ------------------------------------------------------------------------------------------------ | --------------------------------------------------------- |
| **Exact model ID**<br>“Give me the Hugging Face link for `mistralai/Mixtral-8x7B-Instruct-v0.1`” | “Show popular Hugging Face models for text summarization” |
| **Validation**<br>“Is `facebook/bart-large-cnn` available on Hugging Face?”                      | “What is the best summarization model on Hugging Face?”   |
| **Direct lookup**<br>“Hugging Face link for `google/pegasus-arxiv`”                              | “List Hugging Face models by popularity”                  |
| **Exact dataset/model**<br>“Hugging Face link for `openai/whisper-large-v3`”                     | “Recommend a Hugging Face model for me”                   |

---  

- **Github_agent (Repo Inspection Only)**

| ✅ Valid prompts                                                            | ❌ Invalid prompts                      |
| -------------------------------------------------------------------------- | ----------------------------------------- |
| **Explicit repo**<br>“Show me details of `langchain-ai/langchain`”         | “Find good GitHub repos for AI”           |
| **Explicit URL**<br>“Summarize `github.com/openai/evals`”                  | “Who maintains the best AI repos?”        |
| **Repo discovery**<br>“Show me the GitHub repo for LangGraph”              | “Search GitHub for trending LLM projects” |
| **Activity insights**<br>“Summarize activity for the LangChain repository” | “Compare LangChain vs LlamaIndex”         |
| **Stats lookup**<br>“Give repo stats for `crewAIInc/crewAI`”               | “Which GitHub repo should I use?”         |

---  

## Examples Usage (UI)

### ADK Web UI: 
![ADK_interface](https://github.com/micag2025/Toolkit_Google_ADK/blob/739b84b0c46e2b53255baa3bdc2a6614666bbc57/Screenshots_Examples_Usage/Screenshot_UI_interface.jpeg)

After selecting the appropriate app (`app_01`) from the dropdown menu from the ADK Web UI,  below is a high-signal, comprehensive set of prompt examples designed to systematically test the application end-to-end, aligned with the agent architecture, routing rules, MCP integrations, and UI flows.  

> _Note_ : Different Run Results: The output generated can vary with each execution due to their dynamic, probabilistic nature.     

### 1. Example Prompts: AI News AIDevSearchAgent     
-  AI news discovery `General discovery (clarification expected)`:    
   - Ask: "What's the latest AI news about Google?" → Should ask: “How many news items would you like me to find?”  
   - Flow: RootAgent → AIDevSearchAgent → google_search → summarize & cite sources.

![Google_Search_Agent_1](https://github.com/micag2025/Toolkit_Google_ADK/blob/7f9f9847b6f6e58bc90626556ab965c883c994d6/Screenshots_Examples_Usage/Screenshot_Aidevsearch_1.jpeg)

![Google_Search_Agent_2](https://github.com/micag2025/Toolkit_Google_ADK/blob/7f9f9847b6f6e58bc90626556ab965c883c994d6/Screenshots_Examples_Usage/Screenshot_Aidevseach_2.jpeg)  

-  AI news discovery `Invalid prompts`:
   - Ask: “What’s the weather today?”   

![Google_Search_Agent_3](https://github.com/micag2025/Toolkit_Google_ADK/blob/7f9f9847b6f6e58bc90626556ab965c883c994d6/Screenshots_Examples_Usage/Screenshot_Aidevsearch_3.jpeg)

### 2.  Example Prompts: Python Code Execution 
- Python execution (`valid prompt):
   - Ask: "Run this Python code..." / "Execute python code: print(2 + 2)" / Simple execution and Data handling
   - Flow: RootAgent → CodeAgent → BuiltInCodeExecutor (sandbox) → return execution output (no extra commentary).
- Python execution (`invalid prompt`):
     
![PythonDevelopr_Agent](https://github.com/micag2025/Toolkit_Google_ADK/blob/7f9f9847b6f6e58bc90626556ab965c883c994d6/Screenshots_Examples_Usage/Screenshot_code_agent_1.jpeg)

### 3.  Example Prompts: Python Explain Code   
-  Python explain code
   - Ask :  "Explain this Python code:”
   - Flow: RootAgent → CodeExplainAgent  →  return explanation only (no execution).  
        
![PythonExplainCode_Agent_1](https://github.com/micag2025/Toolkit_Google_ADK/blob/7f9f9847b6f6e58bc90626556ab965c883c994d6/Screenshots_Examples_Usage/Screenshot_code_explain_agent_1.jpeg)

![PythonExplainCode_Agent_2](https://github.com/micag2025/Toolkit_Google_ADK/blob/7f9f9847b6f6e58bc90626556ab965c883c994d6/Screenshots_Examples_Usage/Screenshot_code_explain_agent_2.jpeg)  

![PythonExplainCode_Agent_3](https://github.com/micag2025/Toolkit_Google_ADK/blob/7f9f9847b6f6e58bc90626556ab965c883c994d6/Screenshots_Examples_Usage/Screenshot_code_explain_agent_3.jpeg)  

### 4.  Example Prompts: HuggingFace 
- Enrichment tests  
  - Ask :“Is this model available on Hugging Face: facebook/bart-large-cnn?” / Give me the Hugging Face link for mistralai/Mixtral-8x7B-Instruct-v0.1    
  - Flow: RootAgent → hugging_face_agent   →  *HF MCP Server"  →  return link     
 - Python execution (`invalid prompt`):
    
![HuggingFace_Agent_3](https://github.com/micag2025/Toolkit_Google_ADK/blob/7f9f9847b6f6e58bc90626556ab965c883c994d6/Screenshots_Examples_Usage/Screenshot_hf_agent_3.jpeg)

### 5.  Example Prompts: GitHub Code Execution    
-  Enrichment:
   - RootAgent can request Hugging Face signals to rank or annotate discoveries.   
   - Flow: RootAgent → github_agent  →  GitHub MCP Server → return explanation only     
         
![GitHub_Agent_1](https://github.com/micag2025/Toolkit_Google_ADK/blob/7f9f9847b6f6e58bc90626556ab965c883c994d6/Screenshots_Examples_Usage/Screenshot_github_agent_1.jpeg)   

![GitHub_Agent_2](https://github.com/micag2025/Toolkit_Google_ADK/blob/7f9f9847b6f6e58bc90626556ab965c883c994d6/Screenshots_Examples_Usage/Screenshot_github_agent_2.jpeg) 

---

## Limitations & Workarounds

### ADK Tool Restrictions

Some built-in ADK tools (for example `google_search` and code execution) typically **cannot be combined within a single agent instance**.

**Workaround:**

* Create **specialized agents** (e.g. `SearchAgent`, `CodeAgent`)
* Orchestrate them exclusively via the **RootAgent**
* Delegate requests using `AgentTool.create()`

This preserves architectural clarity while respecting ADK constraints.

---

### Model Variability

LLM responses may vary between runs, even with identical inputs.

**Mitigation:**

* Avoid relying on implicit determinism
* Explicitly test and validate determinism in **production-critical workflows**
* Prefer structured outputs where possible

---

### API Quotas & Billing

Usage is subject to **Vertex AI / Google Cloud quotas and billing limits**.

**Recommendation:**

* Monitor usage and costs closely
* Set budget alerts and quota thresholds
* Test new agents or models in controlled environments first

---

## Contributing

Contributions are welcomed to improve the ADK Toolkit! Suggested workflow:  

1. Fork the GitHub repository
2. Create a feature branch:
```bash
git checkout -b feat/your-feature
```
3. Commit and push your changes  
4. Submit a Pull Request and describe your contribution.  

Please follow the repository code style and add tests for major features.

---

## Future Implementations

We actively welcome contributors who want to help **extend the system without compromising its architectural guarantees**. The following items represent suggested and validated directions for future work.

### Intentional Model Selection

The current implementation uses `gemini-2.5-flash` across agents. A promising improvement is to **intentionally mix Gemini models by responsibility**. For example, upgrading **AIDevSearchAgent** to `gemini-2.5-pro` and evaluating trade-offs:

| Aspect     | Expected Impact      |
| ---------- | -------------------- |
| Latency    | Slightly higher      |
| Cost       | Higher per token     |
| Throughput | Lower                |
| Quality    | Significantly higher |

This enables controlled experimentation around **quality vs cost vs latency**, while preserving RootAgent orchestration.

---

### Additional AgentTools

* Add new `AgentTool`s **without destabilizing** existing flows
* Preserve RootAgent-only delegation
* Avoid agent-to-agent invocation chains

---

### Structured Outputs

* Produce **machine-readable JSON outputs** for headlines and summaries
* Enable downstream automation and evaluation pipelines

---

### Session & State Management

* Persistent session storage across restarts
* Reproducible conversations and debugging support

---

### Search & Retrieval Refinements

* Filters (e.g. *only open-source*)
* Date ranges and recency controls
* Improved relevance scoring

---

### UI & Observability

* UI buttons for explicit selection and confirmation
* Debug / observability modes
* Clear visibility into control vs data flow at runtime

---

### Stronger Execution Guardrails

* Tighter resource limits
* Enhanced sandbox policies
* Explicit failure modes and reporting


Feel free to suggest more ideas by opening an issue or starting a discussion! For bug reports or feature requests, 
 [open an issue](https://github.com/micag2025/Toolkit_Google_ADK/issues).  

---

## References  

- [Google AI Studio](https://cloud.google.com/free?hl=en)
- [Gemini API key](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/quickstart?usertype=apikey#python-gen-ai-sdk)
- [Gemini Models](https://ai.google.dev/gemini-api/docs/models#model-variations)  
- [Tools for Agents](https://google.github.io/adk-docs/tools/)  
- [Limitations for ADK tools](https://google.github.io/adk-docs/tools/limitations/)  
- [The Open Source Repository Guide: Best Practices for Sharing Your AI/ML and Data Science Projects](https://app.readytensor.ai/publications/best-practices-for-ai-project-code-repositories-0llldKKtn8Xb)  
- [Markdown for Machine Learning Projects: A Comprehensive Guide](https://app.readytensor.ai/publications/markdown-for-machine-learning-projects-a-comprehensive-guide-LX9cbIx7mQs9)    

---

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/micag2025/Toolkit_Google_ADK/blob/d18bda56849caea6efeda3803da893b29d5bfa23/LICENSE) file for details.

---

## Contact

If you encounter bugs, have questions, or want to request a new feature, please [open an issue](https://github.com/micag2025/Toolkit_Google_ADK/issues) on this repository.  

---

## Acknowledgements

An acknowledgement to **Ready Tensor developer community** for creating a vibrant ecosystem where AI professionals can share projects, insights, and innovations, playing a meaningful role in accelerating the advancement of AI technology and in shaping practical, real-world developer tools such as this project.    
