#!/bin/bash

# Run any setup steps or pre-processing tasks here
echo "FastAPI-Service für Lufthansa-Retrieval-Chatbot wird gestartet..."

# Start the main application
# In chatbot_api>src >main.py, the FastAPI object was instantiated as "app"
# The following command runs the FastAPI application at port 8000 on your machine
uvicorn main:app --host 0.0.0.0 --port 8000