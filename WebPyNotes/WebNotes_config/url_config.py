from os.path import join as os_path_join


class WebNotesURL:
    """Class with main patterns and URLS of the application."""
    def __init__(self):
        self.app_url = '/webnotes/'
        self.home_url = 'home/'
        self.create_url = 'create/'
        self.all_notes_url = 'all/'
        self.note_content_url = 'view/<data_id>/'
        self.edit_note_url = 'edit/<data_id>/'
        self.delete_note_url = 'delete/<data_id>/'
        self.search_note_url = 'search/'
        self.server_error_url = '500/'

    def get_home_pattern(self):
        return self.home_url

    def get_create_pattern(self):
        return self.create_url

    def get_all_notes_pattern(self):
        return self.all_notes_url

    def get_note_content_pattern(self):
        return self.note_content_url

    def get_edit_note_pattern(self):
        return self.edit_note_url

    def get_delete_note_pattern(self):
        return self.delete_note_url

    def get_search_note_pattern(self):
        return self.search_note_url

    def get_server_error_pattern(self):
        return self.server_error_url

    def get_home_url(self):
        return os_path_join(self.app_url, self.home_url)

    def get_create_url(self):
        return os_path_join(self.app_url, self.create_url)

    def get_all_notes_url(self):
        return os_path_join(self.app_url, self.all_notes_url)

    def get_note_content_url(self):
        return os_path_join(self.app_url, self.note_content_url)

    def get_edit_note_url(self):
        return os_path_join(self.app_url, self.edit_note_url)

    def get_delete_note_url(self):
        return os_path_join(self.app_url, self.delete_note_url)

    def get_search_note_url(self):
        return os_path_join(self.app_url, self.search_note_url)

    def get_server_error_url(self):
        return os_path_join(self.app_url, self.server_error_url)


NotesURLs = WebNotesURL()
