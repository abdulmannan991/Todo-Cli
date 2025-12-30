"""Stylized CLI interface with color-coded output.

This module implements the argparse-based CLI with ANSI color codes for
a visually impressive terminal experience. All functions include strict
type hints per the type-hint-enforcer skill requirement.
"""

import argparse
import sys
from typing import Optional
from src.models import Task
from src.store import TodoStore


# ANSI Color Codes for stylized output
class Colors:
    """ANSI escape codes for terminal colors."""

    # Success messages - Bright Green
    SUCCESS = '\033[92m'

    # Error messages - Bright Red
    ERROR = '\033[91m'

    # Status: Done - Dim/Gray
    DONE = '\033[92m'

    # Status: Pending - Bold Yellow
    PENDING = '\033[1;33m'

    # Bold for headers
    BOLD = '\033[1m'

    # Cyan for menu headers
    CYAN = '\033[96m'

    # Reset to default
    RESET = '\033[0m'


def format_table(tasks: list[Task]) -> str:
    """Format tasks as a styled table with auto-width columns and color coding.

    Args:
        tasks: List of tasks to display

    Returns:
        Formatted table string with ANSI color codes, or "No tasks found" message
    """
    if not tasks:
        return f"{Colors.BOLD}No tasks found{Colors.RESET}"

    # Calculate column widths
    id_width: int = max(len(str(t.id)) for t in tasks)
    id_width = max(id_width, len("ID"))

    title_width: int = max(len(t.title) for t in tasks)
    title_width = max(title_width, len("Title"))

    status_width: int = max(len(t.status) for t in tasks)
    status_width = max(status_width, len("Status"))

    # Build bold header with separator
    header: str = f"{Colors.BOLD}{'ID':<{id_width}} | {'Title':<{title_width}} | {'Status':<{status_width}}{Colors.RESET}"
    separator: str = "═" * (id_width + title_width + status_width + 6)  # 6 for " | " separators

    # Build rows with color-coded status
    rows: list[str] = []
    for task in sorted(tasks, key=lambda t: t.id):
        # Color code the status based on value
        if task.status == 'done':
            status_display: str = f"{Colors.DONE}{task.status}{Colors.RESET}"
        else:  # pending
            status_display = f"{Colors.PENDING}{task.status}{Colors.RESET}"

        row: str = f"{task.id:<{id_width}} | {task.title:<{title_width}} | {status_display}"
        rows.append(row)

    return "\n".join([header, separator] + rows)


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser with subcommands.

    Returns:
        Configured ArgumentParser with add, list, complete, delete subcommands
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description=f"{Colors.BOLD}In-Memory Todo CLI{Colors.RESET} - Manage your tasks with style"
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    # add command
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('title', help='Task title')

    # list command
    list_parser = subparsers.add_parser('list', help='List all tasks')

    # complete command
    complete_parser = subparsers.add_parser('complete', help='Mark task as done')
    complete_parser.add_argument('id', type=int, help='Task ID')

    # delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('id', type=int, help='Task ID')

    return parser


def handle_add(store: TodoStore, args: argparse.Namespace) -> int:
    """Handle the add command with success message in bright green.

    Args:
        store: TodoStore instance
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        task: Task = store.add_task(args.title)
        print(f"{Colors.SUCCESS}Task {task.id} added: {task.title}{Colors.RESET}")
        return 0
    except ValueError as e:
        print(f"{Colors.ERROR}Error: {e}{Colors.RESET}", file=sys.stderr)
        return 1


def handle_list(store: TodoStore, args: argparse.Namespace) -> int:
    """Handle the list command with styled table output.

    Args:
        store: TodoStore instance
        args: Parsed command-line arguments

    Returns:
        Exit code (always 0 for list command)
    """
    tasks: list[Task] = store.list_tasks()
    print(format_table(tasks))
    return 0


def handle_complete(store: TodoStore, args: argparse.Namespace) -> int:
    """Handle the complete command with success message in bright green.

    Args:
        store: TodoStore instance
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    result: Optional[Task] = store.complete_task(args.id)
    if result is None:
        print(f"{Colors.ERROR}Error: Task with ID {args.id} not found{Colors.RESET}", file=sys.stderr)
        return 1
    print(f"{Colors.SUCCESS}Task {result.id} marked as done{Colors.RESET}")
    return 0


def handle_delete(store: TodoStore, args: argparse.Namespace) -> int:
    """Handle the delete command with success message in bright green.

    Args:
        store: TodoStore instance
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    success: bool = store.delete_task(args.id)
    if not success:
        print(f"{Colors.ERROR}Error: Task with ID {args.id} not found{Colors.RESET}", file=sys.stderr)
        return 1
    print(f"{Colors.SUCCESS}Task {args.id} deleted{Colors.RESET}")
    return 0


def start_interactive_mode(store: TodoStore) -> int:
    """Start interactive menu mode with continuous user interaction.

    Args:
        store: TodoStore instance for task management

    Returns:
        Exit code (0 for normal exit)
    """
    while True:
        # Display menu header
        print()
        print(f"{Colors.CYAN}{Colors.BOLD}{'=' * 30}{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}   TODO APPLICATION{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}{'=' * 30}{Colors.RESET}")
        print()
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task (Complete)")
        print("4. Delete Task")
        print("5. Edit Task Title")
        print("6. Exit")
        print()

        # Get user choice with yellow prompt
        choice: str = input(f"{Colors.PENDING}Enter your choice: {Colors.RESET}").strip()

        # Handle menu choices
        if choice == "1":
            # Add Task
            title: str = input("Enter task title: ").strip()
            if not title:
                print(f"{Colors.ERROR}Error: Task title cannot be empty{Colors.RESET}", file=sys.stderr)
                continue
            try:
                task: Task = store.add_task(title)
                print(f"{Colors.SUCCESS}Task {task.id} added successfully: {task.title}{Colors.RESET}")
            except ValueError as e:
                print(f"{Colors.ERROR}Error: {e}{Colors.RESET}", file=sys.stderr)

        elif choice == "2":
            # View Tasks
            tasks: list[Task] = store.list_tasks()
            print()
            print(format_table(tasks))

        elif choice == "3":
            # Update Task (Complete)
            task_id_str: str = input("Enter task ID to complete: ").strip()
            try:
                task_id: int = int(task_id_str)
                result: Optional[Task] = store.complete_task(task_id)
                if result is None:
                    print(f"{Colors.ERROR}Error: Task with ID {task_id} not found{Colors.RESET}", file=sys.stderr)
                else:
                    print(f"{Colors.SUCCESS}Task {result.id} marked as done{Colors.RESET}")
            except ValueError:
                print(f"{Colors.ERROR}Error: Invalid ID format. Please provide a positive integer.{Colors.RESET}", file=sys.stderr)

        elif choice == "4":
            # Delete Task
            task_id_str: str = input("Enter task ID to delete: ").strip()
            try:
                task_id: int = int(task_id_str)
                success: bool = store.delete_task(task_id)
                if not success:
                    print(f"{Colors.ERROR}Error: Task with ID {task_id} not found{Colors.RESET}", file=sys.stderr)
                else:
                    print(f"{Colors.SUCCESS}Task {task_id} deleted successfully{Colors.RESET}")
            except ValueError:
                print(f"{Colors.ERROR}Error: Invalid ID format. Please provide a positive integer.{Colors.RESET}", file=sys.stderr)

        elif choice == "5":
            # Edit Task Title
            task_id_str: str = input(f"{Colors.PENDING}Enter task ID to edit: {Colors.RESET}").strip()
            try:
                task_id: int = int(task_id_str)
                new_title: str = input(f"{Colors.PENDING}Enter new title: {Colors.RESET}").strip()

                if not new_title:
                    print(f"{Colors.ERROR}Error: Task title cannot be empty{Colors.RESET}", file=sys.stderr)
                    continue

                result: Optional[Task] = store.update_task_title(task_id, new_title)
                if result is None:
                    print(f"{Colors.ERROR}Error: Task with ID {task_id} not found{Colors.RESET}", file=sys.stderr)
                else:
                    print(f"{Colors.SUCCESS}Task {result.id} title updated successfully!{Colors.RESET}")
            except ValueError as e:
                if "Invalid literal" in str(e) or "invalid literal" in str(e):
                    print(f"{Colors.ERROR}Error: Invalid ID format. Please provide a positive integer.{Colors.RESET}", file=sys.stderr)
                else:
                    print(f"{Colors.ERROR}Error: {e}{Colors.RESET}", file=sys.stderr)

        elif choice == "6":
            # Exit
            print(f"{Colors.SUCCESS}Goodbye!{Colors.RESET}")
            return 0

        else:
            print(f"{Colors.ERROR}Error: Invalid choice. Please select 1-6.{Colors.RESET}", file=sys.stderr)
