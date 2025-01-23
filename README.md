# About

Bachelor's thesis project.
A chatGPT-based RAG chatbot answering questions about German airline Lufthansa

> [!IMPORTANT]
> This project does not function without a `.env` file in the root folder.

> [!IMPORTANT]
> If you are using the `.env` file provided by the author, the project will not function if
 the author's neo4j database is not running. You may create your own neo4j database to be independent
 of the author's database. See [Step 3: Set Up a Neo4j Graph Database](https://realpython.com/build-llm-rag-chatbot-with-langchain/#step-3-set-up-a-neo4j-graph-database).

> [!IMPORTANT]
> For the **main branch**, you need to install the [Docker](https://www.docker.com/products/docker-desktop/) containerization software.

# .env file

This project uses APIs and services for which accounts, passwords and API keys are required.
These need to be specified in a `.env` file. This file also contains project parameters,
namely some paths to source data files and the names of the language models to be used.

The **.env file** may be requested from the author of this repository, or it may be created by
project users themselves who are going to use their own accounts and API keys. The name of the file must be `.env`
and it must be located in the root directory of the project. The parameters specified in the table below must be 
written into the `.env` file with their corresponding values (OPENAI_API_KEY=foobar123, and so on).

**Parameters to be set in the .env file:**

| Parameter name | Parameter value                                                                                                                                                              |
|---|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| OPENAI_API_KEY | OpenAI API key, [see here how to create one](https://platform.openai.com/docs/quickstart).                                                                                   |
| NEO4J_URI | Uniform Resource Identifier of the neo4j database, [issued upon creation](https://realpython.com/build-llm-rag-chatbot-with-langchain/#step-3-set-up-a-neo4j-graph-database) |
| NEO4J_USERNAME | User name of the neo4j database, [issued upon creation](https://realpython.com/build-llm-rag-chatbot-with-langchain/#step-3-set-up-a-neo4j-graph-database)                   |
| NEO4J_PASSWORD | Password of the neo4j database, [issued upon creation](https://realpython.com/build-llm-rag-chatbot-with-langchain/#step-3-set-up-a-neo4j-graph-database)                    |
| LUFTHANSA_AGENT_MODEL | Language model for chatbot agent                                                                                                                                             |
| LUFTHANSA_CYPHER_MODEL | Language model for cypher query generation                                                                                                                                   |
| LUFTHANSA_QA_MODEL | Language model for cypher chain QA and retrieval chain QA                                                                                                                    |
| AKTIE_CSV_PATH | Path to statistical source data file ´aktie.csv´, needs to be an online location                                                                                             |
| LEISTUNG_CSV_PATH | Path to statistical source data file ´leistungsdaten.csv´, needs to be an online location                                                                                    |
| UMSATZ_CSV_PATH | Path to statistical source data file ´umsatz_ergebnis.csv´, needs to be an online location                                                                                   |
| AGGREGATE_CSV_PATH | Path to statistical source data file ´aggregate.csv´, needs to be an online location                                                                                         |
| CHATBOT_URL | FastAPI URL of the chatbot, needed by Streamlit GUI                                                                                                                           |


# Branches

This project has 2 major branches: `main` and `more_control`. For the **main branch**, you need not install dependencies
manually, but you need to install the [Docker](https://www.docker.com/products/docker-desktop/) containerization software. 
The **main branch** provides a browser-based **GUI** for users to interact with the chatbot.

The **more_control** branch runs without Docker, directly in the IDE. It also has a  

# Starting the main branch:

1. Install the [Docker](https://www.docker.com/products/docker-desktop/) containerization software.
2. Start Docker Desktop.
3. Open the project in your IDE.
4. Add a `.env` file to the root directory of the project. You can either request one from the author or create your own (see [.env file](#env-file) above).
5. Make sure the neo4j database (the one that contains statistical Lufthansa data) is running. If you are using the author's
database, contact the author about this. Otherwise, create your own [neo4j database](https://realpython.com/build-llm-rag-chatbot-with-langchain/#step-3-set-up-a-neo4j-graph-database)
and write the required neo4j parameters into the `.env` file.
6. Open a terminal in your IDE and enter the following command: `docker-compose up --build`.
7. Wait for the Docker containers to be created and for the code to be executed. This may take around 5 minutes.
8. Open the Streamlit GUI in your browser under the following address: `http://localhost:8501`. You can now chat with the chatbot there.
9. Alternatively, you may open the FastAPI in your browser (`http://localhost:8000/docs`) and test the chatbot there.

# Starting the more_control branch: