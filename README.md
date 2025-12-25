# Toolkit Agents with Google’s Agent Development Kit (ADK)   

An interactive **ADK Web application** that helps AI developers:
- Discover **recent AI news, articles, platforms, and use cases**
- Interactively explore headlines and summaries
- **Execute Python code on demand** in the same interface

Built using **Google Agent Development Kit (ADK)** with a clean multi-agent architecture.

This project focuses on building a comprehensive AI Developer Agent capable of:  
- Researching the latest AI developments in real-time.  
- Generating Python code.  
- Leveraging platforms like HuggingFace and GitHub.    

The project uses **Google’s Agent Development Kit (ADK)** to build, orchestrate, and deploy advanced multi-agent systems. The ultimate goal is to create an AI agent with access to real-time information from the web.  

An agent is a system where an LLM serves as the "brain" providing generative capabilities, combined with tools that allow actions in the real world. This foundation enables further expansion into research, code generation, and multimedia content creation.

---

## Core Capabilities
**Real-Time Text Agents**  
- Build real-time text agents with ADK that can carry natural, conversational interactions.  
- Connect agents to external tools and data sources to execute real-world tasks.  

**Multi-Agent Systems**
- Design systems using memory, tools, and orchestration patterns to coordinate specialized agents, such as planners, researchers, and writers.  
- Enable collaboration between agents for complex workflows, including research, code generation, and content creation.  

**Production-Ready Agents**
- Deploy agents with guardrails, persistent memory, automated evaluations, and review methods.  
- Run production workloads on Google Cloud’s Vertex AI Agent Engine with monitoring and security features.

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



## Tool Schema

| Tool                  | Type                      | Attached To      | Purpose                     |
| --------------------- | ------------------------- | ---------------- | --------------------------- |
| `AIDevSearchAgent`    | AgentTool                 | RootAgent        | AI news workflow            |
| `CodeAgent`           | AgentTool                 | RootAgent        | Python execution            |
| `google_search`       | Built-in ADK Tool         | AIDevSearchAgent | Web discovery               |
| `BuiltInCodeExecutor` | ADK Executor              | CodeAgent        | Safe Python                 |
| Hugging Face Hub API  | Third-party Tool (Custom) | RootAgent        | Model & platform enrichment |
| GitHub API            | Third-party Tool (Custom) | RootAgent        | Repo & OSS signals          |

> Second option schema to show the **Tool Categorization**

```bash
RootAgent Tools
├─ Gemini Agent Tools
│  ├─ AIDevSearchAgent (news + search workflow)
│  └─ CodeAgent (python execution)
│
├─ Built-in ADK Tools
│  └─ google_search
│
└─ Third-Party Developer APIs (Custom Tools)
   ├─ Hugging Face Hub API
   └─ GitHub API
```
---

## Key Features

### AI Developer News Assistant
- Finds **recent AI news** relevant to developers
- Focuses on:
  - AI articles
  - AI platforms
  - AI developer use cases
- Uses **`google_search`** for transparent sourcing
- Interactive workflow:
  - Asks how many items you want
  - Displays numbered headlines
  - Summarizes one item at a time
  - Allows fetching more news dynamically

### Python Code Execution
- Execute Python code directly in the chat
- Supports multi-line code
- Returns **only execution results**
- Runs safely using `BuiltInCodeExecutor`

### Smart Agent Routing
- A **RootAgent** routes requests to:
  - News Search Agent
  - Python Code Execution Agent
- Ensures clean separation of responsibilities

---

## Architecture Overview  

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
- Ensures correct agent selection  
 
The RootAgent has **direct access** to:
- Gemini-powered specialist agents
- Third-party developer APIs

### Gemini-Powered Agents

- **AIDevSearchAgent** (know also as AI Developer News Agent)  
  - Discovers and summarizes AI developer news (Specializes in AI news for developers)
  - Uses `google_search`
  - Manages headline selection and summaries
  - Follows an interactive, multi-step workflow:  
    1. Clarify number of items  
    2. Search and filter AI-related content  
    3. Present headlines  
    4. Summarize selected items  

- **CodeAgent** (known also as  Python Code Agent)  
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

In this scenario, to fetch the latest news, let's provide the agent with a built-in tool, `google_search`. These built-in tools come pre-packed with the library. To add it to the agent, just import it and provide it as a tool in the tools array.  

**Refresh the ADK Web UI.** You should see a new app name (app_02) in the dropdown. Select it and start a text conversation with your agent.

Let's test the agent with the Google search tool by asking a query `"What is the latest AI News?"`. The agent will use the Google Search tool to find current information, process the results, and give you a comprehensive, up-to-date response with sources. Just like that, the agent can now access **real-time information** from across the web!

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

---

## Repository structure (Project Structure)

```bash
Toolkit_Google_ADK/(ai_dev_news_web)/
├──app_01/
    __init__.py
    agent.py
    .env
├── app.py
├── requirements.txt
├── .env.example
├── licence
├── README.md
```
---

## Getting Started
This section shows how to install dependencies, configure authentication, and run the full pipeline.

### Prerequisites
Required:
Python 3.10+
Google Cloud & API Key

_Set relevant API keys in your environment_:  
```bash
export GEMINI_API_KEY=your_gemini_api_key
export HF_API_KEY = your-hf_api_key
export GIT_API_KEY= you git_api_key
```  
> _SET UP Google API key and Vertex AI based authentication_   
You can create a [Gemini API key](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/quickstart?usertype=apikey#python-gen-ai-sdk). This key is essential for authenticating your requests to the Gemini API.  Here's a step-by-step guide:  	Go to [Google AI Studio](https://cloud.google.com/free?hl=en) : Open your web browser and navigate to the Google AI Studio website. Access API Keys Page : Once logged in, open the "API keys" page from the left-side panel. Create API Key : Click on the "Create API key" button.    

you should create a Python virtual environment and use the `requirements.txt` file to install the required Python packages.

### Installation

```bash
git clone https://github.com/micag2025/Toolkit_Google_ADK.git
cd Toolkit_Google_AKD
pip install -r requirements.txt
```
>_Note_: This will install a handy set of command-line tools that will be useful when working with ADK.  

### Launch the ADK Web App  / Get the app URL
Run:  
```
adk web
```
- It will start a local web server.  / Run the cell above and open the link in a new tab : This launches a browser-based interface for testing and debugging.  
- Open the provided URL in a browser.  When you open the (provided URL) interface in your browser, you'll see the Google ADK user interface. In the left pane, select your agent from the dropdown (app_01)
- You can now chat with the AI Developer News + Code Assistant + HuggingFace + GitHub interactively.  Try asking the agent a question with text. The agent responds text-to-text with real-time. It thinks and provide text answer  in a natural flow.
- Explore the ADK Web UI for tracing agent reasoning and code interactions.     

### Kill ADK process  
After finishing, make sure to run the cell below to close your connection.  

Run:
```bash
!pkill -f "adk web"  
```
---

## Examples Usage 
<p style="background-color:#f7fff8; padding:15px; border-width:3px; border-color:#e0f0e0; border-style:solid; border-radius:6px"> 🚨
&nbsp; <b>Different Run Results:</b> The output generated by AI chat models can vary with each execution due to their dynamic, probabilistic nature.</p>  

After selecting the appropriate app (app_01) from the dropdown menu from the ADK Web UI: 
INITIAL INTERFACE SCREENSHOT TO BE ENCLOSED. 

### 1. Example Prompts: AI News 

![Google_Search&PythonDevelopr Tool](https://github.com/micag2025/Toolkit_Google_ADK/blob/2346fda5b929151f790eb73e30a15b6350158637/Screenshot_22-12-2025_14428_127.0.0.1.jpeg)

### 2.  Example Prompts: Python Code Execution 
![HuggingFace_Tool](https://github.com/micag2025/Toolkit_Google_ADK/blob/2346fda5b929151f790eb73e30a15b6350158637/Screenshot_22-12-2025_145157_127.0.0.1.jpeg)  

### 3.  Example Prompts: HuggingFace Code Execution  
SCREENSHOT TO BE ENCLOSED  

### 4.  Example Prompts: GitHub Code Execution    
SCREENSHOT TO BE ENCLOSED  

---

## Automated Testing

The app supports:
- Agent routing tests
- News workflow tests
- Code execution tests
- Mixed news + code scenarios  
(See test prompt suite for validation coverage.)

## Design Principles

- Interactive, not verbose
- Deterministic workflows  
- Tool transparency  
- Developer-first UX  
- Safe code execution  

## Possible Enhancements  

- Structured JSON outputs for headlines  
- Session state persistence  
- Search refinement (e.g. “only open-source”)  
- Debug / observability mode  
- UI buttons for headline selection  
- Code execution guardrails


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
