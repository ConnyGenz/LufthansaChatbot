import dotenv
dotenv.load_dotenv()
from chatbot_api.src.agents.lufthansa_rag_agent import lufthansa_qa_agent_executor

question = "Wie viele Flugzeuge welchen Flugzeugtyps möchte die Lufthansa bis 2027 anschaffen?"
question= "Welche Positionen könnten Max Strobel und Nina Hagenau potentiell bei der Lufthansa innehaben?"
response = lufthansa_qa_agent_executor.invoke({"input": question})
