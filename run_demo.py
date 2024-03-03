from multiprocessing import Process
from os import chdir as os_chdir
from os import environ
from os import system as os_system
from os.path import join as os_path_join
from pathlib import Path
from time import sleep
from webbrowser import open_new_tab as open_url

from django.core.management.utils import get_random_secret_key

SCRIPT_DIR = Path(__file__).resolve().parent
PYNOTES_DIR = os_path_join(SCRIPT_DIR, 'WebPyNotes')
GRAPHQL_API_DIR = os_path_join(SCRIPT_DIR, 'PyNotes_GraphQL')
DATABASE_API_DIR = os_path_join(SCRIPT_DIR, 'PyNotes_Database')


def set_demo_env_var():
    """Sets Environment variables for demo run of the application."""
    environ['WEBPYNOTES_DJANGO_SECRET_KEY'] = get_random_secret_key()
    environ['WEBPYNOTES_DATABASE_NAME'] = 'web_py_notes'
    environ['WEBPYNOTES_COLLECTION_NAME'] = 'default_user'
    environ['WEBPYNOTES_DATABASE_HOST'] = 'mongodb://127.0.0.1:27017'


def start_container():
    """Starts docker container with demo MongoDB."""
    command = 'docker container start py_notes_project'
    os_system(command)


def run_graphql_server():
    """Runs the PyNotes GraphQl API server."""
    os_chdir(GRAPHQL_API_DIR)
    command = 'python3 main.py'
    os_system(command)


def run_app_server():
    """Runs the WebPyNotes application."""
    os_chdir(PYNOTES_DIR)
    command = 'python3 manage.py runserver'
    os_system(command)


def run_database_server():
    """Runs PyNotes Database API server."""
    os_chdir(DATABASE_API_DIR)
    command = 'python3 database_api.py'
    os_system(command)


if __name__ == '__main__':
    set_demo_env_var()
    project_container = Process(target=start_container)
    graphql_server = Process(target=run_graphql_server)
    database_server = Process(target=run_database_server)
    app_server = Process(target=run_app_server)

    # TODO: ERROR
    # Address already in use
    # Port 5000 is in use by another program.
    os_system('kill $(lsof -i:5000 -t)')
    os_system('kill $(lsof -i:30000 -t)')

    project_container.start()
    database_server.start()
    graphql_server.start()
    app_server.start()
    sleep(1)
    open_url('http://127.0.0.1:8000/webnotes/')
    # TODO: stop all processes.
    project_container.join()
    graphql_server.join()
    database_server.join()
    app_server.join()
