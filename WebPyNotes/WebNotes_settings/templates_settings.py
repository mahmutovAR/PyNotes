class WebNotesTemplates:
    """Class with main templates for view functions of the application."""
    def __init__(self):
        self.index_template = 'index.html'
        self.add_note_template = 'note-add-edit.html'
        self.all_notes_template = 'notes-all.html'
        self.note_content_template = 'note-content.html'
        self.edit_note_template = 'note-add-edit.html'
        self.search_note_template = 'note-search.html'
        self.server_error_template = 'server-error.html'

    def get_server_error_template(self):
        return self.server_error_template

    def get_index_template(self):
        return self.index_template

    def get_add_note_template(self):
        return self.add_note_template

    def get_all_notes_template(self):
        return self.all_notes_template

    def get_note_content_template(self):
        return self.note_content_template

    def get_edit_note_template(self):
        return self.edit_note_template

    def get_search_note_template(self):
        return self.search_note_template


NotesTemplates = WebNotesTemplates()
