import file_log
import sys
import pprint
import shelve
from abc import abstractmethod, ABC
from utils import pass_file, is_correct_time, split_apps, edit_task_key
# from typing import TYPE_CHECKING

# if TYPE_CHECKING:
#     from .features import Task
'''TODO: Task class shouldn't have any storage since they all share the same storage object'''
logger = file_log.get_logger(__name__)

class TaskStorage(ABC):

    @abstractmethod
    def save_task(self, task): # can't type hint task task: Task because of circular import 
        pass

    def list_task(self):
        pass

    def delete_all_tasks(self):
        pass

    def update_task(self, task):
        pass

# TODO: Pass task object to storage methods
class ShelveStorage(TaskStorage):
    @pass_file(file='tasks_details')
    def save_task(self, task, task_file=None):
        # tasks_file = shelve.open('tasks')
        try:
            task_file[task.task_name] = {
                'start_time':task.start_time,
                'end_time':task.end_time,
                'apps':task.task_apps
            }
            # task_file.close()
            logger.info(f'Task {task.task_name} saved successfully.')
            print(f'Task {task.task_name} saved successfully.')
        except Exception as e:
            raise ValueError(e)
        

    @pass_file(file='tasks_details')
    def list_tasks(self, task_file=None):
        """Lists all the tasks in the database."""
        # task_file = shelve.open('tasks')
        if not task_file.keys():
            logger.info('No Tasks Found.')
            sys.exit('No Tasks Found.')
        for k, v in task_file.items():
            pprint.pprint(f'{k}: {v}')

    
    @pass_file(file='tasks_details')
    def delete_all_tasks(self, task_file=None):
        """Delete all tasks."""
        task_obj_file = shelve.open('tasks')
        logger.info('Deleting all tasks...')
        print('Are you sure you want to delete all tasks?\
            \n(Enter "yes" to proceed, Press any key to cancel operation.)')
        response = input().lower()
        if not response.startswith('y'):
            logger.info('Operation cancelled.')
            sys.exit('Operation cancelled.')
            
        task_file.clear()
        task_obj_file.clear()
        task_obj_file.close()
        logger.info('All tasks deleted.')
        sys.exit('\nAll tasks deleted.\n')


    @pass_file(file='tasks_details')
    def update_task(self, task, task_file=None):
        """Update the value of a particular task."""
        # task_file = shelve.open('tasks')
        key: str = input('Enter Key: ')
        try:
            print(f"What do you want to update for {key}? \n apps \n start time")
            value = input(f'Enter choice: ')

            if key == 'apps':
                app_value = split_apps(value)
                task_file[task.task_name]['apps'] = task_file[task.task_name][key] + app_value
            else:
                time_value = is_correct_time(value.strip())
                task_to_update = task_file.get(task.task_name, {})
                if key == 'start time':
                    end_time = task_file[task.task_name]['end_time']
                    if time_value > end_time:
                        raise ValueError('Start time must be before end time.')
                    
                elif key == 'end time':
                    start_time = task_file[task.task_name]['start_time']
                    if time_value < start_time:
                        raise ValueError('End time must be before start time.')
                    
                task_to_update[key] = time_value
                task_file[task.task_name] = task_to_update

            task_file.sync()
            logger.info(f'Task "{task.task_name}" updated successfully.')
            print(f'Task "{task.task_name}" updated successfully.')
        except KeyError:
            raise Exception(f"An error occurred while updating task. Please check the spelling of your task name or it's keys.")
        except ValueError as e:
            raise Exception(f'An error occurred while updating task: {e}')
 