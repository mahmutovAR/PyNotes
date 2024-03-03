class WebNotesPages:
    """Class with pages (URLS) of the application."""
    __slots__ = ['index', 'add_note', 'all_notes', 'note_content',
                 'edit_note', 'delete_note', 'search_note', 'server_error']

    def __init__(self):
        self.index = 'webnotes/'
        self.add_note = 'webnotes/add'
        self.all_notes = 'webnotes/all'
        self.note_content = 'webnotes/view/<data_id>'
        self.edit_note = 'webnotes/edit/<data_id>'
        self.delete_note = 'webnotes/delete/<data_id>'
        self.search_note = 'webnotes/search'
        self.server_error = 'webnotes/500'

    def get_index_page(self):
        """Returns 'homepage'."""
        return self.index

    def get_add_page(self):
        """Returns 'add note' page."""
        return self.add_note

    def get_all_notes_page(self):
        """Returns 'all notes' page."""
        return self.all_notes

    def get_note_content_page(self):
        """Returns 'note content' page."""
        return self.note_content

    def get_edit_note_page(self):
        """Returns 'edit note' page."""
        return self.edit_note

    def get_delete_note_page(self):
        """Returns 'delete note' page."""
        return self.delete_note

    def get_search_note_page(self):
        """Returns 'note search' page."""
        return self.search_note

    def get_server_error_page(self):
        """Returns 'server error' page."""
        return self.server_error


NotesPages = WebNotesPages()
