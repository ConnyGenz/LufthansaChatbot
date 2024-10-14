# tells the container to use the python:3.11-slim distribution
FROM python:3.11-slim

# Maybe needed for error:
# Couldn't find a valid ICU package installed on the system. Please install libicu
# (or icu-libs) using your package manager and try again. Alternatively you can set the
# configuration flag System.Globalization.Invariant to true if you want to run with no
# globalization support.
# https://forum.aspose.com/t/use-aspose-words-on-docker-image-python-3-11-not-working/282823/7
ENV DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1

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