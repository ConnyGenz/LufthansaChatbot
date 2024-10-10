# chatbot_frontend/Dockerfile

# tells the container to use the python:3.11-slim distribution
FROM python:3.11-slim

# Working directory "app" is created
WORKDIR /app
# The code in "src" is copied to the directory "app" in the Docker container
# "./src/ refers to the "src" directory under "chatbot_frontend"
COPY ./src/ /app

# Copies content from pyproject.toml to "code" directory in Docker container
# installs the dependencies named in pyproject.toml
COPY ./pyproject.toml /code/pyproject.toml
RUN pip install /code/.

CMD ["sh", "entrypoint.sh"]
