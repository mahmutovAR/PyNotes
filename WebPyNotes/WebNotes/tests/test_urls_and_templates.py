from WebNotes_config import NotesTemplates, NotesURLs, TEST_DB
from django.urls import resolve

from . import MongoTestCase
from ..views import *


class UrlsAnDTemplatesTest(MongoTestCase):
    """Tests URLS and used templates."""
    def setUp(self):
        TEST_DB.insert_one({'_title': 'test note', '_text': 'just test note text'})
        self.test_note = TEST_DB.find_one()
        self.test_note_id = str(self.test_note['_id'])

        self.home_url = NotesURLs.get_home_url()
        self.create_url = NotesURLs.get_create_url()
        self.all_notes_url = NotesURLs.get_all_notes_url()
        self.note_content_url = NotesURLs.get_note_content_url()
        self.note_content_testing_template = NotesURLs.get_note_content_url().replace('<data_id>',
                                                                                           self.test_note_id)
        self.edit_note_url = NotesURLs.get_edit_note_url()
        self.edit_note_testing_template = NotesURLs.get_edit_note_url().replace('<data_id>', self.test_note_id)
        self.delete_note_url = NotesURLs.get_delete_note_url()
        self.search_note_url = NotesURLs.get_search_note_url()

        self.home_template = NotesTemplates.get_homepage_template()
        self.create_template = NotesTemplates.get_create_template()
        self.all_notes_template = NotesTemplates.get_all_notes_template()
        self.note_content_template = NotesTemplates.get_note_content_template()
        self.edit_note_template = NotesTemplates.get_edit_note_template()
        self.search_note_template = NotesTemplates.get_search_note_template()

    def tearDown(self) -> None:
        TEST_DB.delete_many({})

    def test_homepage(self):
        """Tests the match between the link and the template used for the homepage."""
        url = resolve(self.home_url)
        response = self.client.get(self.home_url)
        self.assertEqual(url.func, homepage)
        self.assertTemplateUsed(response, self.home_template)

    def test_create_new_note(self):
        """Tests the match between the link and the template used for the note creating."""
        url = resolve(self.create_url)
        response = self.client.get(self.create_url)
        self.assertEqual(url.func, create_note)
        self.assertTemplateUsed(response, self.create_template)

    def test_view_all_notes(self):
        """Tests the match between the link and the template used for the displaying all notes."""
        url = resolve(self.all_notes_url)
        response = self.client.get(self.all_notes_url)
        self.assertEqual(url.func, view_all_notes)
        self.assertTemplateUsed(response, self.all_notes_template)

    def test_view_note_content(self):
        """Tests the match between the link and the template used for the displaying notes content."""
        url = resolve(self.note_content_url)
        response = self.client.get(self.note_content_testing_template)
        self.assertEqual(url.func, view_note_content)
        self.assertTemplateUsed(response, self.note_content_template)

    def test_edit_note(self):
        """Tests the match between the link and the template used for the note editing."""
        url = resolve(self.edit_note_url)
        response = self.client.get(self.edit_note_testing_template)
        self.assertEqual(url.func, edit_note)
        self.assertTemplateUsed(response, self.edit_note_template)

    def test_delete_note(self):
        """Tests the match between the link and the template used for the note deleting."""
        url = resolve(self.delete_note_url)
        self.assertEqual(url.func, delete_note)

    def test_note_search(self):
        """Tests the match between the link and the template used for the note searching."""
        url = resolve(self.search_note_url)
        response = self.client.get(self.search_note_url)
        self.assertEqual(url.func, search_note)
        self.assertTemplateUsed(response, self.search_note_template)
