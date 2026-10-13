"""Business logic: add, list, complete, delete, search, filter, sort."""
import datetime
import logging

from .task import Task, DueDateTask, PriorityTask
from .data_persistence import DataPersistence

logger = logging.getLogger(__name__)


class TaskManager:
    PRIORITY_MAP = {"High": 1, "Medium": 2, "Low": 3}

    def __init__(self, data_file="data/tasks.json"):
        self.persistence = DataPersistence(data_file)
        self.tasks = self.persistence.load_tasks()
        self.next_id = self._get_next_task_id()

    def _get_next_task_id(self):
        return max((t.id for t in self.tasks), default=0) + 1

    def _save_changes(self):
        self.persistence.save_tasks(self.tasks)
        logger.info("Tasks saved to file.")

    # --- CRUD ---
    def _add(self, task):
        self.tasks.append(task)
        self.next_id += 1
        self._save_changes()
        return task

    def add_normal_task(self, description, tags=None):
        return self._add(Task(self.next_id, description, tags=tags))

    def add_due_date_task(self, description, due_date_str, tags=None):
        try:
            return self._add(DueDateTask(self.next_id, description, due_date_str, tags=tags))
        except (ValueError, TypeError):
            logger.error("Invalid due date: %s", due_date_str)
            return None

    def add_priority_task(self, description, priority, tags=None):
        try:
            return self._add(PriorityTask(self.next_id, description, priority, tags=tags))
        except ValueError:
            logger.error("Invalid priority: %s", priority)
            return None

    def get_task_by_id(self, task_id):
        return next((t for t in self.tasks if t.id == task_id), None)

    def get_all_tasks(self):
        return list(self.tasks)

    def complete_task(self, task_id):
        task = self.get_task_by_id(task_id)
        if not task:
            return False, "Task not found."
        if task.completed:
            return False, "Task is already completed."
        task.mark_complete()
        self._save_changes()
        return True, "Task marked as completed."

    def delete_task(self, task_id):
        original_len = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.id != task_id]
        if len(self.tasks) < original_len:
            self._save_changes()
            return True, "Task deleted successfully."
        return False, "Task not found."

    # --- Search ---
    def search_tasks(self, keyword):
        """Case-insensitive partial match in description or tags."""
        if not keyword:
            return []
        kw = keyword.lower()
        return [t for t in self.tasks
                if kw in t.description.lower() or any(kw in tag for tag in t.tags)]

    # --- Filter ---
    def filter_tasks(self, status=None, due_date_before=None, due_date_after=None,
                     priority_level=None, contains_tags=None):
        """
        Combine criteria with AND.
        status: True=completed, False=pending.
        due_date_before/after: datetime.date (inclusive); only DueDateTask match.
        priority_level: High/Medium/Low; only PriorityTask match.
        contains_tags: list; task must have ALL tags.
        """
        result = self.tasks
        if status is not None:
            result = [t for t in result if t.completed == status]
        if due_date_before:
            result = [t for t in result
                      if isinstance(t, DueDateTask) and t.due_date <= due_date_before]
        if due_date_after:
            result = [t for t in result
                      if isinstance(t, DueDateTask) and t.due_date >= due_date_after]
        if priority_level:
            result = [t for t in result
                      if isinstance(t, PriorityTask) and t.priority == priority_level]
        if contains_tags:
            wanted = [tag.lower() for tag in contains_tags]
            result = [t for t in result
                      if all(w in [x.lower() for x in t.tags] for w in wanted)]
        return list(result)

    # --- Sort ---
    def sort_tasks(self, criterion="id", reverse=False):
        """criterion: id, description, completed, due_date, priority."""
        tasks = list(self.tasks)
        if criterion == "description":
            tasks.sort(key=lambda t: t.description.lower(), reverse=reverse)
        elif criterion == "completed":
            tasks.sort(key=lambda t: (t.completed, t.id), reverse=reverse)
        elif criterion == "due_date":
            tasks.sort(key=lambda t: (t.due_date if isinstance(t, DueDateTask)
                                      else datetime.date.max, t.id), reverse=reverse)
        elif criterion == "priority":
            tasks.sort(key=lambda t: (self.PRIORITY_MAP.get(t.priority, 99)
                                      if isinstance(t, PriorityTask) else 99, t.id),
                       reverse=reverse)
        else:
            tasks.sort(key=lambda t: t.id, reverse=reverse)
        return tasks
