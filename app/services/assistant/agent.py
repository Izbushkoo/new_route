from typing import List

from langchain.agents.openai_assistant import OpenAIAssistantRunnable

from app.models.database_models import UserSettings


# tools = [
#     Tool.from_function(
#         func=search_web,
#         description="is used to make a web search",
#         name="search_web",
#     )
# ]

# tools = [format_tool_to_openai_function(tool) for tool in tools]

from langchain_core.agents import AgentFinish



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

# res = openai.beta.threads.messages.list("thread_GbqfHXjcPt8x6mtczJWspbW0")
# print(res)
