from WebNotes_config import TEST_DB
from . import MongoTestCase


class DatabaseTest(MongoTestCase):
    """Tests database part of the application."""
    def setUp(self) -> None:
        self.test_note_1 = {'_title': 'test note creating CREATE_01', '_text': 'just test note text'}
        self.test_note_2 = {'_title': 'test note creating CREATE_02', '_text': 'another test note text'}
        self.test_note_only_title = {'_title': 'test note creating CREATE_03', '_text': None}

        self.test_note_to_edit_1 = {'_title': 'test note to edit UPDATE_01', '_text': 'note text to edit'}
        self.new_title_to_edit_1 = {'_title': 'EDITED TITLE UPDATE_01'}
        self.edited_test_note_1 = {'_title': self.new_title_to_edit_1['_title'],
                                   '_text': self.test_note_to_edit_1['_text']}

        self.test_note_to_edit_2 = {'_title': 'test note to edit UPDATE_02', '_text': 'another note text to edit'}
        self.new_text_to_edit_2 = {'_text': 'EDITED TEXT'}
        self.edited_test_note_2 = {'_title': self.test_note_to_edit_2['_title'],
                                   '_text': self.new_text_to_edit_2['_text']}

        self.test_note_delete_1 = {'_title': 'test note to delete 01', '_text': 'note text to delete'}
        self.test_note_delete_2 = {'_title': 'test note to delete 02', '_text': 'another note text to delete'}

    def tearDown(self) -> None:
        TEST_DB.delete_many({})

    def test_note_creating(self):
        """Tests inserting of a new documents to the test collection."""
        total_notes = TEST_DB.count_documents({})
        test_notes_to_insert = [self.test_note_1, self.test_note_2, self.test_note_only_title]
        TEST_DB.insert_many(test_notes_to_insert)
        total_notes_after_create_operations = TEST_DB.count_documents({})

        query_01 = TEST_DB.find_one({'_title': {'$regex': 'CREATE_01', '$options': 'im'}})
        query_02 = TEST_DB.find_one({'_title': {'$regex': 'CREATE_02', '$options': 'im'}})
        query_03 = TEST_DB.find_one({'_title': {'$regex': 'CREATE_03', '$options': 'im'}})

        self.assertEqual(total_notes_after_create_operations, total_notes + len(test_notes_to_insert))
        self.assertEqual(return_note_object_data(self.test_note_1), return_note_object_data(query_01))
        self.assertEqual(return_note_object_data(self.test_note_2), return_note_object_data(query_02))
        self.assertEqual(return_note_object_data(self.test_note_only_title), return_note_object_data(query_03))

    def test_note_editing(self):
        """Tests updating of the documents in the test collection."""
        test_notes_to_insert = [self.test_note_to_edit_1, self.test_note_to_edit_2]
        TEST_DB.insert_many(test_notes_to_insert)

        TEST_DB.find_one_and_update({'_title': self.test_note_to_edit_1['_title']},
                                    {'$set': {'_title': self.new_title_to_edit_1['_title']}})
        TEST_DB.find_one_and_update({'_text': self.test_note_to_edit_2['_text']},
                                    {'$set': {'_text': self.new_text_to_edit_2['_text']}})

        query_01 = TEST_DB.find_one({'_title': {'$regex': 'UPDATE_01', '$options': 'im'}})
        query_02 = TEST_DB.find_one({'_title': {'$regex': 'UPDATE_02', '$options': 'im'}})

        self.assertEqual(return_note_object_data(self.edited_test_note_1), return_note_object_data(query_01))
        self.assertEqual(return_note_object_data(self.edited_test_note_2), return_note_object_data(query_02))

    def test_note_deleting(self):
        """Tests deleting of the documents from test collection."""
        total_notes = TEST_DB.count_documents({})
        test_notes_to_insert = [self.test_note_delete_1, self.test_note_delete_2]
        TEST_DB.insert_many(test_notes_to_insert)
        total_notes_after_create_operations = TEST_DB.count_documents({})

        TEST_DB.find_one_and_delete({'_title': self.test_note_delete_1['_title']})
        TEST_DB.find_one_and_delete({'_title': self.test_note_delete_2['_title']})
        total_notes_after_delete_operations = TEST_DB.count_documents({})

        self.assertEqual(total_notes_after_create_operations, total_notes + len(test_notes_to_insert))
        self.assertEqual(total_notes_after_delete_operations, total_notes)


def return_note_object_data(note_object: dict) -> list:
    """Converts a document from a collection to a list object.
    Initial document contains id title and text, only title and text are returned."""
    return [note_object['_title'], note_object['_text']]
