import unittest
import shelve
from ..models.features import Task
from ..models.task_storage import ShelveStorage


class TestTask(unittest.TestCase):
    
    def test_task_saves_to_shelve_storage(self):

        Task.storage = ShelveStorage()
        task = Task(task_name='Work')
        with shelve.open('task_details') as task_file:
            self.assertIn(task.task_name, task_file.keys())
            


if __name__ == '__main__':
    unittest.main()