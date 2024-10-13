# tells the container to use the python:3.11-slim distribution
FROM python:3.11-slim

WORKDIR /app

# "./src/ refers to the "src" directory under "chroma_etl"
# The code in "src" is copied to a directory "app" in the Docker container
COPY ./src/ /app

# Copies content from pyproject.toml to "code" directory in Docker container
# installs the dependencies named in pyproject.toml
COPY ./pyproject.toml /code/pyproject.toml
RUN pip install /code/.

# Command to run the "entrypoint.sh"
# The "entrypoint.sh" basically says to run "prepare_textual_material.py"
CMD ["sh", "entrypoint.sh"]