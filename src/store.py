"""In-memory task storage and business logic.

This module implements the TodoStore class that manages tasks in memory.
All methods include strict type hints per the type-hint-enforcer skill requirement.
"""

from typing import Optional
from src.models import Task


class TodoStore:
    """Manages in-memory task storage and operations.

    Attributes:
        _tasks: In-memory list of all tasks
        _next_id: Counter for generating unique task IDs
    """

    def __init__(self) -> None:
        """Initialize an empty TodoStore with ID counter starting at 1."""
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str) -> Task:
        """Create and store a new task with auto-generated ID.

        Args:
            title: The task description (must be non-empty, 1-1000 characters)

        Returns:
            The newly created Task object with unique ID and 'pending' status

        Raises:
            ValueError: If title is empty or exceeds 1000 characters
        """
        task: Task = Task(id=self._next_id, title=title, status='pending')
        self._next_id += 1
        self._tasks.append(task)
        return task

    def list_tasks(self) -> list[Task]:
        """Retrieve all tasks sorted by ID in ascending order.

        Returns:
            List of all tasks, sorted by ID (oldest first). Empty list if no tasks.
        """
        return sorted(self._tasks, key=lambda t: t.id)

    def get_task(self, task_id: int) -> Optional[Task]:
        """Find a task by its unique ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The Task object if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def complete_task(self, task_id: int) -> Optional[Task]:
        """Mark a task as done by its ID (one-way transition only).

        Args:
            task_id: The ID of the task to complete

        Returns:
            The updated Task object if found, None otherwise

        Note:
            This operation is idempotent - marking an already-done task
            as done will succeed without error.
        """
        task: Optional[Task] = self.get_task(task_id)
        if task is None:
            return None
        task.status = 'done'
        return task

    def delete_task(self, task_id: int) -> bool:
        """Remove a task from storage by its ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if task was found and deleted, False otherwise

        Note:
            The deleted task's ID will never be reused for new tasks.
        """
        task: Optional[Task] = self.get_task(task_id)
        if task is None:
            return False
        self._tasks.remove(task)
        return True

    def update_task_title(self, task_id: int, new_title: str) -> Optional[Task]:
        """Update the title of an existing task by its ID.

        Args:
            task_id: The ID of the task to update
            new_title: The new title for the task (must be non-empty, 1-1000 characters)

        Returns:
            The updated Task object if found, None otherwise

        Raises:
            ValueError: If new_title is empty or exceeds 1000 characters

        Note:
            Title validation follows the same rules as task creation.
        """
        task: Optional[Task] = self.get_task(task_id)
        if task is None:
            return None

        # Validate new title (same rules as Task.__post_init__)
        if not new_title or len(new_title) == 0:
            raise ValueError("Task title cannot be empty")
        if len(new_title) > 1000:
            raise ValueError("Task title cannot exceed 1000 characters")

        # Update the title
        task.title = new_title
        return task
