import asyncio
from dotenv import load_dotenv

from agents import (
    Agent,
    Runner,
    HostedMCPTool,
    MCPToolApprovalRequest,
    MCPToolApprovalFunctionResult,
)

load_dotenv()


SAFE_TOOLS = {
    "read_wiki_structure",
    "read_wiki_contents",
    "ask_question",
}


def approve_tool(
    request: MCPToolApprovalRequest,
) -> MCPToolApprovalFunctionResult:

    print(f"\nTool Requested: {request.data.name}")

    if request.data.name in SAFE_TOOLS:
        print("Approved")
        return {"approve": True}

    print("Rejected ")
    return {
        "approve": False,
        "reason": "Escalate to a human reviewer",
    }



deepwiki = HostedMCPTool(
    tool_config={
        "type": "mcp",
        "server_label": "deepwiki",
        "server_url": "https://mcp.deepwiki.com/mcp",
        "require_approval": "always",
    },
    on_approval_request=approve_tool,
)


agent = Agent(
    name="DeepWiki Assistant",
    instructions="""
You are an AI assistant.

Whenever possible use the DeepWiki MCP server.

Answer the user's questions clearly.
""",
    tools=[deepwiki],
)



async def main():

    print("=" * 50)
    print("DeepWiki MCP Assistant")
    print("Type 'exit' to quit")
    print("=" * 50)

    while True:

        question = input("\nYou: ")

        if question.lower() == "exit":
            print("Goodbye")
            break

        try:

            result = await Runner.run(
                agent,
                question,
            )

            print("\nAssistant:\n")
            print(result.final_output)

        except Exception as e:
            print("\nError:")
            print(e)


if __name__ == "__main__":
    asyncio.run(main())