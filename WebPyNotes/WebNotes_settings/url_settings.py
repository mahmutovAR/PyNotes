from urllib.parse import urljoin


class WebNotesPattern:
    """Class with patterns of the application."""
    def __init__(self):
        self.homepage = 'home/'
        self.create_note = 'create/'
        self.all_notes = 'all/'
        self.note_content = 'view/<data_id>/'
        self.edit_note = 'edit/<data_id>/'
        self.delete_note = 'delete/<data_id>/'
        self.search_note = 'search/'
        self.server_error = '500/'

    def get_home_pattern(self):
        return self.homepage

    def get_create_pattern(self):
        return self.create_note

    def get_all_notes_pattern(self):
        return self.all_notes

    def get_note_content_pattern(self):
        return self.note_content

    def get_edit_note_pattern(self):
        return self.edit_note

    def get_delete_note_pattern(self):
        return self.delete_note

    def get_search_note_pattern(self):
        return self.search_note

    def get_server_error_pattern(self):
        return self.server_error


class WebNotesURL:
    """Class with URLS of the application."""
    def __init__(self):
        self.homepage = '/webnotes/home/'
        self.create_note = '/webnotes/create/'
        self.all_notes = '/webnotes/all/'
        self.note_content = '/webnotes/view/<data_id>/'
        self.edit_note = '/webnotes/edit/<data_id>/'
        self.delete_note = '/webnotes/delete/<data_id>/'
        self.search_note = '/webnotes/search/'
        self.server_error = '/webnotes/500/'

    def get_home_url(self):
        return self.homepage

    def get_create_url(self):
        return self.create_note

    def get_all_notes_url(self):
        return self.all_notes

    def get_note_content_url(self):
        return self.note_content

    def get_edit_note_url(self):
        return self.edit_note

    def get_delete_note_url(self):
        return self.delete_note

    def get_search_note_url(self):
        return self.search_note

    def get_server_error_url(self):
        return self.server_error


class WebNotesAPI:
    """Class with API settings."""
    def __init__(self):
        self.ip_and_port = 'http://127.0.0.1:5000/'
        self.notes_endpoint = '/webnotes/api/v1.0/notes/'
        self.test_notes_endpoint = '/webnotes/api/v1.0/test/notes/'

    def get_api_url(self):
        return self.notes_endpoint

    def get_api_url_data_id(self):
        return urljoin(self.notes_endpoint, '<data_id>')

    def get_api_url_search(self):
        return urljoin(self.notes_endpoint, 'search')

    def get_test_api_url(self):
        return self.test_notes_endpoint

    def get_api_url_for_views(self):
        return urljoin(self.ip_and_port, self.notes_endpoint)

    def get_api_url_for_tests(self):
        return urljoin(self.ip_and_port, self.test_notes_endpoint)


NotesPatterns = WebNotesPattern()
NotesURLs = WebNotesURL()
NotesAPI = WebNotesAPI()
