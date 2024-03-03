from WebNotes_settings import NotesPages
from django.urls import path

from . import views as notes_views


urlpatterns = [
    path(NotesPages.get_index_page(),
         notes_views.index, name='index'),

    path(NotesPages.get_add_page(),
         notes_views.add_note, name='add_note'),

    path(NotesPages.get_all_notes_page(),
         notes_views.view_all_notes, name='all_notes'),

    path(NotesPages.get_note_content_page(),
         notes_views.view_note_content, name='note_content'),

    path(NotesPages.get_edit_note_page(),
         notes_views.edit_note, name='edit_note'),

    path(NotesPages.get_delete_note_page(),
         notes_views.delete_note, name='delete_note'),

    path(NotesPages.get_search_note_page(),
         notes_views.search_note, name='search_note'),

    path(NotesPages.get_server_error_page(),
         notes_views.web_notes_server_error, name='notes_server_error')
]
