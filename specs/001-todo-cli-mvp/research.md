# Research: In-Memory Python CLI Todo App MVP

**Feature**: 001-todo-cli-mvp
**Date**: 2025-12-30
**Phase**: 0 - Technical Research

## Research Questions

This document resolves technical unknowns identified during initial planning to enable detailed design in Phase 1.

---

## R1: Python Dataclass Best Practices for In-Memory Storage

**Question**: What is the optimal dataclass configuration for the Task model to ensure type safety and proper in-memory behavior?

**Decision**: Use `@dataclass` with `frozen=False` (mutable) and explicit type hints

**Rationale**:
- **Mutable dataclasses** allow status updates (pending → done) without creating new instances
- **Type hints** on all fields ensure strict type checking (aligns with Constitution Principle IV)
- **Default factory** for status field ensures 'pending' default without mutable default arguments
- **`__post_init__`** can validate title length if needed

**Implementation Approach**:
```python
from dataclasses import dataclass, field

@dataclass
class Task:
    id: int
    title: str
    status: str = field(default='pending')
```

**Alternatives Considered**:
- **Frozen dataclasses** (`frozen=True`): Rejected because marking tasks complete requires mutating the status field
- **NamedTuple**: Rejected due to immutability and lack of default values
- **Regular class with `__init__`**: Rejected due to unnecessary boilerplate when dataclasses provide the same functionality

---

## R2: ID Generation Strategy for In-Memory Storage

**Question**: What is the simplest, most reliable ID generation strategy that ensures uniqueness and never reuses IDs even after deletion?

**Decision**: Use a simple counter (integer) that increments with each task creation

**Rationale**:
- **Simplicity**: Single integer variable tracks next ID
- **Uniqueness**: Monotonically increasing counter guarantees no collisions
- **No reuse**: Counter never decrements, even when tasks are deleted
- **Performance**: O(1) ID generation with no lookups required
- **Thread-safe**: Single-process application (per Constitution) eliminates concurrency concerns

**Implementation Approach**:
```python
class TodoStore:
    def __init__(self) -> None:
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str) -> Task:
        task = Task(id=self._next_id, title=title, status='pending')
        self._next_id += 1
        self._tasks.append(task)
        return task
```

**Alternatives Considered**:
- **UUID/GUID**: Rejected as overly complex for MVP; integer IDs are more user-friendly for CLI
- **Hash-based IDs**: Rejected due to collision risk and complexity
- **Max ID + 1**: Rejected because it requires scanning all tasks on each add (O(n) vs O(1))

---

## R3: Table Formatting for CLI Output

**Question**: Which Python standard library module provides the best table formatting for the list command?

**Decision**: Manual formatting using f-strings with dynamic column width calculation

**Rationale**:
- **No external dependencies**: Aligns with Constitution (standard library only)
- **Full control**: Left-alignment and auto-width as specified in clarifications
- **Simplicity**: ~20 lines of code vs adding a dependency
- **Performance**: Negligible for <1000 tasks (spec's performance target)

**Implementation Approach**:
```python
def format_table(tasks: list[Task]) -> str:
    if not tasks:
        return "No tasks found"

    # Calculate column widths
    id_width = max(len(str(t.id)) for t in tasks)
    id_width = max(id_width, len("ID"))

    title_width = max(len(t.title) for t in tasks)
    title_width = max(title_width, len("Title"))

    status_width = max(len(t.status) for t in tasks)
    status_width = max(status_width, len("Status"))

    # Build table
    header = f"{'ID':<{id_width}} | {'Title':<{title_width}} | {'Status':<{status_width}}"
    separator = "-" * len(header)
    rows = [f"{t.id:<{id_width}} | {t.title:<{title_width}} | {t.status:<{status_width}}"
            for t in sorted(tasks, key=lambda t: t.id)]

    return "\n".join([header, separator] + rows)
```

**Alternatives Considered**:
- **tabulate library**: Rejected (external dependency violates Constitution)
- **PrettyTable library**: Rejected (external dependency violates Constitution)
- **CSV/TSV output**: Rejected (not human-readable enough for CLI)

---

## R4: argparse Configuration for Subcommands

**Question**: What is the optimal argparse structure for implementing the four CLI commands (add, list, complete, delete)?

**Decision**: Use `argparse.ArgumentParser` with `add_subparsers()` for command routing

**Rationale**:
- **Standard pattern**: Subparsers are the recommended approach for multi-command CLIs
- **Built-in help**: Automatic help generation for each subcommand
- **Type safety**: Can specify `type=int` for ID arguments to handle validation
- **Clean routing**: Each subcommand maps to a handler function

**Implementation Approach**:
```python
import argparse

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="In-Memory Todo CLI")
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
```

**Alternatives Considered**:
- **Click library**: Rejected (external dependency)
- **Custom argument parsing**: Rejected (reinventing the wheel)
- **Single command with flags**: Rejected (less intuitive UX than subcommands)

---

## R5: Error Handling Strategy for ID Validation

**Question**: How should the application handle the two types of invalid IDs: non-integers (e.g., "abc") and valid integers that don't exist (e.g., -1, 0, 999)?

**Decision**: Two-tier validation approach:
1. argparse handles type validation (rejects non-integers)
2. Store layer handles existence validation (returns None for non-existent IDs)

**Rationale**:
- **Separation of concerns**: argparse validates format, store validates business logic
- **Clear error messages**: Different error types get different, helpful messages
- **Type safety**: argparse `type=int` prevents non-integer values from reaching business logic
- **Graceful handling**: Negative/zero IDs pass type check but fail existence check (per clarification Q3)

**Implementation Approach**:
```python
# argparse automatically handles non-integer rejection
complete_parser.add_argument('id', type=int, help='Task ID')

# Store returns None for non-existent IDs
class TodoStore:
    def get_task(self, task_id: int) -> Task | None:
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def complete_task(self, task_id: int) -> Task | None:
        task = self.get_task(task_id)
        if task is None:
            return None
        task.status = 'done'
        return task

# CLI layer handles the response
if result is None:
    print(f"Error: Task with ID {task_id} not found", file=sys.stderr)
    sys.exit(1)
```

**Alternatives Considered**:
- **Exceptions for not found**: Rejected (None is more Pythonic for "not found" cases)
- **Custom validation in CLI**: Rejected (business logic should live in store layer)
- **Strict ID range validation**: Rejected (per clarification, negative/zero should report "not found" not "invalid format")

---

## Summary

All technical unknowns resolved. Key decisions:
- **Dataclass**: Mutable with explicit defaults
- **ID Generation**: Simple incrementing counter
- **Table Formatting**: Manual f-string formatting
- **argparse**: Subparsers with type=int for IDs
- **Error Handling**: Two-tier (format vs existence)

Ready to proceed to Phase 1 (Design & Contracts).
