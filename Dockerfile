FROM python:2.7

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        libxml2-dev libxslt-dev

COPY pip.requirements /var
RUN pip install --no-cache-dir --upgrade -r /var/pip.requirements

COPY src /app

# clean things
RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1

USER www-data
ENTRYPOINT ["/app/runner.py"]
