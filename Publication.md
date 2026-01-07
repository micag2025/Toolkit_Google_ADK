# Designing a Safe Multi-Agent Developer Assistant with Google ADK      

---
![cover_Image](https://github.com/micag2025/Toolkit_Google_ADK/blob/a5f9dd6f448c88fd5fda4c816d5bb509236f3e17/Cover_image_publication.png)
---

## Tags  

`multi-agent-systems`, `llm-agents`, `agent-development-kit`, `google-adk`, `gemini-models`, `developer-intelligence`, `code-assistant`, `huggingface`, `github`, `mcp`, `tool-grounded-ai`, `agent-routing`, `agent-orchestration`, `open-source`,` web-ui`  


## Author  

Michela Agostini 


## TL;DR  

This project demonstrates how to design, orchestrate, and deploy a **safe, tool‑grounded, multi‑agent developer assistant** using **Google Agent Development Kit (ADK)** and **Gemini models**.  

The system implements a **strictly routed multi‑agent architecture** where a central RootAgent orchestrates specialist agents for:  
- Real‑time AI developer news discovery  
- Safe Python code execution and explanation  
- Enrichment via Hugging Face and GitHub  

The result is an **opinionated developer‑intelligence toolkit** that prioritizes **safety, determinism, and architectural clarity**, while remaining extensible for real‑world production use. This ADK Toolkit is designed not only for AI developers, since it supports a wide range of technical and non-technical users such as  Ready Tensor users, ML Engineers, Researchers, Technical Writers.     

---

## Key Highlights    

- Interactive **ADK Web UI** for agent experimentation  
- **Central RootAgent** enforcing deterministic routing  
- Real‑time web discovery using `google_search`  
- Secure Python execution via ADK’s sandboxed executor
- Explanation Python code   
- Modular integrations with **Hugging Face** and **GitHub**    

---

## Core Capabilities  

- **Real‑time conversational agents** with web access.  
- **Multi‑agent orchestration** with strict separation of concerns.
- **Production‑ready design**: guardrails, logging, and deployment support via Vertex AI Agent Engine

---

## Target Users & Use Cases  

This toolkit supports a broad range of users across the AI development lifecycle. By combining specialist agents with explicit tool constraints, users can retrieve high‑signal information, execute safe code, and access authoritative references without managing agent complexity directly.

The following table gives an overview of use cases that illustrate how different user roles can leverage the toolkit to address role-specific needs, highlighting its flexibility, practical relevance, and applicability beyond expert AI practitioners.  

|  User Role        | Value Delivered                    | Example Use Cases                          |
| ----------------- | ---------------------------------- | -------------------------------------------|
| ML Engineers      | AI tooling insights                | Compare open‑source models, frameworks     |
| Backend Engineers | AI relevance without ML overhead   | Identify deployable AI tools               |
| MLOps Engineers   | Deployment signals                 | Assess model maturity and ops readiness    |
| Tech Leads        | Strategic summaries                | Weekly AI trend overviews                  |
| Dev Advocates     | Clear narratives                   | Explain AI articles to non‑experts         |
| Product Managers  | Competitive insight                | Open‑source vs proprietary analysis        |
| Researchers       | Research‑to‑practice bridge        | Discover implementations of papers         |
| Students          | Guided learning                    | Learn Python and AI tooling                |

---

## Architecture (High-Level)    
The application is built using a state-aware, **RootAgent-centric multi-agent architecture** powered by **Google ADK** and **Gemini models**.  

At a high level, the system consists of:  

1. **ADK Web UI**: Handles user input, headline selection, and explicit execution requests.  
2. **Session state**: Maintains lightweight UI state, such as retrieved headlines, user selections and interaction context.   
3. **RootAgent (Router / Orchestrator)**: Performs deterministic intent classification and delegates requests to specialist agents.
4. **Specialist agents**: Purpose-built agents responsible for a single, well-defined task:   
   - AIDevSearchAgent — AI developer news discovery  
   - CodeAgent — safe Python execution
   - CodeExplainAgent — Python code explanation  
   - HuggingFaceAgent — canonical Hugging Face references
   - GitHubAgent — GitHub repository inspection
  
The below table shows the main **Agent Responsibilities**

| Agent                | Purpose                         | Capabilities                                                                                      | Constraints                                                            |
| -------------------- | ------------------------------- | ------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **RootAgent**        | Central router and orchestrator | • Intent detection<br>• Deterministic routing<br>• Delegation to specialist agents                | • Never answers directly<br>• No tool calls<br>• Delegation only       |
| **AIDevSearchAgent** | AI developer news discovery     | • Search AI dev news<br>• Headline extraction<br>• Structured summaries<br>• Uses `google_search` | • AI content only<br>• Must use `google_search`<br>• No code execution |
| **CodeAgent**        | Safe Python execution           | • Execute Python code<br>• Return raw output or errors                                            | • Python only<br>• No filesystem<br>• No network<br>• No explanations  |
| **CodeExplainAgent** | Explain Python code             | • Step-by-step explanation<br>• Highlight logic and pitfalls                                      | • No execution<br>• No code modification                               |
| **HuggingFaceAgent** | Canonical HF references         | • Validate exact HF IDs<br>• Return official URLs                                                 | • Exact IDs only<br>• No guessing<br>• No recommendations              |
| **GitHubAgent**      | GitHub repository inspection    | • Fetch repo metadata<br>• Stars, issues, PRs<br>• Recent activity via MCP                        | • Explicit `owner/repo` required<br>• No discovery<br>• No inference   |

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
║  │   Agent      │ │              │ │   Agent        │  │ Agent         │    │ Agent          │    ║
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
* Clarifies **execution, transport and authority**
* Supports audits, reviews, and future extension
* Prevents accidental agent autonomy or tool misuse

---

## Design Principles

* **Separation of concerns** – RootAgent routes, specialist agents execute
* **Deterministic workflows** – Minimal LLM guesswork for critical steps
* **Tool transparency** – Explicit tool usage and sources
* **Developer‑first UX** – Safe code execution and predictable outputs

---  

## Installation Instructions
This pubblication has a [GitHub code repository](https://github.com/micag2025/Toolkit_Google_ADK.git) attached also under the **Code** section.  

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

## Running the Application

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

### Understanding Advanced Instructions

This enhanced instruction pattern includes:

- **Clear Identity**: Explicitly defines the agent's role purpose
- **Refusal Mechanism**: Provides exact phrases for rejecting off-topic requests  
- **Workflow Requirements**: Forces the agent to use tools and cite sources
- **Behavioral Boundaries**: Sets expectations for valid vs. invalid requests

This creates a much more reliable and focused agent behavior.

### Testing Instructions    

You can test the enhanced multi-agent system using both **valid** and **invalid prompts**.  A full set of reproducible test prompts and expected behaviors is provided in the accompanying [GitHub repository](https://github.com/micag2025/Toolkit_Google_ADK.git).  

---  

## Examples Usage UI    

### ADK Web UI: 
![ADK_interface](https://github.com/micag2025/Toolkit_Google_ADK/blob/739b84b0c46e2b53255baa3bdc2a6614666bbc57/Screenshots_Examples_Usage/Screenshot_UI_interface.jpeg)

After selecting the appropriate app (`app_01`) from the dropdown menu from the ADK Web UI,  below is a high-signal, comprehensive set of prompt examples designed to systematically test the application end-to-end, aligned with the agent architecture, routing rules, MCP integrations, and UI flows.  

> _Note_ : Different Run Results: The output generated can vary with each execution due to their dynamic, probabilistic nature.     

---

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

![PythonExplainCode_Agent_3](https://github.com/micag2025/Toolkit_Google_ADK/blob/7f9f9847b6f6e58bc90626556ab965c883c994d6/Screenshots_Examples_Usage/Screenshot_code_explain_agent_3.jpeg)  

---

### 4.  Example Prompts: HuggingFace 
   
![HuggingFace_Agent_3](https://github.com/micag2025/Toolkit_Google_ADK/blob/7f9f9847b6f6e58bc90626556ab965c883c994d6/Screenshots_Examples_Usage/Screenshot_hf_agent_3.jpeg)

---

### 5.  Example Prompts: GitHub Code Execution    
             
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

- **Intentional Model Selection** : The current implementation uses `gemini-2.5-flash` across agents. A promising improvement is to `intentionally mix Gemini models by responsibility`. For example, upgrading `AIDevSearchAgent` to `gemini-2.5-pro` and evaluating trade-offs enables controlled experimentation around **quality vs cost vs latency**, while preserving RootAgent orchestration.  
  
- **Additional AgentTools** :  Add new `AgentTool`s `without destabilizing` existing flows, preserving  RootAgent-only delegation and avoiding agent-to-agent invocation chains.    

- **Structured Outputs**:  Produce `machine-readable JSON outputs` for headlines and summaries . Enable downstream automation and evaluation pipelines.  

- **Session & State Management**:  Persistent session storage across restarts.  Reproducible conversations and debugging support.  

- **Search & Retrieval Refinements** : Filters (e.g. *only open-source*).  Date ranges and recency controls. Improved relevance scoring.  

- **UI & Observability** :  UI buttons for explicit selection and confirmation.  Debug / observability modes. Clear visibility into control vs data flow at runtime.  

- **Stronger Execution Guardrails** :  Tighter resource limits. Enhanced sandbox policies. Explicit failure modes and reporting.  


Feel free to suggest more ideas by opening an issue or starting a discussion! For bug reports or feature requests, 
 [open an issue](https://github.com/micag2025/Toolkit_Google_ADK/issues).      

---    

## References  

- [Google AI Studio](https://cloud.google.com/free?hl=en)
- [Gemini API key](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/quickstart?usertype=apikey#python-gen-ai-sdk)
- [Gemini Models](https://ai.google.dev/gemini-api/docs/models#model-variations)  
- [Tools for Agents](https://google.github.io/adk-docs/tools/)  
- [Limitations for ADK tools](https://google.github.io/adk-docs/tools/limitations/)
- [Technical Evaluation Rubric](https://app.readytensor.ai/publications/technical-excellence-in-aiml-and-data-science-publications-an-evaluation-rubric-WsaE5uxLBqnH)
- [Engage and Inspire: Best Practices for Publishing on Ready Tensor](https://app.readytensor.ai/publications/engage-and-inspire-best-practices-for-publishing-on-ready-tensor-SBgkOyUsP8qQ)
- [The Open Source Repository Guide: Best Practices for Sharing Your AI/ML and Data Science Projects](https://app.readytensor.ai/publications/best-practices-for-ai-project-code-repositories-0llldKKtn8Xb)
- [Markdown for Machine Learning Projects: A Comprehensive Guide](https://app.readytensor.ai/publications/markdown-for-machine-learning-projects-a-comprehensive-guide-LX9cbIx7mQs9)  

---

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/micag2025/Toolkit_Google_ADK/blob/d18bda56849caea6efeda3803da893b29d5bfa23/LICENSE) file for details.

---

## Contact

michelaagostini73@gmail.com

---

## Acknowledgements  

An acknowledgement to **Ready Tensor developer community** for creating a vibrant ecosystem where AI professionals can share projects, insights, and innovations, playing a meaningful role in accelerating the advancement of AI technology and in shaping practical, real-world developer tools such as this project.  
