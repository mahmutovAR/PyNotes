# WebPyNotes
This web application provides following functionality to the user:
- creating plain text notes
* saving notes to the database
- listing previously created notes
* editing previously created notes
***


## Installation
### Install MongoDB from Docker Hub
`docker pull mongo`  
### Start a mongo server, for example use next settings:
`docker run --detach --name py_notes_project \
  --env MONGO_INITDB_DATABASE=web_py_notes \
  -p 27017:27017 \`
***


## Requirements
* `Python` 3.9+
* `configparser` (tested to work with >= 5.3.0)  
* `Django` (tested to work with >= 4.1.7)  
* `django-bootstrap-v5` (tested to work with >= 1.0.11)  
* `pymongo` (tested to work with >= 4.3.3)  
* `mongomock` (tested to work with >= 4.1.2)  
* `pytz` (tested to work with >= 2022.7.1)  

**Note:** All packages can be installed by running `python -m pip install -r requirements.txt`
***


### The configuration file `config.ini` has the following structure:
`[django]`  
secret key  

`[database]`  
database name  
collection  
host

### Example of `config.ini`
```
[django]
password = n2e7G@}7WVK6-st98$Z7=dSTtRi6@*{b_ZNJ6MK+bQ50wRVC)CN

[database]
name = web_py_notes
collection = default_user
host = mongodb://127.0.0.1:27017
```
***

## Running WebPyNotes
1. Edit `config.ini` or use default settings  
2. Run the `python manage.py runserver`  
3. Open `http://127.0.0.1:8000/`
***


## Testing WebPyNotes
Run `python manage.py test WebNotes.tests` to test the application
***


## Files and directories:
- `config.ini` configuration file (not required)
* `requirements.txt` required packages
- `/WebNotes/`
  - `forms` Note form
  - `urls` app urls
  - `views` views
* `/WebNotes/tests` package for testing
- `/WebNotes_config/` application settings
