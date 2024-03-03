from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator


NO_TITLE_ERROR = 'Note cannot be saved without a title'
TITLE_MAX_LENGTH = 40
TITLE_MAX_LENGTH_ERROR = f'Invalid title length: above {TITLE_MAX_LENGTH}'
TEXT_MAX_LENGTH = 200
TEXT_MAX_VALUE_ERROR = f'Invalid text length: above {TEXT_MAX_LENGTH}'


class TextNoteForm(forms.Form):
    """The main form of the application, contains a title and text (optional)."""
    note_title = forms.CharField(label='Enter note title',
                                 required=True,
                                 error_messages={'required': NO_TITLE_ERROR,
                                                 'max_length': TITLE_MAX_LENGTH_ERROR},
                                 validators=[MaxLengthValidator(TITLE_MAX_LENGTH)])
    note_text = forms.CharField(label='Enter note text',
                                required=False,
                                error_messages={'max_length': TEXT_MAX_VALUE_ERROR},
                                validators=[MaxLengthValidator(TEXT_MAX_LENGTH)])

    def clean_note_title(self):
        """Verifies the note title for the presence and the maximum length,
        otherwise an ValidationError is raised."""
        data = self.cleaned_data['note_title']
        if not data:
            raise ValidationError(NO_TITLE_ERROR)
        elif len(data) > TITLE_MAX_LENGTH:
            raise ValidationError(TITLE_MAX_LENGTH_ERROR)
        return data

    def clean_note_text(self):
        """Verifies the note text for the maximum length,
        otherwise an ValidationError is raised."""
        data = self.cleaned_data['note_text']
        if len(data) > TEXT_MAX_LENGTH:
            raise ValidationError(TEXT_MAX_VALUE_ERROR)
        return data
