from urllib.parse import urljoin


class WebNotesPages:
    """Class with pages (URLS) of the application."""
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
        return self.index

    def get_add_page(self):
        return self.add_note

    def get_all_notes_page(self):
        return self.all_notes

    def get_note_content_page(self):
        return self.note_content

    def get_edit_note_page(self):
        return self.edit_note

    def get_delete_note_page(self):
        return self.delete_note

    def get_search_note_page(self):
        return self.search_note

    def get_server_error_page(self):
        return self.server_error


class WebNotesAPI:
    """Class with API settings."""
    def __init__(self):
        self.ip_and_port = 'http://127.0.0.1:5000/'
        self.notes_endpoint = '/webnotes/api/v1.0/notes/'
        self.test_notes_endpoint = '/webnotes/api/v1.0/test/notes/'

    def get_api(self):
        return self.notes_endpoint

    def get_api_data_id(self):
        return urljoin(self.notes_endpoint, '<data_id>')

    def get_api_search(self):
        return urljoin(self.notes_endpoint, 'search')

    def get_test_api(self):
        return self.test_notes_endpoint

    def get_api_for_views(self):
        return urljoin(self.ip_and_port, self.notes_endpoint)

    def get_api_for_tests(self):
        return urljoin(self.ip_and_port, self.test_notes_endpoint)


NotesPages = WebNotesPages()
NotesAPI = WebNotesAPI()
