import os
import re
from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool
from google.adk.code_executors import BuiltInCodeExecutor

# ======================================================
# Environment variables
# ======================================================
HF_TOKEN = os.getenv("HUGGING_FACE_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
# ======================================================
# Helper functions
# ======================================================
def extract_headlines(text: str):
    return re.findall(r"\d+\.\s*(.+)", text)


def extract_repo_candidate(text: str):
    """
    STRICT GitHub repo extraction.
    Returns owner/repo or None.
    """
    match = re.search(r"(?:github\.com/)?([\w\-]+/[\w\-]+)", text)
    return match.group(1) if match else None


def extract_hf_candidate(text: str):
    """
    STRICT Hugging Face ID extraction: org/name
    """
    match = re.search(r"\b([\w\-]+/[\w\-]+)\b", text)
    return match.group(1) if match else None


# ======================================================
# AI Developer News Agent
# ======================================================
search_agent = Agent(
    model="gemini-2.5-flash",
    name="AIDevSearchAgent",
    description="AI developer news analyst with structured output.",
    instruction="""
You are an AI News Analyst for developers.

Rules:
- ONLY AI-related developer news
- ALWAYS use google_search
- DEFAULT to 3 articles if no number specified
- NEVER ask follow-up questions

Required output:

Using google_search, here are the top headlines:

---
[NUMBER]. HEADLINE

Summary:
1–2 sentence technical summary

Tech stack:
- frameworks / languages / infra OR Not mentioned

License:
- Open-source | Proprietary | Mixed | Not mentioned

GitHub repository:
- owner/repo if mentioned
- Otherwise: Not referenced

Hugging Face:
- Model / Dataset / Space if mentioned
- Otherwise: Not mentioned

Who should care:
- ML Engineer / Backend / MLOps / Data Scientist
---

End with:
"Which headline would you like to explore in more detail?"
""",
    tools=[google_search],
)

# ======================================================
# Python Execution Agent
# ======================================================
coding_agent = Agent(
    model="gemini-2.5-flash",
    name="CodeAgent",
    description="Safe Python execution agent.",
    instruction="""
Execute Python safely.

Rules:
- No filesystem access
- No network calls
- No infinite loops
- Return result or error only
""",
    code_executor=BuiltInCodeExecutor(),
)

# ======================================================
# Python Explanation Agent
# ======================================================
code_explain_agent = Agent(
    model="gemini-2.5-flash",
    name="CodeExplainAgent",
    description="Explains Python code safely.",
    instruction="""
Explain Python code step by step.
Do NOT execute or modify code.
""",
)

# ======================================================
# Hugging Face Canonical Reference Agent
# ======================================================
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

hf_agent = Agent(
    model="gemini-2.5-flash",
    name="hugging_face_agent",
    description="Returns canonical Hugging Face URLs for exact IDs.",
    instruction="""
Rules:
- ONLY accept exact Hugging Face IDs (org/name)
- NEVER guess or infer
- If not found, respond exactly:
"No Hugging Face resource found for the provided identifier."

Valid output ONLY:

Hugging Face URL:
https://huggingface.co/<exact_id>
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

# ======================================================
# GitHub MCP Agent (STRICT, DATA-ONLY)
# ======================================================
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams

git_agent = Agent(
    model="gemini-2.5-flash",
    name="github_agent",
    description="GitHub MCP repository inspector.",
    instruction="""
Input will be EXACT owner/repo.

MANDATORY:
- Call GitHub MCP
- No guessing
- No prose
- If MCP fails, say exactly:
  "No GitHub repository found."

Output format ONLY:

Repository: owner/repo
Stars: <number>
Forks: <number>
Open issues: <number>
Open PRs: <number>
Recent activity:
- Commits (30d): <number>
- Last commit date: <date>
Overall activity level: High | Medium | Low
""",
    tools=[
        McpToolset(
            connection_params=StreamableHTTPServerParams(
                url="https://api.githubcopilot.com/mcp/",
                headers={
                    "Authorization": f"Bearer {GITHUB_TOKEN}",
                    "X-MCP-Toolsets": "all",
                    "X-MCP-Readonly": "true",
                },
            )
        )
    ] if GITHUB_TOKEN else [],
)

# ======================================================
# Root Routing Agent
# ======================================================
root_agent = Agent(
    name="RootAgent",
    model="gemini-2.5-flash",
    description="Strict routing agent.",
    instruction="""
Routing rules:
- AI news → AIDevSearchAgent
- Python execution → CodeAgent
- Python explanation → CodeExplainAgent
- Hugging Face links → hugging_face_agent
- GitHub repos → github_agent

Rules:
- ALWAYS delegate
- NEVER answer directly
""",
    tools=[
        AgentTool(agent=search_agent),
        AgentTool(agent=coding_agent),
        AgentTool(agent=code_explain_agent),
        AgentTool(agent=hf_agent),
        AgentTool(agent=git_agent),
    ],
)

# ======================================================
# Main Input Handler
# ======================================================
def handle_user_input(user_input: str, session_state: dict):
    if session_state is None:
        session_state = {"headlines": []}

    if user_input.lower() in {"exit", "quit"}:
        return "Goodbye!", {"headlines": []}

    # Python execution
    if user_input.lower().startswith("execute python code:"):
        code = user_input[len("execute python code:"):].strip()
        return coding_agent.run(code), session_state

    # Python explanation
    if user_input.lower().startswith("explain this python code:"):
        code = user_input[len("explain this python code:"):].strip()
        return code_explain_agent.run(code), session_state

# 🔴 FORCE GitHub routing FIRST
    repo = extract_repo_candidate(user_input)
    if repo and "/" in repo:
        return git_agent.run(repo), session_state

    # Python execution
    #if user_input.lower().startswith("execute python code:"):
        #code = user_input.split(":", 1)[1]
        #return coding_agent.run(code), session_state


# ️⃣ Explicit Hugging Face ID → MCP
    hf_id = extract_hf_candidate(user_input)
    if hf_id and "/" in hf_id:
        hf_result = hf_agent.run(hf_id)
        if hf_result:
            return hf_result, session_state

 # Default routing
    response = root_agent.run(user_input)
    session_state["headlines"] = extract_headlines(response)
    return response, session_state

