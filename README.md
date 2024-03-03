# WebPyNotes
This web application provides following functionality to the user:
- creating plain text notes
* saving notes to the database
- listing previously created notes
* editing previously created notes
***

## Structure
The UI runs on `django` server.

Database REST API runs on `flask` server.
Driver `PyMongo` is used to access the `MongoDB` database.

GraphQL API runs on `fastapi` server.
`Strawberry` is used for implementing code server.  
`graphql_query` is used as Domain Specific Language (DSL) for query.
***


## Installation
### Install MongoDB from Docker Hub
`docker pull mongo:6.0.6-jammy`
### Start a mongo server, for example use next settings:
```
docker run --detach --name py_notes_project \
  --env MONGO_INITDB_DATABASE=web_py_notes \
  -p 27017:27017 \
  mongo:6.0.6-jammy
```
### Requirements
* `Python` 3.9+ (tested to work with == 3.11.6)  
* `Django` (tested to work with == 5.0.2)  
* `django-bootstrap-v5` (tested to work with == 1.0.11)
* `fastapi` (tested to work with == 0.110.0)
* `flask` (tested to work with == 3.0.2)  
* `graphql_query` (tested to work with == 1.3.1)  
* `mongomock` (tested to work with == 4.1.2)  
* `pymongo` (tested to work with == 4.6.2)  
* `pytz` (tested to work with == 2024.1)  
* `requests` (tested to work with == 2.31.0)  
* `strawberry_graphql` (tested to work with == 0.219.2)  
* `uvicorn` (tested to work with == 0.27.1)  

**Note:** All packages can be installed by running `python3 -m pip install -r requirements.txt`
***


### Set configuration settings in Environment Variables
In `bash` run:
```
export WEBPYNOTES_DJANGO_SECRET_KEY="django secret key"
export WEBPYNOTES_DATABASE_NAME="user database name"
export WEBPYNOTES_COLLECTION_NAME="user collection name"
export WEBPYNOTES_DATABASE_HOST="mongodb://127.0.0.1:27017"
```
In `Python Console` run:
```
from os import environ
environ['WEBPYNOTES_DJANGO_SECRET_KEY'] = 'django_secret_key'
environ['WEBPYNOTES_DATABASE_NAME'] = 'user_database_name'
environ['WEBPYNOTES_COLLECTION_NAME'] = 'user_collection_name'
environ['WEBPYNOTES_DATABASE_HOST'] = 'mongodb://127.0.0.1:27017'
```
***


## Demo version of the application
1. Run the `run_demo.py`  
2. If the application does not open, then go to `http://127.0.0.1:8000/webnotes/` in local browser.
***


## Testing WebPyNotes
Run the `test_webpynotes.py`
***


## Files and directories:
- `requirements.txt` contains required packages
* `run_demo.py` runs the demo version of the application
- `test_webpynotes.py` tests the application
* `/PyNotes_Database/` is database REST API on `flask` server
- `/PyNotes_GraphQL/` is GraphQL API on `fastapi` server
* `/WebPyNotes/` is WebPyNotes application on `django` server
- `/WebNotes_settings/` contains application settings
