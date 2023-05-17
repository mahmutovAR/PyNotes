class WebNotesMSG:
    """The class with the main application system messages."""

    def __init__(self):
        self.note_inserted = 'Note was inserted'
        self.note_edited = 'Note was updated'
        self.note_deleted = 'Note was deleted'
        self.note_already_exists = 'Note with entered title already exists'
        self.no_notes_in_db = 'No notes in current database'
        self.database_error = 'Database connection failed'

    def get_msg_note_inserted(self):
        return self.note_inserted

    def get_msg_note_edited(self):
        return self.note_edited

    def get_msg_note_deleted(self):
        return self.note_deleted

    def get_msg_note_already_exists(self):
        return self.note_already_exists

    def get_msg_no_notes_in_db(self):
        return self.no_notes_in_db

    def get_msg_database_error(self):
        return self.database_error


NotesMSG = WebNotesMSG()
