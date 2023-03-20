from django.contrib import admin
from .models import TextNote


@admin.register(TextNote)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('note_title', 'note_text')
