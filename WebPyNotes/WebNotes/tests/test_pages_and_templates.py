from WebNotes_settings import NotesTemplates, NotesPages, NotesAPI
from django.urls import resolve

from . import MongoTestCase, format_url
from ..views import *

NOTES_API = NotesAPI.get_api_for_views()
TEST_NOTES_API = NotesAPI.get_api_for_tests()


class PagesAnDTemplatesTest(MongoTestCase):
    """Tests pages and used templates."""
    def setUp(self):
        requests_post(TEST_NOTES_API, json={'test_notes_num': 1})
        api_response = requests_get(NOTES_API)
        all_notes = api_response.json()
        test_note = all_notes['notes'][0]
        self.test_note_id = test_note['id']

        self.index_page = format_url(NotesPages.get_index_page())
        self.add_page = format_url(NotesPages.get_add_page())
        self.all_notes_page = format_url(NotesPages.get_all_notes_page())
        self.note_content_page = format_url(NotesPages.get_note_content_page())
        self.note_content_testing_template = format_url(NotesPages.get_note_content_page().replace('<data_id>',
                                                                                                   self.test_note_id))
        self.edit_note_page = format_url(NotesPages.get_edit_note_page())
        self.edit_note_testing_template = format_url(NotesPages.get_edit_note_page().replace('<data_id>',
                                                                                             self.test_note_id))
        self.delete_note_page = format_url(NotesPages.get_delete_note_page())
        self.search_note_page = format_url(NotesPages.get_search_note_page())

        self.index_template = NotesTemplates.get_index_template()
        self.create_template = NotesTemplates.get_add_note_template()
        self.all_notes_template = NotesTemplates.get_all_notes_template()
        self.note_content_template = NotesTemplates.get_note_content_template()
        self.edit_note_template = NotesTemplates.get_edit_note_template()
        self.search_note_template = NotesTemplates.get_search_note_template()

    def tearDown(self) -> None:
        requests_delete(TEST_NOTES_API)

    def test_homepage(self):
        """Tests the match between the link and the template used for the homepage."""
        url = resolve(self.index_page)
        response = self.client.get(self.index_page)
        self.assertEqual(url.func, index)
        self.assertTemplateUsed(response, self.index_template)

    def test_add_note(self):
        """Tests the match between the link and the template used for the note creating."""
        url = resolve(self.add_page)
        response = self.client.get(self.add_page)
        self.assertEqual(url.func, add_note)
        self.assertTemplateUsed(response, self.create_template)

    def test_view_all_notes(self):
        """Tests the match between the link and the template used for the displaying all notes."""
        url = resolve(self.all_notes_page)
        response = self.client.get(self.all_notes_page)
        self.assertEqual(url.func, view_all_notes)
        self.assertTemplateUsed(response, self.all_notes_template)

    def test_view_note_content(self):
        """Tests the match between the link and the template used for the displaying notes content."""
        url = resolve(self.note_content_page)
        response = self.client.get(self.note_content_testing_template)
        self.assertEqual(url.func, view_note_content)
        self.assertTemplateUsed(response, self.note_content_template)

    def test_edit_note(self):
        """Tests the match between the link and the template used for the note editing."""
        url = resolve(self.edit_note_page)
        response = self.client.get(self.edit_note_testing_template)
        self.assertEqual(url.func, edit_note)
        self.assertTemplateUsed(response, self.edit_note_template)

    def test_delete_note(self):
        """Tests the match between the link and the template used for the note deleting."""
        url = resolve(self.delete_note_page)
        self.assertEqual(url.func, delete_note)

    def test_note_search(self):
        """Tests the match between the link and the template used for the note searching."""
        url = resolve(self.search_note_page)
        response = self.client.get(self.search_note_page)
        self.assertEqual(url.func, search_note)
        self.assertTemplateUsed(response, self.search_note_template)
