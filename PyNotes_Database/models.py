from datetime import datetime

from bson.objectid import ObjectId
from mongomock import MongoClient as TestMockClient
from pymongo import MongoClient

from WebPyNotes_settings.app_settings import DATABASE_HOST, DATABASE_NAME, COLLECTION_NAME

mongo_client = MongoClient(DATABASE_HOST)
db_name = mongo_client[DATABASE_NAME]
APP_COLLECTION = db_name[COLLECTION_NAME]

test_mongo_client = TestMockClient(DATABASE_HOST)
test_db_name = test_mongo_client['web_py_notes_testing']
TEST_COLLECTION = test_db_name['app_testing']


def get_current_datetime() -> str:
    """Return date and time in format: "day/month/year hour:minute"."""
    return datetime.now().strftime("%d/%m/%Y %H:%M")


def format_dict(input_data: dict | None) -> dict | None:
    """Converts initial 'ObjectId' field of the note data into a str value."""
    if input_data is None:
        return None
    return {'id': str(input_data['_id']),
            'title': input_data['title'],
            'text': input_data['text'],
            'created': input_data['created'],
            'updated': input_data['updated']}


class AppDatabase:
    """Class with main database settings and operations."""
    __slots__ = ['__app_database']

    def __init__(self, collection=APP_COLLECTION):
        """Initializes a collection of notes."""
        self.__app_database = collection

    def db_count_notes(self) -> int:
        """Returns the total number of notes in the collection."""
        try:
            total_notes = self.__app_database.count_documents({})
        except Exception as exc:
            exc.add_note('PyNotes Database Error')
            raise
        else:
            return total_notes

    def db_get_all_notes(self) -> list[dict]:
        """Returns all notes from a collection."""
        try:
            all_notes = self.__app_database.find({})
        except Exception as exc:
            exc.add_note('PyNotes Database Error')
            raise
        else:
            return [format_dict(note)
                    for note in all_notes]

    def db_query_note_by_id(self, data_id: str) -> dict | None:
        """Returns note data with the specified ID."""
        try:
            note_content = self.__app_database.find_one({'_id': ObjectId(data_id)})
        except Exception as exc:
            exc.add_note('PyNotes Database Error')
            raise
        else:
            return format_dict(note_content)

    def db_insert_note(self, note_title: str, note_text: str = None) -> dict:
        """Inserts note into the collection and returns its data."""
        try:
            input_data = {'title': note_title, 'text': note_text,
                          'created': get_current_datetime(), 'updated': None}
            inserted_note_id = self.__app_database.insert_one(input_data).inserted_id
            note_content = self.__app_database.find_one({'_id': ObjectId(inserted_note_id)})
        except Exception as exc:
            exc.add_note('PyNotes Database Error')
            raise
        else:
            return format_dict(note_content)

    def db_update_note(self, input_id: str, note_title: str, note_text: str = None) -> dict:
        """Updates a note data and returns it."""
        try:
            input_data = {"$set": {'title': note_title, 'text': note_text,
                                   'updated': get_current_datetime()}}
            self.__app_database.update_one({'_id': ObjectId(input_id)}, input_data)
            note_content = self.__app_database.find_one({'_id': ObjectId(input_id)})
        except Exception as exc:
            exc.add_note('PyNotes Database Error')
            raise
        else:
            return format_dict(note_content)

    def db_delete_note(self, data_id: str) -> None:
        """Deletes a note from the collection."""
        try:
            self.__app_database.find_one_and_delete({'_id': ObjectId(data_id)})
        except Exception as exc:
            exc.add_note('PyNotes Database Error')
            raise

    def db_query_note_by_obj(self, query_obj: dict) -> list[dict]:
        """Returns notes from the collection that contain the specified expression."""
        try:
            notes_found = self.__app_database.find(query_obj)
        except Exception as exc:
            exc.add_note('PyNotes Database Error')
            raise
        else:
            return [format_dict(note)
                    for note in notes_found]

    def db_note_title_is_taken(self, note_title: str, note_id: str = None) -> dict | None:
        """Check if document with the specified 'TITLE' field exists.
        Returns an existing document or None."""
        try:
            note_data = self.__app_database.find_one({'title': note_title})
        except Exception as exc:
            exc.add_note('PyNotes Database Error')
            raise
        else:
            if not note_data or str(note_data['_id']) == note_id:
                return None
            elif str(note_data['_id']) != note_id:
                return format_dict(note_data)


class TestDatabase(AppDatabase):
    """Class with test database settings and methods."""
    def __init__(self):
        self.__app_database = TEST_COLLECTION
        super().__init__(TEST_COLLECTION)

    def db_insert_test_data(self, notes_num: int) -> None:
        """Inserts the specified number of notes into the test collection."""
        try:
            test_data = [{'title': f'test note {cnt}',
                          'text': f'test note text  {cnt}',
                          'created': get_current_datetime(),
                          'updated': None}
                         for cnt in range(notes_num)]
            self.__app_database.insert_many(test_data)
        except Exception as exc:
            exc.add_note('PyNotes Database Error')
            raise

    def db_delete_test_data(self) -> None:
        """Deletes all notes from the test collection."""
        try:
            self.__app_database.delete_many({})
        except Exception as exc:
            exc.add_note('PyNotes Database Error')
            raise


NOTES_DB = AppDatabase()
TEST_DB = TestDatabase()
