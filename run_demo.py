from multiprocessing import Process
from os import chdir as os_chdir
from os import environ
from os import system as os_system
from os.path import join as os_path_join
from pathlib import Path

from django.core.management.utils import get_random_secret_key

SCRIPT_DIR = Path(__file__).resolve().parent
RUNSERVER_DIR = os_path_join(SCRIPT_DIR, 'WebPyNotes')
REST_DIR = os_path_join(SCRIPT_DIR, 'WebNotes_API')


def set_env_var():
    """Sets Environment variables for demo run of the application."""
    environ['WEBPYNOTES_DJANGO_SECRET_KEY'] = get_random_secret_key()
    environ['WEBPYNOTES_DATABASE_NAME'] = 'web_py_notes'
    environ['WEBPYNOTES_COLLECTION_NAME'] = 'default_user'
    environ['WEBPYNOTES_DATABASE_HOST'] = 'mongodb://127.0.0.1:27017'


def start_container():
    """Starts docker container with demo MongoDB."""
    command = 'docker container start py_notes_project'
    os_system(command)


def app_runserver():
    """Runs the WebPyNotes application."""
    os_chdir(RUNSERVER_DIR)
    command = 'python manage.py runserver'
    os_system(command)


def run_api():
    """Runs API microservice."""
    os_chdir(REST_DIR)
    command = 'python3 pynotes_api.py'
    os_system(command)


if __name__ == '__main__':
    set_env_var()
    start_container_process = Process(target=start_container)
    run_api_process = Process(target=run_api)
    app_runserver_process = Process(target=app_runserver)

    # TODO: ERROR
    # Address already in use
    # Port 5000 is in use by another program.
    os_system('kill $(lsof -i:5000 -t)')

    start_container_process.start()
    run_api_process.start()
    app_runserver_process.start()
    # TODO: how stop all processes?
    start_container_process.join()
    run_api_process.join()
    app_runserver_process.join()
