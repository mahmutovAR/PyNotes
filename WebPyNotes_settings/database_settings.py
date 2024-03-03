from urllib.parse import urljoin


class PyNotesDatabaseAPI:
    """Class with database API settings."""
    __slots__ = ['ip_and_port', 'api_path_and_version', 'notes_endpoint',
                 'absolut_notes_endpoint', 'total_notes_endpoint', 'test_notes_endpoint']

    def __init__(self):
        self.ip_and_port = 'http://127.0.0.1:5000/'
        self.api_path_and_version = urljoin('/webnotes/api', 'v1.0')
        self.notes_endpoint = urljoin(self.api_path_and_version, 'notes')
        self.absolut_notes_endpoint = urljoin(self.ip_and_port, self.notes_endpoint)
        self.total_notes_endpoint = urljoin(self.notes_endpoint, 'total')
        self.test_notes_endpoint = urljoin(self.api_path_and_version, 'test')

    def get_notes_api(self):
        """Returns the application's main endpoint."""
        return self.notes_endpoint

    def get_notes_schema(self):
        """Returns the application's main absolut URL."""
        return self.absolut_notes_endpoint

    def get_total_notes_api(self):
        """Returns the 'total notes' endpoint."""
        return self.total_notes_endpoint

    def get_total_notes_schema(self):
        """Returns the 'total notes' absolut URL."""
        return urljoin(self.ip_and_port, self.total_notes_endpoint)

    def get_note_by_id_api(self):
        """Returns the 'data ID' endpoint."""
        return urljoin(self.notes_endpoint, '<data_id>')

    def get_note_by_id_schema(self):
        """Returns the 'data ID' absolut URL."""
        return urljoin(self.absolut_notes_endpoint, '<data_id>')

    def get_note_by_query_api(self):
        """Returns the 'note search' endpoint."""
        return urljoin(self.notes_endpoint, 'search')

    def get_note_by_query_schema(self):
        """Returns the 'note search' absolut URL."""
        return urljoin(self.absolut_notes_endpoint, 'search')

    def get_note_by_text_api(self):
        """Returns the 'query object for note search' endpoint."""
        return urljoin(self.notes_endpoint, 'search_text', '<query_obj>')

    def get_note_by_text_schema(self):
        """Returns the 'query object for note search' absolut URL."""
        return urljoin(self.absolut_notes_endpoint, 'search_text', '<query_obj>')

    def get_test_api(self):
        """Returns the 'application test' endpoint."""
        return self.test_notes_endpoint

    def get_test_absolut_url(self):
        """Returns the 'application test' absolut URL."""
        return urljoin(self.ip_and_port, self.test_notes_endpoint)


DatabaseAPI = PyNotesDatabaseAPI()
