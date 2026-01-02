"""CLI menu interface for the Todo application."""

from typing import Optional

from src.services.task_service import (
    TaskAlreadyCompleteError,
    TaskNotFoundError,
    TaskService,
    TaskServiceError,
)


def get_string_input(prompt: str, allow_empty: bool = False) -> str:
    """Get a string input from the user.

    Args:
        prompt: The prompt to display.
        allow_empty: Whether to allow empty input.

    Returns:
        The user's input (stripped).
    """
    while True:
        user_input = input(prompt).strip()
        if user_input or allow_empty:
            return user_input
        print("Error: Input cannot be empty. Please try again.")


def get_int_input(
    prompt: str,
    min_value: Optional[int] = None,
    max_value: Optional[int] = None,
) -> int:
    """Get an integer input from the user.

    Args:
        prompt: The prompt to display.
        min_value: Minimum allowed value (inclusive).
        max_value: Maximum allowed value (inclusive).

    Returns:
        The user's input as an integer.
    """
    while True:
        try:
            user_input = input(prompt).strip()
            value = int(user_input)
            if min_value is not None and value < min_value:
                print(f"Error: Value must be at least {min_value}. Please try again.")
                continue
            if max_value is not None and value > max_value:
                print(f"Error: Value must be at most {max_value}. Please try again.")
                continue
            return value
        except ValueError:
            print("Error: Please enter a valid number.")


def get_yes_no_input(prompt: str) -> bool:
    """Get a yes/no input from the user.

    Args:
        prompt: The prompt to display.

    Returns:
        True for 'y' or 'Y', False for 'n' or 'N'.
    """
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in ("y", "yes"):
            return True
        if user_input in ("n", "no"):
            return False
        print("Error: Please enter 'y' or 'n'.")


def format_error(message: str) -> str:
    """Format an error message consistently.

    Args:
        message: The error message.

    Returns:
        Formatted error message.
    """
    return f"Error: {message}"


class TodoMenu:
    """Main menu handler for the Todo CLI application."""

    def __init__(self, task_service: TaskService) -> None:
        """Initialize the menu with a task service.

        Args:
            task_service: The TaskService instance to use.
        """
        self._service = task_service

    def run(self) -> None:
        """Run the main application loop."""
        while True:
            self._display_main_menu()
            choice = get_int_input("Enter your choice (1-6): ", 1, 6)

            if choice == 1:
                self.handle_add_task()
            elif choice == 2:
                self.handle_view_tasks()
            elif choice == 3:
                self.handle_update_task()
            elif choice == 4:
                self.handle_mark_complete()
            elif choice == 5:
                self.handle_delete_task()
            elif choice == 6:
                self.handle_exit()
                break

    def _display_main_menu(self) -> None:
        """Display the main menu."""
        print()
        print("=== TODO LIST MENU ===")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Mark Complete")
        print("5. Delete Task")
        print("6. Exit")
        print()

    def handle_add_task(self) -> None:
        """Handle the Add Task menu option."""
        print()
        print("--- Add New Task ---")

        # Get title with validation
        title = ""
        while not title:
            title = get_string_input("Enter task title: ")
            if not title:
                print(format_error("Task title cannot be empty. Please enter a valid title."))

        # Get description (optional)
        description = get_string_input("Enter task description (optional): ", allow_empty=True)

        # Create the task
        try:
            task = self._service.add_task(title, description)
            print(f"Task added successfully! (ID: {task.id})")
        except ValueError as e:
            print(format_error(str(e)))

    def handle_view_tasks(self) -> None:
        """Handle the View Tasks menu option."""
        print()
        print("--- View Tasks ---")

        tasks = self._service.get_all_tasks()

        if not tasks:
            print("No tasks yet. Add your first task!")
            return

        print()
        print("ID | Status     | Title")
        print("-" * 50)

        for task in tasks:
            status = task.status.ljust(9)
            print(f"{task.id} | {status} | {task.title}")
            if task.description:
                print(f"    Description: {task.description}")

        print()
        print(f"({len(tasks)} task(s) total)")

    def handle_update_task(self) -> None:
        """Handle the Update Task menu option."""
        print()
        print("--- Update Task ---")

        # Get task ID
        task_id = get_int_input("Enter task ID to update: ", 1)

        try:
            task = self._service.get_task_by_id(task_id)
        except TaskServiceError:
            print(format_error(f"Task with ID {task_id} not found."))
            return

        # Show current task
        print(f"Current task: {task.title}")
        if task.description:
            print(f"Current description: {task.description}")

        # Get new title (optional)
        print("Enter new title (or press Enter to keep current):")
        new_title = get_string_input("> ", allow_empty=True)
        if not new_title:
            new_title = None  # Keep current

        # Get new description (optional)
        print("Enter new description (or press Enter to keep current):")
        new_description = get_string_input("> ", allow_empty=True)
        if new_description == "":
            new_description = None  # Keep current

        # Update the task
        try:
            self._service.update_task(task_id, new_title, new_description)
            print(f"Task {task_id} updated successfully!")
        except (TaskServiceError, ValueError) as e:
            print(format_error(str(e)))

    def handle_mark_complete(self) -> None:
        """Handle the Mark Complete menu option."""
        print()
        print("--- Mark Task as Complete ---")

        # Get task ID
        task_id = get_int_input("Enter task ID to mark as complete: ", 1)

        try:
            self._service.mark_complete(task_id)
            print(f"Task {task_id} marked as complete!")
        except TaskNotFoundError:
            print(format_error(f"Task with ID {task_id} not found."))
        except TaskAlreadyCompleteError:
            print(format_error(f"Task {task_id} is already marked as complete."))

    def handle_delete_task(self) -> None:
        """Handle the Delete Task menu option."""
        print()
        print("--- Delete Task ---")

        # Get task ID
        task_id = get_int_input("Enter task ID to delete: ", 1)

        # Check if task exists first
        try:
            task = self._service.get_task_by_id(task_id)
        except TaskServiceError:
            print(format_error(f"Task with ID {task_id} not found."))
            return

        # Confirm deletion
        print(f"Are you sure you want to delete '{task.title}'? (y/n):")
        if not get_yes_no_input("> "):
            print("Delete cancelled.")
            return

        # Delete the task
        try:
            self._service.delete_task(task_id)
            print("Task deleted successfully!")
        except TaskServiceError as e:
            print(format_error(str(e)))

    def handle_exit(self) -> None:
        """Handle the Exit menu option."""
        print()
        print("Goodbye! Thanks for Todo List.")
