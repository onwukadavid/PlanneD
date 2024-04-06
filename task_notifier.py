from plyer import notification

def send_notification(title, message):
    notification_title = title 
    notification_message = message 
    
    notification.notify(  
        title = notification_title,  
        message = notification_message,  
        app_icon = None,  
        timeout = 10,  
        toast = True,
        )
    




































# @pass_file(file='tasks_details')
# def list_tasks(task_file=None):
#     """Lists all the tasks in the database."""
#     # task_file = shelve.open('tasks')
#     if not task_file.keys():
#         logger.info('No Tasks Found.')
#         sys.exit('No Tasks Found.')
#     for k, v in task_file.items():
#         pprint.pprint(f'{k}: {v}')
#     # task_file.close()


# @pass_file(file='tasks_details')
# def delete_all_tasks(task_file=None):
#     """Delete all tasks."""
#     task_obj_file = shelve.open('tasks')
#     logger.info('Deleting all tasks...')
#     print('Are you sure you want to delete all tasks?\
#           \n(Enter "yes" to proceed, Press any key to cancel operation.)')
#     response = input().lower()
#     if not response.startswith('y'):
#         logger.info('Operation cancelled.')
#         sys.exit('Operation cancelled.')
        
#     task_file.clear()
#     task_obj_file.clear()
#     task_obj_file.close()
#     logger.info('All tasks deleted.')
#     sys.exit('\nAll tasks deleted.\n')


# def open_task(apps):
#     """Open the apps for a specific task"""
#     app_process = []
#     for app in apps:
#         print(f'Opening {app}')
#         task_process = subprocess.Popen(app.strip())
#         app_process.append(task_process)     
#     return app_process
    

# def close_task(task_processes):
#     """Close the apps for a task"""
#     for task_process in task_processes:
#         os.kill(task_process.pid, signal.SIGTERM)
    

# @pass_file(file='tasks_details')
# def delete_task(task_name, task_file=None):
#     """Delete a particular task."""
#     task_obj_file = shelve.open('tasks')
#     try:
#         task_file.pop(task_name)
#         task_obj_file.pop(task_name)
#     except KeyError:
#         raise Exception(f'task "{task_name}" does not exist.')
#     finally:
#         task_obj_file.close()
#     logger.info(f'task "{task_name}" deleted.')
#     list_tasks()
#     sys.exit(f'task "{task_name}" deleted.')