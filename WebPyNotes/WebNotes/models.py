from django.db import models


class TextNote(models.Model):
    """."""
    note_title = models.CharField(default='',
                                  max_length=50,
                                  help_text="Enter note's label",
                                  verbose_name="Note's title")
    note_text = models.TextField(default='',
                                 help_text="Enter note's text",
                                 verbose_name="Note's text")
