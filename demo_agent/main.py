from agents import Agent, Runner, ModelSettings, HostedMCPTool
from dotenv import load_dotenv
import os
import asyncio

from demo_agent.prompt_library import language_prompts, framework_prompts
from .tools import ls, read_files, tree, glob, ast_grep
from .models import LanguageFrameworkResult

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
        "You are a code review agent. You will be given files in a codebase and you will need to review it."
        "Your job is to specifically focus on the database schema, queries and architecture design pertaining to performance."
        "You may run read-only queries on the db to get detailed information about the schema, queries and performance, especially running the EXPLIN queries"
        "Use context7_mcp_server to read documentation about the language, framework, libraries, etc."
        "Use ast_grep to search for specific patterns in the codebase."
        "Use glob to search for files in the codebase."
        "Use ls to list the files in the codebase."
        "Use tree to visualize the directory structure of the codebase."
        "Use read_files to read the contents of the files in the codebase."
        "Do not suggest anything just because you are asked. Before suggesting anything, think if an engineer would find it helpful and necessary."
    ),
    tools=[ls, tree, read_files, ast_grep, glob, context7_mcp_server],
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
            f"The given codebase is written in {lang_framework_result.final_output.language} using {lang_framework_result.final_output.framework}. "
            f"{language_prompts.get(lang_framework_result.final_output.language, "")} "
            f"{framework_prompts.get(lang_framework_result.final_output.framework, "")}"
            f"Review the APIs in privybox/activity/views.py"
        ),
    )

    print(f"Review: {review_agent_result.final_output}")






def cli():
    """CLI entry point - synchronous wrapper for the async main function"""
    asyncio.run(main())


if __name__ == "__main__":
    cli()
