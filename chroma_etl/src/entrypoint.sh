#!/bin/bash

# Run any setup steps or pre-processing tasks here
echo """Aktion 'extract, transform, load' (ETL) wird ausgeführt, um Daten aus
Word-Dateien zu lesen, zu vektorisieren und in Chroma-Datenbank zu schreiben..."""

# Run the ETL script
python prepare_textual_material.py