#!python3

import shelve
import datetime
import time
import file_log
import models.features as features
import sys
import threading
from utils import pass_file, get_current_time
# from task_notifier import send_notification


logger = file_log.get_logger(__name__)

'''TODO: Task class shouldn't have any storage since they all share the same storage object'''

'''
TODO: rather than going through each task checking the time assign a time to all task
      and run it when the time reaches. FIX:  USE Classes and data structures(heap, queue, ordereddicts())
'''
'''TODO: make changes if necessary to the run_task.py file with respect to the task class if necessary'''

def task_app_handler(apps, wait_time, task_name):
    print(threading.current_thread())
    task_to_run_apps = features.open_task(apps)
    print(task_to_run_apps)
    print(f'Sleeping for {wait_time.seconds}s')
    time.sleep(wait_time.seconds)

    logger.info(f'Closing task {task_name}')
    print(f'Closing task {task_name}')
    #TODO: fix task not closing issue. DONE
    features.close_task(task_to_run_apps)

@pass_file(file='tasks') # task_scheduler file store the time of all task
def run_task(task_file=None):
    #TODO: How should newly added task be treated when program is running.
    tasks = sorted(task_file.keys())
    while True:
        storage = features.Task.storage
        logger.debug(f'{storage.list_tasks()}')
        year = datetime.datetime.today().year
        month = datetime.datetime.today().month
        day = datetime.datetime.today().day
        
        # task_file = shelve.open('tasks')
        # logger.debug(list(task_file.keys()))
        if task_file.keys() is None:
            logger.debug("There's no task to run. Please create a task.")
            sys.exit("There's no task to run. Please create a task.")

        print(tasks)

        if not tasks:
            sys.exit('All tasks done for the day')

        finished_tasks = []
        task_to_run = task_file[tasks[0]]

        with shelve.open('tasks_details') as task_d_file:
            task = task_to_run.task_name
            start_time = task_d_file[task]['start_time']
            end_time = task_d_file[task]['end_time']
            start_time_obj = datetime.datetime(year=year, month=month, day=day, hour=start_time.hour, minute=start_time.minute)
            end_time_obj = datetime.datetime(year=year, month=month, day=day, hour=end_time.hour, minute=end_time.minute)
            wait_time = end_time_obj - start_time_obj
            apps = task_d_file[task]['apps']
            five_minutes = start_time_obj - datetime.timedelta(minutes=5) 
            current_time = get_current_time()
            
            if len(tasks) > 1:          
                next_task_to_run = task_file[tasks[1]]
                next_task = next_task_to_run.task_name
                next_task_start_time = task_d_file[next_task_to_run.task_name]['start_time']
                next_task_start_time_obj = datetime.datetime(year=year, month=month, day=day, hour=next_task_start_time.hour, minute=next_task_start_time.minute)
                five_minutes_for_next_task = next_task_start_time_obj - datetime.timedelta(minutes=5)

        #TODO: remove task when finished or set start_time < current_time to be skipped. DONE
        if start_time < current_time:
            print('Task time has passed')
            finished_tasks.append(tasks.pop(task_to_run.index()))
            continue
        
        current_time_obj = datetime.datetime(year=year, month=month, day=day, hour=current_time.hour, minute=current_time.minute)
        if five_minutes.time() > current_time:
            time_to_wait = start_time_obj - current_time_obj - datetime.timedelta(minutes=5)
            print(f'Waiting for {time_to_wait.seconds}sec')
            time.sleep(time_to_wait.seconds)

            title = "PlanneD manager"
            message = f'''Your task "{task}" begins in 5 minutes.\n
                    Please save all unsaved documents.
                    '''
            
            # send_notification(title=title, message=message)
            logger.info('5 minutes notification sent.')
            time.sleep(60*5)
        else:
            time_to_wait = start_time_obj - current_time_obj
            print(f'Waiting for {time_to_wait.seconds}s')
            time.sleep(time_to_wait.seconds)

        logger.info(f'Running task {task_to_run}')
        print(f'Running task {task_to_run}')

        '''TODO: Ensure the main thread continues in a loop up until this point.''' #DONE
        thread = threading.Thread(target=task_app_handler, args=(apps, wait_time, task))
        thread.start()

        if len(tasks) > 1:
            while True:
                ct = get_current_time()
                # ct_obj = datetime.datetime(year=year, month=month, day=day, hour=ct.hour, minute=ct.minute)
                if ct == five_minutes_for_next_task.time():
                    title = "PlanneD manager"
                    message = f'''Your task "{next_task}" begins in 5 minutes.\n
                        Please save all unsaved documents.
                        '''
                    # send_notification(title=title, message=message)
                    logger.info('5 minutes notification sent.')
                    # add a sleeper here to avoid wasting resources.
                    # time.sleep(60)
                    break
        thread.join()
        print('Task finished')
        finished_tasks.append(tasks.pop(0))            


if __name__ == '__main__':
    run_task()