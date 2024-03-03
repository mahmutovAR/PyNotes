class WebNotesMSG:
    """The class with the main application system messages."""

    __slots__ = ['note_inserted', 'note_updated', 'note_deleted',
                 'title_is_taken', 'no_notes_in_db', 'note_not_found', 'database_error']

    def __init__(self):
        self.note_inserted = 'Note was inserted'
        self.note_updated = 'Note was updated'
        self.note_deleted = 'Note was deleted'
        self.title_is_taken = 'Note with entered title already exists'
        self.no_notes_in_db = 'No notes in database'
        self.note_not_found = 'Note not found'
        self.database_error = 'Database connection failed'

    def get_msg_note_inserted(self):
        """Returns a message that a note has been inserted."""
        return self.note_inserted

    def get_msg_note_updated(self):
        """Returns a message that a note has been updated."""
        return self.note_updated

    def get_msg_note_deleted(self):
        """Returns a message that a note has been deleted."""
        return self.note_deleted

    def get_msg_title_is_taken(self):
        """Returns a message that a note title is taken."""
        return self.title_is_taken

    def get_msg_no_notes_in_db(self):
        """Returns a message that there are no notes in the collection."""
        return self.no_notes_in_db

    def get_msg_note_not_found(self):
        """Returns a message that note was not found."""
        return self.note_not_found

    def get_msg_database_error(self):
        """Returns a database error message."""
        return self.database_error


NotesMSG = WebNotesMSG()
