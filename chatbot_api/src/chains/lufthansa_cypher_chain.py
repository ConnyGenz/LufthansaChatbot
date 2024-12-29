import os
import dotenv
from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

# Load variables from .env file
# Can also be passed into the Docker container that runs your script in another way
dotenv.load_dotenv()

# Access necessary environment variables
LUFTHANSA_QA_MODEL = os.getenv("LUFTHANSA_QA_MODEL")
LUFTHANSA_CYPHER_MODEL = os.getenv("LUFTHANSA_CYPHER_MODEL")

# Create Langchain object Neo4jGraph based on my graph database
graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
)

# to sync any recent changes to the graph instance
graph.refresh_schema()

# Create a prompt for the cypher chain
cypher_generation_template = """
Task:
Generate Cypher query for a Neo4j graph database.

Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.

Schema:
{schema}

Note:
Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything other than
for you to construct a Cypher statement. Do not include any text except
the generated Cypher statement. Make sure the direction of the relationship is
correct in your queries. Make sure you alias both entities and relationships
properly. Do not run any queries that would add to or delete from
the database. If you need to divide numbers, make sure to filter the denominator 
to be non zero. The requests based on which you should create cypher queries will 
be in German, the names for the nodes and properties in the graph are German, as well.

Examples:
# Was war der Jahresschlusskurs der Lufthansa-Aktie im Jahr 2017?
MATCH (aktie:Aktie)
WHERE aktie.jahr=2017
RETURN aktie.jahresschlusskurs

# Wie viel betrug das Ergebnis pro Aktie im Jahr 2020?
MATCH (aktie:Aktie)
WHERE aktie.jahr=2020
RETURN aktie.jahr, aktie.ergebnis_pro_aktie

# In welchem Jahr war der Schlusskurs der Lufthansa-Aktie am höchsten?
MATCH (aktie:Aktie)
RETURN aktie.jahr AS Jahr, aktie.jahresschlusskurs AS Schlusskurs
ORDER BY Schlusskurs DESC 
LIMIT 1

# In welchen Jahren wurde für die Lufthansa-Aktie keine Dividende ausgeschüttet?
MATCH (aktie:Aktie)
WHERE aktie.dividendenvorschlag = 0
RETURN aktie.jahr AS Jahr

# Um wie viel Euro veränderte sich der Jahresschlusskurs der Lufthansa-Aktie 
# vom Jahr 2010 zum Jahr 2011?
MATCH (aktie1:Aktie), (aktie2:Aktie)
WHERE aktie1.jahr = 2010 AND aktie2.jahr = 2011
RETURN aktie2.jahresschlusskurs - aktie1.jahresschlusskurs

# Wie hoch ist der Jahresschlusskurs der Lufthansa Aktie im Jahr 2021 im Vergleich 
# mit dem Jahresschlusskurs im Jahr 2011 in Prozent?
MATCH (aktie1:Aktie), (aktie2:Aktie)
WHERE aktie1.jahr = 2011 AND aktie2.jahr = 2021
RETURN aktie2.jahresschlusskurs/(aktie1.jahresschlusskurs/100)

# In welchen Jahren war das Ergebnis pro Aktie negativ?
MATCH (aktie:Aktie)
WHERE aktie.ergebnis_pro_aktie < 0
RETURN aktie.jahr

# In welchem Jahr hatte die Lufthansa den niedrigsten Sitzladefaktor?
MATCH (leistung:Leistung)
RETURN leistung.jahr AS Jahr, leistung.sitzladefaktor AS Sitzladefaktor
ORDER BY Sitzladefaktor ASC
LIMIT 1

# Wie viele Flüge hat die Lufthansa im Jahr durchschnittlich durchgeführt?
MATCH (leistung:Leistung)
RETURN avg(leistung.fluege) AS Durchschnitt

# Wie viele Flüge hat die Lufthansa zwischen 2019 und 2022 durchgeführt?
MATCH (leistung:Leistung)
WHERE leistung.jahr >= 2019 AND leistung.jahr <= 2022
RETURN sum(leistung.fluege) AS Summe_Flüge

# Ist die Zahl der von Lufthansa durchgeführten Flüge im Jahr 2014 im Vergleich 
# zum Vorjahr gestiegen oder gesunken?
MATCH (leistung:Leistung)
WHERE leistung.jahr = 2013 OR leistung.jahr = 2014
RETURN leistung.jahr, leistung.fluege

# In welchen Jahren führte die Lufthansa weniger als 1000000 Flüge durch?
MATCH (leistung:Leistung)
WHERE leistung.fluege < 1000000
RETURN leistung.jahr

# Nenne mir die Kennzahlen der Lufthansa für das Jahr 2013.
MATCH (aggregate:Aggregat)-[r]-(n)
WHERE aggregate.jahr = 2011
RETURN n

# In welchem Jahr war der Schlusskurs der Lufthansa-Aktie höher? 2010 oder 2014?
MATCH (n:Aktie), (m:Aktie)
WHERE n.jahr = 2010 AND m.jahr = 2014
WITH n.jahresschlusskurs AS JSK2014, m.jahresschlusskurs AS JSK2010
RETURN 
CASE JSK2014
WHEN > JSK2010 THEN "2014 ist größer"
WHEN < JSK2010 THEN "2010 ist größer"
ELSE "Keiner der beiden Werte ist höher"
END

If the user question resembles one of the examples, do take the cypher query from the example.

The question is:
{question}
"""

cypher_generation_prompt = PromptTemplate(
    input_variables=["schema", "question"], template=cypher_generation_template
)

# prompt template for the question-answer component of the cypher chain

qa_generation_template = """You are an assistant that takes the results
from a Neo4j Cypher query and forms a human-readable response. The
query results section contains the results of a Cypher query that was
generated based on a user's natural language question. The provided
information is authoritative, you must never doubt it or try to use
your internal knowledge to correct it. Make the answer sound like a
response to the question.

Query Results:
{context}

Question:
{question}

If the provided information is empty, say you don't know the answer.
Empty information looks like this: []

If the information is not empty, you must provide an answer using the
results. If the question involves the Lufthansa-Aktie, and the result is not a year, 
assume that any numerical results of the Cypher query are expressed in euros.

When decimal numbers are provided in the query results, round them to two digits
behind the decimal point.

Provide your answer in the German language.

Helpful Answer:
"""

qa_generation_prompt = PromptTemplate(
    input_variables=["context", "question"], template=qa_generation_template
)

lufthansa_cypher_chain = GraphCypherQAChain.from_llm(
    cypher_llm=ChatOpenAI(model=LUFTHANSA_CYPHER_MODEL, temperature=0),
    qa_llm=ChatOpenAI(model=LUFTHANSA_QA_MODEL, temperature=0),
    graph=graph,
    verbose=True,
    qa_prompt=qa_generation_prompt,
    cypher_prompt=cypher_generation_prompt,
    validate_cypher=True,
    top_k=100,
    # In order to use this chain, you must acknowledge that it can make dangerous
    # requests by setting `allow_dangerous_requests` to `True`
    allow_dangerous_requests=True
)
