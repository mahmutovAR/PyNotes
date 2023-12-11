from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('WebNotes.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler500 = 'WebNotes.views.web_notes_server_error'
