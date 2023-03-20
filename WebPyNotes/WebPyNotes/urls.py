from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from WebNotes import views as notes_views


urlpatterns = [
    path('', notes_views.homepage, name='homepage'),  # homepage
    path('note/create', notes_views.create_note, name='create_note'),  # create new note
    path('all_notes/', notes_views.view_all_notes, name='all_notes'),  # all notes # pagination!!
    path('note/view/<record_id>', notes_views.view_note_content, name='note_content'),  # note content
    path('note/edit/<record_id>', notes_views.edit_note, name='edit_note'),  # editing note
    path(r'note/delete/<record_id>', notes_views.delete_note, name='delete_note'),  # deleting note
    path('note/search', notes_views.search_note, name='search_note'),  # searching for note
    path('admin/', admin.site.urls),
]
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
