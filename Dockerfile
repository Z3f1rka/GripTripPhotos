FROM python:3.12-alpine AS build
RUN mkdir /application
COPY ./requirements/prod.txt /application/requirements.txt
WORKDIR /application
RUN python -m venv .venv \
&& source .venv/bin/activate \
&& pip install -r requirements.txt
COPY . .

FROM python:3.12-alpine AS runner
RUN mkdir /application
COPY --from=build /application /application
WORKDIR /application
RUN ls -la
CMD source /application/.venv/bin/activate \
&& export PYTHONPATH=$(pwd) \
&& python server.py