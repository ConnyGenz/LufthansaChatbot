import os
import requests
import streamlit as st

CHATBOT_URL = os.getenv("CHATBOT_URL", "http://localhost:8000/lufthansa-rag-agent")

with st.sidebar:
    st.header("About")
    st.markdown(
        """
        Dieser Chatbot ist das Bachelor-Projekt von Cornelia Genz. Er basiert auf 
        ChatGPT(ggf. anderen Sprachmodellen) und nutzt das Prinzip der 
        Retrieval-Augmented-Generation, um Fragen über die Fluggesellschaft Lufthansa
        zu beantworten. Dazu stehen die Aktionärsinformationen der Jahre 2017-2021 in 
        vektorisierter Form sowie Leistungsdaten des Unternehmens der Jahre 2010-2023
        in einer Graph-Datenbank zur Verfügung. Der Chatbot wurde mit der Bibliothek
        [LangChain](https://python.langchain.com/docs/get_started/introduction)
        als Agent realisiert und in Python programmiert.
        """
    )

    st.header("Beispielfragen")
    st.markdown("- Wer bist du?")
    st.markdown("- Wie ist das Wetter heute?")
    st.markdown("- Wie hoch war der Jahresschlusskurs der Lufthansa-Aktie im Jahr 2013??")
    st.markdown("- Wie viele Flüge führte die Lufthansa im Jahr 2016 durch?")
    st.markdown("- Haben die Lufthansa-Mitarbeiter gestreikt?")
    st.markdown("- Wie wurde auf den Streik der Lufthansa-Mitarbeiter reagiert?")
    st.markdown("- Wer sitzt im Vorstand der Lufthansa?")
    st.markdown("- Was unternimmt die Lufthansa, um ihren CO2-Ausstoß zu verringern?")
    st.markdown("- In welchen Jahren wurde für die Lufthansa-Aktie keine Dividende ausgeschüttet?")
    st.markdown("- Um wie viel Euro veränderte sich der Jahresschlusskurs der Lufthansa-Aktie vom Jahr 2010 zum Jahr 2011?")
    st.markdown("- In welchem Jahr hatte die Lufthansa den niedrigsten Sitzladefaktor?")
    st.markdown("- Wie viele Flüge hat die Lufthansa im Jahr durchschnittlich durchgeführt?")


st.title("Bachelor-Projekt Lufthansa-Chatbot")
st.info(
    """Hier können Sie Fragen zur Fluggesellschaft Lufthansa und deren Geschäftsentwicklung
    in den letzten 14 Jahren stellen."""
)

# Generate empty list of messages. This will store the chat history.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all the messages from message history with role+message
# Add intermediate steps as explanation?
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "output" in message.keys():
            st.markdown(message["output"])

        if "explanation" in message.keys():
            with st.status("How was this generated", state="complete"):
                st.info(message["explanation"])

# Prompt takes the user's inpput and formats it as a user chat message
if prompt := st.chat_input("Was möchten Sie wissen?"):
    st.chat_message("user").markdown(prompt)

    # The user's question is added to the chat history
    st.session_state.messages.append({"role": "user", "output": prompt})

    # User question is formatted to send to the chatbot API
    data = {"text": prompt}

    with st.spinner("Antwort wird gesucht..."):
        # The question is sent to the chatbot API
        response = requests.post(CHATBOT_URL, json=data)

        # For a successful response from the API, get the text response from the agent
        # and also the intermediate steps from the chain
        if response.status_code == 200:
            output_text = response.json()["output"]
            explanation = response.json()["intermediate_steps"]

        # For an unsuccessful response from the API, generate error message
        else:
            output_text = """Bei der Bearbeitung Ihrer Anfrage ist ein Fehler aufgetreten.
            Bitte versuchen Sie es erneut, gegebenenfalls mit einer umformulierten Anfrage."""
            explanation = output_text

    # Response from the chatbot API is formatted as a chat message
    st.chat_message("assistant").markdown(output_text)
    st.status("How was this generated", state="complete").info(explanation)

    # Format the output to be given as a message and append to "messages", which serves
    # as the chat history in this UI.
    st.session_state.messages.append(
        {
            "role": "assistant",
            "output": output_text,
            "explanation": explanation,
        }
    )

