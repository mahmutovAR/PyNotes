from multiprocessing import Process
from os import chdir as os_chdir
from os import system as os_system
from os.path import join as os_path_join
from pathlib import Path
from time import sleep

from run_demo import set_demo_env_var

SCRIPT_DIR = Path(__file__).resolve().parent

PYNOTES_DIR = os_path_join(SCRIPT_DIR, 'WebPyNotes')
GRAPHQL_API_DIR = os_path_join(SCRIPT_DIR, 'PyNotes_GraphQL')
DATABASE_API_DIR = os_path_join(SCRIPT_DIR, 'PyNotes_Database')


def run_app_tests():
    """Runs WebPyNotes tests."""
    os_chdir(PYNOTES_DIR)
    command = 'python3 manage.py test --verbosity 2'
    os_system(command)


def run_graphql_server():
    """Runs the PyNotes GraphQl API server."""
    os_chdir(GRAPHQL_API_DIR)
    command = 'python3 main.py'
    os_system(command)


def run_database_server():
    """Runs PyNotes Database API server."""
    os_chdir(DATABASE_API_DIR)
    command = 'python3 database_api.py test'
    os_system(command)


if __name__ == '__main__':
    set_demo_env_var()
    graphql_server = Process(target=run_graphql_server)
    database_server = Process(target=run_database_server)
    app_tests = Process(target=run_app_tests)

    # TODO: ERROR
    # Address already in use
    # Port 5000 is in use by another program.
    os_system('kill $(lsof -i:5000 -t)')
    os_system('kill $(lsof -i:30000 -t)')

    database_server.start()
    graphql_server.start()
    sleep(1)
    app_tests.start()
    app_tests.join()
    app_tests.terminate()
    graphql_server.terminate()
    database_server.terminate()
