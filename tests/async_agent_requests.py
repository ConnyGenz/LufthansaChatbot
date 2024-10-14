import asyncio
import time
import httpx

# URL to the chatbot served via FastAPI
CHATBOT_URL = "http://localhost:8000/lufthansa-rag-agent"

# Function to make one asynchronous request
async def make_async_post(url, data):
    timeout = httpx.Timeout(timeout=120)
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, timeout=timeout)
        return response


# Function to make several asynchronous requests at once using the above function
async def make_bulk_requests(url, data):
    tasks = [make_async_post(url, payload) for payload in data]
    responses = await asyncio.gather(*tasks)
    outputs = [r.json()["output"] for r in responses]
    return outputs

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
outputs = asyncio.run(make_bulk_requests(CHATBOT_URL, request_bodies))
end_time = time.perf_counter()

print(f"Run time: {end_time - start_time} seconds")