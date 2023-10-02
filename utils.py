import re
import shelve
import datetime
import file_log

logger = file_log.get_logger(__name__)

def pass_file(_func=None, *, file='tasks_details'):
    def file_decorator(func):
        def wrapper(*args, **kwargs): #TODO: IF more than one file was passed
            with shelve.open(file) as task:
                func(*args, **kwargs, task_file=task)
        return wrapper
    
    if _func is None:
        return file_decorator
    else:
        return file_decorator(_func)

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

def edit_task_key(dic, old_key, new_key):
    if new_key in dic.keys():
        raise KeyError(f'Task name "{new_key}" already exists. Please enter another name.')
    try:
        dic[new_key] = dic.pop(old_key)
    except KeyError:
        raise KeyError(f'Task name "{old_key}" does not exist') from None
    
def get_current_time():
    time_obj = datetime.datetime.now()
    time_str = time_obj.strftime('%H:%M')
    new_time_obj = datetime.datetime.strptime(time_str, '%H:%M')
    # logger.debug(f'Current time: {new_time_obj.time()}')
    return new_time_obj.time()