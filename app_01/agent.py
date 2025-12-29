
import os
import re
from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool
from google.adk.code_executors import BuiltInCodeExecutor

# ============================
# Environment validation
# ============================
HF_TOKEN = os.getenv("HUGGING_FACE_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

#HUGGING_FACE_TOKEN = "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"
#GITHUB_TOKEN = "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"


# ============================
# AI Developer News Agent
# ============================
search_agent = Agent(
    model="gemini-2.5-flash",
    name="AIDevSearchAgent",
    description="Specialist agent for AI news relevant to developers.",
    instruction="""
You are an AI News Analyst for developers.

Rules:
- Only discuss AI-related news relevant to developers.
- Always use google_search for factual information.

Workflow:
1. If the request is general AI news, ask:
   "Sure — how many news items would you like me to find?"
2. Use google_search to find recent articles.
3. Respond with:
   "Using google_search, here are the top headlines:"
   followed by a numbered list:
   1. Headline – Platform / Use case
4. Ask the user which headline to explore next.
5. When asked, provide a detailed summary and cite google_search.
""",
    tools=[google_search],
)

# ============================
# Python Code Execution Agent
# ============================
coding_agent = Agent(
    model="gemini-2.5-flash",
    name="CodeAgent",
    description="Executes safe Python code and returns results only.",
    instruction="""
You execute Python code safely.

Rules:
- Do NOT access the file system
- Do NOT import os, sys, subprocess, socket, or requests
- Do NOT perform network calls
- Do NOT run infinite loops
- Only return the execution result or error
""",
    code_executor=BuiltInCodeExecutor(),
)

# ============================
# Hugging Face MCP Agent
# ============================
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

hf_agent = Agent(
    model="gemini-2.5-flash",
    name="hugging_face_agent",
    description="Provides information about Hugging Face models, datasets, and Spaces.",
    instruction="""
If Hugging Face access is unavailable:
- Respond with: "Hugging Face integration is not configured."
Otherwise:
- Use MCP tools to answer Hugging Face questions.
""",
    tools=(
        [
            McpToolset(
                connection_params=StdioConnectionParams(
                    server_params=StdioServerParameters(
                        command="npx",
                        args=["-y", "@llmindset/hf-mcp-server"],
                        env={"HF_TOKEN": HF_TOKEN},
                    ),
                    timeout=30,
                ),
            )
        ]
        if HF_TOKEN
        else []
    ),
)


# ============================
# GitHub MCP Agent
# ============================
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams

git_agent = Agent(
    model="gemini-2.5-flash",
    name="github_agent",
    description="Read-only GitHub repository assistant.",
    instruction="""
If GitHub access is unavailable:
- Respond with: "GitHub integration is not configured."
Otherwise:
- Use GitHub MCP tools.
""",
    tools=(
        [
            McpToolset(
                connection_params=StreamableHTTPServerParams(
                    url="https://api.githubcopilot.com/mcp/",
                    headers={
                        "Authorization": f"Bearer {GITHUB_TOKEN}",
                        "X-MCP-Toolsets": "all",
                        "X-MCP-Readonly": "true",
                    },
                ),
            )
        ]
        if GITHUB_TOKEN
        else []
    ),
)


# ============================
# Root Routing Agent
# ============================
root_agent = Agent(
    name="RootAgent",
    model="gemini-2.5-flash",
    description="Strict routing agent that delegates to specialist agents.",
    instruction="""
You are a STRICT routing agent.

Routing rules:
- AI developer news → AIDevSearchAgent
- Python code execution → CodeAgent
- Hugging Face questions → hugging_face_agent
- GitHub repositories or activity → github_agent

Rules:
- Always delegate to a specialist agent
- NEVER answer directly
- If intent is unclear, ask the user to clarify
""",
    tools=[
        AgentTool(agent=search_agent),
        AgentTool(agent=coding_agent),
        AgentTool(agent=hf_agent),
        AgentTool(agent=git_agent),
    ],
)

# ============================
# Helper functions
# ============================
def extract_headlines(response_text: str):
    """Extracts numbered headlines from agent responses."""
    return re.findall(r"\d+\.\s*(.+?)\s*–", response_text)


def handle_user_input(user_input: str, session_state: dict):
    """
    Handles a single user message for ADK Web.
    """
    if session_state is None:
        session_state = {"headlines": []}

    headlines = session_state.get("headlines", [])

    # Exit
    if user_input.lower() in {"exit", "quit"}:
        return "Goodbye!", {"headlines": []}

    # Explicit Python execution trigger
    if user_input.lower().startswith("execute python code:"):
        code = user_input[len("execute python code:"):].strip()
        try:
            result = coding_agent.run(code)
            return f"**Code Result:**\n{result}", session_state
        except Exception as e:
            return f"Execution error: {e}", session_state

    # Headline selection
    if user_input.isdigit() and headlines:
        idx = int(user_input) - 1
        if 0 <= idx < len(headlines):
            headline = headlines[idx]
            summary = search_agent.run(
                f"Provide a detailed developer-focused summary for: {headline}"
            )
            return summary, session_state
        return "Invalid selection.", session_state

    # More news
    if user_input.lower() in {"more", "search more"} and headlines:
        response = root_agent.run("Find more AI news for developers")
        session_state["headlines"] = extract_headlines(response)
        return response, session_state

    # Default: delegate to RootAgent
    response = root_agent.run(user_input)
    session_state["headlines"] = extract_headlines(response)
    return response, session_state
