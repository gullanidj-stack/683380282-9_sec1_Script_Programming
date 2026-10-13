# Project Plan: Enhanced Task Manager CLI (Final Version)

## 1. Introduction
Blueprint and final reflection for the CLI Task Manager.

## 2. Requirements (Implemented)
- Create, list, complete, delete tasks; `DueDateTask` and `PriorityTask` types
- Tags on all tasks
- Search by keyword (description or tags, case-insensitive)
- Filter by status, due-date range, priority, tags
- Sort by id, description, completed, due date, priority
- Automatic JSON persistence
- Non-functional: usability, reliability (input validation), maintainability, extensibility

## 3. Architecture
| Module | Responsibility |
|---|---|
| `task.py` | Data models, tags, `to_dict`, `__str__` |
| `data_persistence.py` | JSON load/save, object reconstruction |
| `task_manager.py` | CRUD, search, filter, sort |
| `cli_interface.py` | Menus, input validation, output |
| `main.py` | Wires everything together |

## 4. Implementation Notes
- **Tags:** list on base `Task`; old JSON without tags loads with `[]`.
- **Search:** `keyword in description.lower()` or in any tag.
- **Filter:** criteria applied sequentially (AND); `isinstance` checks for date/priority.
- **Sort:** `list.sort` with lambda keys; missing due date -> `date.max`,
  missing priority -> 99; `id` as tie-breaker.
- **Debugging lessons:** isolating logic errors (manager) vs input errors (CLI);
  inspecting object state; the `src` package needs `from src...` imports in `main.py`.

## 5. Future Work
GUI, SQLite, reminders, user accounts, recurring tasks, more tests.
