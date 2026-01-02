# Designing a Safe Multi-Agent Developer Assistant with ADK  

This repository contains the full implementation for the publication **Designing a Safe Multi-Agent Developer Assistant with ADK**, published on the [Ready Tensor](https://www.readytensor.ai/) platform.

This project is built using **Google Agent Development Kit (ADK)** with a clean multi-agent architecture,  giving an example toolkit that demonstrates how to build, orchestrate, and deploy multi-agent systems using Google’s Agent Development Kit (ADK). The project focuses on creating an **AI Developer Agent** capable of discovering real-time AI news, generating Python code, and integrating with developer platforms like Hugging Face and GitHub.  

Key goals:
- Real-time discovery and summarization of AI news relevant to developers
- Execute and return Python code results in a sandboxed environment
- Provide a clean, multi-agent architecture for reliable orchestration and extensibility

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

The application is built using a **state-aware, multi-agent architecture powered by Gemini models and Google ADK Web**, designed specifically for AI developers.   

### Architecture Diagram (Control Flow vs Data Flow)

The architecture Diagram is based on a `Control Flow lane` and a `Data Flow lane` that identifies who decides and delegates and points out where data actually travels, respectively. 

- **Control Flow Lane answers** 
  - Who decides what happens next? 
  - Only RootAgent      
  - All agents are children      
  - No agent self-invokes       
  - No external system can trigger logic      

- **Data Flow Lane answers**:  
  - Where does execution/data actually go?    
  - Some flows stay local    
  - Some cross process boundaries    
  - Some cross network boundaries    
  - Transport differences do not imply authority    

```yaml
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
║  │ AIDevSearch  │ │   CodeAgent  │ │   CodeExplain  │ │ hugging_face   │    │ github_agent   │    ║
║  │   Agent      │ │              │ │   _agent       │ │    _agent      │    │                │    ║
║  │ (Gemini Tool)│ │ (Gemini Tool)│ │ (Gemini Tool)  │ │ (Gemini Tool)  │    │ (Gemini Tool)  │    ║
║  └──────────────┘ └──────────────┘ └────────────────┘ └────────────────┘    └────────────────┘    ║
║                                                                                                   ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════╝



╔════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                           DATA FLOW                                                                ║
║            (Execution, transport, external systems)                                                ║                                
╠════════════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                                    ║
║  ┌─────────────────────┐      ┌──────────────────────────────┐    ┌──────────────────────────────┐ ║
║  │ google_search (ADK) │      │ BuiltInCodeExecutor          │    │CodeExplain                   │ ║
║  └─────────┬───────────┘      │ (Python sandbox, no net/fs)  │    │ (Python sandbox, no net/fs)  │ ║
║            │                  └─────────┬────────────────────┘    └─────────┬────────────────────┘ ║
║            ▼                            ▼                                   ▼                      ║
║  External search results          Python execution output              Python explain output       ║
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

## Agents & tools

### Tool schema:  

|              Component | Type                             | Attached To        | Purpose                                      |
| ---------------------: | -------------------------------- | ------------------ | -------------------------------------------- |
|   **AIDevSearchAgent** | `AgentTool`                      | RootAgent          | Discover & summarize AI developer news       |
|          **CodeAgent** | `AgentTool`                      | RootAgent          | Execute Python code safely                   |
|   **CodeExplainAgent** | `AgentTool`                      | RootAgent          | Explain Python code safely                   |
| **hugging_face_agent** | `AgentTool` (Gemini + MCP stdio) | RootAgent          | Hugging Face models, datasets, spaces        |
|       **github_agent** | `AgentTool` (Gemini + MCP HTTP)  | RootAgent          | GitHub repositories, issues, PRs (read-only) |
|        `google_search` | Built-in ADK Tool                | AIDevSearchAgent   | Web discovery for news                       |
|  `BuiltInCodeExecutor` | ADK Executor                     | CodeAgent          | Deterministic Python sandbox                 |
|      **HF MCP Server** | MCP Backend (stdio)              | hugging_face_agent | Transport to Hugging Face Hub                |
|  **GitHub MCP Server** | MCP Backend (HTTP)               | github_agent       | Transport to GitHub API (Copilot MCP)        |


> _Note_
```bash
 User → "Explain this Python code"  
             │  
             ▼  
        RootAgent  
             ├─ detects "explain"  
             └─ delegates to CodeExplainAgent  
                      │  
                      ▼  
               Explanation only (no execution)
```

### Agents  

### RootAgent (Central Orchestrator)

The **RootAgent** is the intelligence hub of the system. It is responsible for:

- Intent detection
- Deterministic workflow control
- Tool and agent selection
- Context aggregation
- Final response assembly
- Routes user input  
- Never answers directly   
- Ensures correct agent selection ( Ensures clean separation of responsibilities:  News Search Agent or Python Code Execution Agent)
 
The RootAgent has **direct access** to:
- Gemini-powered specialist agents
- Third-party developer APIs

### Gemini-Powered Agents

- **AIDevSearchAgent** (know also as `AI Developer News Agent`)  
  - Discovers and summarizes AI developer news (Specializes in AI news for developers from AI articles, platforms and uses cases)
  - Uses `google_search`
  - Manages headline selection and summaries
  - Follows an interactive, multi-step workflow:  
    1. Clarify number of items  
    2. Search and filter AI-related content  
    3. Present headlines  
    4. Summarize selected items  

- **CodeAgent** (known also as  `Python Code Agent`)  
  - Executes Python code only
  - Uses `BuiltInCodeExecutor`
  - Returns execution results without explanation  
  - No explanations, no commentary  
  - Returns execution output or errors  

- **CodeExplainAgent**
- Explain Python code (no execution)

### Third-Party Developer APIs (Custom Tools)

- **Hugging Face Hub Agent**
  - Model metadata
  - Spaces
  - Datasets
  - Popularity and usage signals

- **GitHub Agent**
  - Repository metadata
  - Stars, issues, commits
  - Open-source activity signals

---

### Design principles:
- Separation of concerns: RootAgent routes, specialist agents perform tasks.
- Deterministic workflows: minimal LLM guesswork for critical steps.
- Tool transparency: sources and tool usage are explicit.
- Developer-first UX and safe code execution.

---  

## Project structure (Repository structure)

```bash
Toolkit_Google_ADK/                          # Root directory of the project; contains all source code, configs, and documentation
├── app_01/                                  # Main application module containing the core agent implementation
│   ├── __init__.py                          # Marks app_01 as a Python package and enables module imports
│   ├── agent.py                             # Defines the primary agent logic (Google ADK integration, tools, prompts, execution flow)
│   └── .env                                 # Local environment variables (API keys, secrets); not committed to version control
├── Notebbook_app_001.ipynb                  # Jupyter Notebook for experimentation, testing, and demoing agent behavior
├── requirements.txt                         # List of Python dependencies   
├── .env.example                             # Example environment variable template   
├── LICENSE                                  # License
├── .gitignore                               # Defines ignore rules for environment variables, Python artifacts, notebooks, logs, and local editor files  
├── README.md                                # Project documentation: setup, usage, architecture, and examples
├── Screenshots_Examples_Usage/              # Visual assets demonstrating application usage and outputs
│   ├── Screenshot_UI_interface.jpeg         # Example screenshot showing initial UI or agent interaction
│   ├── Screenshot_AIDevSearchAgent_2.jpeg   # Example screenshot demonstrating AIDevSearchAgent output  
│   ├── Screenshot_AIDevSearchAgent_3.jpeg   # Example screenshot highlighting a core feature of AIDevSearchAgen
│   ├── Screenshot_CodeAgent_1.jpeg          # Example screenshot demonstrating CodeAgent output 
│   ├── Screenshot_CodeExplainAgent1.jpeg    # Example screenshot highlighting a core feature of CodeExplainAgent1
│   ├── Screenshot_HuggingFaceAgent1.jpeg    # Example screenshot highlighting a core feature of HuggingFaceAgent1 TO BE ENCLOSED UPDATED VERSION 
│   ├── Screenshot_GitHubAgent1.Agentjpeg    # Example screenshot highlighting a core feature of GitHub TO BE ENCLOSED UPDATED VERSION 
│   ├── Screenshot_2                    # Example screenshot highlighting a core feature or workflow
│   ├── Screenshot_3                    # Example screenshot demonstrating agent output or results
│   ├── Screenshot_4                    # Example screenshot showing advanced or edge-case behavior
```

---  

## Quick start / Getting Started
This section shows how to install dependencies, configure authentication, and run the full pipeline.  

### Prerequisites:
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
Set environment variables (keys) in `.env` or your environment. See example `.env.example`:

```env
GEMINI_API_KEY=your_gemini_api_key
HF_API_KEY=your_hf_api_key
GIT_API_KEY=your_github_api_key
ADK_DEV_MODE=true
```

> _Notes:_  
> - The project expects API keys to be correctly provisioned for Vertex AI / Gemini usage.
> - You can create a [Gemini API key](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/quickstart?usertype=apikey#python-gen-ai-sdk). This key is essential for authenticating your requests to the Gemini API. A step-by-step guide can be found on o [Google AI Studio](https://cloud.google.com/free?hl=en) : O


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

## Examples Usage (UI)

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

## Limitations & workarounds

- [ADK tool restrictions](https://google.github.io/adk-docs/tools/limitations/): some built-in tools (e.g., google_search, code execution) typically cannot be combined inside a single agent instance. Workaround: create specialized agents (SearchAgent, CodeAgent) and orchestrate via RootAgent using AgentTool.create() to delegate requests.
- Model variability: responses can differ between runs. Test determinism in production-critical workflows.
- API quotas and billing: monitor Vertex AI / Google Cloud costs.

See ADK docs:
- Tools: https://google.github.io/adk-docs/tools/
- Limitations: https://google.github.io/adk-docs/tools/limitations/

---

## Testing & CI

Suggested test categories:
- Agent routing tests (RootAgent → specialists)
- News workflow tests (search → summary → citation)
- Code execution tests (sandboxed runs, error handling)
- Integration tests for Hugging Face & GitHub enrichments

Add automated tests and CI pipelines as needed (e.g., GitHub Actions).

---

## Contributing

Contributions are welcomed to improve the ADK Toolkit! Suggested workflow:  

1. Fork the GitHub repository
2. Create a feature branch:
```bash
git checkout -b feat/your-feature
```
3 Commit and push your changes  
4 Submit a Pull Request and describe your contribution.  

Please follow the repository code style and add tests for major features.

---

## Future Implementations  

We are actively seeking contributors who want to help implement and/or propose the following future features (suggested improvements): 
-  **Use different Gemini models intentionally** :  The current design uses `gemini-2.5-flash`. You might upgrade AIDevSearchAgent using model `gemini-2.5-pro` and investigate its impact
  on several aspects such as latency, cost, quality. 

| Aspect     | Impact               |
| ---------- | -------------------- |
| Latency    | Slightly higher      |
| Cost       | Higher per token     |
| Throughput | Lower                |
| Quality    | Significantly higher |

- **Adding new AgentTools** without destabilizing the system.  
- **Structured JSON outputs for headlines** (machine-readable)  
- **Persistent session storage across restarts**  
- **Search refinements** (filters, "only open-source", date ranges)
- **UI enhancements** (buttons for selection, debugging/observability mode)
- **Stronger execution guardrails and resource limits**  

Feel free to suggest more ideas by opening an issue or starting a discussion! For bug reports or feature requests, 
 [open an issue](https://github.com/micag2025/Toolkit_Google_ADK/issues). For general questions or share your thoughts, start a 
[comment](LINK TO BE ENCLOSED).

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

An acknowledgement to the contributions of the Ready Tensor developer community (for their guidance and contributions) for  creating a vibrant ecosystem where AI professionals can share their projects, insights, and innovations, fostering collective growth and accelerating the advancement of AI technology.
