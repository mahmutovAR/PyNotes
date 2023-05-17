import mongomock
from pymongo import MongoClient

from . import NotesConfig

mongo_client = MongoClient(NotesConfig.get_database_client_host())
db_name = mongo_client[NotesConfig.get_database_name()]
NOTES_DB = db_name[NotesConfig.get_database_collection()]


test_mongo_client = mongomock.MongoClient(NotesConfig.get_database_client_host())
test_db_name = test_mongo_client[NotesConfig.get_database_name()]
TEST_DB = test_db_name['app_testing']
