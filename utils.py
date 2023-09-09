import re
import shelve
import datetime
import file_log

logger = file_log.get_logger(__name__)

def file_decorator(func):
    def wrapper(*args, **kwargs):
        with shelve.open('tasks_details') as task:
            func(*args, **kwargs, task_file=task)
    return wrapper

def is_correct_time(time_string):
    time_regex = re.compile(r'([01]\d|2[0-3]):[0-5]\d')
    if re.fullmatch(time_regex, time_string) is None:
        raise ValueError(f'{time_string} is not a proper time format.')
    time = datetime.datetime.strptime(time_string, '%H:%M').time()
    return time

def split_apps(app_file):
    app_file_regex = re.compile(r'.+?\.exe')
    app_file_match = re.findall(app_file_regex, app_file)
    logger.debug(app_file_match)
    if (app_file_match is None):
        raise ValueError('Please enter a proper application file path.')
    return app_file_match