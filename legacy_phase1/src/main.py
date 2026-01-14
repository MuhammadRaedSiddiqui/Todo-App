"""Main entry point for the Todo CLI application."""

from src.cli.menu import TodoMenu
from src.services.task_service import TaskService


def main() -> None:
    """Run the Todo CLI application."""
    # Initialize the task service (in-memory storage)
    task_service = TaskService()

    # Create and run the menu
    menu = TodoMenu(task_service)
    menu.run()


if __name__ == "__main__":
    main()
