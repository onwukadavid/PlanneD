#!python3

import shelve
import datetime
import time
import file_log
import features
import sys
from utils import pass_file


logger = file_log.get_logger(__name__)

'''
TODO: rather than going through each task checking the time assign a time to all task
      and run it when the time reaches. FIX:  USE Classes and data structures(heap, queue, ordereddicts())
'''
'''TODO: make changes if necessary to the run_task.py file with respect to the task class if necessary'''

def get_current_time():
    time_obj = datetime.datetime.now()
    time_str = time_obj.strftime('%H:%M')
    new_time_obj = datetime.datetime.strptime(time_str, '%H:%M')
    logger.debug(f'Current time: {new_time_obj.time()}')
    return new_time_obj.time()

@pass_file('task_scheduler') #task_scheduler file store the time of all task
def run_task(task_file=None):
    currently_running_task = ''
    while True:
        logger.debug(f'{features.list_tasks()}')
        year = datetime.datetime.today().year
        month = datetime.datetime.today().month
        day = datetime.datetime.today().day
        
        # task_file = shelve.open('tasks')
        logger.debug(list(task_file.keys()))
        if task_file.keys() is None:
            logger.debug("There's no task to run. Please create a task.")
            sys.exit("There's no task to run. Please create a task.")
        
        for task_name in task_file.keys():
            start_time = task_file[task_name]['start_time']
            end_time = task_file[task_name]['end_time']
            start_time_obj = datetime.datetime(year=year, month=month, day=day, hour=start_time.hour, minute=start_time.minute)
            five_minutes = start_time_obj - datetime.timedelta(minutes=5)
            logger.debug(f'Start time: {start_time_obj}')
            logger.debug(f'Five minutes time: {five_minutes}')

            assert isinstance(start_time, datetime.time), f'start_time must be of datetime obj and not of {type(start_time)}'
            assert isinstance(end_time, datetime.time), f'end_time must be of datetime obj and not of {type(end_time)}'

            if get_current_time() == five_minutes.time():
                print(f'{task_name} begins in 5 minutes. Please save all opened documents.')
                logger.info(f'{task_name} begins in 5 minutes. Please save all opened documents.')
                time.sleep(60)

            current_time = get_current_time()
            if current_time != start_time:
                print('Sleeping...')
                time.sleep(5)
                continue

            currently_running_task = task_name
            end_time_obj = datetime.datetime(year=year, month=month, day=day, hour=end_time.hour, minute=end_time.minute)
            apps = task_file[task_name]['apps']
            wait_time = end_time_obj - start_time_obj
            print(f'Running {currently_running_task}')
            logger.info(f'Running {currently_running_task}')

            # Run the apps
            task_id = features.open_task(apps)
            time.sleep(wait_time.total_seconds())
            
            # Close task when end time reaches.
            features.close_task(task_id)


if __name__ == '__main__':
    run_task()