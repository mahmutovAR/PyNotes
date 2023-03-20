from os.path import abspath, dirname, isdir, isfile, normpath, splitext
from pathlib import Path
from os.path import join as os_path_join
from configparser import ConfigParser
import sys


class ConfigData:
    __slots__ = ['__application_dir', '__templates_dir',
                 '__django_password', '__django_language', '__django_time_zone',
                 '__database_name', '__database_client_host', '__database_client_port',
                 '__database_client_username', '__database_client_password',
                 '__database_client_authSource', '__database_client_authMechanism']

    def __init__(self, django_pass: str, django_language: str, django_time_zone: str,
                 db_name: str, db_host: str, db_port: str,
                 db_username: str, db_password: str,
                 db_authSource: str, db_authMechanism: str):
        """Creates an object of the ConfigData class,
        assigns values to the main script parameters from a configuration file."""
        self.__application_dir = Path(__file__).resolve().parents[1]
        self.__templates_dir = os_path_join(self.__application_dir, 'templates', 'WebNotes')
        self.__django_password = django_pass
        self.__django_language = django_language
        self.__django_time_zone = django_time_zone
        self.__database_name = db_name
        self.__database_client_host = db_host
        self.__database_client_port = db_port
        self.__database_client_username = db_username
        self.__database_client_password = db_password
        self.__database_client_authSource = db_authSource
        self.__database_client_authMechanism = db_authMechanism

    def get_application_dir(self) -> Path:
        """Returns the data file format."""
        return self.__application_dir

    def get_django_password(self) -> str:
        """Returns the data file format."""
        # django_pass_file = os_path_join(self.__application_dir.parents[2], 'settings', 'django_pass.txt')
        # with open(django_pass_file) as pass_file:
        #     self.__django_password = pass_file.read().rstrip()
        return self.__django_password

    def get_django_language(self) -> str:
        """Returns the data file format."""
        return self.__django_language

    def get_django_time_zone(self) -> str:
        """Returns the data file format."""
        return self.__django_time_zone

    def get_templates_dir(self) -> str:
        """Returns the data file format."""
        return self.__templates_dir

    def get_database_name(self) -> str:
        """Returns the data file format."""
        return self.__database_name

    def get_database_client_host(self) -> str:
        """Returns the data file format."""
        return self.__database_client_host

    def get_database_client_port(self) -> str:
        """Returns the data file format."""
        return self.__database_client_port

    def get_database_client_username(self) -> str:
        """Returns the data file format."""
        return self.__database_client_username

    def get_database_client_password(self) -> str:
        """Returns the data file format."""
        return self.__database_client_password

    def get_database_client_authSource(self) -> str:
        """Returns the data file format."""
        return self.__database_client_authSource

    def get_database_client_authMechanism(self) -> str:
        """Returns the data file format."""
        return self.__database_client_authMechanism

    def verify_application_build(self) -> None:
        pass
    # authMechanism must be in ('SCRAM-SHA-256', 'GSSAPI', 'SCRAM-SHA-1', 'DEFAULT', 'MONGODB-X509', 'MONGODB-AWS', 'PLAIN', 'MONGODB-CR')
    # port must be int

    #     """Validates configuration data.
    #     The data file type, output file type, analysis mode,
    #     and math point value (only for 'AFFL' mode) are checked for correctness.
    #     The data file and output file directory are checked for existence.
    #     If the check fails, an appropriate exception will be raised."""

        # if self.__analysis_mode == 'AFFL':
    #         if not self.__input_point:
    #             raise ConfigFileParsingError('"point" in the section [general]')
    #         self.__input_point = float(self.__input_point)
    #     elif self.__analysis_mode == 'INTS':
    #         self.__input_point = None
    #     else:
    #         raise ConfigFileParsingError('"mode" in the section [general]')
    #
    #     if self.__data_format not in ('JSON', 'TXT', 'XML'):
    #         raise ConfigFileParsingError('"format" in the section [input]')
    #
    #     input_file_path, input_file_type = splitext(self.__data_file)
    #     if input_file_type and input_file_type[1:] != self.__data_format.lower():
    #         raise ConfigFileParsingError('"format" and "path" in the section [input]')
    #
    #     if not self.__data_file:
    #         raise ConfigFileParsingError('"path" in the section [input]')
    #     if not isfile(normpath(self.__data_file)):
    #         raise DataFileNotFoundError(self.__data_file)
    #
    #     if self.__output_file_format not in ('json', 'txt', 'xml'):
    #         raise ConfigFileParsingError('"format" in the section [output]')
    #
    #     if not self.__output_file_path:
    #         raise ConfigFileParsingError('"path" in the section [output]')
    #     output_dir = dirname(self.__output_file_path)
    #     if not isdir(normpath(output_dir)):
    #         raise OutputDirectoryNotFoundError(output_dir)
    #
    #     output_file_path, output_file_type = splitext(self.__output_file_path)
    #     if output_file_type and output_file_type[1:] != self.__output_file_format.lower():
    #         raise ConfigFileParsingError('"format" and "path" in the section [output]')


def parse_configuration_file() -> 'ConfigData object':
    """Checks for the presence of 'config.ini', if the file is not found ConfigFileNotFoundError will be raised.
    Validates the configuration data from the given configuration file.
    Returns ConfigData class object with the main configuration arguments."""
    config_file_path = os_path_join(Path(__file__).resolve().parents[2], 'config.ini')
    if not isfile(config_file_path):
        sys.exit('ConfigFileNotFoundError')
        # raise ConfigFileNotFoundError(config_file_path)
    try:
        data_from_config_ini = ConfigParser()
        data_from_config_ini.read(config_file_path)

        section_django = data_from_config_ini['django']
        section_database = data_from_config_ini['database']

        config_parameters = {'django_pass': section_django.get('password'),
                             'django_language': section_django.get('language'),
                             'django_time_zone': section_django.get('time_zone'),
                             'db_name': section_database.get('name'),
                             'db_host': section_database.get('host'),
                             'db_port': section_database.getint('port'),
                             'db_username': section_database.get('username'),
                             'db_password': section_database.get('password'),
                             'db_authSource': section_database.get('authSource'),
                             'db_authMechanism': section_database.get('authMechanism')}

    except KeyError as err:
        sys.exit(f'ConfigFileParsingError: section [{err}]')
        # raise ConfigFileParsingError(f'section [{err}]')
    except Exception:
        print(f'Error! The parsing of the configuration file raised an exception:')
        raise
    else:
        config_data = ConfigData(**config_parameters)
        config_data.verify_application_build()
    return config_data


# if __name__ == '__main__':
    # app_config = parse_configuration_file()
