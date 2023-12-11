from WebNotes_settings import NotesTemplates, NotesPages, NotesAPI, NotesMSG

from . import MongoTestCase, format_url
from ..forms import TITLE_MAX_LENGTH_ERROR, TEXT_MAX_VALUE_ERROR
from ..views import *

NOTES_API = NotesAPI.get_api_for_views()
TEST_NOTES_API = NotesAPI.get_api_for_tests()


class ViewsTest(MongoTestCase):
    """Tests view functions of the application."""
    def setUp(self) -> None:
        self.index_page = format_url(NotesPages.get_index_page())
        self.add_note_page = format_url(NotesPages.get_add_page())
        self.all_notes_page = format_url(NotesPages.get_all_notes_page())
        self.note_content_page = format_url(NotesPages.get_note_content_page())
        self.edit_note_page = format_url(NotesPages.get_edit_note_page())
        self.delete_note_page = format_url(NotesPages.get_delete_note_page())
        self.search_note_page = format_url(NotesPages.get_search_note_page())
        self.server_error_page = format_url(NotesPages.get_server_error_page())

        self.note_already_exists = NotesMSG.get_msg_note_already_exists()
        self.no_notes_in_db = NotesMSG.get_msg_no_notes_in_db()
        self.note_was_inserted = NotesMSG.get_msg_note_inserted()
        self.note_was_edited = NotesMSG.get_msg_note_updated()
        self.note_was_deleted = NotesMSG.get_msg_note_deleted()
        self.database_error = NotesMSG.get_msg_database_error()

        self.test_notes = 12

        self.note_title = 'test_note_1'
        self.note_text = 'some text'

        self.edited_note_title = 'test_2'
        self.edited_note_text = 'edited text'
        self.new_note_title = 'test_note_2'

        self.invalid_title = 'a' * TITLE_MAX_LENGTH + 'b'
        self.invalid_text = 'a' * TEXT_MAX_LENGTH + 'b'

    def tearDown(self):
        requests_delete(TEST_NOTES_API)

    def test_homepage(self):
        """Tests homepage views when there are documents in the collection and not."""
        response_without_notes = self.client.get(self.index_page)
        self.assertContains(response_without_notes, self.no_notes_in_db)
        requests_post(TEST_NOTES_API, json={'test_notes_num': self.test_notes})
        response_with_notes = self.client.get(self.index_page)
        content_with_notes = 'The database contains'
        self.assertContains(response_with_notes, content_with_notes)
        self.assertEqual(response_with_notes.context['total_notes'], self.test_notes)

    def test_all_notes(self):
        """Tests displaying the notes when there are documents in the collection and not.
        Pagination is also tested."""
        response_without_notes = self.client.get(self.all_notes_page)
        self.assertContains(response_without_notes, self.no_notes_in_db)
        requests_post(TEST_NOTES_API, json={'test_notes_num': self.test_notes})
        response_with_notes = self.client.get(self.all_notes_page)
        content_with_notes = 'notes in database'
        self.assertContains(response_with_notes, content_with_notes)
        self.assertEqual(response_with_notes.context['total_notes'], 12)
        self.assertTrue('notes_in_db' in response_with_notes.context)
        pagination = 'Page 1 of 3'
        self.assertContains(response_with_notes, pagination)

    def test_search_note(self):
        """Tests searching for notes regardless of case for the next cases:
        - nothing found;
        - one (several) note(s) found only in the titles;
        - one (several) note(s) found only in the texts;
        - one (several) note(s) found both in the title and in the text."""
        test_notes = [{'note_title': '#DtESt_1Atest_4d', 'note_text': 'n7y2eTest_3cteST_5E'},
                      {'note_title': '01Test_4dtEst_8h Test_7G', 'note_text': 'teSt_7G3Jk'},
                      {'note_title': 'teST_6f gwq', 'note_text': 'TEst_6f_uteSt_7g'},
                      {'note_title': '@@wtesT_6F5', 'note_text': 'asdtest_2bTest_8h'},
                      {'note_title': 'TeSt_4dtest_8hdtESt_6f', 'note_text': 'FtEst_7G  1 TeSt_8haqb'},
                      {'note_title': 'QMtest_6f_rttEst_3ctESt_8h', 'note_text': 'nTest_5E_=2'}]
        for test_data in test_notes:
            requests_post(NOTES_API, json=test_data)

        query_no_title_no_text = 'not found'
        query_one_title_no_text = 'test_1a'
        query_no_title_one_text = 'test_2b'
        query_one_title_one_text = 'test_3c'
        query_titles_no_text = 'test_4d'
        query_no_title_texts = 'test_5e'
        query_titles_one_text = 'test_6f'
        query_one_title_texts = 'test_7g'
        query_titles_texts = 'test_8h'

        not_found_in_titles = 'Not found in titles'
        not_found_in_texts = 'Not found in texts'
        found_in_titles = 'Found in the title:'
        found_in_texts = 'Found in the text:'

        self.assertContains_search_page(query_no_title_no_text, not_found_in_titles)
        self.assertContains_search_page(query_no_title_no_text, not_found_in_texts)

        self.assertContains_search_page(query_one_title_no_text, found_in_titles)
        self.assertContains_search_page(query_one_title_no_text, not_found_in_texts)
        self.assertContains_search_page(query_one_title_no_text, test_notes[0]['note_title'])

        self.assertContains_search_page(query_no_title_one_text, not_found_in_titles)
        self.assertContains_search_page(query_no_title_one_text, found_in_texts)
        self.assertContains_search_page(query_no_title_one_text, test_notes[3]['note_title'])

        self.assertContains_search_page(query_one_title_one_text, found_in_titles)
        self.assertContains_search_page(query_one_title_one_text, found_in_texts)
        self.assertContains_search_page(query_one_title_one_text, test_notes[0]['note_title'])
        self.assertContains_search_page(query_one_title_one_text, test_notes[5]['note_title'])

        self.assertContains_search_page(query_titles_no_text, found_in_titles)
        self.assertContains_search_page(query_titles_no_text, not_found_in_texts)
        self.assertContains_search_page(query_titles_no_text, test_notes[0]['note_title'])
        self.assertContains_search_page(query_titles_no_text, test_notes[1]['note_title'])
        self.assertContains_search_page(query_titles_no_text, test_notes[4]['note_title'])

        self.assertContains_search_page(query_no_title_texts, not_found_in_titles)
        self.assertContains_search_page(query_no_title_texts, found_in_texts)
        self.assertContains_search_page(query_no_title_texts, test_notes[0]['note_title'])
        self.assertContains_search_page(query_no_title_texts, test_notes[5]['note_title'])

        self.assertContains_search_page(query_titles_one_text, found_in_titles)
        self.assertContains_search_page(query_titles_one_text, found_in_texts)
        self.assertContains_search_page(query_titles_one_text, test_notes[2]['note_title'], 2)
        self.assertContains_search_page(query_titles_one_text, test_notes[3]['note_title'])
        self.assertContains_search_page(query_titles_one_text, test_notes[4]['note_title'])
        self.assertContains_search_page(query_titles_one_text, test_notes[5]['note_title'])

        self.assertContains_search_page(query_one_title_texts, found_in_titles)
        self.assertContains_search_page(query_one_title_texts, found_in_texts)
        self.assertContains_search_page(query_one_title_texts, test_notes[1]['note_title'], 2)
        self.assertContains_search_page(query_one_title_texts, test_notes[2]['note_title'])
        self.assertContains_search_page(query_one_title_texts, test_notes[4]['note_title'])

        self.assertContains_search_page(query_titles_texts, found_in_titles)
        self.assertContains_search_page(query_titles_texts, found_in_texts)
        self.assertContains_search_page(query_titles_texts, test_notes[1]['note_title'])
        self.assertContains_search_page(query_titles_texts, test_notes[3]['note_title'])
        self.assertContains_search_page(query_titles_texts, test_notes[4]['note_title'], 2)
        self.assertContains_search_page(query_titles_texts, test_notes[5]['note_title'])

        for _ in range(6):
            self.assertContains_search_page('test_', test_notes[_]['note_title'], 2)

    def assertContains_search_page(self, input_query: str, test_result: str, count_num: int = 1) -> None:
        """Additional function to check if the response contains a check value.
        The number of matches to check is also specified, default is ONE."""
        response = self.client.post(self.search_note_page, {'search_for': input_query})
        self.assertContains(response, test_result, count=count_num)

    def test_add_note(self):
        """Tests notes creating for valid and invalid entered data.
        The case of notes title existing in the collection is also tested."""
        note_create = self.client.post(self.add_note_page, {'note_title': self.note_title,
                                                            'note_text': self.note_text})
        api_response = requests_get(NOTES_API)
        created_note = api_response.json()['notes'][0]

        self.assertEqual(created_note['title'], self.note_title)
        self.assertEqual(created_note['text'], self.note_text)
        self.assertContains(note_create, self.note_was_inserted)

        create_note_already_exists = self.client.post(self.add_note_page, {'note_title': self.note_title})
        self.assertContains(create_note_already_exists, self.note_already_exists)

        note_create_title_error = self.client.post(self.add_note_page, {'note_title': self.invalid_title,
                                                                        'note_text': self.note_text})
        self.assertContains(note_create_title_error, TITLE_MAX_LENGTH_ERROR)
        self.assertContains(note_create_title_error, self.invalid_title)
        self.assertContains(note_create_title_error, self.note_text)

        note_create_text_error = self.client.post(self.add_note_page, {'note_title': self.note_title,
                                                                       'note_text': self.invalid_text})
        self.assertContains(note_create_text_error, self.note_title)
        self.assertContains(note_create_text_error, self.invalid_text)
        self.assertContains(note_create_text_error, TEXT_MAX_VALUE_ERROR)

        note_create_error = self.client.post(self.add_note_page, {'note_title': self.invalid_title,
                                                                  'note_text': self.invalid_text})
        self.assertContains(note_create_error, TITLE_MAX_LENGTH_ERROR)
        self.assertContains(note_create_error, self.invalid_title)
        self.assertContains(note_create_error, TEXT_MAX_VALUE_ERROR)
        self.assertContains(note_create_error, self.invalid_text)

    def test_edit_note(self):
        """Tests notes editing for valid and invalid entered data.
        The case of notes title existing in the collection is also tested."""
        note_added = requests_post(NOTES_API, json={'note_title': self.note_title, 'note_text': None})
        inserted_note_id = note_added.json()['inserted_note_id']
        self.notes_api_with_data_id = urljoin(NOTES_API, inserted_note_id)

        requests_post(NOTES_API, json={'note_title': self.new_note_title, 'note_text': None})

        self.edit_page_with_id = self.edit_note_page.replace('<data_id>', inserted_note_id)

        self.post_and_assert_result({'note_title': self.note_title, 'note_text': self.note_text},)

        self.post_and_assert_result({'note_title': self.edited_note_title, 'note_text': self.note_text},)

        self.post_and_assert_result({'note_title': self.edited_note_title, 'note_text': self.edited_note_text})

        self.post_and_assert_result({'note_title': self.note_title, 'note_text': self.note_text})

        try_to_edit_note = self.client.post(self.edit_page_with_id,
                                            {'note_title': self.new_note_title,
                                             'note_text': self.note_text})
        self.assertContains(try_to_edit_note, self.note_already_exists)

        note_edit_title_error = self.client.post(self.edit_page_with_id,
                                                 {'note_title': self.invalid_title,
                                                  'note_text': self.note_text})
        self.assertContains(note_edit_title_error, TITLE_MAX_LENGTH_ERROR)
        self.assertContains(note_edit_title_error, self.invalid_title)
        self.assertContains(note_edit_title_error, self.note_text)

        note_edit_text_error = self.client.post(self.edit_page_with_id,
                                                {'note_title': self.note_title,
                                                 'note_text': self.invalid_text})
        self.assertContains(note_edit_text_error, self.note_title)
        self.assertContains(note_edit_text_error, TEXT_MAX_VALUE_ERROR)
        self.assertContains(note_edit_text_error, self.invalid_text)

        note_edit_error = self.client.post(self.edit_page_with_id,
                                           {'note_title': self.invalid_title,
                                            'note_text': self.invalid_text})
        self.assertContains(note_edit_error, TITLE_MAX_LENGTH_ERROR)
        self.assertContains(note_edit_error, self.invalid_title)
        self.assertContains(note_edit_error, TEXT_MAX_VALUE_ERROR)
        self.assertContains(note_edit_error, self.invalid_text)

    def post_and_assert_result(self, input_data: dict) -> None:
        """Additional function to check if the response contains a check values."""
        post_note_edit = self.client.post(self.edit_page_with_id, input_data)

        api_response = requests_get(self.notes_api_with_data_id)
        edited_note = api_response.json()['note']

        self.assertEqual(edited_note['title'], input_data['note_title'])
        self.assertEqual(edited_note['text'], input_data['note_text'])
        self.assertContains(post_note_edit, self.note_was_edited)

    def test_delete_note(self):
        """Tests deleting of the note."""
        test_notes = [{'note_title': 'test note 01', 'note_text': 'text_ABC'},
                      {'note_title': 'test note 02', 'note_text': 'text 123'},
                      {'note_title': 'test note 03', 'note_text': 'text ONE-TWO-THREE'},
                      {'note_title': 'test note 04', 'note_text': None}]
        for test_data in test_notes:
            requests_post(NOTES_API, json=test_data)

        note_added = requests_post(NOTES_API, json={'note_title': self.note_title, 'note_text': self.note_text})
        note_id = note_added.json()['inserted_note_id']

        total_notes = get_total_notes()

        response_total_notes = self.client.get(self.all_notes_page)
        self.assertEqual(response_total_notes.context['total_notes'], total_notes)
        response_delete_note = self.client.get(self.delete_note_page.replace('<data_id>', str(note_id)))
        self.assertContains(response_delete_note, self.note_was_deleted)
        response_total_notes = self.client.get(self.all_notes_page)
        self.assertEqual(response_total_notes.context['total_notes'], total_notes - 1)

    def test_view_note_content(self):
        """Tests the displaying of the note content."""
        note_added = requests_post(NOTES_API, json={'note_title': self.note_title, 'note_text': self.note_text})
        note_1_id = note_added.json()['inserted_note_id']

        response = self.client.get(self.note_content_page.replace('<data_id>', str(note_1_id)))
        self.assertContains(response, 'Title:')
        self.assertContains(response, self.note_title)
        self.assertContains(response, 'Text:')
        self.assertContains(response, self.note_text)

        note_with_only_title = 'test note title #2'
        note_added = requests_post(NOTES_API, json={'note_title': note_with_only_title, 'note_text': None})
        note_2_id = note_added.json()['inserted_note_id']

        response = self.client.get(self.note_content_page.replace('<data_id>', str(note_2_id)))
        self.assertContains(response, 'Title:')
        self.assertContains(response, note_with_only_title)
        self.assertNotContains(response, 'Text:')

    def test_database_error(self):
        """Tests displaying of the Server Error URL."""
        server_error_response = self.client.get(self.server_error_page)
        self.assertContains(server_error_response, self.database_error, status_code=500)


def get_total_notes() -> int:
    """Returns the number of documents in the collection."""
    api_response = requests_get(NOTES_API)
    all_notes = api_response.json()
    return all_notes['total notes']
