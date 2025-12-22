# Toolkit Agents with Google’s Agent Development Kit (ADK(   

 build a complete AI News AI Developer Agent that can research the latest AI developments, generate Python code, use HuggingFace and GitHUb platform  and generate professional audio podcasts.

- Build real-time text agents with Google’s Agent Development Kit (ADK) that can carry natural, real-time conversations while connecting to external tools and data.  
- Design multi-agent systems that use memory, tools, and orchestration patterns to coordinate specialized agents like planners, researchers, and writers.  
- Take agents to production by adding guardrails, persistent memory, automated evaluations, and review methods for deploying on Google Cloud’s Vertex AI Agent Engine.

-  how to build and deploy AI agents with Google’s open source Agent Development Kit (ADK). ADK provides modular components such as models, tools, memory, and orchestration,
   that make it easier to create both simple and complex systems.
-  building a text agent that takes text input, reasons with an LLM, and responds with text output. Then evaluation of sessions, state, and memory, and extend the agents
   with tools and APIs to perform real-world tasks. Add callbacks and guardrails for reliability and orchestrate specialized agents like planners and researchers. Build a podcast agent
   that researches a topic, drafts a conversational script, and produces multi-speaker audio with Gemini text-to-speech models. Then, build in guardrails to secure and optimize the agents before
   reviewing methods for deploying them into production.

In detail:   

- Build the agent with ADK, connect it to Google Search, and test text interactions in the ADK Web UI.  
- Use sessions, state, and memory to manage conversations, share context between tools, and give agents short-term tracking and long-term recall across interactions.  
- Add custom tools and API, integrate them with ADK, and refine agent instructions so they follow defined workflows effectively.  
- Generate structured research reports by defining schemas, rewriting agent instructions to act as a coordinator, and saving results as markdown files for downstream use.  
- Add guardrails with callbacks to filter unsafe sources, enforce rules, and log tool activity, making your agents safer, more predictable, and production-ready.  
- Build a agent by combining schemas, callbacks, and a dedicated audio agent, and generate multi-speaker episodes with Gemini text-to-text in a scalable workflow.  
- Learn how to productionize your agents by giving them persistent memory, testing their reliability, deploying on Vertex AI, and adding security and monitoring for safe scaling.



## Overview  from the DLAI_adk _course  
- Build your first agent    >L1
- ADK primitives - Session, State, and Memory  
- Tools for your agent  >L2
- Adding a research agent  >L3
- Instruction tuning and guardrails  >L4
- Multi-agent orchestration >L5
- [Optional] Productionize your agent

## SET UP Google API key and Vertex AI based authentication   
You can create a [Gemini API key](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/quickstart?usertype=apikey#python-gen-ai-sdk). This key is essential for authenticating your requests to the Gemini API.  
Here's a step-by-step guide:  
1.	Go to [Google AI Studio](https://cloud.google.com/free?hl=en) : Open your web browser and navigate to the Google AI Studio website.  
2.	Access API Keys Page : Once logged in, open the "API keys" page from the left-side panel.  
3.	Create API Key : Click on the "Create API key" button.  
4.	Acknowledge Notices (if prompted) : If any legal notices or safety setting reminders appear, read and acknowledge them to proceed.  
5.	Select Project : In the `Create API key` dialog, you'll have two options:  
	- "Create API key in new project": Choose this if you want to create a new Google Cloud project for your API key.  
	- "Create API key in existing project": Select this if you want to associate the API key with an existing Google Cloud project. It's recommended to choose the same project you plan to use for your application.  
6.	Copy the API Key : After creation, a string for your new API key will be displayed. Copy this key string immediately and keep it secure. You will need this key to authenticate your calls to the Gemini API.  
7.	Note Project Number (optional but recommended) : It's also a good practice to copy the project number of the Google Cloud project where the API key was generated, as this can be useful for later configurations.
     


## Repo structure  

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

you should create a Python virtual environment and use the `requirements.txt` file to install the required Python packages.

### Installation

```bash
git clone https://github.com/micag2025/Toolkit_Google_ADK.git
cd Toolkit_Google_AKD
pip install -r requirements.txt
```
---

## Running the Pipeline




## References  

- [Google AI Studio](https://cloud.google.com/free?hl=en)
- [Gemini API key](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/quickstart?usertype=apikey#python-gen-ai-sdk)
- [Gemini Models](https://ai.google.dev/gemini-api/docs/models#model-variations)  
- 

## License

This project is licensed under the MIT License. See the [LICENSE]() file for details.

---

## Contact

If you encounter bugs, have questions, or want to request a new feature, please [open an issue]() on this repository.   
