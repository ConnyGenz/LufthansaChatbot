import logging
import os

from neo4j import GraphDatabase
from retry import retry

AKTIE_CSV_PATH = os.getenv("AKTIE_CSV_PATH")
UMSATZ_CSV_PATH = os.getenv("UMSATZ_CSV_PATH")
LEISTUNG_CSV_PATH = os.getenv("LEISTUNG_CSV_PATH")
AGGREGATE_CSV_PATH = os.getenv("AGGREGATE_CSV_PATH")

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

LOGGER = logging.getLogger(__name__)

# define nodes to be created in the graph database
NODES = ["Aktie", "Leistung", "Umsatz", "Aggregat"]


# Does the "id" mentioned in this function have anything to do with the
# "hospital_id" etc. from the table that is saved as "id" of the node?
# Or is it different from that? Not a property, but an id for every existing node,
# no matter what type
# Ggf muss ich dass uniqueness constraint über das Jahr laufen lassen,
# weil ich die Eigenschaft "id" gar nicht eingerichtet habe
# "n.jahr" instead of "n.id"?
def _set_uniqueness_constraints(tx, node):
    query = f"""CREATE CONSTRAINT IF NOT EXISTS FOR (n:{node})
        REQUIRE n.id IS UNIQUE;"""
    _ = tx.run(query, {})


@retry(tries=3, delay=10)
def load_lufthansa_graph_from_csv() -> None:
    """Load structured lufthansa CSV data following
    a specific ontology into Neo4j"""

    driver = GraphDatabase.driver(
        NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    )

    LOGGER.info("Setze Einschränkung, dass jeder Knoten einzigartig ist.")
    with driver.session(database="neo4j") as session:
        for node in NODES:
            session.execute_write(_set_uniqueness_constraints, node)

    # Table "Aggregate" is loaded
    LOGGER.info("Lade Knoten für Tabelle 'Aggregate'")
    with driver.session(database="neo4j") as session:
        query = f"""
        LOAD CSV WITH HEADERS
        FROM '{AGGREGATE_CSV_PATH}' AS aggregate_infos
        MERGE (a:Aggregat {{jahr: toInteger(aggregate_infos.jahr)
                            }});
        """
        _ = session.run(query, {})

    # Table "Leistung" is loaded
    # A "Leistung"-type node is generated (see list with node types defined above)
    # This node will have the properties listed in one row of the "Leistung" table
    # Why "Merge"? What does it do? Does ist create the node?
    LOGGER.info("Lade Knoten für Tabelle 'Leistung'")
    with driver.session(database="neo4j") as session:
        query = f"""
        LOAD CSV WITH HEADERS
        FROM '{LEISTUNG_CSV_PATH}' AS leistungs_infos
        MERGE (l:Leistung {{jahr: toInteger(leistungs_infos.jahr),
                            fluege: toFloat(leistungs_infos.fluege),
                            fluggaeste: toFloat(leistungs_infos.fluggaeste),
                            sitzladefaktor: toFloat(leistungs_infos.sitzladefaktor),
                            aggregate_id: toInteger(leistungs_infos.aggregate_id)
                            }});
        """
        _ = session.run(query, {})

    LOGGER.info("Lade Knoten für Tabelle 'Umsatz'")
    with driver.session(database="neo4j") as session:
        query = f"""
        LOAD CSV WITH HEADERS
        FROM '{UMSATZ_CSV_PATH}' AS umsatz_infos
        MERGE (u:Umsatz {{jahr: toInteger(umsatz_infos.jahr),
                        umsatzerloese: toFloat(umsatz_infos.umsatzerloese),
                        verkehrserloese: toFloat(umsatz_infos.verkehrserloese),
                        ebit: toFloat(umsatz_infos.ebit),
                        konzernergebnis: toFloat(umsatz_infos.konzernergebnis),
                        aggregate_id: toInteger(umsatz_infos.aggregate_id)}});
        """
        _ = session.run(query, {})


    LOGGER.info("Lade Knoten für Tabelle 'Aktie'")
    with driver.session(database="neo4j") as session:
        query = f"""
        LOAD CSV WITH HEADERS
        FROM '{AKTIE_CSV_PATH}' AS aktien_infos
        MERGE (a:Aktie {{jahr: toInteger(aktien_infos.jahr),
                            jahresschlusskurs: toFloat(aktien_infos.jahresschlusskurs),
                            ergebnis_pro_aktie: toFloat(aktien_infos.ergebnis_pro_aktie),
                            dividendenvorschlag: toFloat(aktien_infos.dividendenvorschlag),
                            aggregate_id: toInteger(aktien_infos.aggregate_id)}});
        """
        _ = session.run(query, {})


    # Loading relationships. Example from hospital chatbot (tutorial)
    #LOGGER.info("Loading 'AT' relationships")
    #with driver.session(database="neo4j") as session:
        #query = f"""
        #LOAD CSV WITH HEADERS FROM '{VISITS_CSV_PATH}' AS row
        #MATCH (source: `Visit` {{ `id`: toInteger(trim(row.`visit_id`)) }})
        #MATCH (target: `Hospital` {{ `id`:
        #toInteger(trim(row.`hospital_id`))}})
        #MERGE (source)-[r: `AT`]->(target)
        #"""
        #_ = session.run(query, {})

    LOGGER.info("Lade 'PART_OF_AGGREGATE' Verknüpfung für Umsatz-Tabelle")
    with driver.session(database="neo4j") as session:
        # A table with a foreign key in it is loaded
        # the private and the foreign key are read from the table
        # the relationship between the entities identified by the keys is expressed using
        # a cypher expression
        # Why "Merge"? What does it do?
        query = f"""
        LOAD CSV WITH HEADERS FROM '{UMSATZ_CSV_PATH}' AS umsatz_tabelle
            MATCH (u:Umsatz {{jahr: toInteger(umsatz_tabelle.jahr)}})
            MATCH (a:Aggregat {{jahr: toInteger(umsatz_tabelle.aggregate_id)}})
            MERGE (u)-[part_of:PART_OF_AGGREGATE]->(a)
        """
        _ = session.run(query, {})

    # Part-of-aggregate-relationship für die anderen Tabellen (Leistung und Aktie) wiederholen

    LOGGER.info("Lade 'PART_OF_AGGREGATE' Verknüpfung für Aktie-Tabelle")
    with driver.session(database="neo4j") as session:
        # Tabelle mit Foreign-Key darin wird geladen
        # Der eigene und der fremde Key werden aus der Tabelle gelesen
        # Relationship/Verknüpfung mit Cypher-Ausdruck ausdrücken
        # Warum "Merge"?
        query = f"""
        LOAD CSV WITH HEADERS FROM '{AKTIE_CSV_PATH}' AS aktie_tabelle
            MATCH (f:Aktie {{jahr: toInteger(aktie_tabelle.jahr)}})
            MATCH (a:Aggregat {{jahr: toInteger(aktie_tabelle.aggregate_id)}})
            MERGE (f)-[part_of:PART_OF_AGGREGATE]->(a)
        """
        _ = session.run(query, {})

    LOGGER.info("Lade 'PART_OF_AGGREGATE' Verknüpfung für Leistung-Tabelle")
    with driver.session(database="neo4j") as session:
        # Tabelle mit Foreign-Key darin wird geladen
        # Der eigene und der fremde Key werden aus der Tabelle gelesen
        # Relationship/Verknüpfung mit Cypher-Ausdruck ausdrücken
        # Warum "Merge"?
        query = f"""
        LOAD CSV WITH HEADERS FROM '{LEISTUNG_CSV_PATH}' AS leistung_tabelle
            MATCH (l:Leistung {{jahr: toInteger(leistung_tabelle.jahr)}})
            MATCH (a:Aggregat {{jahr: toInteger(leistung_tabelle.aggregate_id)}})
            MERGE (l)-[part_of:PART_OF_AGGREGATE]->(a)
        """
        _ = session.run(query, {})


if __name__ == "__main__":
    load_lufthansa_graph_from_csv()
