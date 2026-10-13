# Final Project: Enhanced Task Manager CLI

A command-line task manager built with OOP, modular design, JSON persistence,
and search / filter / sort features.

## Features
- **Task types:** normal, `DueDateTask`, `PriorityTask`
- **Tags** on every task
- **CRUD:** add, list, complete, delete
- **Search:** case-insensitive, partial match in description or tags
- **Filter:** status, due-date range, priority, tags (must have ALL), combined with AND
- **Sort:** id, description, completed, due_date, priority (tasks without the attribute go last)
- **Persistence:** auto-saved to `data/tasks.json`

## How to Run
```bash
git clone https://github.com/YOUR_USERNAME/final-task-manager-project.git
cd final-task-manager-project
python main.py
```
Run the tests with `python -m unittest discover -s tests`.

## Project Structure
```
final-task-manager-project/
├── src/
│   ├── __init__.py
│   ├── task.py              # Task models
│   ├── data_persistence.py  # JSON I/O
│   ├── task_manager.py      # Business logic
│   └── cli_interface.py     # User interaction
├── tests/
│   └── test_task_manager.py
├── data/
│   └── tasks.json
├── main.py
├── .gitignore
├── README.md
└── PLAN.md
```

## Future Work
GUI, SQLite database, reminders, user accounts, recurring tasks, CSV export, web interface.
