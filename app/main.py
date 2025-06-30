from typing import TypedDict, Annotated
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
import asyncio
from dotenv import load_dotenv

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct")

message_history = []

async def main():
    try:
        server_params = StdioServerParameters(
            command="npx",
            args=["@cocal/google-calendar-mcp"],
            env={
                "GOOGLE_OAUTH_CREDENTIALS": r"D:\Github\gmeet-ai-agent\app\credentials.json"
            },
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()

                # Get tools
                tools = await load_mcp_tools(session)
                print(f"Loaded {len(tools)} tools: {[tool.name for tool in tools]}")

                # Create and run the agent
                agent = create_react_agent(llm, tools)
                print("🗓️ Google Calendar Agent (type 'exit' to quit)\n")
                
                while True:
                    user_input = input("🧑 You: ")
                    if user_input.lower() in ["exit", "quit"]:
                        break

                    # Add Human message to the message history
                    message_history.append(HumanMessage(content=user_input))
                    print("Input:", user_input)
                    
                    try:
                        # Pass the actual user input and message history to the agent
                        agent_response = await agent.ainvoke({
                            "messages": message_history
                        })
                        
                        # Get the last message from the response (which is the agent's response)
                        if "messages" in agent_response and agent_response["messages"]:
                            last_message = agent_response["messages"][-1]
                            
                            # Check if it's an AI message and get the content
                            if isinstance(last_message, AIMessage):
                                agent_content = last_message.content
                            else:
                                agent_content = str(last_message.content)
                            
                            # Add agent's response to message history
                            message_history.append(AIMessage(content=agent_content))
                            print("🤖 Agent:", agent_content, "\n")
                        else:
                            print("🤖 Agent: No response received\n")
                            
                    except Exception as e:
                        print(f"Error processing request: {e}")
                        print("Continuing...\n")

                await session.shutdown()

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())