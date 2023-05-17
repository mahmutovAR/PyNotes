class WebNotesTemplates:
    """Class with main templates for view functions of the application."""
    def __init__(self):
        self.homepage_template = 'homepage.html'
        self.create_template = 'note_create.html'
        self.all_notes_template = 'notes_all.html'
        self.note_content_template = 'note_content.html'
        self.edit_note_template = 'note_edit.html'
        self.search_note_template = 'note_search.html'
        self.server_error_template = 'server_error.html'

    def get_server_error_template(self):
        return self.server_error_template

    def get_homepage_template(self):
        return self.homepage_template

    def get_create_template(self):
        return self.create_template

    def get_all_notes_template(self):
        return self.all_notes_template

    def get_note_content_template(self):
        return self.note_content_template

    def get_edit_note_template(self):
        return self.edit_note_template

    def get_search_note_template(self):
        return self.search_note_template


NotesTemplates = WebNotesTemplates()
