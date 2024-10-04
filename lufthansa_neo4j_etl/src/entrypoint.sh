#!/bin/bash

# Run any setup steps or pre-processing tasks here
echo "Aktion 'extract, transform, load' (ETL) wird ausgeführt, um Daten aus csv-Dateien in Neo4j-Datenbank zu schreiben..."

# Run the ETL script
python lufthansa_bulk_csv_write.py
