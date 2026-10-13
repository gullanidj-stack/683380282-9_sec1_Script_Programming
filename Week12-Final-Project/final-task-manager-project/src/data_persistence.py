"""JSON load/save for tasks."""
import json
import os

from .task import Task, DueDateTask, PriorityTask


class DataPersistence:
    """Centralizes all file I/O and (de)serialization logic."""

    def __init__(self, data_file="data/tasks.json"):
        self.data_file = data_file
        self._data_file_path = os.path.normpath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", data_file)
        )

    def load_tasks(self):
        """Loads tasks from JSON, rebuilding objects based on '_type'."""
        if not os.path.exists(self._data_file_path):
            os.makedirs(os.path.dirname(self._data_file_path), exist_ok=True)
            return []
        try:
            with open(self._data_file_path, "r", encoding="utf-8") as f:
                raw_tasks = json.load(f)
            loaded = []
            for t_dict in raw_tasks:
                task_type = t_dict.pop("_type", "Task")
                t_dict.setdefault("tags", [])  # support old files without tags
                if task_type == "Task":
                    loaded.append(Task(**t_dict))
                elif task_type == "DueDateTask":
                    loaded.append(DueDateTask(**t_dict))
                elif task_type == "PriorityTask":
                    loaded.append(PriorityTask(**t_dict))
                else:
                    print(f"Warning: Unknown task type '{task_type}'. "
                          f"Skipping task ID {t_dict.get('id', 'N/A')}.")
            return loaded
        except json.JSONDecodeError:
            print("Warning: tasks.json is empty or corrupted. Starting with an empty list.")
            return []
        except Exception as e:
            print(f"Unexpected error while loading tasks: {e}. Starting with an empty list.")
            return []

    def save_tasks(self, tasks):
        """Saves tasks using each task's polymorphic to_dict()."""
        os.makedirs(os.path.dirname(self._data_file_path), exist_ok=True)
        with open(self._data_file_path, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in tasks], f, indent=4, ensure_ascii=False)
