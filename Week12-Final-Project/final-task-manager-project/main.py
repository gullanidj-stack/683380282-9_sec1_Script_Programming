"""Entry point for the Enhanced Task Manager."""
from src.task_manager import TaskManager
from src.cli_interface import CLIInterface


def main():
    manager = TaskManager()
    cli = CLIInterface(manager)
    cli.run()


if __name__ == "__main__":
    main()
