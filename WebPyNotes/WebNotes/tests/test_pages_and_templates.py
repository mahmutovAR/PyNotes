from django.urls import resolve
import requests

from WebPyNotes_settings import NotesTemplates, NotesPages, DatabaseAPI
from . import MongoTestCase, format_url
from .. import views


DB_API = DatabaseAPI.get_notes_schema()
DB_TEST_API = DatabaseAPI.get_test_absolut_url()


class PagesAnDTemplatesTest(MongoTestCase):
    """Tests pages and used templates."""
    def setUp(self):
        requests.post(DB_TEST_API, json={'test_notes_num': 1}).json()
        all_notes = requests.get(DB_API).json()
        self.test_note_id = all_notes['notes_all'][0]['id']

        self.index_page = format_url(NotesPages.get_index_page())
        self.add_page = format_url(NotesPages.get_add_page())
        self.all_notes_page = format_url(NotesPages.get_all_notes_page())
        self.note_content_page = format_url(NotesPages.get_note_content_page())
        self.note_content_testing_template = format_url(
            NotesPages.get_note_content_page().replace('<data_id>', self.test_note_id))
        self.edit_note_page = format_url(NotesPages.get_edit_note_page())
        self.edit_note_testing_template = format_url(
            NotesPages.get_edit_note_page().replace('<data_id>', self.test_note_id))
        self.delete_note_page = format_url(NotesPages.get_delete_note_page())
        self.search_note_page = format_url(NotesPages.get_search_note_page())

        self.index_template = NotesTemplates.get_index_template()
        self.create_template = NotesTemplates.get_add_note_template()
        self.all_notes_template = NotesTemplates.get_all_notes_template()
        self.note_content_template = NotesTemplates.get_note_content_template()
        self.edit_note_template = NotesTemplates.get_edit_note_template()
        self.search_note_template = NotesTemplates.get_search_note_template()

    def tearDown(self) -> None:
        requests.delete(DB_TEST_API)

    def test_homepage(self):
        """Tests the match between the link and the template used for the homepage."""
        url = resolve(self.index_page)
        self.assertEqual(url.func, views.view_index)
        response = self.client.get(self.index_page)
        self.assertTemplateUsed(response, self.index_template)

    def test_add_note(self):
        """Tests the match between the link and the template used for the note creating."""
        url = resolve(self.add_page)
        self.assertEqual(url.func, views.view_add_note)
        response = self.client.get(self.add_page)
        self.assertTemplateUsed(response, self.create_template)

    def test_view_all_notes(self):
        """Tests the match between the link and the template used for the displaying all notes."""
        url = resolve(self.all_notes_page)
        self.assertEqual(url.func, views.view_all_notes)
        response = self.client.get(self.all_notes_page)
        self.assertTemplateUsed(response, self.all_notes_template)

    def test_view_note_content(self):
        """Tests the match between the link and the template used for the displaying note content."""
        url = resolve(self.note_content_page)
        self.assertEqual(url.func, views.view_note_content)
        response = self.client.get(self.note_content_testing_template)
        self.assertTemplateUsed(response, self.note_content_template)

    def test_edit_note(self):
        """Tests the match between the link and the template used for the note editing."""
        url = resolve(self.edit_note_page)
        self.assertEqual(url.func, views.view_edit_note)
        response = self.client.get(self.edit_note_testing_template)
        self.assertTemplateUsed(response, self.edit_note_template)

    def test_delete_note(self):
        """Tests the match between the link and the function used for the note deleting."""
        url = resolve(self.delete_note_page)
        self.assertEqual(url.func, views.view_delete_note)

    def test_note_search(self):
        """Tests the match between the link and the template used for the note searching."""
        url = resolve(self.search_note_page)
        self.assertEqual(url.func, views.view_search_note)
        response = self.client.get(self.search_note_page)
        self.assertTemplateUsed(response, self.search_note_template)
