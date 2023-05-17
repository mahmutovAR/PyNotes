from configparser import ConfigParser
from os.path import isfile
from os.path import join as os_path_join
from pathlib import Path


DEFAULT_DJANGO_PASS = 'n2e7G@}7WVK6-st98$Z7=dSTtRi6@*{b_ZNJ6MK+bQ50wRVC)CN'
DEFAULT_DATABASE_NAME = 'web_py_notes'
DEFAULT_COLLECTION_NAME = 'default_user'
DEFAULT_DATABASE_HOST = 'mongodb://127.0.0.1:27017'


class ConfigData:
    """Class with main application settings.
    Django settings include the secret key, application language and time zone.
    Database settings include the name, collection name, host, port."""
    __slots__ = ['__application_dir', '__templates_dir',
                 '__django_password',
                 '__database_name', '__database_collection',
                 '__database_client_host']

    def __init__(self, django_pass: str, db_name: str, db_collection: str, db_host: str):

        self.__application_dir = Path(__file__).resolve().parents[1]
        self.__templates_dir = os_path_join(self.__application_dir, 'templates', 'WebNotes')
        self.__django_password = django_pass
        self.__database_name = db_name
        self.__database_collection = db_collection
        self.__database_client_host = db_host

    def get_application_dir(self) -> Path:
        """Returns the data file format."""
        return self.__application_dir

    def get_django_password(self) -> str:
        """Returns the data file format."""
        return self.__django_password

    def get_templates_dir(self) -> str:
        """Returns the data file format."""
        return self.__templates_dir

    def get_database_name(self) -> str:
        """Returns the data file format."""
        return self.__database_name

    def get_database_collection(self) -> str:
        """Returns the data file format."""
        return self.__database_collection

    def get_database_client_host(self) -> str:
        """Returns the data file format."""
        return self.__database_client_host


class DefaultConfigData(ConfigData):
    """Class with default application settings."""
    def __init__(self):
        super().__init__(DEFAULT_DJANGO_PASS, DEFAULT_DATABASE_NAME,
                         DEFAULT_COLLECTION_NAME, DEFAULT_DATABASE_HOST)


def get_config_settings(config_file_name: str = 'config.ini'):
    """Checks for the presence of 'config.ini',
    if the file is not found or data is invalid default settings will be used."""
    config_file_path = os_path_join(Path(__file__).resolve().parents[2], config_file_name)

    if isfile(config_file_path):
        app_configuration = parse_configuration_file(config_file_path)
    else:
        app_configuration = DefaultConfigData()
        display_default_settings()
    return app_configuration


def parse_configuration_file(file_path: str) -> 'ConfigData object':
    """Parses configuration file.
    Validates the configuration data from the given configuration file.
    Returns ConfigData class object with the main configuration arguments."""
    try:
        data_from_config_ini = ConfigParser()
        data_from_config_ini.read(file_path)
    except Exception as err:
        print(f'Attention! The parsing of the configuration file raised an exception:\n{err}')
        config_data = DefaultConfigData()
        display_default_settings()
    else:
        config_data = verify_config_settings(data_from_config_ini)

    return config_data


def verify_config_settings(config_file: 'ConfigParser object') -> 'ConfigData object':
    """Validates configuration data.
    If the check fails, default settings will be used."""
    try:
        section_django = config_file['django']
        section_database = config_file['database']
    except Exception as err:
        print(f'Attention! The parsing of the configuration file raised an exception:\n{err}')
        display_default_settings()
        return DefaultConfigData()
    else:
        django_pass = section_django.get('password')
        db_name = section_database.get('name')
        db_collection = section_database.get('collection')
        db_host = section_database.get('host')

        if not django_pass or django_pass.isspace():
            display_default_settings()
            return DefaultConfigData()
        if not db_name or db_name.isspace():
            display_default_settings()
            return DefaultConfigData()
        if not db_collection or db_collection.isspace():
            display_default_settings()
            return DefaultConfigData()
        if not (db_host.startswith('mongodb://') or db_host.startswith('mongodb+srv://')):
            # TODO: try to connect to a deployment?
            display_default_settings()
            return DefaultConfigData()

        db_name = clean_spaces(db_name)
        db_collection = clean_spaces(db_collection)

        config_parameters = {'django_pass': django_pass,
                             'db_name': db_name,
                             'db_collection': db_collection,
                             'db_host': db_host}

        return ConfigData(**config_parameters)


def clean_spaces(ini_data: str or None) -> str:
    """Removes escape characters from given string object."""
    if ini_data:
        ini_data = ini_data.replace('\r', '_')
        ini_data = ini_data.replace('\t', '_')
        ini_data = ini_data.replace('\f', '_')
        ini_data = ini_data.replace('\n', '_')
        ini_data = ini_data.replace(' ', '_')
    return ini_data


NotesConfig = get_config_settings()


def display_default_settings():
    """informs that default configuration setting are used."""
    print(f"Default settings will be used:\n"
          f"django secret key = '{NotesConfig.get_django_password()}'\n"
          f"database name = '{NotesConfig.get_database_name()}'\n"
          f"database collection = '{NotesConfig.get_database_collection()}'\n"
          f"database host = '{NotesConfig.get_database_client_host()}'")
