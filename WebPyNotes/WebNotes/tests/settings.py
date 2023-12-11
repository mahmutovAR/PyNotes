from django.test import TestCase
from django.test.runner import DiscoverRunner


class MongoTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass


class MongoTestCase(TestCase):
    def _fixture_setup(self):
        pass

    def _fixture_teardown(self):
        pass


def format_url(input_url: str) -> str:
    """Formats the input pattern into a test URL, by adding the leading slash."""
    if input_url.startswith('/'):
        return input_url
    else:
        return f'/{input_url}'
