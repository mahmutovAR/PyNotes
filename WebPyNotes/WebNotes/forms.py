from django import forms

from .models import TextNote


class NewNoteForm(forms.ModelForm):
    """Form for object of TextNote class."""
    class Meta:
        model = TextNote
        fields = '__all__'
