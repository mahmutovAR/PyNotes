from fastapi import FastAPI
from uvicorn import run as uvicorn_run

from PyNotes_GraphQL.schema import graphql_app

app = FastAPI()
app.include_router(graphql_app, prefix='/pynotes/graphql')


if __name__ == "__main__":
    uvicorn_run(app, host="127.0.0.1", port=30000)
