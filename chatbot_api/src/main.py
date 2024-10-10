from fastapi import FastAPI
from agents.lufthansa_rag_agent import lufthansa_qa_agent_executor
from models.lufthansa_retrieval_query import LufthansaQueryInput, LufthansaQueryOutput
from utils.async_utils import async_retry

# Instantiate a FastAPI object
app = FastAPI(
    title="Lufthansa Chatbot",
    description="Endpoints for a Lufthansa chatbot with text and database retrieval",
)

# Function takes string query and invokes the agent (as defined in lufthansa_rag_agent.py)
# asynchronously (async ... await). Retry if needed.
@async_retry(max_retries=10, delay=1)
async def invoke_agent_with_retry(query: str):
    """Retry the agent if a tool fails to run.

    This can help when there are intermittent connection issues
    to external APIs.
    """
    return await lufthansa_qa_agent_executor.ainvoke({"input": query})

@app.get("/")
async def get_status():
    return {"status": "running"}

# This function serves POST requests to the agent at "/lufthansa-rag-agent"
# and returns the response
# The query comes in my "LufthansaQueryInput format (has one string parameter "text")
# In order to get the response from the agent, the function "invoke_agent_with_retry" as
# defined above is executed
@app.post("/lufthansa-rag-agent")
async def query_lufthansa_agent(query: LufthansaQueryInput) -> LufthansaQueryOutput:
    query_response = await invoke_agent_with_retry(query.text)
    query_response["intermediate_steps"] = [
        str(s) for s in query_response["intermediate_steps"]
    ]

    return query_response