#! python3
# planned.py - A time and habit or task scheduler that primes your software environment for increased_productivity.

USAGE = '''
    Usage:  python main.py save <task_name>           - save a particular tasks to the storage. task_name must be one word.
            python main.py update <task_name> <key>   - update a particular task.
            python main.py edit                       - edit a particular task name.
            python main.py list                       - list all tasks.
            python main.py delete                     - delete all tasks.
            python main.py delete_task <task_name>    - delete a particular task.
'''
import sys
import file_log
import shelve
import utils
from models.task_storage import ShelveStorage
# import models.features as features
from models.features import Task

logger = file_log.get_logger(__name__)

#TODO: find out if updating while running or stopped is better. Pick either of them.
'''TODO: make changes if necessary to the delete_task, delete and list statements with respect
        to the task class if necessary'''
def main():
    try:
        if (len(sys.argv) < 2) or (len(sys.argv) > 4):
            sys.exit(USAGE)


        Task.storage = ShelveStorage()

        #TODO: REDO Update feature.
        if len(sys.argv) == 4:
            if sys.argv[1] == 'update':
                '''get task object and update the necessary details.'''
                task_name = sys.argv[2]
                key = sys.argv[3]
                with shelve.open('tasks') as tasks:
                    task = tasks[task_name]
                task.update_task(key=key)
                Task.list_tasks()
            print(f'Task "{task_name}" updated successfully.')
            sys.exit()

        if len(sys.argv) == 3:
            if sys.argv[1] == 'save': # WORKS AS EXPECTED
                print('Saving new task...')
                logger.info('Saving new task...')
                start_time = input('Enter start time (24hours) e.g 00:00: ')
                end_time = input('Enter end time (24hours) e.g 00:00: ')
                apps = input('Enter applications to open: ')
                task_name = sys.argv[2].strip()

                task = Task(task_name)
                task.save_task(start_time_string=start_time, end_time_string=end_time, apps=apps)

                # key should be task object or task name, value should be start time
                with shelve.open('tasks') as tasks:
                    tasks[start_time] = task
                print('Task saved successfully.')
                sys.exit()
            
            # TODO: Decide if this uses a class method or the task object
            if sys.argv[1] == 'delete_task':
                task_name = sys.argv[2]
                Task.delete_task(task_name)
        
        if len(sys.argv) == 2:
            if sys.argv[1] == 'list': # WORKS AS EXPECTED
                Task.list_tasks()
            
            if sys.argv[1] == 'delete': # WORKS AS EXPECTED
                Task.delete_all_tasks()

            if sys.argv[1] == 'edit':
                with shelve.open('tasks') as tasks: # tasks file stores task objects
                    for task_name in tasks.keys():
                        print(task_name)

                    logger.info('Editing task name...')
                    old_key = input('Enter task name to edit: ')
                    task = tasks[task_name] # get task object
                    new_key = input('Enter new name: ')
                    utils.edit_task_key(tasks, old_key, new_key)
                    task.task_name = new_key
                    task.edit_task_name(old_key, new_key)
                    print(f'Task name "{old_key}" changed to "{new_key}"')
                    logger.info(f'Task name "{old_key}" changed to "{new_key}"')

    except KeyboardInterrupt:
        print("Operation cancelled.") 
        logger.error("Operation cancelled.") 
    except Exception as e:
        logger.error(e, exc_info=True)
        print(e)


if __name__ == '__main__':
    main()