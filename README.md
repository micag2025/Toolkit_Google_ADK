# Toolkit Agents with Google’s Agent Development Kit (ADK)   

An interactive **ADK Web application** that helps AI developers:
- Discover **recent AI news, articles, platforms, and use cases**
- Interactively explore headlines and summaries
- **Execute Python code on demand** in the same interface

Built using **Google Agent Development Kit (ADK)** with a clean multi-agent architecture.

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

The application is built using a **multi-agent architecture powered by Gemini models and Google ADK Web**.

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
  

## Agents

### 1. AI Developer News Agent
- Specializes in AI news for developers
- Uses `google_search`
- Follows an interactive, multi-step workflow:
  1. Clarify number of items
  2. Search and filter AI-related content
  3. Present headlines
  4. Summarize selected items

### 2. Python Code Agent
- Executes Python code only
- No explanations, no commentary
- Returns execution output or errors

### 3. Root Agent
- Routes user input
- Never answers directly
- Ensures correct agent selection

---

 build a complete AI News AI Developer Agent that can research the latest AI developments, generate Python code, use HuggingFace and GitHUb platform  and generate professional audio podcasts.

- Build real-time text agents with Google’s Agent Development Kit (ADK) that can carry natural, real-time conversations while connecting to external tools and data.  
- Design multi-agent systems that use memory, tools, and orchestration patterns to coordinate specialized agents like planners, researchers, and writers.  
- Take agents to production by adding guardrails, persistent memory, automated evaluations, and review methods for deploying on Google Cloud’s Vertex AI Agent Engine.

-  how to build and deploy AI agents with Google’s open source Agent Development Kit (ADK). ADK provides modular components such as models, tools, memory, and orchestration,
   that make it easier to create both simple and complex systems.
-  building a text agent that takes text input, reasons with an LLM, and responds with text output. Then evaluation of sessions, state, and memory, and extend the agents
   with tools and APIs to perform real-world tasks. Add callbacks and guardrails for reliability and orchestrate specialized agents like planners and researchers. Build a text agent
   that researches a topic, drafts a conversational script, and produces outputs with Gemini text-to-speech models. Then, build in guardrails to secure and optimize the agents before
   reviewing methods for deploying them into production.

In detail:   

- Build the agent with ADK, connect it to Google Search, and test text interactions in the ADK Web UI.  
- Use sessions, state, and memory to manage conversations, share context between tools, and give agents short-term tracking and long-term recall across interactions.  
- Add custom tools and API, integrate them with ADK, and refine agent instructions so they follow defined workflows effectively.  
- Generate structured research reports by defining schemas, rewriting agent instructions to act as a coordinator, and saving results as markdown files for downstream use.  
- Add guardrails with callbacks to filter unsafe sources, enforce rules, and log tool activity, making your agents safer, more predictable, and production-ready.  
- Build a agent by combining schemas, callbacks, and a dedicated audio agent, and generate multi-speaker episodes with Gemini text-to-text in a scalable workflow.  
- Learn how to productionize your agents by giving them persistent memory, testing their reliability, deploying on Vertex AI, and adding security and monitoring for safe scaling.

The objective is to build an AI agent and give it the power to access real-time information from the web. 

This project lays the foundation with a `simple agent that can fetch recent AI news from the web`. Briefly, it will give an overview of the fundamental structure of an agent and explore the ADK Web UI, which is a convenient way to trace your agent's thinking and interact through live voice conversations.


Firstly, it has been  built a simple agent that can fetch recent AI news from the web. An `agent' is a construct that has an LLM as the brain of the agent providing it the generative language capabilities and tools that let the agent take actions in the real world. besides, it will be also explored  alternative development approaches including YAML configuration and Web Builder options.

## 1.2 Setting up the agent

Before we dive into building agents, let's set up a new folder structure with ADK's built-in project scaffolding using the `adk create` command.

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

ADK create supports two project types. The `--type=code` option generates a Python-based agent in `agent.py`. The `--type=config` option creates a YAML-based agent configuration. The `--model` parameter specifies the LLM to be used by the agent. We will override this and experiment with different tools.  

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

### 1. Example Prompts: AI News 

![Google_Search&PythonDevelopr Tool](https://github.com/micag2025/Toolkit_Google_ADK/blob/2346fda5b929151f790eb73e30a15b6350158637/Screenshot_22-12-2025_14428_127.0.0.1.jpeg)

### 2.  Example Prompts: Python Code Execution 
![HuggingFace_Tool](https://github.com/micag2025/Toolkit_Google_ADK/blob/2346fda5b929151f790eb73e30a15b6350158637/Screenshot_22-12-2025_145157_127.0.0.1.jpeg)

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
