from agents import Agent, Runner, ModelSettings, HostedMCPTool
from dotenv import load_dotenv
import os
import asyncio

from demo_agent.prompt_library import language_prompts, framework_prompts
from .tools import ls, read_files, tree, glob, ast_grep, find
from .models import LanguageFrameworkResult
from .schemas import ReviewResult

# Load environment variables from .env file in the project root
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

# Simple language and framework detection agent
stack_detection_agent = Agent(
    name="stack_detection_agent",
    instructions=(
        "You are a quick identifier of programming language and framework. "
        "Be efficient: "
        "1) Run ls to see file extensions and structure "
        "2) Run tree only if ls does not provide enough information to identify the language and framework "
        "3) Check main config file(s) (package.json, requirements.txt, go.mod, Cargo.toml, etc.) "
        "Only identify language and framework. Return immediately once identified. Use None if not clear from file structure."
    ),
    output_type=LanguageFrameworkResult,
    tools=[ls, tree, read_files],
    model_settings=ModelSettings(
        parallel_tool_calls=True,
    ),
)

# database_mcp_server = HostedMCPTool(
#     tool_config = {
#         "type": "mcp",
#         "server_label": "google_mcp_toolbox_for_database",
#         "server_url": "http://localhost:5000",
#         "require_approval": "never",
#     },
# )

context7_mcp_server = HostedMCPTool(
    tool_config = {
        "type": "mcp",
        "server_label": "context7_mcp_server",
        "server_url": "https://mcp.context7.com/mcp",
        "require_approval": "never",
        "headers": {
            "Authorization": f"Bearer {os.getenv('CONTEXT7_API_KEY')}",
        },
    },
)

review_agent = Agent(
    name="review_agent",
    instructions=(
        "You are a focused code review agent specializing in database performance.\n"
        "IMPORTANT: Be mindful of token usage - focus on the specific file requested first.\n"
        "Process:\n"
        "1. Start by reading ONLY the target file specified\n"
        "2. Identify imports and references that need context\n"
        "3. Only read additional files if they contain:\n"
        "   - Database models referenced in the target file\n"
        "   - Utility functions called from the target file\n"
        "   - Parent classes or interfaces\n"
        "4. Use ast_grep to find specific patterns instead of reading entire files\n"
        "5. When reading large files, use max_lines_per_file parameter (e.g., 200 lines)\n"
        "6. Use ls or find or glob if necessary for finding a specific file or snippets of code\n"
        "Review focus: database schema, queries, and performance architecture.\n"
        "Only suggest improvements that would be helpful and necessary for an engineer."
    ),
    output_type=ReviewResult,
    tools=[read_files, ast_grep, glob, find, ls, context7_mcp_server],
    model_settings=ModelSettings(
        parallel_tool_calls=True,
    ),

)

async def main():
    print("Hello from demo-agent!")

    # Step 1: Detect language and framework
    print("Step 1: Detecting language and framework...")
    lang_framework_result = await Runner.run(
        starting_agent=stack_detection_agent,
        input="Identify the programming language and framework of this codebase. Be quick and efficient.",
    )

    print(f"Detected: {lang_framework_result.final_output.language}, {lang_framework_result.final_output.framework}")


    review_agent_result = await Runner.run(
        starting_agent=review_agent,
        input=(
            f"Language: {lang_framework_result.final_output.language}\n"
            f"Framework: {lang_framework_result.final_output.framework}\n"
            f"Target file: privybox/activity/views.py\n"
            f"Task: Review this specific file for database performance issues.\n"
            f"Start by reading ONLY this file, then identify what additional context you need."
        ),
        max_turns=60
    )

    print(f"Review: {review_agent_result.final_output}")






def cli():
    """CLI entry point - synchronous wrapper for the async main function"""
    asyncio.run(main())


if __name__ == "__main__":
    cli()
