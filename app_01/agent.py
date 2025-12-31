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
# AI Developer News Agent (FIXED – NO LOOPS)
# ======================================================
search_agent = Agent(
    model="gemini-2.5-flash",
    name="AIDevSearchAgent",
    description="Specialist agent for AI developer news with structured enrichment.",
    instruction="""
You are an AI News Analyst for developers.

Scope:
- ONLY AI-related news relevant to developers.
- ALWAYS use google_search for factual information.

Rules:
- NEVER ask follow-up questions.
- If the user does not specify a number of articles, DEFAULT to 3.
- If a number is present in the request, use it as the article count.

Response format (REQUIRED):

Using google_search, here are the top headlines:

---
[NUMBER]. HEADLINE

Summary:
1–2 sentence technical summary

Tech stack:
- frameworks / languages / infrastructure OR "Not mentioned"

License:
- Open-source | Proprietary | Mixed | Not mentioned

GitHub repository:
- Repository name if explicitly referenced
- Otherwise: Not referenced

Hugging Face:
- Model / Dataset / Space name if mentioned
- Otherwise: Not mentioned

Who should care:
- ML Engineer / Backend Engineer / MLOps / Data Scientist
---

End by asking:
"Which headline would you like to explore in more detail?"
""",
    tools=[google_search],
)


# ======================================================
# Python Code Execution Agent
# ======================================================
coding_agent = Agent(
    model="gemini-2.5-flash",
    name="CodeAgent",
    description="Executes safe Python code in a sandbox.",
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
# Python Code Explanation Agent
# ============================
code_explain_agent = Agent(
    model="gemini-2.5-flash",
    name="CodeExplainAgent",
    description="Explains Python code without executing it.",
    instruction="""
Explain Python code clearly and safely.

Rules:
- Do NOT execute code
- Do NOT modify code
- Explain step-by-step
- Mention pitfalls or edge cases if relevant
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
    description="Returns validated canonical Hugging Face URLs for exact IDs only.",
    instruction="""
You are a Hugging Face reference agent.

STRICT RULES:
- ONLY return a Hugging Face URL if the user provides an EXACT Hugging Face ID.
- Do NOT guess, normalize, or infer names.

If the resource does not exist, respond:
"No Hugging Face resource found for the provided identifier."

Output format (ONLY if validated):

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
# GitHub MCP Agent
# ======================================================
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams

git_agent = Agent(
    model="gemini-2.5-flash",
    name="github_agent",
    description="Read-only GitHub repository enrichment agent.",
    instruction="""
You are a GitHub repository reference agent.

Rules:
- ONLY summarize repositories explicitly mentioned by the user.
- Do NOT invent repositories.

If no repository is mentioned or found:
Respond with:
"No GitHub repository found."
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


# ======================================================
# Root Routing Agent
# ======================================================
root_agent = Agent(
    name="RootAgent",
    model="gemini-2.5-flash",
    description="Strict routing agent that delegates all work to specialists.",
    instruction="""
You are a STRICT routing agent.

Routing rules:
- AI developer news → AIDevSearchAgent
- Python execution or code explanation → CodeAgent
- Python code explanation → CodeExplainAgent
- Hugging Face canonical links → hugging_face_agent
- GitHub repositories or activity → github_agent

Rules:
- ALWAYS delegate
- NEVER answer directly
- Ask for clarification only if intent is unclear
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
# Helper functions
# ======================================================
def extract_headlines(response_text: str):
    return re.findall(r"\d+\.\s*(.+)", response_text)


def extract_limit(text: str, default: int = 3) -> int:
    match = re.search(r"\b(\d+)\b", text)
    return int(match.group(1)) if match else default


def handle_user_input(user_input: str, session_state: dict):
    if session_state is None:
        session_state = {"headlines": []}

    headlines = session_state.get("headlines", [])

    # Exit
    if user_input.lower() in {"exit", "quit"}:
        return "Goodbye!", {"headlines": []}

    # Explicit Python execution
    if user_input.lower().startswith("execute python code:"):
        code = user_input[len("execute python code:"):].strip()
        try:
            result = coding_agent.run(code)
            return f"**Code Result:**\n{result}", session_state
        except Exception as e:
            return f"Execution error: {e}", session_state

    # Explicit Python code explanation

    if user_input.lower().startswith("explain this python code:"):
        code = user_input[len("explain this python code:"):].strip()
        return code_explain_agent.run(code), session_state

    # Headline selection
    if user_input.isdigit() and headlines:
        idx = int(user_input) - 1
        if 0 <= idx < len(headlines):
            headline = headlines[idx]

            summary = search_agent.run(
                f"Provide a deeper technical summary for: {headline}"
            )

            github_info = git_agent.run(
                "Summarize the GitHub repository mentioned, if any."
            )

            hf_info = hf_agent.run(
                "Return the Hugging Face URL if an exact ID is mentioned."
            )

            return (
                f"{summary}\n\n---\n"
                f"GitHub enrichment:\n{github_info}\n\n"
                f"Hugging Face enrichment:\n{hf_info}"
            ), session_state

    # Default routing (news count handled by agent)
    response = root_agent.run(user_input)
    session_state["headlines"] = extract_headlines(response)
    return response, session_state
