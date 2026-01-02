
# An Agent-Based Developer Intelligence Toolkit : Structured AI news, safe code execution, and platform intelligence — powered by ADK.  
# An ADK-Powered Developer Intelligence Platform  
# Designing a Safe Multi-Agent Developer Assistant with ADK  


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

Built with: Google ADK, Gemini models, and a minimal ADK Web interface.  

The project is best described as `Agent-based developer intelligence with strict routing and tool grounding`. The system is a `Structured, agent-based, tool-grounded developer intelligence`. it’s an agent-based developer intelligence toolkit. It’s a developer intelligence system opinionated, structured, tool-grounded and role-aware.

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


### Design principles:
- Separation of concerns: RootAgent routes, specialist agents perform tasks.
- Deterministic workflows: minimal LLM guesswork for critical steps.
- Tool transparency: sources and tool usage are explicit.
- Developer-first UX and safe code execution.

---  

## Installation Instructions
This pubblication has a **GitHub code repository** attached under the "Code" section.

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
Set environment variables. Put keys in `.env` or your environment. See example `.env.example`:

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

## Step-by-Step Development Process
**Agent Setup**  
Build the agent in ADK and connect it to Google Search.  
Test text interactions via the ADK Web UI.  
**Memory & Context Management**  
Use sessions, state, and memory to manage conversations.  
Enable short-term tracking and long-term recall across interactions.  
**Tools & API Integration**  
Add custom tools and APIs.  
Refine agent instructions to ensure adherence to defined workflows.  
**Research & Reporting**  
Generate structured research reports using schemas.  
Act as a coordinator to collect, organize, and save outputs in markdown for downstream use.  
**Guardrails & Callbacks**  
Filter unsafe sources and enforce rules.    
Log tool activity for predictability and production readiness.    
**Production Deployment**  
Give agents persistent memory.  
Test reliability and deploy on Vertex AI.    
Add security, monitoring, and scaling features for safe production use.     

---

## Agents  

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

### Third-Party Developer APIs (Custom Tools)

- **Hugging Face Hub API**
  - Model metadata
  - Spaces
  - Datasets
  - Popularity and usage signals

- **GitHub API**
  - Repository metadata
  - Stars, issues, commits
  - Open-source activity signals

These APIs are exposed as **custom tools** directly to the RootAgent and are used for enrichment, ranking, and developer relevance scoring.

---

## Design Principles

- Clear separation of concerns
- Deterministic workflows
- Minimal LLM guesswork
- Tool transparency
- Developer-first UX

---

## 1.1 Setting up the agent

Before we dive into building agents, a new folder structure with ADK's built-in project is set up scaffolding using the `adk create` command.

When you run `adk create`, it generates three essential files. 
1. The `.env` file securely stores your API credentials and configuration. 
2. The `__init__.py` file marks the directory as a Python package, nabling proper imports. 
3. Most importantly, the `agent.py` file provides a clean foundation where you'll implement your agent.

File structure:
```
app_01/
    __init__.py
    agent.py
    .env
```

>_Note_ : In this the project `--type=code` option has been selected to generate a Python-based agent in `agent.py`. The `--model` parameter specifies the LLM to be used by the agent. We will override this and experiment with different tools.       

## 1.2 Writing the first `agent.py`

 `adk create` command is used to create folders and then write to its `agent.py` using the specific command, `%%writefile FILENAME`,  to interact with the files in the new agent folder.  

## 1.3 Adding a text model  

The next steps is to create an Agent with a unique name, specify the LLM model, and give it basic instructions. As with any agent, an LLM is required to start with ADK is model agnostic - meaning you can provide it with any model of your choice like Gemini, Claude, Ollama and even use LiteLLM to bring in other models. In this project the `Gemini 2.0 flash` is used since text-focused models like `gemini-2.5-flash` are ideal when the purpose is to optimize text processing. They often provide faster response times.   

## 1.4 Adding tools to your agent  

**But here's the problem:** try asking this agent about the latest AI developments, and you'll quickly discover it can only tell you about things that happened before its training cutoff date. For an AI news assistant that's supposed to fetch the latest news, that's not particularly helpful.

Therefore, you need to fix that by providing your agent with **Tools**. In Google ADK, the word [“tool”](https://google.github.io/adk-docs/tools/) has two meanings:  


| Term                 | Meaning                                                                   |
| -------------------- | ------------------------------------------------------------------------- |
| **ADK Tool**         | A callable object exposed to an agent (e.g. `google_search`, `AgentTool`) |
| **Third-Party Tool** | Any external system or API                                                |


### Adding Google Search Tool

In this scenario, to fetch the latest news, let's provide the agent with a built-in tool, `google_search`. These built-in tools come pre-packed with the library. To add it to the agent, just import it and provide it as a tool in the tools array.  Let's test the agent with the Google search tool by asking a query `"What is the latest AI News?"`. The agent will use the Google Search tool to find current information, process the results, and give you a comprehensive, up-to-date response with sources. Just like that, the agent can now access **real-time information** from across the web!

ADK comes with several other `powerful built-in tools—there` are tools for running your code in a `sandbox`, `querying databases`, even `integrations with Google Workspace tools` like Calendar, Drive etc.  

### Adding Python code executor Tool

To fetch the latest news, the agent has been provided with a built-in tool, **google_search**. These built-in tools come `pre-packed with the library`. Now, in order to allow the agent also to execute code and debug using Gemini models, it has been used the **built_in_code_execution tool** that enables the agent to execute code, specifically when using Gemini 2 and higher models. This allows the model to perform tasks like calculations, data manipulation, or running small scripts. Also this tool comes from `pre-packed with the library`. To add it to the agent, just import it and provide it as a tool in the tools array. Run the cell below to import it

### Adding HuggingFace Execution Agent Tool  
TO BE DRAFTED   

### Adding GitHub Execution Agent Tool  
TO BE DRAFTED     

## 1.5 Fine-tuning agent instructions

So far the agent has simple instructions, but for reliable behavior, you need more sophisticated instruction engineering. Therefore, the agent has been enhanced  with strict behavioral controls.  

### Understanding Advanced Instructions

This enhanced instruction pattern includes:

- **Clear Identity**: Explicitly defines the agent's sole purpose
- **Refusal Mechanism**: Provides exact phrases for rejecting off-topic requests  
- **Workflow Requirements**: Forces the agent to use tools and cite sources
- **Behavioral Boundaries**: Sets expectations for valid vs. invalid requests

This creates a much more reliable and focused agent behavior.

### Testing Instructions

You can test the enhanced agent with both valid and invalid requests:

**Valid prompts** (should get a response):
- "What's the latest AI news about Google?"
- "Tell me about recent AI chip developments"

**Invalid prompts** (should be refused):
- "What's the weather today?"

Analyze how the agent now maintains strict boundaries while still being helpful for AI-related queries.

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

## Use Cases and Usage Examples:
 The below table gives an overview of how this ADK Toolkit is not designed only for AI developers and builders but it can be used also by different user types. Example general 
 queries for each user tyoe is also shown in the table.

| User Type         | Core Value                         |       Example prompts                                                                                                 |
| ----------------- | ---------------------------------- |---------------------------------------------------------------------------------------------------------------------- |
| ML Engineers      | Deep, accurate AI tooling insights |“What are the latest open-source LLM tools for summarization?”, Show me Hugging Face models for text generation”       |
| Backend Engineers | AI relevance without ML overload   |“Any AI tools relevant for backend search or summarization?”, Which of these tools are production-ready?”              |
| MLOps             | Deployment & infra signals         |“Which of these tools are open-source and actively maintained?”, “Are these models deployable on-prem?”                |
| Tech Leads        | High-signal summaries              |“Summarize the most relevant AI dev news this week”, “Which of these trends impact backend teams?”                     |
| Dev Advocates     | Structured content                 |“Explain this article for developers new to LLMs”, “Extract the key technical points” (Technical Writers|              |
| Product Managers  | Strategic clarity                  |“Which of these tools are proprietary?”, “What trends should we care about?”
| Researchers       | Research → practice bridge         |“Which research projects have working implementations?”, “Are there Hugging Face models for this approach?”
| Students          | Guided learning                    |“Explain this Python code”, “Which tools should I learn first?”

---

## Limitations & workarounds

- ADK tool restrictions: some built-in tools (e.g., google_search, code execution) typically cannot be combined inside a single agent instance. Workaround: create specialized agents (SearchAgent, CodeAgent) and orchestrate via RootAgent using AgentTool.create() to delegate requests.
- Model variability: responses can differ between runs. Test determinism in production-critical workflows.
- API quotas and billing: monitor Vertex AI / Google Cloud costs.

See ADK docs:
- Tools: https://google.github.io/adk-docs/tools/
- Limitations: https://google.github.io/adk-docs/tools/limitations/


## Limitations for ADK tools¶
Some [ADK tools have limitations](https://google.github.io/adk-docs/tools/limitations/#workaround-2-bypass_multi_tools_limit) that can impact how you implement them within an agent workflow. Here we list these tool limitations and workarounds, if available.

One tool per agent limitation¶
In general, you can use more than one tool in an agent, but use of specific tools within an agent excludes the use of any other tools in that agent. The following ADK Tools can only be used by themselves, without any other tools, in a single agent object:  

- Code Execution with Gemini API  
- Google Search with Gemini API

Therefore, the approach that uses one of these tools along with other tools, within a single agent, is not supported. To overcome these limitation, it has been used a Workaround, called `AgentTool.create() method`,  
that consists in using a soecific code that shows how to use `multiple built-in tools` or `how to use built-in tools with other tools by using multiple agent`.

This snippet defines a multi-agent setup using Google ADK:
- It creates a **SearchAgent** specialized in Google Search, equipped with the google_search tool.  
- It creates a **CodeAgent** specialized in executing code, using the built-in code executor.
- It creates a **HuggingFaceAgent** specialized in ...................  
- It creates a **GitHubAgent** specialized in ...................  
- It then defines a **RootAgent** that acts as an orchestrator, delegating tasks to either the SearchAgent or the CodeAgent or HuggingFaceAgent or GitHubAgent via AgentTool.

In short, the **RootAgent** coordinates specialized agents for search and code execution using the Gemini 2.0 Flash model. Happy coding! Don't hesitate to return if you have more questions.

---

## Testing & CI

Suggested test categories:
- Agent routing tests (RootAgent → specialists)
- News workflow tests (search → summary → citation)
- Code execution tests (sandboxed runs, error handling)
- Integration tests for Hugging Face & GitHub enrichments

Add automated tests and CI pipelines as needed (e.g., GitHub Actions).

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

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/micag2025/Toolkit_Google_ADK/blob/d18bda56849caea6efeda3803da893b29d5bfa23/LICENSE) file for details.

---

## Contact

michelaagostini73@gmail.com

---

## Acknowledgements

At Ready Tensor, our mission is to create a vibrant ecosystem where AI professionals can share their projects, insights, and innovations, fostering collective growth and accelerating the advancement of AI technology.
