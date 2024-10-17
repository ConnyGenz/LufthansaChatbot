import dotenv
dotenv.load_dotenv()
from chatbot_api.src.agents.lufthansa_rag_agent import lufthansa_qa_agent_executor

question = "Hier beliebige Frage einfügen"
response = lufthansa_qa_agent_executor.invoke({"input": question})
