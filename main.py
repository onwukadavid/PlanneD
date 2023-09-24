#! python3
# planned.py - A time and habit or task scheduler that primes your software environment for increased_productivity.

USAGE = '''
    Usage:  python main.py save <task_name>           - save a particular tasks to the storage. task_name must be one word.
            python main.py update <task_name> <key>   - update a particular task.
            python main.py list                       - list all tasks.
            python main.py delete                     - delete all tasks.
            python main.py delete_task <task_name>    - delete a particular task.
'''
import sys
import file_log
import features
import shelve

logger = file_log.get_logger(__name__)

#TODO: find out if updating while running or stopped is better. Pick either of them.
'''TODO: make changes if necessary to the delete_task, delete and list statements with respect
        to the task class if necessary'''
def main():
    try:
        if (len(sys.argv) < 2) or (len(sys.argv) > 4):
            sys.exit(USAGE)

        if len(sys.argv) == 4:
            if sys.argv[1] == 'update':
                '''get task object and update the necessary details.'''
                task_name = sys.argv[2]
                key = sys.argv[3]
                with shelve.open('tasks') as tasks:
                    task = tasks[task_name]
                task.update_task(key=key)
                features.list_tasks()
            print(f'Task "{task_name}" updated successfully.')
            sys.exit()

        if len(sys.argv) == 3:
            if sys.argv[1] == 'save':
                start_time = input('Enter start time (24hours) e.g 00:00: ')
                end_time = input('Enter end time (24hours) e.g 00:00: ')
                apps = input('Enter applications to open: ')
                task_name = sys.argv[2].strip()
                task = features.Task(task_name)
                task.save_task(start_time_string=start_time, end_time_string=end_time, apps=apps)
                with shelve.open('tasks') as tasks:
                    tasks[task_name] = task
                print('Task saved successfully.')
                sys.exit()
            
            if sys.argv[1] == 'delete_task':
                task_name = sys.argv[2]
                features.delete_task(task_name=task_name)
        
        if len(sys.argv) == 2:
            if sys.argv[1] == 'list':
                features.list_tasks()
            
            if sys.argv[1] == 'delete':
                features.delete_all_tasks()
    except KeyboardInterrupt:
        print("Operation cancelled.") 
        logger.error("Operation cancelled.") 
    except Exception as e:
        logger.error(e, exc_info=True)
        print(e)


if __name__ == '__main__':
    main()