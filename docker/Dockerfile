ARG PROJECT_NAME=timezone-api
ARG APP_NAME=timezone_api
ARG APP_PATH=/opt/$PROJECT_NAME
ARG PYTHON_VERSION=3.10
ARG POETRY_VERSION=1.4.2


##
## STAGE: Staging
##

FROM python:$PYTHON_VERSION as staging
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
## STAGE: Development
##

FROM staging as development

ARG APP_NAME
ARG APP_PATH

ENV FLASK_APP=$APP_NAME \
    FLASK_ENV=development \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_DEBUG=True

WORKDIR $APP_PATH
RUN poetry install --no-root

ENTRYPOINT ["poetry", "run"]
# CMD ["python", "-m debugpy", "--listen 0.0.0.0:5678", "--wait-for-client", "-m flask run"]
CMD python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m flask run


##
## STAGE: Build
##

FROM staging as build
ARG APP_PATH

WORKDIR $APP_PATH
COPY ./$APP_NAME ./$APP_NAME
RUN poetry build --format wheel
RUN poetry export --format requirements.txt --output constraints.txt --without-hashes


##
## STAGE: Production
##

FROM python:$PYTHON_VERSION as production
ARG APP_NAME
ARG APP_PATH

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

ENV \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR $APP_PATH
COPY --from=build $APP_PATH/dist/*.whl ./
COPY --from=build $APP_PATH/constraints.txt ./
# RUN pip install ./$APP_NAME*.whl --constraint constraints.txt
RUN pip install ./$APP_NAME*.whl 

ENV PORT=8888
ENV APP_NAME=$APP_NAME

CMD gunicorn --bind :$PORT --workers 1 --threads 1 --timeout 0 "$APP_NAME:create_app()"