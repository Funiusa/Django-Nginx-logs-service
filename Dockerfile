FROM python:3.11-alpine as build-python

ENV PYTHONUNBUFFERED=1 \
    PORT=8000 \
    STATIC_ROOT=/static \
    MEDIA_ROOT=/media

EXPOSE 8000

ENV PATH "/root/.local/bin:$PATH"

RUN apk update \
    && apk add postgresql-dev gcc musl-dev curl openssl-dev libffi-dev \
    && curl -sSL https://install.python-poetry.org | python - \
    && poetry config virtualenvs.create false \
    && poetry config virtualenvs.in-project false

WORKDIR /app

COPY ./pyproject.toml /app/

ARG DEV
ENV DEV ${DEV:-true}
RUN pip install --upgrade pip
RUN /bin/sh -c "if [ $DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"


FROM python:3.11-alpine

WORKDIR /app

ENV PATH "/root/.local/bin::$PATH"

COPY --from=build-python /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=build-python /usr/local/bin/ /usr/local/bin/
COPY --from=build-python /usr/lib/libpq.so.5 \
                        /usr/lib/libxml2.so.2 /usr/lib/

RUN apk update

COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
RUN pip install ipython
COPY ./src /app

ENV PYTHONUNBUFFERED=1 \
    PORT=8000 \
    STATIC_ROOT=/static \
    MEDIA_ROOT=/media


CMD ["/docker-entrypoint.sh"]
