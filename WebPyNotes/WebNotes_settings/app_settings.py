from os import environ


class ConfigData:
    """Class with main application settings.
    Django's settings include the secret key.
    Database settings include the name, collection name, host."""
    __slots__ = ['__django_secret_key',
                 '__database_name', '__database_collection',
                 '__database_client_host']

    def __init__(self, django_secret_key: str, database_name: str,
                 database_collection: str, database_host: str):

        self.__django_secret_key = django_secret_key
        self.__database_name = database_name
        self.__database_collection = database_collection
        self.__database_client_host = database_host

    def get_django_secret_key(self) -> str:
        """Returns the django secret key."""
        return self.__django_secret_key

    def get_database_name(self) -> str:
        """Returns the database name."""
        return self.__database_name

    def get_database_collection(self) -> str:
        """Returns the collection name."""
        return self.__database_collection

    def get_database_client_host(self) -> str:
        """Returns the database client host."""
        return self.__database_client_host


class EnvVarError(Exception):
    """Error class, is raised if required settings are not set."""
    __slots__ = ['__invalid_data']

    def __init__(self, invalid_data):
        self.__invalid_data = invalid_data

    def __str__(self):
        return f'Error! Environment variable does not exist or is invalid: {self.__invalid_data}'


def get_app_settings() -> 'ConfigData object':
    """Returns main application settings obtained from environment variables."""
    django_secret_key = get_env_var('WEBPYNOTES_DJANGO_SECRET_KEY')
    database_host = get_env_var('WEBPYNOTES_DATABASE_HOST')
    database_name = get_env_var('WEBPYNOTES_DATABASE_NAME')
    collection_name = get_env_var('WEBPYNOTES_COLLECTION_NAME')

    config_parameters = {'django_secret_key': django_secret_key,
                         'database_name': database_name,
                         'database_collection': collection_name,
                         'database_host': database_host}

    return ConfigData(**config_parameters)


def get_env_var(var_name: str) -> str:
    """Returns value of the environment variable if it is valid,
    otherwise the EnvVarError is raised."""
    try:
        var_value = environ[var_name]
    except KeyError:
        raise EnvVarError(var_name)
    else:
        if not var_value or var_value.isspace():
            raise EnvVarError(var_name)
        if var_name == 'WEBPYNOTES_DATABASE_HOST' and \
                not (var_value.startswith('mongodb://') or var_value.startswith('mongodb+srv://')):
            raise EnvVarError(var_value)
        return var_value


NotesConfig = get_app_settings()
