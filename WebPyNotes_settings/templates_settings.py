class WebNotesTemplates:
    """Class with main templates for view functions of the application."""
    __slots__ = ['index_template', 'add_note_template', 'all_notes_template', 'note_content_template',
                 'edit_note_template', 'search_note_template', 'server_error_template']

    def __init__(self):
        self.index_template = 'index.html'
        self.add_note_template = 'note-add-edit.html'
        self.all_notes_template = 'notes-all.html'
        self.note_content_template = 'note-content.html'
        self.edit_note_template = 'note-add-edit.html'
        self.search_note_template = 'note-search.html'
        self.server_error_template = 'server-error.html'

    def get_index_template(self):
        """Returns 'homepage' template."""
        return self.index_template

    def get_add_note_template(self):
        """Returns 'add note' template."""
        return self.add_note_template

    def get_all_notes_template(self):
        """Returns 'all notes' template."""
        return self.all_notes_template

    def get_note_content_template(self):
        """Returns 'note content' template."""
        return self.note_content_template

    def get_edit_note_template(self):
        """Returns 'edit note' template."""
        return self.edit_note_template

    def get_search_note_template(self):
        """Returns 'note search' template."""
        return self.search_note_template

    def get_server_error_template(self):
        """Returns 'server error' template."""
        return self.server_error_template


NotesTemplates = WebNotesTemplates()
