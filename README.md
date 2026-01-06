# Designing a Safe Multi-Agent Developer Assistant with Google ADK  
_An extensible toolkit for AI news, code execution, and MCP-based enrichment_

## Overview

This repository contains the full implementation for the publication **Designing a Safe Multi-Agent Developer Assistant with ADK**, published on the [Ready Tensor](https://www.readytensor.ai/) platform.  

The project is built using the **Google Agent Development Kit (ADK)** and provides a multi-agent architecture, thus a reference **multi-agent developer intelligence toolkit** that demonstrates how to build, orchestrate, and deploy agent-based systems with strict routing and tool grounding. At its core, the system implements an **AI Developer Assistant** capable of discovering and summarizing real-time AI news relevant to developers, executing and explaining Python code safely, and integrating transparently with developer platforms such as **Hugging Face** and **GitHub**.  

The architecture is centered around a **RootAgent-based design** designed for developers.  The RootAgent never answers user queries directly. Instead, it performs deterministic intent detection and **routes each request to a specialized agent**, enforcing clear separation of responsibilities,  predictable, auditable behaviorand strong safety and tooling boundaries

This sysyem (toolkit)  is designed not only for AI developers, but also for a broader audience including Ready Tensor users,  ML Engineers and Researchers and Technical Writers.    

Overall, this repository serves as an **extensible ADK toolkit** illustrating how to design safe, modular, and production-oriented multi-agent systems using Google ADK.    

---

## Key Highlights    

- Interactive **ADK Web UI** for agent experimentation  
- **Central RootAgent** enforcing deterministic routing  
- Real‑time web discovery using `google_search`  
- Secure Python execution via ADK’s sandboxed executor  
- Modular integrations with **Hugging Face** and **GitHub**    

---

## Architecture (High-Level)  

The application is built using a state-aware, RootAgent-centric multi-agent architecture powered by Google Agent Development Kit (ADK) and Gemini models.  

At a high level, the system consists of:  

1. **ADK Web UI**: Handles user input, headline selection, and explicit execution requests.  
2. **Session state**: Maintains lightweight UI state, such as:Retrieved headlines, User selections and Interaction context (No business logic or routing decisions are stored here.)  
3. **RootAgent (Router / Orchestrator)**: Performs deterministic intent classification and delegates requests to specialist agents.
4. **Specialist agents**: Purpose-built agents responsible for a single, well-defined task:   
   - AIDevSearchAgent — AI developer news discovery  
   - CodeAgent — safe Python execution
   - CodeExplainAgent — Python code explanation  
   - HuggingFaceAgent — canonical Hugging Face references
   - GitHubAgent — GitHub repository inspection  

---

| Agent                | Purpose                         | Capabilities                                                                                      | Constraints                                                            |
| -------------------- | ------------------------------- | ------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **RootAgent**        | Central router and orchestrator | • Intent detection<br>• Deterministic routing<br>• Delegation to specialist agents                | • Never answers directly<br>• No tool calls<br>• Delegation only       |
| **AIDevSearchAgent** | AI developer news discovery     | • Search AI dev news<br>• Headline extraction<br>• Structured summaries<br>• Uses `google_search` | • AI content only<br>• Must use `google_search`<br>• No code execution |
| **CodeAgent**        | Safe Python execution           | • Execute Python code<br>• Return raw output or errors                                            | • Python only<br>• No filesystem<br>• No network<br>• No explanations  |
| **CodeExplainAgent** | Explain Python code             | • Step-by-step explanation<br>• Highlight logic and pitfalls                                      | • No execution<br>• No code modification                               |
| **HuggingFaceAgent** | Canonical HF references         | • Validate exact HF IDs<br>• Return official URLs                                                 | • Exact IDs only<br>• No guessing<br>• No recommendations              |
| **GitHubAgent**      | GitHub repository inspection    | • Fetch repo metadata<br>• Stars, issues, PRs<br>• Recent activity via MCP                        | • Explicit `owner/repo` required<br>• No discovery<br>• No inference   |

---

## Architecture Overview (Control Flow vs Data Flow)

The diagrams below highlight the strict separation between **control flow*** and **data flow** in the system. **Control flow** is centrally managed 
by the `RootAgent`, which receives all user input, performs intent classification, and deterministically routes requests to the appropriate specialist agent. The `RootAgent` never generates user-facing answers itself. **Data flow** occurs only within specialist agents and their attached tools (such as `google_search`, GitHub MCP, and Hugging Face MCP), where external data is retrieved, processed, and returned as structured outputs. This design enforces clear responsibility boundaries, predictable behavior, and tool-grounded execution across the multi-agent architecture.

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

## Tool & Agent Mapping  

This section provides a **concise, authoritative mapping** between agents, tools, and execution backends. It complements the architecture diagrams by making *attachments, responsibilities, and transport mechanisms explicit*.  

| Component              |  Type                 | Attached To        |   Purpose                                     |
| ---------------------- | ----------------------| ------------------ | -------------------------------------------- |
| AIDevSearchAgent       | AgentTool             | RootAgent          | Discover & summarize AI developer news       |
| CodeAgent              | AgentTool             | RootAgent          | Execute Python code safely                   |
| CodeExplainAgent       | AgentTool             | RootAgent          | Explain Python code safely                   |
| hugging_face_agent     | AgentTool + MCP       | RootAgent          | Hugging Face data (models, datasets, spaces) access      |
| github_agent           | AgentTool + MCP       | RootAgent          |GitHub insights                               |
| google_search          | ADK Tool              | AIDevSearchAgent   | Web discovery                                |
| BuiltInCodeExecutor    | ADK Executor          | CodeAgent          | Deterministic Python sandbox                 |

**Why this matters:**

* Makes **agent–tool attachment explicit**
* Clarifies **execution vs transport vs authority**
* Supports audits, reviews, and future extension
* Prevents accidental agent autonomy or tool misuse

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
│   ├── Screenshot_CodeExplainAgent2.jpeg
│   ├── Screenshot_CodeExplainAgent3.jpeg
│   ├── Screenshot_HuggingFaceAgent1.jpeg
│   ├── Screenshot_HuggingFaceAgent2.jpeg
│   ├── Screenshot_HuggingFaceAgent3.jpeg
│   ├── Screenshot_GitHubAgent1.jpeg
│   ├── Screenshot_GitHubAgent2.jpeg

```
> _Note_: For hands-on learning and experimentation, [`Notebbook_app_001.ipynb`](https://github.com/micag2025/Toolkit_Google_ADK/blob/96b5476392dc201e4710fbf9aa76c7bb0fa63d99/Notebook_app_01.ipynb)
 demonstrates:  
>- Setting up a new agent folder (`adk create`)
>- Writing the  `agent.py`
>- Adding text models and built-in tools (`google_search`, `BuiltInCodeExecutor`)
>- Fine-tuning agent instructions and behavior
>- Testing valid and invalid prompts

---

## Getting Started

This section shows how to install dependencies, configure authentication, and run the full pipeline.  

Prerequisites:

- Python 3.10+
- Google Cloud account with Vertex AI / Gemini access
- (Optional) Hugging Face and GitHub API keys

Clone and install:

```bash
git clone https://github.com/micag2025/Toolkit_Google_ADK.git
cd Toolkit_Google_ADK
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Configure environment variables (see .env.example):

```env
GEMINI_API_KEY=your_gemini_api_key
HF_API_KEY=your_hf_api_key
GIT_API_KEY=your_github_api_key
ADK_DEV_MODE=true
```

> _Notes:_  
> - The project expects API keys to be correctly provisioned for Vertex AI / Gemini usage.
> - You can create a [Gemini API key](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/quickstart?usertype=apikey#python-gen-ai-sdk). This key is essential for authenticating your requests to the Gemini API. A step-by-step guide can be found on o [Google AI Studio](https://cloud.google.com/free?hl=en)


Start the ADK Web UI:

```bash
adk web
```

ADK will provide a local URL. Open it in your browser. From the Google ADK user interface in the left pane, select the `app_01` agent. You can now interact with the ADK AI Developer.    

Stop the ADK process if needed:

```bash
pkill -f "adk web"
```
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

---

## Testing and prompts

Each agent in the system accepts **strictly scoped prompt types**. Testing should include both **valid** and **invalid** prompts to verify correct routing, enforced guardrails, MCP usage, and safe failure behavior.

**Agent scopes (at a glance):**

- **AIDevSearchAgent:** AI developer news discovery and summarization (via `google_search`)  
- **CodeAgent:** sandboxed Python execution only (no network or filesystem)  
- **CodeExplainAgent:** Python code explanation only (no execution)
- **hugging_face_agent / github_agent:** read-only metadata lookups (no discovery or recommendations)

Use valid prompts to confirm expected behavior, and invalid prompts to ensure the system **refuses, redirects, or degrades safely**.

---

### AIDevSearchAgent — — AI developer news

Discovers and summarizes AI news relevant to developers, returning headlines and concise summaries backed by sources.

| ✅ Valid prompts                              | ❌ Invalid prompts           |
| -------------------------------------------- | --------------------------- |
| “Give me AI news for Google”                 | “What’s the weather today?” |
| “Give me 3 top AI news items for developers” | “Give me sports news”       |
| “Tell me more about the first one”           | “Celebrity gossip”          |
| “Recent AI developer news from Meta”         | “Apple stock price”         |
| “AI tooling news for Python developers”      | “Movie releases this week”  |

---

### CodeAgent — Python execution (sandboxed)

Executes user-provided Python in a restricted environment and eeturns raw output or errors only.

| ✅ Valid prompts                                    | ❌ Invalid prompts                    |
| -------------------------------------------------- | ------------------------------------ |
| `Execute python code: print(sum(range(10)))`       | `import os; os.listdir()`            |
| `Execute python code: import math; math.sqrt(16)`  | `import requests; requests.get(...)` |
| `Execute python code: sum(i*i for i in range(10))` | `while True: pass`                   |
| `Execute python code: [x*2 for x in range(5)]`     | `open("file.txt")`                   |

---

### CodeExplainAgent — Python explanation (no execution)

Explains code logic, intent, and edge cases. Good for pedagogical, line‑by‑line, or conceptual explanations. This agent does not run code.

| ✅ Valid prompts                                    | ❌ Invalid prompts                |
| -------------------------------------------------- | -------------------------------- |
| “Explain this Python code”                         | “Execute this code”              |
| “Explain this line by line for a junior developer” | “Explain this JavaScript code”   |
| “What does this loop do?”                          | “Rewrite and optimize this code” |
| “Explain possible pitfalls in this function”       | “Convert this code to Rust”      |

---

### Hugging Face agent — exact ID lookups  

Performs exact, read-only lookups for Hugging Face models or datasets. Not a recommendation engine.

| ✅ Valid prompts                                                | ❌ Invalid prompts           |
| -------------------------------------------------------------- | --------------------------- |
| “Hugging Face link for `mistralai/Mixtral-8x7B-Instruct-v0.1`” | “Show popular HF models”    |
| “Is `facebook/bart-large-cnn` available?”                      | “Recommend a HF model”      |
| “Link for `google/pegasus-arxiv`”                              | “Rank models by popularity” |

---

### GitHub agent — repository inspection

Inspects explicitly referenced repositories and returns metadata and activity signals.  

| ✅ Valid prompts                            | ❌ Invalid prompts               |
| ------------------------------------------ | ---------------------------------- |
| “Show details of `langchain-ai/langchain`” | “Find good GitHub repos for AI”    |
| “Summarize `github.com/openai/evals`”      | “Who maintains the best AI repos?” |
| “Summarize activity for LangChain”         | “Search GitHub for trending LLMs”  |
| “Repo stats for `crewAIInc/crewAI`”        | “Which repo should I use?”         |

---

## UI Walkthrough & Example Runs

### ADK Web UI: 
![ADK_interface](https://github.com/micag2025/Toolkit_Google_ADK/blob/739b84b0c46e2b53255baa3bdc2a6614666bbc57/Screenshots_Examples_Usage/Screenshot_UI_interface.jpeg)

After selecting the appropriate app (`app_01`) from the dropdown menu from the ADK Web UI,  below is a high-signal, comprehensive set of prompt examples designed to systematically test the application end-to-end, aligned with the agent architecture, routing rules, MCP integrations, and UI flows.  

> _Note_ : Different Run Results: The output generated can vary with each execution due to their dynamic, probabilistic nature.     

### 1. Example Prompts: AI News AIDevSearchAgent     
-  AI news discovery `General discovery (clarification expected)`:    
   - Ask: "What's the latest AI news about Google?" → After poviding a list of 3 headlines  → Should ask: “Which headline would you explore in more details”  
   - Flow: RootAgent → AIDevSearchAgent → `google_search` → summarize & cite sources    

![Google_Search_Agent_1](https://github.com/micag2025/Toolkit_Google_ADK/blob/7f9f9847b6f6e58bc90626556ab965c883c994d6/Screenshots_Examples_Usage/Screenshot_Aidevsearch_1.jpeg)

![Google_Search_Agent_2](https://github.com/micag2025/Toolkit_Google_ADK/blob/7f9f9847b6f6e58bc90626556ab965c883c994d6/Screenshots_Examples_Usage/Screenshot_Aidevseach_2.jpeg)  

-  AI news discovery `Invalid prompts`:
   - Ask: “What’s the weather today?”   → Should say:"My capabilities are limited only to AI developrs news. 

![Google_Search_Agent_3](https://github.com/micag2025/Toolkit_Google_ADK/blob/7f9f9847b6f6e58bc90626556ab965c883c994d6/Screenshots_Examples_Usage/Screenshot_Aidevsearch_3.jpeg)

>_Note_: **Workflow:**    
>         1. Clarify the number of items to retrieve  
>         2. Search and filter AI‑related content  
>         3. Present candidate headlines  
>         4. Summarize selected items  

---

### 2.  Example Prompts: Python Code Execution 
- Python execution (`valid prompt):
   - Ask: "Execute python code:→  Simple execution and Data handling
   - Flow: RootAgent → CodeAgent → BuiltInCodeExecutor (sandbox) → return execution output (no extra commentary).
- Python execution (`invalid prompt`):
  - Ask: "Excute import os → Should cloarify the this operation is not allowed for secuirty reasons. 
     
![PythonDevelopr_Agent](https://github.com/micag2025/Toolkit_Google_ADK/blob/7f9f9847b6f6e58bc90626556ab965c883c994d6/Screenshots_Examples_Usage/Screenshot_code_agent_1.jpeg)

---

### 3.  Example Prompts: Python Explain Code   
-  Python explain code
   - Ask :  "Explain this Python code:” →  Should explain the given code
   - Flow: RootAgent → CodeExplainAgent  →  return explanation only (no execution).  
        
![PythonExplainCode_Agent_1](https://github.com/micag2025/Toolkit_Google_ADK/blob/7f9f9847b6f6e58bc90626556ab965c883c994d6/Screenshots_Examples_Usage/Screenshot_code_explain_agent_1.jpeg)

![PythonExplainCode_Agent_2](https://github.com/micag2025/Toolkit_Google_ADK/blob/7f9f9847b6f6e58bc90626556ab965c883c994d6/Screenshots_Examples_Usage/Screenshot_code_explain_agent_2.jpeg)  

![PythonExplainCode_Agent_3](https://github.com/micag2025/Toolkit_Google_ADK/blob/7f9f9847b6f6e58bc90626556ab965c883c994d6/Screenshots_Examples_Usage/Screenshot_code_explain_agent_3.jpeg)  

---

### 4.  Example Prompts: HuggingFace 
- Enrichment tests  
  - "validi prompt": Ask :“Is this model available on Hugging Face: facebook/bart-large-cnn?” / Give me the Hugging Face link for mistralai/Mixtral-8x7B-Instruct-v0.1    →  return link    
  - Flow: RootAgent → hugging_face_agent   →  *HF MCP Server"  →  return link     
 - `invalid prompt`: List HuggingFace for popularity  → Should clarify that this can not allowed. 
    
![HuggingFace_Agent_3](https://github.com/micag2025/Toolkit_Google_ADK/blob/7f9f9847b6f6e58bc90626556ab965c883c994d6/Screenshots_Examples_Usage/Screenshot_hf_agent_3.jpeg)

---

### 5.  Example Prompts: GitHub Code Execution    
-  Enrichment:
   - RootAgent can request Hugging Face signals to rank or annotate discoveries. Ask:  Show me details about https://github.com/langchain-ai/langgraph? → Return overview github
   - Flow: RootAgent → github_agent  →  GitHub MCP Server → return explanation only
- - `invalid prompt` Ask : Show me the repo for Langchain      
         
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
