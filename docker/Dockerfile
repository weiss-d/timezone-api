ARG PROJECT_NAME=timezone-api
ARG APP_NAME=timezone_api
ARG APP_PATH=/opt/$PROJECT_NAME
ARG PYTHON_VERSION=3.10
ARG POETRY_VERSION=1.4.2

##
## STAGE: base
##

FROM python:$PYTHON_VERSION as base
ARG APP_NAME
ARG APP_PATH
ARG POETRY_VERSION

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1
ENV \
    POETRY_VERSION=$POETRY_VERSION \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR $APP_PATH
COPY ./poetry.lock ./pyproject.toml ./

##
## STAGE: debug
##

FROM base as debug

ARG APP_NAME
ARG APP_PATH

ENV FLASK_APP=$APP_NAME \
    FLASK_ENV=development \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_DEBUG=True

WORKDIR $APP_PATH
RUN poetry install --no-root

ENTRYPOINT ["poetry", "run"]
CMD python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m flask run 
