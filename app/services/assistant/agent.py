from dotenv import load_dotenv

load_dotenv()

from langchain.agents.openai_assistant import OpenAIAssistantRunnable
from langchain.tools import tool, Tool
from langchain.callbacks import FinalStreamingStdOutCallbackHandler
from langchain.agents import AgentExecutor


def search_web(query: str) -> str:
    """is used to make a web search"""
    # await asyncio.sleep(1)
    print("tool was used")
    return "inspecto patronum"


tools = [
    Tool.from_function(
        func=search_web,
        description="is used to make a web search",
        name="search_web",
    )
]

# tools = [format_tool_to_openai_function(tool) for tool in tools]

from langchain_core.agents import AgentFinish


async def execute_agent(agent, tools, input, thread_id):
    tool_map = {tool.name: tool for tool in tools}
    input.update({"thread_id": "thread_M2gJBB1QZwgMl020n2wUNOvx"})
    response = await agent.ainvoke(input)
    while not isinstance(response, AgentFinish):
        tool_outputs = []
        for action in response:
            print(action.tool_input)
            tool_output = await tool_map[action.tool].ainvoke(action.tool_input)
            print(action.tool, action.tool_input, tool_output, end="\n\n")
            tool_outputs.append(
                {"output": tool_output, "tool_call_id": action.tool_call_id}
            )
        print(action.thread_id)
        response = await agent.ainvoke(
            {
                "tool_outputs": tool_outputs,
                "run_id": action.run_id,
                "thread_id": thread_id,
            }
        )

    return response


async def main():
    # test_assistant = OpenAIAssistantRunnable.create_assistant(
    #     name="New test",
    #     instructions="Answer users questions using appropriate tools",
    #     tools=tools,
    #     model="gpt-4-1106-preview",
    #     as_agent=True
    # )
    #
    # print(test_assistant)
    agent = OpenAIAssistantRunnable(assistant_id="asst_SziteqdkuV6ghYQNlmTSeeAy", as_agent=True, streaming=True,
                                    )
    print(agent)
    # print(agent)
    response = await execute_agent(agent, tools,
                                   {
                                       "content": "make a web search about patronum and return what would you find exactly"},
                                   thread_id="thread_M2gJBB1QZwgMl020n2wUNOvx")

    # exec_ = AgentExecutor(agent=agent, tools=tools)
    # response = exec_.invoke({"content": "make a web search about patronum and return what would you find exactly"})
    print(response)


# thread_GbqfHXjcPt8x6mtczJWspbW0
# asyncio.run(main())
from langchain.schema.messages import messages_from_dict

res = openai.beta.threads.messages.list("thread_GbqfHXjcPt8x6mtczJWspbW0")
print(res)
