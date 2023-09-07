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

logger = file_log.get_logger(__name__)

#TODO: find out if updating while running or stopped is better. Pick either of them.
def main():
    try:
        if (len(sys.argv) < 2) or (len(sys.argv) > 4):
            sys.exit(USAGE)

        if len(sys.argv) == 4:
            if sys.argv[1] == 'update':
                task_name = sys.argv[2]
                key = sys.argv[3]
                features.update_task(task_name = task_name, key=key)
                features.list_tasks()

        if len(sys.argv) == 3:
            if sys.argv[1] == 'save':
                start_time = input('Enter start time (24hours) e.g 00:00: ')
                end_time = input('Enter end time (24hours) e.g 00:00: ')
                apps = input('Enter applications to open: ')
                features.save_task(task_name=sys.argv[2].strip(), start_time_string=start_time, end_time_string=end_time, apps=apps)
                features.list_tasks()
            
            if sys.argv[1] == 'delete_task':
                task_name = sys.argv[2]
                features.delete_task(task_name=task_name)
        
        if len(sys.argv) == 2:
            if sys.argv[1] == 'list':
                features.list_tasks()
            
            if sys.argv[1] == 'delete':
                features.delete_all_tasks()
    except Exception as e:
        logger.error(e, exc_info=True)
        print(e)


if __name__ == '__main__':
    main()