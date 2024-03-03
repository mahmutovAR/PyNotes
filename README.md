# WebPyNotes
This web application provides following functionality to the user:
- creating plain text notes
* saving notes to the database
- listing previously created notes
* editing previously created notes
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
* `Python` 3.9+ (tested to work with == 3.11.2)  
* `Django` (tested to work with == 4.2.1)  
* `Flask` (tested to work with == 2.3.2)  
* `django-bootstrap-v5` (tested to work with == 1.0.11)   
* `mongomock` (tested to work with == 4.1.2)  
* `pymongo` (tested to work with == 4.3.3)  
* `pytz` (tested to work with == 2023.3)  
* `requests` (tested to work with == 2.31.0)  

**Note:** All packages can be installed by running `python3 -m pip install -r requirements.txt`
***


### Set configuration settings in Environment Variables
In bash run:
```
export WEBPYNOTES_DJANGO_SECRET_KEY="django secret key"
export WEBPYNOTES_DATABASE_NAME="user database name"
export WEBPYNOTES_COLLECTION_NAME="user collection name"
export WEBPYNOTES_DATABASE_HOST="mongodb://127.0.0.1:27017"
```
In Python Console run:
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
2. If the application does not open, then navigate to `http://127.0.0.1:8000/webnotes/` in local browser
***


## Testing WebPyNotes
Run the `test_webpynotes.py`
***


## Files and directories:
- `requirements.txt` required packages
* `run_demo.py`  script to run the demo version of the application
- `test_webpynotes.py`  script to test the application
* `/WebNotes_API/` database settings and API module
- `/WebPyNotes/WebNotes/tests/` tests
* `/WebPyNotes/WebNotes/` Form, URLs and views functions
- `/WebPyNotes/WebNotes_settings/` application settings
