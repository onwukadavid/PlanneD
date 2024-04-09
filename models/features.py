#!python3

import sys
import shelve
import datetime
import file_log
import pprint
import re
import os
from typing import List
# from models.task_storage import TaskStorage
from utils import pass_file, is_correct_time, split_apps, edit_task_key

logger = file_log.get_logger(__name__)
# file_log.disable_logger()

'''TODO: Task class shouldn't have any storage since they all share the same storage object'''
class Task():

    storage = None

    def __init__(self, task_name):
        """Initialize the object with a task_name attribute."""
        self.task_name: str = task_name
        self.start_time: str = None
        self.end_time: str = None
        self.task_apps: List[str] = None


    # @pass_file(file='tasks_details') # tasks_details file store the details of each task
    def save_task(self, start_time_string: str, end_time_string: str, apps: str) -> None:
        """Saves a new task."""
        # assert is_correct_time([start_time, end_time]) != False, 'Please enter the proper time format.'
        self.start_time = start_time_string
        self.end_time = end_time_string
        apps = apps
        try: 
            start_time = is_correct_time(self.start_time)
            end_time = is_correct_time(self.end_time)
            if start_time >= end_time:
                raise ValueError('Start time must be before end time.')
            
            self.task_apps = split_apps(apps)

            Task.storage.save_task(task=self)
            
            logger.info(f'Task {self.task_name} saved successfully.')
            print(f'Task {self.task_name} saved successfully.')
        except Exception as e:
                raise Exception(f'An error occurred while saving task: {e}')


    #TODO: REDO Update feature.
    # @pass_file(file='tasks_details')
    def update_task(self, key, task_file=None):
        """Update the value of a particular task."""
    #     # task_file = shelve.open('tasks')
        logger.info(f'Updating task "{self.task_name}"')
        print(f'Updating task "{self.task_name}"')
    
        try:
            Task.storage.update_task(task=self)
    #         value = input(f'Enter {key}: ')
    #         if key == 'apps':
    #             app_value = split_apps(value)
    #             task_file[self.task_name]['apps'] = task_file[self.task_name][key] + app_value
    #         else:
    #             time_value = is_correct_time(value.strip())
    #             task_update = task_file.get(self.task_name, {})
    #             if key == 'start_time':
    #                 end_time = task_file[self.task_name]['end_time']
    #                 if time_value > end_time:
    #                     raise ValueError('Start time must be before end time.')
    #             elif key == 'end_time':
    #                 start_time = task_file[self.task_name]['start_time']
    #                 if time_value < start_time:
    #                     raise ValueError('End time must be before start time.')
    #             task_update[key] = time_value
    #             task_file[self.task_name] = task_update
    #         task_file.sync()
    #         logger.info(f'Task "{self.task_name}" updated successfully.')
    #         print(f'Task "{self.task_name}" updated successfully.')
        except Exception as e:
            raise Exception(f'An error occurred while updating task: {e}')
        

    @pass_file(file='tasks_details')
    def edit_task_name(self, old_key, new_key, task_file=None):
        try:
            edit_task_key(task_file, old_key, new_key)
        except KeyError as e:
            raise Exception(f'An error occured while updating task name: {e}') from None
        

    # @pass_file(file='tasks_details')
    @classmethod
    def delete_task(cls, task_name):
        """Delete a particular task."""

        cls.storage.delete_task(task_name)

        # task_obj_file = shelve.open('tasks')
        # try:
        #     task_file.pop(task_name)
        #     task_obj_file.pop(task_name)
        # except KeyError:
        #     raise Exception(f'task "{task_name}" does not exist.')
        # finally:
        #     task_obj_file.close()
        # logger.info(f'task "{task_name}" deleted.')
        # self.list_tasks()
        # sys.exit(f'task "{task_name}" deleted.')


    @classmethod
    def list_tasks(cls): # implemented in task_storage
        """Lists all the tasks in the storage."""

        cls.storage.list_tasks()


    @classmethod
    def delete_all_tasks(cls, task_file=None): # implemented in task_storage
        """Delete all tasks."""

        cls.storage.delete_all_tasks()


    @property
    def task_name(self):
        return self._task_name
    
    @task_name.setter
    def task_name(self, value):
        self._task_name = value

    @task_name.deleter
    def task_name(self):
        del self._task_name

    def __repr__(self):
        """Returns a string of an expression that re-creates this object."""
        return f'{self.__class__.__qualname__}({self.task_name}, {self.start_time_string}, {self.end_time_string}, {self.apps})'
    
    def __str__(self):
        """Returns a human-readable string representation of this object."""
        return f'Task({self.task_name})'
    


       







    # def open_task(self, apps):
    #     """Open the apps for a specific task"""
    #     app_process = []
    #     for app in apps:
    #         print(f'Opening {app}')
    #         task_process = subprocess.Popen(app.strip())
    #         app_process.append(task_process)     
    #     return app_process
        

    # def close_task(self, task_processes):
    #     """Close the apps for a task"""
    #     for task_process in task_processes:
    #         os.kill(task_process.pid, signal.SIGTERM)