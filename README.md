# Designing a Safe Multi-Agent Developer Assistant with Google ADK  
_An extensible toolkit for AI news, code execution, and MCP-based enrichment_

## Overview

This repository contains the full implementation for the publication **Designing a Safe Multi-Agent Developer Assistant with ADK**, published on the [Ready Tensor](https://www.readytensor.ai/) platform.  

This project is built with the **Google Agent Development Kit (ADK)** and serves as a reference **multi-agent developer intelligence toolkit**. It demonstrates how to design, orchestrate, and deploy agent-based systems with strict routing, tool grounding, and safety boundaries.

At its core is an **AI Developer Assistant** that can discover and summarize real-time AI news, safely execute and explain Python code, and integrate transparently with developer platforms such as Hugging Face and GitHub. The system follows a **RootAgent-centric architecture**: the RootAgent never responds directly, but instead performs deterministic routing to specialized agents, enforcing clear separation of concerns, predictable behavior, and auditable execution.

Designed for more than just AI developers, the toolkit also supports **Ready Tensor users, ML engineers, researchers, and technical writers**.

Overall, this repository illustrates how to build **safe, modular, and production-oriented multi-agent systems** using Google ADK.

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

Design rationale, architectural trade-offs, and **control- vs data-flow diagrams** are discussed in the **accompanying Ready Tensor publication**.

---

## Agent Responsibilities  

| Agent                | Purpose                         | Capabilities                                                                                      | Constraints                                                            |
| -------------------- | ------------------------------- | ------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **RootAgent**        | Central router and orchestrator | • Intent detection<br>• Deterministic routing<br>• Delegation to specialist agents                | • Never answers directly<br>• No tool calls<br>• Delegation only       |
| **AIDevSearchAgent** | AI developer news discovery     | • Search AI dev news<br>• Headline extraction<br>• Structured summaries<br>• Uses `google_search` | • AI content only<br>• Must use `google_search`<br>• No code execution |
| **CodeAgent**        | Safe Python execution           | • Execute Python code<br>• Return raw output or errors                                            | • Python only<br>• No filesystem<br>• No network<br>• No explanations  |
| **CodeExplainAgent** | Explain Python code             | • Step-by-step explanation<br>• Highlight logic and pitfalls                                      | • No execution<br>• No code modification                               |
| **HuggingFaceAgent** | Canonical HF references         | • Validate exact HF IDs<br>• Return official URLs                                                 | • Exact IDs only<br>• No guessing<br>• No recommendations              |
| **GitHubAgent**      | GitHub repository inspection    | • Fetch repo metadata<br>• Stars, issues, PRs<br>• Recent activity via MCP                        | • Explicit `owner/repo` required<br>• No discovery<br>• No inference   |

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

- **Prerequisites:**

  - Python 3.10+  
  - Google Cloud account with Vertex AI / Gemini access  
  - (Optional) Hugging Face and GitHub API keys  

- **Clone and install:**

```bash
git clone https://github.com/micag2025/Toolkit_Google_ADK.git
cd Toolkit_Google_ADK
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

- **Configure environment variables (see .env.example):**

```env
GEMINI_API_KEY=your_gemini_api_key
HF_API_KEY=your_hf_api_key
GIT_API_KEY=your_github_api_key
ADK_DEV_MODE=true
```

> _Notes:_  
> - The project expects API keys to be correctly provisioned for Vertex AI / Gemini usage.
> - You can create a [Gemini API key](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/quickstart?usertype=apikey#python-gen-ai-sdk). This key is essential for authenticating your requests to the Gemini API. A step-by-step guide can be found on o [Google AI Studio](https://cloud.google.com/free?hl=en)


- **Start the ADK Web UI:**

```bash
adk web
```

ADK will provide a local URL. Open it in your browser. From the Google ADK user interface in the left pane, select the `app_01` agent. You can now interact with the ADK AI Developer.    

- **Stop the ADK process if needed:**  

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

## Testing and prompts

Each agent in the system accepts **strictly scoped prompt types**. Testing should include both **valid** and **invalid** prompts to verify correct routing, enforced guardrails, MCP usage, and safe failure behavior.

**Agent scopes (at a glance):**

- **AIDevSearchAgent:** AI developer news discovery and summarization (via `google_search`)  
- **CodeAgent:** sandboxed Python execution only (no network or filesystem)  
- **CodeExplainAgent:** Python code explanation only (no execution)
- **hugging_face_agent / github_agent:** read-only metadata lookups (no discovery or recommendations)

Use valid prompts to confirm expected behavior, and invalid prompts to ensure the system **refuses, redirects, or degrades safely**.

### AIDevSearchAgent — AI developer news

Discovers and summarizes AI news relevant to developers, returning headlines and concise summaries backed by sources.

| ✅ Valid prompts                              | ❌ Invalid prompts           |
| -------------------------------------------- | --------------------------- |
| “Give me AI news for Google”                 | “What’s the weather today?” |
| “Give me 3 top AI news items for developers” | “Give me sports news”       |
| “Tell me more about the first one”           | “Celebrity gossip”          |
| “Recent AI developer news from Meta”         | “Apple stock price”         |
| “AI tooling news for Python developers”      | “Movie releases this week”  |


### CodeAgent — Python execution (sandboxed)

Executes user-provided Python in a restricted environment and returns raw output or errors only.

| ✅ Valid prompts                                    | ❌ Invalid prompts                    |
| -------------------------------------------------- | ------------------------------------ |
| `Execute python code: print(sum(range(10)))`       | `import os; os.listdir()`            |
| `Execute python code: import math; math.sqrt(16)`  | `import requests; requests.get(...)` |
| `Execute python code: sum(i*i for i in range(10))` | `while True: pass`                   |
| `Execute python code: [x*2 for x in range(5)]`     | `open("file.txt")`                   |


### CodeExplainAgent — Python explanation (no execution)

Explains code logic, intent, and edge cases. Good for pedagogical, line‑by‑line, or conceptual explanations. This agent does not run code.

| ✅ Valid prompts                                    | ❌ Invalid prompts                |
| -------------------------------------------------- | -------------------------------- |
| “Explain this Python code”                         | “Execute this code”              |
| “Explain this line by line for a junior developer” | “Explain this JavaScript code”   |
| “What does this loop do?”                          | “Rewrite and optimize this code” |
| “Explain possible pitfalls in this function”       | “Convert this code to Rust”      |


### Hugging Face agent — exact ID lookups  

Performs exact, read-only lookups for Hugging Face models or datasets. Not a recommendation engine.

| ✅ Valid prompts                                                | ❌ Invalid prompts           |
| -------------------------------------------------------------- | --------------------------- |
| “Hugging Face link for `mistralai/Mixtral-8x7B-Instruct-v0.1`” | “Show popular HF models”    |
| “Is `facebook/bart-large-cnn` available?”                      | “Recommend a HF model”      |
| “Link for `google/pegasus-arxiv`”                              | “Rank models by popularity” |


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

![Google_Search_Agent_1](https://github.com/micag2025/Toolkit_Google_ADK/blob/7f9f9847b6f6e58bc90626556ab965c883c994d6/Screenshots_Examples_Usage/Screenshot_Aidevsearch_1.jpeg)

![Google_Search_Agent_2](https://github.com/micag2025/Toolkit_Google_ADK/blob/7f9f9847b6f6e58bc90626556ab965c883c994d6/Screenshots_Examples_Usage/Screenshot_Aidevseach_2.jpeg)  

![Google_Search_Agent_3](https://github.com/micag2025/Toolkit_Google_ADK/blob/7f9f9847b6f6e58bc90626556ab965c883c994d6/Screenshots_Examples_Usage/Screenshot_Aidevsearch_3.jpeg)

---

### 2.  Example Prompts: Python Code Execution 
     
![PythonDevelopr_Agent](https://github.com/micag2025/Toolkit_Google_ADK/blob/7f9f9847b6f6e58bc90626556ab965c883c994d6/Screenshots_Examples_Usage/Screenshot_code_agent_1.jpeg)

---

### 3.  Example Prompts: Python Explain Code   
        
![PythonExplainCode_Agent_1](https://github.com/micag2025/Toolkit_Google_ADK/blob/7f9f9847b6f6e58bc90626556ab965c883c994d6/Screenshots_Examples_Usage/Screenshot_code_explain_agent_1.jpeg)

![PythonExplainCode_Agent_2](https://github.com/micag2025/Toolkit_Google_ADK/blob/7f9f9847b6f6e58bc90626556ab965c883c994d6/Screenshots_Examples_Usage/Screenshot_code_explain_agent_2.jpeg)  

---

### 4.  Example Prompts: HuggingFace 
    
![HuggingFace_Agent_3](https://github.com/micag2025/Toolkit_Google_ADK/blob/7f9f9847b6f6e58bc90626556ab965c883c994d6/Screenshots_Examples_Usage/Screenshot_hf_agent_3.jpeg)

---

### 5.  Example Prompts: GitHub Code Execution    
             
![GitHub_Agent_1](https://github.com/micag2025/Toolkit_Google_ADK/blob/7f9f9847b6f6e58bc90626556ab965c883c994d6/Screenshots_Examples_Usage/Screenshot_github_agent_1.jpeg)   

![GitHub_Agent_2](https://github.com/micag2025/Toolkit_Google_ADK/blob/7f9f9847b6f6e58bc90626556ab965c883c994d6/Screenshots_Examples_Usage/Screenshot_github_agent_2.jpeg) 

---

## Limitations & Workarounds

### ADK Tool Constraints  

Some built-in ADK tools (such as `google_search` and code execution) **cannot be combined within a single agent**.  

**Workaround:**  

- Use **specialized agents** (e.g., `AIDevSearchAgent`, `CodeAgent`)    
- Route all requests through a central **RootAgent**    
- Delegate execution explicitly via AgentTool    

This approach respects ADK constraints while preserving clear separation of responsibilities.  

### Model Variability

LLM outputs may vary between runs, even with identical inputs.

**Mitigation:**

- Do not assume implicit determinism  
- Validate behavior explicitly in **production-critical paths**  
- Prefer **structured outputs** and constrained instructions where possible  

### API Quotas & Billing

Usage is subject to **Vertex AI / Google Cloud quotas and billing limits**.

**Recommendation:**

-  Monitor usage and costs closely    
- Configure budget alerts and quota thresholds  
- Test new agents and models in controlled environments before scaling  

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

The current system uses gemini-2.5-flash for all agents. A natural next step is to select models by responsibility, rather than uniformly.  For example, upgrading AIDevSearchAgent to gemini-2.5-pro enables higher-quality summarization at a known trade-off:  

| Aspect     | Expected Impact      |
| ---------- | -------------------- |
| Latency    | Slightly higher      |
| Cost       | Higher per token     |
| Throughput | Lower                |
| Quality    | Significantly higher |

This enables controlled experimentation around **quality, cost and latency**, while preserving RootAgent centric orchestration.


### Additional AgentTools

* Add new `AgentTool`s **without destabilizing** existing flows
* Preserve **RootAgent-only delegation**
* Avoid agent-to-agent invocation chains


### Structured Outputs

* Produce **machine-readable JSON outputs** for headlines and summaries
* Enable downstream automation, evaluation and analytics pipelines  


### Session & State Management

* Persistent session storage across restarts
* Reproducible conversations for debugging and evaluation


### Search & Retrieval Refinements

* Content filters (e.g. *open-source only*)
* Date ranges and recency controls
* Improved relevance  


### UI & Observability

* Explicit UI controls for selection and confirmation  
* Debug and observability modes  
* Clear visibility into **control vs data flow** at runtime


### Stronger Execution Guardrails
* Tighter resource limits
* Enhanced sandbox policies
* Explicit failure modes and structured error reporting  


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
