from os.path import join as os_path_join

from WebNotes_config import NotesTemplates, NotesURLs, TEST_DB, NotesMSG

from . import MongoTestCase
from ..forms import TITLE_MAX_LENGTH, TITLE_MAX_LENGTH_ERROR, TEXT_MAX_LENGTH, TEXT_MAX_VALUE_ERROR


class ViewsTest(MongoTestCase):
    """Tests view functions of the application."""
    def setUp(self) -> None:
        self.base_url = 'http://127.0.0.1:8000/'
        self.home_url = os_path_join(self.base_url, NotesURLs.get_home_url())
        self.create_url = os_path_join(self.base_url, NotesURLs.get_create_url())
        self.all_notes_url = os_path_join(self.base_url, NotesURLs.get_all_notes_url())
        self.note_content_url = os_path_join(self.base_url, NotesURLs.get_note_content_url())
        self.edit_note_url = os_path_join(self.base_url, NotesURLs.get_edit_note_url())
        self.delete_note_url = os_path_join(self.base_url, NotesURLs.get_delete_note_url())
        self.search_note_url = os_path_join(self.base_url, NotesURLs.get_search_note_url())
        self.server_error_url = os_path_join(self.base_url, NotesURLs.get_server_error_url())

        self.note_already_exists = NotesMSG.get_msg_note_already_exists()
        self.no_notes_in_db = NotesMSG.get_msg_no_notes_in_db()
        self.note_was_inserted = NotesMSG.get_msg_note_inserted()
        self.note_was_edited = NotesMSG.get_msg_note_edited()
        self.note_was_deleted = NotesMSG.get_msg_note_deleted()
        self.database_error = NotesMSG.get_msg_database_error()

        self.note_title = 'test_note_1'
        self.note_text = 'some text'

        self.edited_note_title = 'test_2'
        self.edited_note_text = 'edited text'
        self.new_note_title = 'test_note_2'

        self.invalid_title = 'a' * TITLE_MAX_LENGTH + 'b'
        self.invalid_text = 'a' * TEXT_MAX_LENGTH + 'b'

    def tearDown(self):
        TEST_DB.delete_many({})

    def test_homepage(self):
        """Tests homepage views when there are documents in the collection and not."""
        response_without_notes = self.client.get(self.home_url)
        self.assertContains(response_without_notes, self.no_notes_in_db)
        insert_test_data()
        response_with_notes = self.client.get(self.home_url)
        content_with_notes = 'Current database contains'
        self.assertContains(response_with_notes, content_with_notes)
        self.assertEqual(response_with_notes.context['total_notes'], 12)

    def test_all_notes(self):
        """Tests displaying the notes when there are documents in the collection and not.
        Pagination is also tested."""
        response_without_notes = self.client.get(self.all_notes_url)
        self.assertContains(response_without_notes, self.no_notes_in_db)
        insert_test_data()
        response_with_notes = self.client.get(self.all_notes_url)
        content_with_notes = 'Note(s) in database'
        self.assertContains(response_with_notes, content_with_notes)
        self.assertEqual(response_with_notes.context['total_notes'], 12)
        self.assertTrue('notes_in_db' in response_with_notes.context)
        pagination = 'Page 1 of 3'
        self.assertContains(response_with_notes, pagination)

    def test_search_note(self):
        """Tests searching for notes in titles and texts regardless of case."""
        test_notes = [{'_title': '#DtESt_1Atest_4d', '_text': 'n7y2eTest_3cteST_5E'},
                      {'_title': '01Test_4dtEst_8h Test_7G', '_text': 'teSt_7G3Jk'},
                      {'_title': 'teST_6f gwq', '_text': 'TEst_6f_uteSt_7g'},
                      {'_title': '@@wtesT_6F5', '_text': 'asdtest_2bTest_8h'},
                      {'_title': 'TeSt_4dtest_8hdtESt_6f', '_text': 'FtEst_7G  1 TeSt_8haqb'},
                      {'_title': 'QMtest_6f_rttEst_3ctESt_8h', '_text': 'nTest_5E_=2'}]
        TEST_DB.insert_many(test_notes)

        query_no_title_no_text = 'not found'
        query_one_title_no_text = 'test_1a'
        query_no_title_one_text = 'test_2b'
        query_one_title_one_text = 'test_3c'
        query_few_titles_no_text = 'test_4d'
        query_no_title_few_texts = 'test_5e'
        query_few_titles_one_text = 'test_6f'
        query_one_title_few_texts = 'test_7g'
        query_few_titles_few_texts = 'test_8h'

        not_found_in_titles = 'No results in titles were found'
        not_found_in_texts = 'No results in texts were found'
        found_in_titles = 'Found in the title:'
        found_in_texts = 'Found in the text:'

        self.assertContains_search_url(query_no_title_no_text, not_found_in_titles)
        self.assertContains_search_url(query_no_title_no_text, not_found_in_texts)

        self.assertContains_search_url(query_one_title_no_text, found_in_titles)
        self.assertContains_search_url(query_one_title_no_text, not_found_in_texts)
        self.assertContains_search_url(query_one_title_no_text, test_notes[0]['_title'])

        self.assertContains_search_url(query_no_title_one_text, not_found_in_titles)
        self.assertContains_search_url(query_no_title_one_text, found_in_texts)
        self.assertContains_search_url(query_no_title_one_text, test_notes[3]['_title'])

        self.assertContains_search_url(query_one_title_one_text, found_in_titles)
        self.assertContains_search_url(query_one_title_one_text, found_in_texts)
        self.assertContains_search_url(query_one_title_one_text, test_notes[0]['_title'])
        self.assertContains_search_url(query_one_title_one_text, test_notes[5]['_title'])

        self.assertContains_search_url(query_few_titles_no_text, found_in_titles)
        self.assertContains_search_url(query_few_titles_no_text, not_found_in_texts)
        self.assertContains_search_url(query_few_titles_no_text, test_notes[0]['_title'])
        self.assertContains_search_url(query_few_titles_no_text, test_notes[1]['_title'])
        self.assertContains_search_url(query_few_titles_no_text, test_notes[4]['_title'])

        self.assertContains_search_url(query_no_title_few_texts, not_found_in_titles)
        self.assertContains_search_url(query_no_title_few_texts, found_in_texts)
        self.assertContains_search_url(query_no_title_few_texts, test_notes[0]['_title'])
        self.assertContains_search_url(query_no_title_few_texts, test_notes[5]['_title'])

        self.assertContains_search_url(query_few_titles_one_text, found_in_titles)
        self.assertContains_search_url(query_few_titles_one_text, found_in_texts)
        self.assertContains_search_url(query_few_titles_one_text, test_notes[2]['_title'], 2)
        self.assertContains_search_url(query_few_titles_one_text, test_notes[3]['_title'])
        self.assertContains_search_url(query_few_titles_one_text, test_notes[4]['_title'])
        self.assertContains_search_url(query_few_titles_one_text, test_notes[5]['_title'])

        self.assertContains_search_url(query_one_title_few_texts, found_in_titles)
        self.assertContains_search_url(query_one_title_few_texts, found_in_texts)
        self.assertContains_search_url(query_one_title_few_texts, test_notes[1]['_title'], 2)
        self.assertContains_search_url(query_one_title_few_texts, test_notes[2]['_title'])
        self.assertContains_search_url(query_one_title_few_texts, test_notes[4]['_title'])

        self.assertContains_search_url(query_few_titles_few_texts, found_in_titles)
        self.assertContains_search_url(query_few_titles_few_texts, found_in_texts)
        self.assertContains_search_url(query_few_titles_few_texts, test_notes[1]['_title'])
        self.assertContains_search_url(query_few_titles_few_texts, test_notes[3]['_title'])
        self.assertContains_search_url(query_few_titles_few_texts, test_notes[4]['_title'], 2)
        self.assertContains_search_url(query_few_titles_few_texts, test_notes[5]['_title'])

        for _ in range(6):
            self.assertContains_search_url('test_', test_notes[_]['_title'], 2)

    def assertContains_search_url(self, input_query: str, test_result: str, count_num: int = 1):
        """Additional function to check if the response contains a check value.
        The number of matches to check is also specified, default is ONE."""
        response = self.client.post(self.search_note_url, {'search_for': input_query})
        self.assertContains(response, test_result, count=count_num)

    def test_create_note(self):
        """Tests notes creating for valid and invalid entered data.
        The case of notes title existing in the collection is also tested."""
        total_notes = TEST_DB.count_documents({})
        note_create = self.client.post(self.create_url, {'note_title': self.note_title,
                                                         'note_text': self.note_text})
        created_note = TEST_DB.find_one()
        self.assertEqual(created_note['_title'], self.note_title)
        self.assertEqual(created_note['_text'], self.note_text)
        self.assertContains(note_create, self.note_was_inserted)
        self.assertEqual(note_create.context['total_notes'], total_notes + 1)

        create_note_already_exists = self.client.post(self.create_url, {'note_title': self.note_title})
        self.assertContains(create_note_already_exists, self.note_already_exists)

        note_create_title_error = self.client.post(self.create_url, {'note_title': self.invalid_title,
                                                                     'note_text': self.note_text})
        self.assertContains(note_create_title_error, TITLE_MAX_LENGTH_ERROR)

        note_create_text_error = self.client.post(self.create_url, {'note_title': self.note_title,
                                                                    'note_text': self.invalid_text})
        self.assertContains(note_create_text_error, TEXT_MAX_VALUE_ERROR)

        note_create_error = self.client.post(self.create_url, {'note_title': self.invalid_title,
                                                               'note_text': self.invalid_text})
        self.assertContains(note_create_error, TITLE_MAX_LENGTH_ERROR)
        self.assertContains(note_create_error, TEXT_MAX_VALUE_ERROR)

    def test_edit_note(self):
        """Tests notes editing for valid and invalid entered data.
        The case of notes title existing in the collection is also tested."""
        note_id = TEST_DB.insert_one({'_title': self.note_title, '_text': None}).inserted_id
        TEST_DB.insert_one({'_title': self.new_note_title, '_text': None})

        note_edit_url = self.edit_note_url.replace('<data_id>', str(note_id))
        post_note_edit = self.client.post(note_edit_url,
                                          {'note_title': self.note_title,
                                           'note_text': self.note_text})
        edited_note = TEST_DB.find_one({'_id': note_id})
        self.assertEqual(edited_note['_title'], self.note_title)
        self.assertEqual(edited_note['_text'], self.note_text)
        self.assertContains(post_note_edit, self.note_was_edited)

        post_note_edit = self.client.post(note_edit_url,
                                          {'note_title': self.edited_note_title,
                                           'note_text': self.note_text})
        edited_note = TEST_DB.find_one({'_id': note_id})
        self.assertEqual(edited_note['_title'], self.edited_note_title)
        self.assertEqual(edited_note['_text'], self.note_text)
        self.assertContains(post_note_edit, self.note_was_edited)

        post_note_edit = self.client.post(note_edit_url,
                                          {'note_title': self.edited_note_title,
                                           'note_text': self.edited_note_text})
        edited_note = TEST_DB.find_one({'_id': note_id})
        self.assertEqual(edited_note['_title'], self.edited_note_title)
        self.assertEqual(edited_note['_text'], self.edited_note_text)
        self.assertContains(post_note_edit, self.note_was_edited)

        post_note_edit = self.client.post(note_edit_url,
                                          {'note_title': self.note_title,
                                           'note_text': self.note_text})
        edited_note = TEST_DB.find_one({'_id': note_id})
        self.assertEqual(edited_note['_title'], self.note_title)
        self.assertEqual(edited_note['_text'], self.note_text)
        self.assertContains(post_note_edit, self.note_was_edited)

        try_to_edit_note = self.client.post(note_edit_url, {'note_title': self.new_note_title,
                                                            'note_text': self.note_text})
        self.assertContains(try_to_edit_note, self.note_already_exists)

        note_edit_title_error = self.client.post(note_edit_url, {'note_title': self.invalid_title,
                                                                 'note_text': self.note_text})
        self.assertContains(note_edit_title_error, TITLE_MAX_LENGTH_ERROR)

        note_edit_text_error = self.client.post(note_edit_url, {'note_title': self.note_title,
                                                                'note_text': self.invalid_text})
        self.assertContains(note_edit_text_error, TEXT_MAX_VALUE_ERROR)

        note_edit_error = self.client.post(note_edit_url, {'note_title': self.invalid_title,
                                                           'note_text': self.invalid_text})
        self.assertContains(note_edit_error, TITLE_MAX_LENGTH_ERROR)
        self.assertContains(note_edit_error, TEXT_MAX_VALUE_ERROR)

    def test_delete_note(self):
        """Tests deleting of the note."""
        test_notes = [{'_title': 'test_note_1', '_text': 'text_ABC'},
                      {'_title': 'test_note_2', '_text': 'text 123'},
                      {'_title': 'test_note_3', '_text': 'text ONE-TWO-THREE'},
                      {'_title': 'test_note_4', '_text': None}]
        TEST_DB.insert_many(test_notes)
        note_id = TEST_DB.insert_one({'_title': self.note_title, '_text': self.note_text}).inserted_id
        total_notes = TEST_DB.count_documents({})
        response_total_notes = self.client.get(self.all_notes_url)
        self.assertEqual(response_total_notes.context['total_notes'], total_notes)
        response_delete_note = self.client.get(self.delete_note_url.replace('<data_id>', str(note_id)))
        self.assertContains(response_delete_note, self.note_was_deleted)
        response_total_notes = self.client.get(self.all_notes_url)
        self.assertEqual(response_total_notes.context['total_notes'], total_notes - 1)

    def test_view_note_content(self):
        """Tests the displaying of the note content."""
        note_1_id = TEST_DB.insert_one({'_title': self.note_title, '_text': self.note_text}).inserted_id
        response = self.client.get(self.note_content_url.replace('<data_id>', str(note_1_id)))
        self.assertContains(response, 'Title:')
        self.assertContains(response, self.note_title)
        self.assertContains(response, 'Text:')
        self.assertContains(response, self.note_text)

        note_with_only_title = 'test note title #2'
        note_2_id = TEST_DB.insert_one({'_title': note_with_only_title, '_text': None}).inserted_id
        response = self.client.get(self.note_content_url.replace('<data_id>', str(note_2_id)))
        self.assertContains(response, 'Title:')
        self.assertContains(response, note_with_only_title)
        self.assertNotContains(response, 'Text:')

    def test_database_error(self):
        """Tests displaying of the Server Error URL."""
        server_error_response = self.client.get(self.server_error_url)
        self.assertContains(server_error_response, self.database_error, status_code=500)


def insert_test_data():
    """Inserts to the test collection 12 documents."""
    test_notes = [{'_title': f'test note {cnt}', '_text': f'test note text  {cnt}'}
                  for cnt in range(12)]
    TEST_DB.insert_many(test_notes)
