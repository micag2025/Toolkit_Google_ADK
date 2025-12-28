# Toolkit Agents with Google’s Agent Development Kit (ADK)  

This project is built using **Google Agent Development Kit (ADK)** with a clean multi-agent architecture,  giving an example toolkit that demonstrates how to build, orchestrate, and deploy multi-agent systems using Google’s Agent Development Kit (ADK). The project focuses on creating an `AI Developer Agent` capable of discovering real-time AI news, generating Python code, and integrating with developer platforms like Hugging Face and GitHub.  

Key goals:
- Real-time discovery and summarization of AI news relevant to developers
- Execute and return Python code results in a sandboxed environment
- Provide a clean, multi-agent architecture for reliable orchestration and extensibility

Built with: Google ADK, Gemini models, and a minimal ADK Web interface.  

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

## Architecture overview

High-level flow:
1. ADK Web UI: user input, headline selection, and execution requests.
2. Session state: tracks mode (news / code), last query, headlines, selections.
3. RootAgent: intent detection, context aggregation, and deterministic routing.
4. Specialist agents:
   - AIDevSearchAgent (news + google_search)
   - CodeAgent (sandboxed Python execution)
5. External APIs for enrichment: Hugging Face Hub and GitHub.???
   -HugginFaceAgent
   -GitHib Agent

Compact ASCII diagram:  

```bash  
RootAgent (Orchestrator)
├─ AIDevSearchAgent → google_search (discovery)
├─ CodeAgent → BuiltInCodeExecutor (sandbox)
└─ Third-party APIs → Hugging Face, GitHub ???? 
└─ Third-party APIs → Hugging FaceAgent, GitHubAgent ???
``` 

The application is built using a **multi-agent architecture powered by Gemini models and Google ADK Web**. This application uses a **state-aware, multi-agent architecture** built with **Google ADK Web** and **Gemini models**, designed specifically for AI developers. The below schema diplays hows who decides, who executes, and where data comes from.

> _Note_ Option1 

```yaml  
┌──────────────────────────────────────────────┐
│                ADK Web UI                    │
│  - User prompts                              │
│  - Headline selection                        │
│  - Python execution requests                 │
└────────────────────────┬─────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────┐
│                Session State                 │
│  - mode: news | code                         │
│  - last_query                                │
│  - headlines[]                               │
│  - awaiting_count / selection                │
└────────────────────────┬─────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────┐
│                  RootAgent                   │
│   (Gemini 2.5 Flash – Orchestrator)          │
│                                              │
│  - Intent detection                          │
│  - Context aggregation                       │
│  - Agent & tool routing                      │
│  - No direct user responses                  │
└───────────────┬───────────────┬──────────────┘
        ┌───────┴────────┐      │
        ▼                ▼      │_____________
┌──────────────────┐  ┌──────────────────┐    │
│ AIDevSearchAgent │  │     CodeAgent    │    │
│ (Gemini Tool)    │  │   (Gemini Tool)  │    │
│                  │  │                  │    │
│ - AI news flow   │  │ - Python only    │    │
│ - Headline mgmt  │  │ - Deterministic  │    │
│ - Summaries      │  │ - Sandboxed exec │    │
└──────────┬───────┘  └──────────┬───────┘    │
           │                      │           │
           ▼                      ▼           │
┌──────────────────┐   ┌────────────────────┐ │
│  google_search   │   │ BuiltInCodeExecutor│ │
│  (Discovery)     │   │ (Python Sandbox)   │ │
└──────────────────┘   └────────────────────┘ │
                                              │
            ┌─────────────────────────────────│ 
            │
            ▼
┌──────────────────────────────────────────────┐
│       External AI Developer Ecosystem        │
│                                              │
│  ┌──────────────────┐   ┌────────────────┐   │
│  │  Hugging Face    │   │   GitHub       │   │
│  │  - Models        │   │  - Repos       │   │
│  │  - Spaces        │   │  - Code        │   │
│  │  - Datasets      │   │  - Issues      │   │
│  └──────────────────┘   └────────────────┘   │
│                                              │
│  (Referenced by RootAgent for reasoning,     │
│   ranking, and developer relevance)          │
└──────────────────────────────────────────────┘

```
> _Note_ Option2 
```yaml
┌──────────────────────────────────────────────┐
│                ADK Web UI                    │
│  - User prompts                              │
│  - Headline selection                        │
│  - Python execution requests                 │
└────────────────────────┬─────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────┐
│                Session State                 │
│  - mode: news | code                         │
│  - last_query                                │
│  - headlines[]                               │
│  - awaiting_count / selection                │
└────────────────────────┬─────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────┐
│                  RootAgent                   │
│     (Gemini 2.5 Flash – Orchestrator)        │
│                                              │
│  Responsibilities:                           │
│  - Intent detection                          │
│  - Workflow orchestration                    │
│  - Context aggregation                       │
│  - Final response assembly                   │
│                                              │
│  Attached Tools & APIs:                      │
│  - AIDevSearchAgent (Gemini tool)            │
│  - CodeAgent (Gemini tool)                   │
│  - Hugging Face Hub API                      │
│  - GitHub API                                │
└───────────────┬───────────────┬──────────────┘
        ┌───────┴────────┐      │______________________
        ▼                ▼                            ▼
┌──────────────────┐  ┌──────────────────┐   ┌─────────────────────┐
│ AIDevSearchAgent │  │     CodeAgent    │   │ External APIs       │
│ (Gemini Tool)    │  │ (Gemini Tool)    │   │ (Direct Access)     │
│                  │  │                  │   │                     │
│ - AI news flow   │  │ - Python only    │   │ - Hugging Face Hub  │
│ - Headline mgmt  │  │ - Deterministic  │   │   • models          │
│ - Summaries      │  │ - Sandboxed exec │   │   • spaces          │
└──────────┬───────┘  └──────────┬───────┘   │   • datasets        │
           │                      │          │ - GitHub            │
           ▼                      ▼          │   • repos           │
┌──────────────────┐   ┌────────────────────┐│   • stars/issues    │
│  google_search   │   │ BuiltInCodeExecutor││   • activity        │
│  (Discovery)     │   │ (Python Sandbox)   │└─────────────────────┘
└──────────────────┘   └────────────────────┘
```

---

## Agents & tools

### Tool schema (summary):

| Tool                  | Type               | Attached To      | Purpose                     |
|----------------------:|-------------------:|------------------|----------------------------:|
| AIDevSearchAgent      | AgentTool          | RootAgent        | Discover & summarize news   |
| CodeAgent             | AgentTool          | RootAgent        | Execute Python (sandbox)    |
| `google_search`         | Built-in ADK Tool  | AIDevSearchAgent | Web discovery               |
| `BuiltInCodeExecutor`   | ADK Executor       | CodeAgent        | Safe Python execution       |
| Hugging Face Hub API  | Third-party Tool   | RootAgent        | Model & platform metadata   |
| GitHub API            | Third-party Tool   | RootAgent        | Repo & OSS signals          |

### Design principles:
- Separation of concerns: RootAgent routes, specialist agents perform tasks.
- Deterministic workflows: minimal LLM guesswork for critical steps.
- Tool transparency: sources and tool usage are explicit.
- Developer-first UX and safe code execution.

---  

## Project structure (Repository structure)

```
Toolkit_Google_ADK/(ai_dev_news_web)/?
├── app_01/
│   ├── __init__.py
│   ├── agent.py
│   └── .env
├── Notebbook_app_001.ipynb
├── requirements.txt
├── .env.example
├── LICENSE
└── README.md│
├── Screenshots_Examples_Usage/
│   ├── Screenshot_1
│   ├── Screenshot_2
│   ├── Screenshot_3
│   ├── Screenshot_4
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

### Environment variables / .env.example  
Set environment variables. Put keys in `.env` or your environment. Example `.env.example`:

```env
GEMINI_API_KEY=your_gemini_api_key
HF_API_KEY=your_hf_api_key
GIT_API_KEY=your_github_api_key
ADK_DEV_MODE=true
```

> _Notes:_  
> - Do NOT commit your `.env` or secrets to git.  
> - The project expects API keys to be correctly provisioned for Vertex AI / Gemini usage.
> - You can create a [Gemini API key](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/quickstart?usertype=apikey#python-gen-ai-sdk). This key is essential for authenticating your requests to the Gemini API.  Here's a step-by-step guide: Go to [Google AI Studio](https://cloud.google.com/free?hl=en) : Open your web browser and navigate to the Google AI Studio website. Access API Keys Page : Once logged in, open the "API keys" page from the left-side panel. Create API Key : Click on the "Create API key" button.      


### Launch the ADK Web App  / Get the app URL  
Start the ADK Web app:

```bash
adk web
```

Open the provided local URL in your browser, from the Google ADK user interface in the left pane, select the `app_01` agent (or whichever agent you added), and interact.


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

>_Note_ : ADK create supports two project types. The `--type=code` option generates a Python-based agent in `agent.py`. The `--type=config` option creates a YAML-based agent configuration. In this the project `--type=code` option is been selected. The `--model` parameter specifies the LLM to be used by the agent. We will override this and experiment with different tools.   

## 1.2 Writing the first `agent.py`

 `adk create` command is used to create folders and then write to its `agent.py` using the cell magic in the notebook. Cell magic uses specific commands to interact with the files in the new agent folder.  `%%writefile FILENAME` has been used to do this.

The next steps is to create an Agent with a unique name, specify the LLM model, and give it basic instructions.

As with any agent, an LLM is required to start with ADK is model agnostic - meaning you can provide it with any model of your choice like Gemini, Claude, Ollama and even use LiteLLM to bring in other models.
In this project the `Gemini 2.0 flash` is used.

## 1.3 Adding a text model  
Text-focused models like `gemini-2.5-flash` are ideal when want optimized text processing. They often provide faster response times. Let's create a variant of the agent using a text-optimized model to see how it behaves differently.  

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
- "Help me with my homework"

Watch how the agent now maintains strict boundaries while still being helpful for AI-related queries.


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

## Examples Usage 
<p style="background-color:#f7fff8; padding:15px; border-width:3px; border-color:#e0f0e0; border-style:solid; border-radius:6px"> 🚨
&nbsp; <b>Different Run Results:</b> The output generated by AI chat models can vary with each execution due to their dynamic, probabilistic nature.</p>  

### ADK Web UI: 
![ADK_interface](https://github.com/micag2025/Toolkit_Google_ADK/blob/75e09d11b628e536a7a204335f88c19862173c18/Screenshot_27-12-2025_185359_127.0.0.1.jpeg)

After selecting the appropriate app (`app_01`) from the dropdown menu from the ADK Web UI: 

### 1. Example Prompts: AI News  
1. AI news discovery:
   - Ask: "What's the latest AI news about Google?"
   - Flow: RootAgent → AIDevSearchAgent → google_search → summarize & cite sources.

![Google_Search&PythonDevelopr Tool](https://github.com/micag2025/Toolkit_Google_ADK/blob/2346fda5b929151f790eb73e30a15b6350158637/Screenshot_22-12-2025_14428_127.0.0.1.jpeg)

### 2.  Example Prompts: Python Code Execution  
2. Python execution:
   - Ask: "Run this Python code..."
   - Flow: RootAgent → CodeAgent → BuiltInCodeExecutor (sandbox) → return execution output (no extra commentary).
     
![Google_Search&PythonDevelopr Tool](https://github.com/micag2025/Toolkit_Google_ADK/blob/2346fda5b929151f790eb73e30a15b6350158637/Screenshot_22-12-2025_14428_127.0.0.1.jpeg)

### 3.  Example Prompts: HuggingFace Code Execution  
3. Enrichment:
   - RootAgent can request Hugging Face signals to rank or annotate discoveries.
     
![HuggingFace_Tool](https://github.com/micag2025/Toolkit_Google_ADK/blob/2346fda5b929151f790eb73e30a15b6350158637/Screenshot_22-12-2025_145157_127.0.0.1.jpeg)  

### 4.  Example Prompts: GitHub Code Execution    
3. Enrichment:
   - RootAgent can request Hugging Face signals to rank or annotate discoveries.  
SCREENSHOT TO BE ENCLOSED 
---

## Limitations & workarounds

- ADK tool restrictions: some built-in tools (e.g., google_search, code execution) typically cannot be combined inside a single agent instance. Workaround: create specialized agents (SearchAgent, CodeAgent) and orchestrate via RootAgent using AgentTool.create() to delegate requests.
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

## Roadmap & enhancements

Planned / suggested improvements:
- Structured JSON outputs for headlines (machine-readable)
- Persistent session storage across restarts
- Search refinements (filters, "only open-source", date ranges)
- UI enhancements (buttons for selection, debugging/observability mode)
- Additional specialist agents (HuggingFaceAgent, GitHubAgent)
- Stronger execution guardrails and resource limits

---

## Contributing

Contributions welcome. Suggested workflow:
1. Open an issue to discuss changes or features.
2. Create a branch: `git checkout -b feat/your-feature`
3. Implement and add tests.
4. Open a PR describing changes and rationale.

Please follow the repository code style and add tests for major features.

## References  

- [Google AI Studio](https://cloud.google.com/free?hl=en)
- [Gemini API key](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/quickstart?usertype=apikey#python-gen-ai-sdk)
- [Gemini Models](https://ai.google.dev/gemini-api/docs/models#model-variations)  
- [Tools for Agents](https://google.github.io/adk-docs/tools/)  
- [Limitations for ADK tools](https://google.github.io/adk-docs/tools/limitations/)  

---

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/micag2025/Toolkit_Google_ADK/blob/d18bda56849caea6efeda3803da893b29d5bfa23/LICENSE) file for details.

---

## Contact

If you encounter bugs, have questions, or want to request a new feature, please [open an issue](https://github.com/micag2025/Toolkit_Google_ADK/issues) on this repository.  

---

## Acknowledgements

Built with Google Agent Development Kit (ADK). Designed for AI developers and builders
