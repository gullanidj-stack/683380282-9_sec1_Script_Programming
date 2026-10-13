import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.task_manager import TaskManager


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        os.remove(self.tmp.name)
        # absolute path: os.path.join ignores the base when the second part is absolute
        self.m = TaskManager(data_file=self.tmp.name)
        self.m.add_normal_task("Buy milk", tags=["home"])
        self.m.add_due_date_task("Write report", "2026-11-01", tags=["work"])
        self.m.add_priority_task("Fix bug", "High", tags=["work", "urgent"])

    def tearDown(self):
        if os.path.exists(self.tmp.name):
            os.remove(self.tmp.name)

    def test_search(self):
        self.assertEqual(len(self.m.search_tasks("WORK")), 2)
        self.assertEqual(len(self.m.search_tasks("milk")), 1)

    def test_filter_tags(self):
        self.assertEqual(len(self.m.filter_tasks(contains_tags=["work", "urgent"])), 1)

    def test_filter_priority(self):
        self.assertEqual(self.m.filter_tasks(priority_level="High")[0].description, "Fix bug")

    def test_sort_priority(self):
        self.assertEqual(self.m.sort_tasks("priority")[0].description, "Fix bug")

    def test_complete_and_delete(self):
        self.assertTrue(self.m.complete_task(1)[0])
        self.assertFalse(self.m.complete_task(1)[0])
        self.assertTrue(self.m.delete_task(2)[0])
        self.assertFalse(self.m.delete_task(99)[0])

    def test_invalid_input(self):
        self.assertIsNone(self.m.add_due_date_task("x", "not-a-date"))
        self.assertIsNone(self.m.add_priority_task("x", "Urgent"))

    def test_persistence(self):
        reloaded = TaskManager(data_file=self.tmp.name)
        self.assertEqual(len(reloaded.tasks), 3)


if __name__ == "__main__":
    unittest.main()
