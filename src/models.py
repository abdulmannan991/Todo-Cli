"""Task data model for the Todo CLI application.

This module defines the Task dataclass with strict type hints and validation.
All fields are explicitly typed per the type-hint-enforcer skill requirement.
"""

from dataclasses import dataclass, field


@dataclass
class Task:
    """Represents a single todo item.

    Attributes:
        id: Unique integer identifier (auto-assigned, never reused)
        title: Human-readable task description (1-1000 chars)
        status: Current state ('pending' or 'done')
    """

    id: int
    title: str
    status: str = field(default='pending')

    def __post_init__(self) -> None:
        """Validate task attributes after initialization.

        Raises:
            ValueError: If title is empty or exceeds 1000 characters
            ValueError: If status is not 'pending' or 'done'
        """
        if not self.title or len(self.title) == 0:
            raise ValueError("Task title cannot be empty")
        if len(self.title) > 1000:
            raise ValueError("Task title cannot exceed 1000 characters")
        if self.status not in ('pending', 'done'):
            raise ValueError(f"Invalid status: {self.status}")
