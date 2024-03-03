from WebPyNotes_settings import NotesPages
from django.urls import path

from . import views


urlpatterns = [
    path(NotesPages.get_index_page(), views.view_index, name='index'),

    path(NotesPages.get_add_page(), views.view_add_note, name='add_note'),

    path(NotesPages.get_all_notes_page(), views.view_all_notes, name='all_notes'),

    path(NotesPages.get_note_content_page(), views.view_note_content, name='note_content'),

    path(NotesPages.get_edit_note_page(), views.view_edit_note, name='edit_note'),

    path(NotesPages.get_delete_note_page(), views.view_delete_note, name='delete_note'),

    path(NotesPages.get_search_note_page(), views.view_search_note, name='search_note'),

    path(NotesPages.get_server_error_page(), views.web_notes_server_error, name='notes_server_error')
]
