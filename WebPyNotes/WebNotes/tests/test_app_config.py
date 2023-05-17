from os import remove as os_remove
from os.path import isfile
from os.path import join as os_path_join
from pathlib import Path
from unittest import TestCase
from configparser import ConfigParser

from WebNotes_config import DEFAULT_DJANGO_PASS,\
    DEFAULT_DATABASE_NAME, DEFAULT_COLLECTION_NAME, DEFAULT_DATABASE_HOST

from WebNotes_config import get_config_settings


TEST_CONFIG_FILE = os_path_join(Path(__file__).resolve().parents[3], 'test_config.ini')


class AppConfigDataTest(TestCase):
    """Tests parsing of the configuration file."""

    def setUp(self) -> None:
        self.default_django_pass = DEFAULT_DJANGO_PASS
        self.default_db_name = DEFAULT_DATABASE_NAME
        self.default_db_collection = DEFAULT_COLLECTION_NAME
        self.default_db_host = DEFAULT_DATABASE_HOST

        self.default_settings = {'password': self.default_django_pass,
                                 'name': self.default_db_name,
                                 'collection': self.default_db_collection,
                                 'host': self.default_db_host}

        self.test_config = {'password': '1_23-as_df',
                            'name': 'te__st_DB_name',
                            'collection': 'test_collection_name',
                            'host': 'mongodb://127..27'}

        self.test_config_with_spaces = {'password': '1 23-as df',
                                        'name': 'te  st DB name',
                                        'collection': 'test collection name',
                                        'host': 'mongodb://127..27'}

    def tearDown(self) -> None:
        if isfile(TEST_CONFIG_FILE):
            os_remove(TEST_CONFIG_FILE)

    def assertEqual_config_data(self, test_data: dict):
        """Asserts equal for testing configuration data and reference input data."""
        test_notes_config = get_config_settings('test_config.ini')
        django_pass = test_notes_config.get_django_password()
        db_name = test_notes_config.get_database_name()
        db_collection = test_notes_config.get_database_collection()
        db_host = test_notes_config.get_database_client_host()

        self.assertEqual(django_pass, test_data['password'])
        self.assertEqual(db_name, test_data['name'])
        self.assertEqual(db_collection, test_data['collection'])
        self.assertEqual(db_host, test_data['host'])

    def test_valid_config_file(self):
        """Tests valid configuration file."""
        create_test_config_file(self.test_config, 'django', 'database')
        self.assertEqual_config_data(self.test_config)

    def test_valid_config_file_data_with_spaces(self):
        """Tests valid configuration file if data contains spaces."""
        create_test_config_file(self.test_config, 'django', 'database')
        self.assertEqual_config_data(self.test_config)

    def test_no_config_file(self):
        """Tests case if configuration file not found."""
        self.assertEqual_config_data(self.default_settings)

    def test_invalid_config_file_no_section(self):
        """Tests invalid configuration file, required section not found."""
        create_test_config_file(self.test_config, 'django', None)
        self.assertEqual_config_data(self.default_settings)

    def test_invalid_config_file_invalid_section(self):
        """Tests invalid configuration file, unexpected section is given."""
        create_test_config_file(self.test_config, 'section 1', 'wrong section')
        self.assertEqual_config_data(self.default_settings)

    def test_invalid_config_file_no_data(self):
        """Tests invalid configuration file, required data not found."""
        create_test_config_file_without_data('django', 'database')
        self.assertEqual_config_data(self.default_settings)

    def test_invalid_config_file_password_isspace(self):
        """Tests invalid configuration file, django password contains only spaces."""
        self.test_config['password'] = '  '
        create_test_config_file(self.test_config, 'django', 'database')
        self.assertEqual_config_data(self.default_settings)

    def test_invalid_config_file_db_name_isspace(self):
        """Tests invalid configuration file, database name contains only spaces."""
        self.test_config['name'] = '  '
        create_test_config_file(self.test_config, 'django', 'database')
        self.assertEqual_config_data(self.default_settings)

    def test_invalid_config_file_db_collection_isspace(self):
        """Tests invalid configuration file, database collection contains only spaces."""
        self.test_config['collection'] = '  '
        create_test_config_file(self.test_config, 'django', 'database')
        self.assertEqual_config_data(self.default_settings)

    def test_invalid_config_file_invalid_db_host(self):
        """Tests invalid configuration file, database host is invalid."""
        self.test_config['host'] = 'URI://127.0.0.1:0000'
        create_test_config_file(self.test_config, 'django', 'database')
        self.assertEqual_config_data(self.default_settings)

    def test_invalid_config_file_unexpected_data(self):
        """Tests invalid configuration file, unexpected data is given."""
        test_config_data = """
        django password: 6542348
        database name: default
        collection: None
        host: None"""
        create_file(test_config_data)
        self.assertEqual_config_data(self.default_settings)

    def test_invalid_config_file_empty_file(self):
        """Tests empty configuration file."""
        create_file()
        self.assertEqual_config_data(self.default_settings)


def create_test_config_file(input_data: dict, django_section: str, database_section: str or None):
    """Creates test configuration file with given data."""
    test_config = ConfigParser()
    if django_section:
        test_config[django_section] = {'password': input_data['password']}
    if database_section:
        test_config[database_section] = {}
        database_settings = test_config[database_section]
        database_settings['name'] = input_data['name']
        database_settings['collection'] = input_data['collection']
        database_settings['host'] = input_data['host']
    with open(TEST_CONFIG_FILE, 'w') as configfile:
        test_config.write(configfile)


def create_test_config_file_without_data(django_section: str, database_section: str):
    """Creates test file with only sections without any data."""
    test_config = ConfigParser()
    test_config[django_section] = {}
    test_config[database_section] = {}
    with open(TEST_CONFIG_FILE, 'w') as configfile:
        test_config.write(configfile)


def create_file(file_data: str = ''):
    """Creates file with given data, default is empty file."""
    with open(TEST_CONFIG_FILE, 'w') as configfile:
        configfile.write(file_data)
