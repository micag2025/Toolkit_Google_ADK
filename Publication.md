# Designing a Safe Multi-Agent Developer Assistant with ADK    
# Toolkit Google ADK – Multi‑Agent Developer Assistant  

---
![cover_Image](https://github.com/micag2025/Toolkit_Google_ADK/blob/a5f9dd6f448c88fd5fda4c816d5bb509236f3e17/Cover_image_publication.png)
---

## Tags   
`multi-agent-systems`, `llm-agents`, `Agent Development Kit (ADK)`, `google-adk`, `gemini (models)`, `developer-intelligence`, `code-assistant`, `huggingface`, `github`, `mcp`, `tool-grounded-ai`, `agent-routing`, `agent-orchestration`, `open-source`, `web-ui`

## Author 
Michela Agostini 


## TL;DR:

This project is built using **Google Agent Development Kit (ADK)** with a clean multi-agent architecture,  giving an example toolkit that demonstrates how to build, orchestrate, and deploy multi-agent systems using Google’s Agent Development Kit (ADK). The project focuses on creating an **AI Developer Agent** capable of discovering real-time AI news, generating Python code, and integrating with developer platforms like Hugging Face and GitHub.  

Key goals:
- Real-time discovery and summarization of AI news relevant to developers
- Execute and return Python code results in a sandboxed environment
- Provide a clean, multi-agent architecture for reliable orchestration and extensibility  

The project is best described as `Agent-based developer intelligence with strict routing and tool grounding`. The system is a `Structured, agent-based, tool-grounded developer intelligence`. it’s an agent-based developer intelligence toolkit. It’s a developer intelligence system opinionated, structured, tool-grounded and role-aware.
This ADK Toolkit is designed for more than just AI developers. It supports a wide range of technical and non-technical users such as  Ready Tensor users, ML Engineers, Researchers, Technical Writers.   

---

## Highlights
- Interactive ADK Web UI for experimenting with agents
- Multi-agent orchestration with a RootAgent that routes to specialist agents
- Real-time web discovery using `google_search`
- Safe Python execution via ADK's sandboxed executor
- Extensible: plug in Hugging Face and GitHub integrations for richer developer signals

---

## Core capabilities

- **Real-time text agents**: natural conversational interaction with web access for up-to-date information.
- **Multi-agent orchestration**: coordinated workflows (e.g., researchers, planners, executors).
- **Production readiness**: guardrails, persistent memory, logging, and deployment on Vertex AI Agent Engine.

---
## Use Cases and Target Users  

This toolkit is designed to support a diverse set of users involved in the AI development lifecycle, ranging from researchers and machine learning engineers to backend developers and product stakeholders. By combining multiple specialized agents with strict routing and tool-level constraints, the system enables users to access high-signal information, perform code-centric reasoning, and retrieve authoritative references across AI tooling ecosystems. The following use cases illustrate how different user roles can leverage the toolkit to address role-specific needs, highlighting its flexibility, practical relevance, and applicability beyond expert AI practitioners.  

| User Type         | Core Value Provided                | Representative Usage Examples                               |
| ----------------- | ---------------------------------- | ----------------------------------------------------------- |
| ML Engineers      | Deep insights into AI tooling      | Discover open-source LLM tools; compare Hugging Face models |
| Backend Engineers | AI relevance without ML overhead   | Identify AI tools suitable for backend services             |
| MLOps Engineers   | Deployment and maintenance signals | Assess model maturity and on-prem deployability             |
| Tech Leads        | High-level, actionable summaries   | Weekly AI developer trend summaries                         |
| Dev Advocates     | Structured technical narratives    | Explain AI articles for non-experts                         |
| Product Managers  | Strategic and competitive insight  | Identify proprietary vs open-source trends                  |
| Researchers       | Bridge research and implementation | Find working implementations of research ideas              |
| Students          | Guided learning and exploration    | Learn Python and AI tooling fundamentals                    |

---
## Tool Overview & Architecture  

## Architecture overview

High-level flow:
1. ADK Web UI: user input, headline selection, and execution requests.
2. Session state: tracks mode (news / code), last query, headlines, selections.
3. RootAgent: intent detection, context aggregation, and deterministic routing.
4. Specialist agents:
   - AIDevSearchAgent (news + google_search)
   - CodeAgent (sandboxed Python execution)  
   - HugginFaceAgent  
   - GitHib Agent  

Compact ASCII diagram:  

```bash  
RootAgent
   ├── AgentTool → AIDevSearchAgent → google_search
   ├── AgentTool → CodeAgent → BuiltInCodeExecutor  
   ├── AgentTool → CodeExplainAgent   
   ├── AgentTool → hugging_face_agent → HF MCP → HF Hub
   └── AgentTool → github_agent → GitHub MCP → GitHub
``` 
> _Note_: Final architectural rule :   
          - APIs belong to agents.    
          - Agents belong to RootAgent.  
>         - RootAgent never talks to APIs directly.  



The application is built using a **multi-agent architecture powered by Gemini models and Google ADK Web**. This application uses a **state-aware, multi-agent architecture** built with **Google ADK Web** and **Gemini models**, designed specifically for AI developers. The below schema diplays hows who decides, who executes, and where data comes from.

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

### AIDevSearchAgent

*(also known as the **AI Developer News Agent**)*

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

### CodeAgent

*(also known as the **Python Code Agent**)*

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

## Building AI Agents with ADK
**ADK Overview**  
- ADK provides modular components including models, tools, memory, and orchestration.    
- Supports both simple agents and complex multi-agent systems.   

**Text Agents**  
Create a text agent that:
- Takes text input.  
- Uses an LLM to reason and generate responses.  
- Integrates tools and APIs for executing real-world tasks.  
Evaluate agent sessions, memory, and state for reliability.
Extend capabilities with callbacks and guardrails for safe and predictable behavior.

**Specialized Agents**  
Design agents that:
Research topics.
Generate text  outputs using Gemini text-to-text models.
Combine multiple agents with orchestration to create coordinated workflows.  


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

## Design Principles

- Clear separation of concerns
- Deterministic workflows
- Minimal LLM guesswork
- Tool transparency
- Developer-first UX

---

### Understanding Advanced Instructions

This enhanced instruction pattern includes:

- **Clear Identity**: Explicitly defines the agent's sole purpose
- **Refusal Mechanism**: Provides exact phrases for rejecting off-topic requests  
- **Workflow Requirements**: Forces the agent to use tools and cite sources
- **Behavioral Boundaries**: Sets expectations for valid vs. invalid requests

This creates a much more reliable and focused agent behavior.

### Testing Instructions    

You can test the enhanced multi-agent system using both **valid** and **invalid** prompts.  A full set of reproducible test prompts and expected behaviors is provided in the accompanying [GitHub repository](https://github.com/micag2025/Toolkit_Google_ADK.git).  

---  

## Examples Usage UI  

### ADK Web UI: 
![ADK_interface](https://github.com/micag2025/Toolkit_Google_ADK/blob/739b84b0c46e2b53255baa3bdc2a6614666bbc57/Screenshots_Examples_Usage/Screenshot_UI_interface.jpeg)  

After selecting the appropriate app (`app_01`) from the dropdown menu from the ADK Web UI,  below is a high-signal, comprehensive set of prompt examples designed to systematically test the application end-to-end, aligned with the agent architecture, routing rules, MCP integrations, and UI flows.    

> _Note_ : Different Run Results: The output generated can vary with each execution due to their dynamic, probabilistic nature.     

### 1. Example Prompts: AI News AIDevSearchAgent     
-  AI news discovery `General discovery (clarification expected)`:    
   - Ask: "What's the latest AI news about Google?" → Should ask: “How many news items would you like me to find?”  
   - Flow: RootAgent → AIDevSearchAgent → google_search → summarize & cite sources.

![Google_Search_Agent_1](https://github.com/micag2025/Toolkit_Google_ADK/blob/739b84b0c46e2b53255baa3bdc2a6614666bbc57/Screenshots_Examples_Usage/Screenshot_AIDevSearchAgent_1.jpeg)

![Google_Search_Agent_2](https://github.com/micag2025/Toolkit_Google_ADK/blob/739b84b0c46e2b53255baa3bdc2a6614666bbc57/Screenshots_Examples_Usage/Screenshot_AIDevSearchAgent_2.jpeg)  

-  AI news discovery `Focused topic`:
   - Ask: “Any recent news about RAG frameworks for developers?”   

![Google_Search_Agent_3](https://github.com/micag2025/Toolkit_Google_ADK/blob/739b84b0c46e2b53255baa3bdc2a6614666bbc57/Screenshots_Examples_Usage/Screenshot_AIDevSearchAgent_3.jpeg)

### 2.  Example Prompts: Python Code Execution 
- Python execution:
   - Ask: "Run this Python code..." / "Execute python code: print(2 + 2)" / Simple execution and Data handling
   - Flow: RootAgent → CodeAgent → BuiltInCodeExecutor (sandbox) → return execution output (no extra commentary).  
     
![PythonDevelopr_Agent](https://github.com/micag2025/Toolkit_Google_ADK/blob/739b84b0c46e2b53255baa3bdc2a6614666bbc57/Screenshots_Examples_Usage/Screenshot_CodeAgent_1.jpeg)

### 3.  Example Prompts: Python Explain Code   
-  Python explain code
   - Ask :  "Explain this Python code:”
   - Flow: RootAgent → CodeExplainAgent  →  return explanation only (no execution).  
        
![PythonExplainCode_Agent](https://github.com/micag2025/Toolkit_Google_ADK/blob/739b84b0c46e2b53255baa3bdc2a6614666bbc57/Screenshots_Examples_Usage/Screenshot_CodeExplainAgent1.jpeg))  


### 4.  Example Prompts: HuggingFace 
- Enrichment:
   - RootAgent can request Hugging Face signals to rank or annotate discoveries.  
   - Flow: RootAgent → hugging_face_agent  →  return explanation.    
     
![HuggingFace_Agent](https://github.com/micag2025/Toolkit_Google_ADK/blob/2346fda5b929151f790eb73e30a15b6350158637/Screenshot_22-12-2025_145157_127.0.0.1.jpeg) 

- Direct queries  
  - Ask :“Show me popular Hugging Face models for text summarization”  
  - Flow: RootAgent → hugging_face_agent  →  return explanation    
    
![HuggingFace_Agent_1](https://github.com/micag2025/Toolkit_Google_ADK/blob/69f2d33c238f6360544ca3b733e74eb7f219c0b4/Screenshots_Examples_Usage/Screenshot_huggingfaceAgent_1.jpeg)

- Enrichment tests  
  - Ask :“Is this model available on Hugging Face: facebook/bart-large-cnn?” / Give me the Hugging Face link for mistralai/Mixtral-8x7B-Instruct-v0.1    
  - Flow: RootAgent → hugging_face_agent   →  *HF MCP Server"  →  return link     

!![HuggingFace_Agent_2](https://github.com/micag2025/Toolkit_Google_ADK/blob/69f2d33c238f6360544ca3b733e74eb7f219c0b4/Screenshots_Examples_Usage/Screenshot_huggingfaceAgent_2.jpeg)  


### 5.  Example Prompts: GitHub Code Execution    
-  Enrichment:
   - RootAgent can request Hugging Face signals to rank or annotate discoveries.   
   - Flow: RootAgent → github_agent  →  GitHub MCP Server → return explanation only     
         
![GitHub_tool](https://github.com/micag2025/Toolkit_Google_ADK/blob/a67aba7ca64eec68225e5120c11f8ed0b4f5d18c/Screenshot_28-12-2025_111447_127.0.0.1.jpeg)   


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
