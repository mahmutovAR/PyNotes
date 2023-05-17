from ..forms import TextNoteForm,\
    NO_TITLE_ERROR, TITLE_MAX_LENGTH, TITLE_MAX_LENGTH_ERROR,\
    TEXT_MAX_LENGTH, TEXT_MAX_VALUE_ERROR
from . import MongoTestCase


class TextNoteFormTest(MongoTestCase):
    """Tests TextNote form."""
    def setUp(self) -> None:
        self.valid_title = 'test note title'
        self.valid_text = 'test note text'
        self.invalid_title = 'a'*TITLE_MAX_LENGTH + 'b'
        self.invalid_text = 'a'*TEXT_MAX_LENGTH + 'b'

    def test_valid_title(self):
        """Tests form validation of the entered data, title and text are valid."""
        note_form = TextNoteForm(data={'note_title': self.valid_title, 'note_text': self.valid_text})
        self.assertTrue(note_form.is_valid())

    def test_valid_title_without_text(self):
        """Tests form validation without text."""
        note_form = TextNoteForm(data={'note_title': self.valid_title, 'note_text': None})
        self.assertTrue(note_form.is_valid())

    def test_invalid_title_no_data(self):
        """Tests form validation for invalid title, no title."""
        note_form = TextNoteForm(data={'note_title': None, 'note_text': self.valid_text})
        self.assertFalse(note_form.is_valid())
        self.assertEqual(note_form.errors['note_title'], [NO_TITLE_ERROR])

    def test_invalid_title_above_max_length(self):
        """Test form validation for invalid title, maximum length exceeded."""
        note_form = TextNoteForm(data={'note_title': self.invalid_title, 'note_text': self.valid_text})
        self.assertFalse(note_form.is_valid())
        self.assertEqual(note_form.errors['note_title'], [TITLE_MAX_LENGTH_ERROR])

    def test_invalid_text_above_max_length(self):
        """Test form validation for invalid text, maximum length exceeded."""
        note_form = TextNoteForm(data={'note_title': self.valid_title, 'note_text': self.invalid_text})
        self.assertFalse(note_form.is_valid())
        self.assertEqual(note_form.errors['note_text'], [TEXT_MAX_VALUE_ERROR])

    def test_invalid_title_invalid_text_above_max_length(self):
        """Test form validation for invalid title and invalid text, maximum lengths exceeded."""
        note_form = TextNoteForm(data={'note_title': self.invalid_title, 'note_text': self.invalid_text})
        self.assertFalse(note_form.is_valid())
        self.assertEqual(note_form.errors['note_title'], [TITLE_MAX_LENGTH_ERROR])
        self.assertEqual(note_form.errors['note_text'], [TEXT_MAX_VALUE_ERROR])
