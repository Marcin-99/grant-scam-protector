FROM python:3.10

ENV PYTHONUNBUFFERED 1

# Packages
COPY ./requirements /requirements
RUN pip install -r ./requirements/local.txt

# Entrypoints
COPY ./docker/local/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /app
COPY . .

ENTRYPOINT ["/entrypoint.sh"]
