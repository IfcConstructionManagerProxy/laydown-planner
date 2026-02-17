import unittest

from laydown_planner.scheduler import Scheduler

class TestScheduler(unittest.TestCase):

    def setUp(self):
        self.scheduler = Scheduler()  # Initialize Scheduler instance

    def test_add_task(self):
        self.scheduler.add_task('Task 1')
        self.assertIn('Task 1', self.scheduler.tasks)

    def test_remove_task(self):
        self.scheduler.add_task('Task to remove')
        self.scheduler.remove_task('Task to remove')
        self.assertNotIn('Task to remove', self.scheduler.tasks)

    def test_schedule_task(self):
        self.scheduler.add_task('Task 1')
        self.scheduler.schedule_task('Task 1', '2026-02-17 15:00:00')
        task = self.scheduler.get_task('Task 1')
        self.assertEqual(task['scheduled_time'], '2026-02-17 15:00:00')

    def test_complete_task(self):
        self.scheduler.add_task('Task 1')
        self.scheduler.complete_task('Task 1')
        self.assertTrue(self.scheduler.is_task_completed('Task 1'))

if __name__ == '__main__':
    unittest.main()