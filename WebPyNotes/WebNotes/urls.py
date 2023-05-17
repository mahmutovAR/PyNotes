from WebNotes_config import NotesURLs
from django.urls import path

from . import views as notes_views


urlpatterns = [
    path(NotesURLs.get_home_pattern(),
         notes_views.homepage, name='homepage'),

    path(NotesURLs.get_create_pattern(),
         notes_views.create_note, name='create_note'),

    path(NotesURLs.get_all_notes_pattern(),
         notes_views.view_all_notes, name='all_notes'),

    path(NotesURLs.get_note_content_pattern(),
         notes_views.view_note_content, name='note_content'),

    path(NotesURLs.get_edit_note_pattern(),
         notes_views.edit_note, name='edit_note'),

    path(NotesURLs.get_delete_note_pattern(),
         notes_views.delete_note, name='delete_note'),

    path(NotesURLs.get_search_note_pattern(),
         notes_views.search_note, name='search_note'),

    path(NotesURLs.get_server_error_pattern(),
         notes_views.web_notes_server_error, name='notes_server_error')
]
