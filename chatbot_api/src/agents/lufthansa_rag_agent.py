import os
from langchain_openai import ChatOpenAI
from langchain.agents import (
    create_openai_functions_agent,
    Tool,
    AgentExecutor,
)
from langchain import hub

# Import the RAG chains from the respective files (retrieval chain and cypher chain) in my project
from chatbot_api.src.chains.aktionaersinfos_retrieval_chain import text_qa_vector_chain
from chatbot_api.src.chains.lufthansa_cypher_chain import lufthansa_cypher_chain


# Use hwchase17 to create the agent
# The hwchase17/openai-tools repository is a comprehensive toolkit designed to enhance the
# interaction with OpenAI's API. After installation, developers can pull predefined prompts
# from the hub or create custom agents tailored

# The agent model decides which tools to call (see below) with what inputs
LUFTHANSA_AGENT_MODEL = os.getenv("LUFTHANSA_AGENT_MODEL")

# The agent needs a prompt
# Pulling a predefined prompt with hwchase17
# This prompt should have a placeholder for the Human message and an
# agent scratchpad (intermediate agent actions and tool output messages will be passed in here)
lufthansa_agent_prompt = hub.pull("hwchase17/openai-functions-agent")

#  list of tools your agent can use
tools = [
    Tool(
        name="Aktionaersinfos",
        func=text_qa_vector_chain.invoke,
        description="""Useful when you need to answer questions
        about the Lufthansa company and business developments, such as subdivisions, 
        plane models in use, environmental protection, strikes, social responsibility, and 
        any other qualitative question that could be answered about Lufthansa using semantic
        search. Not useful for answering objective questions that involve statistical data,
        such as Lufthansa stocks, flights per year, and other numerical data from the 
        annual report, and anything to do with
        counting, percentages, aggregations. Use the
        entire prompt as input to the tool. For instance, if the prompt is
        "In what ways does Lufthansa reduce CO2 emissions?", the input should be
        "In what ways does Lufthansa reduce CO2 emissions?".
        """,
    ),
    Tool(
        name="Graph-database",
        func=lufthansa_cypher_chain.invoke,
        description="""Useful for answering questions about Lufthansa
        statistics, such as number of flights carried out per year, stock prices, 
        balance sheet, profits, etc. 
        Use the entire prompt as input to the tool. For instance, if the prompt is 
        "How much were the earning per share in the year 2020?", the input should be 
        "How much were the earning per share in the year 2020?".
        """,
    ),
]

# Instantiate the agent

chat_model = ChatOpenAI(
    model=LUFTHANSA_AGENT_MODEL,
    temperature=0,
)

lufthansa_qa_agent = create_openai_functions_agent(
    llm=chat_model,
    prompt=lufthansa_agent_prompt,
    tools=tools,
)

# The agent needs an executor
# AgentExecutor implements the standard Runnable Interface.
# To create the agent run time, you pass your agent and tools into AgentExecutor.

lufthansa_qa_agent_executor = AgentExecutor(
    agent=lufthansa_qa_agent,
    tools=tools,
    return_intermediate_steps=True,
    verbose=True,
)
