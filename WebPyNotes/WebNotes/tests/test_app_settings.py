from unittest import TestCase
from os import environ

from WebNotes_settings import EnvVarError, get_env_var


class AppConfigTest(TestCase):
    """Tests parsing of the configuration data from environment variables."""
    def setUp(self) -> None:
        environ.clear()
        self.env_var_django_secret_key = 'WEBPYNOTES_DJANGO_SECRET_KEY'
        self.env_var_database_name = 'WEBPYNOTES_DATABASE_NAME'
        self.env_var_database_collection = 'WEBPYNOTES_COLLECTION_NAME'
        self.env_var_database_host = 'WEBPYNOTES_DATABASE_HOST'

        self.valid_data = 'user value of Env Var'
        self.invalid_data = '  '
        self.valid_host_1 = 'mongodb://127.0.0.1'
        self.valid_host_2 = 'mongodb+srv://127.0.0.1'
        self.invalid_host = 'errorDB//127.0.0.27:5000'

    def tearDown(self) -> None:
        environ.clear()

    def test_no_env_var(self):
        """Tests raising of the EnvVarError if environment variable is not set."""
        with self.assertRaises(EnvVarError):
            get_env_var(self.env_var_django_secret_key)
        with self.assertRaises(EnvVarError):
            get_env_var(self.env_var_database_name)
        with self.assertRaises(EnvVarError):
            get_env_var(self.env_var_database_collection)
        with self.assertRaises(EnvVarError):
            get_env_var(self.env_var_database_host)

    def test_valid_env_var(self):
        """Tests validation of environment variable value."""
        environ[self.env_var_django_secret_key] = self.valid_data
        get_env_var(self.env_var_django_secret_key)

        environ[self.env_var_database_name] = self.valid_data
        get_env_var(self.env_var_database_name)

        environ[self.env_var_database_collection] = self.valid_data
        get_env_var(self.env_var_database_collection)

        environ[self.env_var_database_host] = self.valid_host_1
        get_env_var(self.env_var_database_host)

        environ[self.env_var_database_host] = self.valid_host_2
        get_env_var(self.env_var_database_host)
        
    def test_invalid_env_var(self):
        """Tests raising of the EnvVarError if environment variable value is not valid."""
        environ[self.env_var_django_secret_key] = self.invalid_data
        with self.assertRaises(EnvVarError):
            get_env_var(self.env_var_django_secret_key)

        environ[self.env_var_database_name] = self.invalid_data
        with self.assertRaises(EnvVarError):
            get_env_var(self.env_var_database_name)

        environ[self.env_var_database_collection] = self.invalid_data
        with self.assertRaises(EnvVarError):
            get_env_var(self.env_var_database_collection)

        environ[self.env_var_database_host] = self.invalid_data
        with self.assertRaises(EnvVarError):
            get_env_var(self.env_var_database_host)

        environ[self.env_var_database_host] = self.invalid_host
        with self.assertRaises(EnvVarError):
            get_env_var(self.env_var_database_host)
