from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('webnotes/', include('WebNotes.urls')),
]

handler500 = 'WebNotes.views.web_notes_server_error'
