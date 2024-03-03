from os import environ


class EnvVarError(Exception):
    """Error class, is raised if required settings are not set."""
    __slots__ = ['__invalid_data']

    def __init__(self, invalid_data):
        self.__invalid_data = invalid_data

    def __str__(self):
        return f'Error! Environment variable does not exist or is invalid: {self.__invalid_data}'


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
        return var_value


DATABASE_HOST = get_env_var('WEBPYNOTES_DATABASE_HOST')
DATABASE_NAME = get_env_var('WEBPYNOTES_DATABASE_NAME')
COLLECTION_NAME = get_env_var('WEBPYNOTES_COLLECTION_NAME')
DJANGO_SECRET_KEY = get_env_var('WEBPYNOTES_DJANGO_SECRET_KEY')
