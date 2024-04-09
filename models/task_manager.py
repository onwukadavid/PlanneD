import os
import signal
import subprocess


class TaskManager():
    def open_task(self, apps):
        """Open the apps for a specific task"""
        app_process = []
        for app in apps:
            print(f'Opening {app}')
            task_process = subprocess.Popen(app.strip())
            app_process.append(task_process)     
        return app_process
        

    def close_task(self, task_processes):
        """Close the apps for a task"""
        for task_process in task_processes:
            os.kill(task_process.pid, signal.SIGTERM)