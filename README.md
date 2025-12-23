# Toolkit Agents with Google’s Agent Development Kit (ADK)   

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


## Repository structure (Project Structure)

```bash
Toolkit_Google_ADK/(ai_dev_news_web)
├── app.py
├── requirements.txt
├── .env.example
├── licence
├── README.md
```




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

### Launch the ADK Web App  
Run:  
```
adk web
```
- It will start a local web server.  
- Open the provided URL in a browser.  
- You can now chat with your AI Developer News + Code Assistant + HuggingFace + GitHub interactively.    


## Examples Usage 




## References  

- [Google AI Studio](https://cloud.google.com/free?hl=en)
- [Gemini API key](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/quickstart?usertype=apikey#python-gen-ai-sdk)
- [Gemini Models](https://ai.google.dev/gemini-api/docs/models#model-variations)  
- 

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/micag2025/Toolkit_Google_ADK/blob/d18bda56849caea6efeda3803da893b29d5bfa23/LICENSE) file for details.

---

## Contact

If you encounter bugs, have questions, or want to request a new feature, please [open an issue](https://github.com/micag2025/Toolkit_Google_ADK/issues) on this repository.   
