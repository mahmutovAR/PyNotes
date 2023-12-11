from multiprocessing import Process
from os import chdir as os_chdir
from os import system as os_system
from os.path import join as os_path_join
from pathlib import Path
from run_demo import set_env_var
from time import sleep


SCRIPT_DIR = Path(__file__).resolve().parent
RUNSERVER_DIR = os_path_join(SCRIPT_DIR, 'WebPyNotes')
REST_DIR = os_path_join(SCRIPT_DIR, 'WebNotes_API')


def app_tests():
    """Runs WebPyNotes tests."""
    os_chdir(RUNSERVER_DIR)
    command = 'python3 manage.py test --verbosity 2'
    os_system(command)


def run_api():
    """Runs API microservice."""
    os_chdir(REST_DIR)
    command = 'python3 pynotes_api.py test'
    os_system(command)


if __name__ == '__main__':
    set_env_var()
    run_api_process = Process(target=run_api)
    app_tests_process = Process(target=app_tests)

    # TODO: ERROR
    # Address already in use
    # Port 5000 is in use by another program.
    os_system('kill $(lsof -i:5000 -t)')

    run_api_process.start()
    sleep(1)
    app_tests_process.start()
    app_tests_process.join()
    run_api_process.terminate()
