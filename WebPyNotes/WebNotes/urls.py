from WebNotes_settings import NotesPatterns
from django.urls import path

from . import views as notes_views


urlpatterns = [
    path(NotesPatterns.get_home_pattern(),
         notes_views.homepage, name='homepage'),

    path(NotesPatterns.get_create_pattern(),
         notes_views.create_note, name='create_note'),

    path(NotesPatterns.get_all_notes_pattern(),
         notes_views.view_all_notes, name='all_notes'),

    path(NotesPatterns.get_note_content_pattern(),
         notes_views.view_note_content, name='note_content'),

    path(NotesPatterns.get_edit_note_pattern(),
         notes_views.edit_note, name='edit_note'),

    path(NotesPatterns.get_delete_note_pattern(),
         notes_views.delete_note, name='delete_note'),

    path(NotesPatterns.get_search_note_pattern(),
         notes_views.search_note, name='search_note'),

    path(NotesPatterns.get_server_error_pattern(),
         notes_views.web_notes_server_error, name='notes_server_error')
]
