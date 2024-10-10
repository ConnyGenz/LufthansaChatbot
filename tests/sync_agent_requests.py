import time
import requests

# URL to the chatbot served via FastAPI
CHATBOT_URL = "http://localhost:8000/lufthansa-rag-agent"

# List of questions to ask the chatbot
questions = [
   "Wer bist du?",
   "Wie ist das Wetter heute?",
   "Wie hoch war der Jahresschlusskurs der Lufthansa-Aktie im Jahr 2013?",
   "Wie geht es dir?",
   "Wie viele Flüge führte die Lufthansa im Jahr 2016 durch?",
   "Haben die Lufthansa-Mitarbeiter gestreikt?",
   "Wer sitzt im Vorstand der Lufthansa?",
   "Was unternimmt die Lufthansa, um ihren CO2-Ausstoß zu verringern?"
]

# Get the requests into the right format for a request via FastAPI
request_bodies = [{"text": q} for q in questions]

start_time = time.perf_counter()
# Post the requests to the chatbot and collect the answers
outputs = [requests.post(CHATBOT_URL, json=data) for data in request_bodies]
end_time = time.perf_counter()

print(f"Run time: {end_time - start_time} seconds")