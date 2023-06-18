from mongomock import MongoClient as mock_client
from pymongo import MongoClient

from django.db import DatabaseError
from WebPyNotes.WebNotes_settings import NotesConfig

DATABASE_HOST = NotesConfig.get_database_client_host()
DATABASE_NAME = NotesConfig.get_database_name()
COLLECTION_NAME = NotesConfig.get_database_collection()

mongo_client = MongoClient(DATABASE_HOST)
db_name = mongo_client[DATABASE_NAME]
APP_COLLECTION = db_name[COLLECTION_NAME]

test_mongo_client = mock_client(DATABASE_HOST)
test_db_name = test_mongo_client['web_py_notes_testing']
TEST_COLLECTION = test_db_name['app_testing']


class AppDatabase:
    """Class with main database settings and operations."""
    __slots__ = ['__app_database']

    def __init__(self, collection=APP_COLLECTION):
        self.__app_database = collection

    def get_count_of_all_docs(self) -> int:
        """Counts documents in the collection."""
        try:
            notes_in_database = self.__app_database.count_documents({})
        except Exception:
            print('DatabaseError')
            raise DatabaseError
        else:
            return notes_in_database

    def get_doc_from_collection(self, query_obj: dict) -> dict:
        """Finds document in the collection by given ID."""
        try:
            found_in_database = self.__app_database.find_one(query_obj)
        except Exception:
            raise DatabaseError
        else:
            return found_in_database

    def insert_doc_into_collection(self, input_data: dict) -> str:
        """Inserts document into the collection."""
        try:
            inserted_note_id = self.__app_database.insert_one(input_data).inserted_id
        except Exception:
            raise DatabaseError
        else:
            return str(inserted_note_id)

    def get_all_docs_from_collection(self) -> 'Cursor object':
        """Returns all documents from the collection."""
        try:
            all_notes = self.__app_database.find({})
        except Exception:
            raise DatabaseError
        return all_notes

    def update_doc_in_collection(self, input_id: dict, input_data: dict) -> None:
        """Updates document in the collection."""
        try:
            self.__app_database.update_one(input_id, input_data)
        except Exception:
            raise DatabaseError

    def delete_doc_from_collection(self, input_data: dict) -> None:
        """Deletes document from the collection."""
        try:
            self.__app_database.find_one_and_delete(input_data)
        except Exception:
            raise DatabaseError

    def find_docs_from_collection_by_query(self, query_obj: dict) -> list:
        """Finds documents in the collection by given expression."""
        try:
            found_in_database = self.__app_database.find(query_obj)
        except Exception:
            raise DatabaseError
        else:
            query_result = [format_fields(found_note)
                            for found_note in found_in_database]
        return query_result


class TestDatabase(AppDatabase):
    """Class with test database settings and methods."""
    def __init__(self):
        self.__app_database = TEST_COLLECTION
        super().__init__(TEST_COLLECTION)

    def insert_test_data(self, notes_num: int) -> None:
        """Additional test function, inserts to the test collection 12 documents."""
        try:
            test_data = [{'title': f'test note {cnt}',
                          'text': f'test note text  {cnt}'}
                         for cnt in range(notes_num)]
            self.__app_database.insert_many(test_data)
        except Exception:
            raise DatabaseError

    def delete_all_docs_from_collection(self) -> None:
        """Additional test function, deletes all documents from the collection."""
        try:
            self.__app_database.delete_many({})
        except Exception:
            raise DatabaseError


def format_fields(input_data: dict) -> dict:
    """Additional function, formats ID field (_id -> id) in the output data."""
    output_data = {}
    for field in input_data:
        if field == '_id':
            output_data['id'] = str(input_data[field])
        else:
            output_data[field] = input_data[field]
    return output_data


NOTES_DB = AppDatabase()
TEST_DB = TestDatabase()
