# Quickstart Guide: In-Memory Python CLI Todo App MVP

**Feature**: 001-todo-cli-mvp
**Date**: 2025-12-30
**Audience**: Developers implementing the MVP

## Prerequisites

- **Python**: 3.12 or higher
- **Dependencies**: None (standard library only)
- **OS**: Cross-platform (Windows, macOS, Linux)

---

## Project Structure

```
todo-app/
├── src/
│   ├── models.py          # Task dataclass definition
│   ├── store.py           # TodoStore class (business logic)
│   ├── cli.py             # CLI interface (argparse + formatting)
│   └── main.py            # Application entry point
├── tests/                 # Optional for MVP
│   ├── test_models.py
│   ├── test_store.py
│   └── test_cli.py
├── todo.py                # Executable script (imports main)
└── specs/
    └── 001-todo-cli-mvp/  # This directory
```

---

## Quick Start (User Perspective)

**Add a task**:
```bash
$ python todo.py add "Buy groceries"
Task 1 added: Buy groceries
```

**List all tasks**:
```bash
$ python todo.py list
ID | Title         | Status
---------------------------------
1  | Buy groceries | pending
```

**Mark task as done**:
```bash
$ python todo.py complete 1
Task 1 marked as done
```

**Delete a task**:
```bash
$ python todo.py delete 1
Task 1 deleted
```

---

## Implementation Workflow

### Phase 1: Foundation & Data Model

**@logic-expert creates `src/models.py`**:
```python
from dataclasses import dataclass, field

@dataclass
class Task:
    """Represents a single todo item."""
    id: int
    title: str
    status: str = field(default='pending')

    def __post_init__(self) -> None:
        """Validate task attributes."""
        if not self.title or len(self.title) == 0:
            raise ValueError("Task title cannot be empty")
        if len(self.title) > 1000:
            raise ValueError("Task title cannot exceed 1000 characters")
        if self.status not in ('pending', 'done'):
            raise ValueError(f"Invalid status: {self.status}")
```

**Validation**:
- Run `type-hint-enforcer` skill to verify all type hints
- Verify default status is 'pending'
- Test with sample data:
  ```python
  task = Task(id=1, title="Test task")
  assert task.status == 'pending'
  ```

---

### Phase 2: In-Memory Logic Layer

**@logic-expert creates `src/store.py`**:
```python
from models import Task

class TodoStore:
    """Manages in-memory task storage and operations."""

    def __init__(self) -> None:
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str) -> Task:
        """Create and store a new task."""
        task = Task(id=self._next_id, title=title, status='pending')
        self._next_id += 1
        self._tasks.append(task)
        return task

    def list_tasks(self) -> list[Task]:
        """Return all tasks sorted by ID."""
        return sorted(self._tasks, key=lambda t: t.id)

    def get_task(self, task_id: int) -> Task | None:
        """Find task by ID, return None if not found."""
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def complete_task(self, task_id: int) -> Task | None:
        """Mark task as done. Returns None if not found."""
        task = self.get_task(task_id)
        if task is None:
            return None
        task.status = 'done'
        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete task by ID. Returns True if deleted, False if not found."""
        task = self.get_task(task_id)
        if task is None:
            return False
        self._tasks.remove(task)
        return True
```

**Validation**:
- Verify ID generation (starts at 1, increments)
- Verify ID uniqueness and non-reuse
- Test `complete_task` with non-existent ID (returns None)
- Test `delete_task` and verify ID is not reused

---

### Phase 3: CLI & User Interface

**@cli-expert creates `src/cli.py`**:
```python
import argparse
import sys
from models import Task
from store import TodoStore

def format_table(tasks: list[Task]) -> str:
    """Format tasks as a table with auto-width columns."""
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
    rows = [
        f"{t.id:<{id_width}} | {t.title:<{title_width}} | {t.status:<{status_width}}"
        for t in sorted(tasks, key=lambda t: t.id)
    ]

    return "\n".join([header, separator] + rows)

def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser with subcommands."""
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

def handle_add(store: TodoStore, args: argparse.Namespace) -> int:
    """Handle add command."""
    try:
        task = store.add_task(args.title)
        print(f"Task {task.id} added: {task.title}")
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

def handle_list(store: TodoStore, args: argparse.Namespace) -> int:
    """Handle list command."""
    tasks = store.list_tasks()
    print(format_table(tasks))
    return 0

def handle_complete(store: TodoStore, args: argparse.Namespace) -> int:
    """Handle complete command."""
    result = store.complete_task(args.id)
    if result is None:
        print(f"Error: Task with ID {args.id} not found", file=sys.stderr)
        return 1
    print(f"Task {result.id} marked as done")
    return 0

def handle_delete(store: TodoStore, args: argparse.Namespace) -> int:
    """Handle delete command."""
    success = store.delete_task(args.id)
    if not success:
        print(f"Error: Task with ID {args.id} not found", file=sys.stderr)
        return 1
    print(f"Task {args.id} deleted")
    return 0
```

**Validation**:
- Verify table formatting (left-aligned, auto-width)
- Verify confirmation messages match spec exactly
- Test error handling for non-integer IDs (argparse should handle)

---

### Phase 4: Integration & QA

**@qa-specialist creates `src/main.py`**:
```python
import sys
from cli import create_parser, handle_add, handle_list, handle_complete, handle_delete
from store import TodoStore

def main() -> int:
    """Main entry point for the Todo CLI application."""
    parser = create_parser()

    try:
        args = parser.parse_args()
    except SystemExit as e:
        # argparse calls sys.exit on error, catch it to handle ID validation
        return e.code if isinstance(e.code, int) else 2

    # Initialize store (in-memory, fresh each run)
    store = TodoStore()

    # Route to appropriate handler
    if args.command == 'add':
        return handle_add(store, args)
    elif args.command == 'list':
        return handle_list(store, args)
    elif args.command == 'complete':
        return handle_complete(store, args)
    elif args.command == 'delete':
        return handle_delete(store, args)
    else:
        print(f"Error: Unknown command '{args.command}'", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

**Create executable `todo.py`** (root directory):
```python
#!/usr/bin/env python3
"""Todo CLI application entry point."""

import sys
from src.main import main

if __name__ == '__main__':
    sys.exit(main())
```

**Verification Steps**:
1. **Smoke test all commands**:
   ```bash
   python todo.py add "Task 1"
   python todo.py add "Task 2"
   python todo.py list
   python todo.py complete 1
   python todo.py list
   python todo.py delete 2
   python todo.py list
   ```

2. **Test error cases**:
   ```bash
   python todo.py add ""                # Empty title error
   python todo.py complete 999          # Not found error
   python todo.py complete abc          # Invalid format error
   python todo.py delete -1             # Not found (negative ID)
   ```

3. **Test in-memory persistence**:
   ```bash
   python todo.py add "Task A"
   python todo.py list                  # Shows Task A
   # Exit and restart
   python todo.py list                  # Empty (data lost as expected)
   ```

4. **Performance test**:
   ```bash
   # Add 100 tasks
   for i in {1..100}; do
       python todo.py add "Task $i"
   done
   # List should complete in < 3 seconds
   time python todo.py list
   ```

---

## Key Constraints

**Constitution Compliance**:
- ✅ Agentic Delegation: @logic-expert handles store, @cli-expert handles CLI, @qa-specialist validates
- ✅ In-Memory State: No databases, no file persistence
- ✅ Modular Architecture: Store and CLI are separate modules
- ✅ Strict Type Safety: All functions have type hints
- ✅ No Feature Creep: Only spec-defined features implemented

**Technical Constraints**:
- ✅ Python 3.12+
- ✅ Standard library only (argparse, dataclasses, typing)
- ✅ Subcommands: add, list, complete, delete
- ✅ Table output: left-aligned, auto-width, sorted by ID

---

## Troubleshooting

**Issue**: `python todo.py` shows "No module named 'src'"`
**Solution**: Run from project root, ensure `src/` directory exists

**Issue**: Type hints not recognized
**Solution**: Verify Python 3.12+ with `python --version`

**Issue**: argparse not catching non-integer IDs
**Solution**: Ensure `type=int` is set on ID arguments in argparse

**Issue**: Table formatting breaks with long titles
**Solution**: Verify auto-width calculation includes all task titles

---

## Next Steps

After implementation:
1. Run `/sp.tasks` to generate detailed task breakdown
2. Run `/sp.implement` to execute tasks with agent delegation
3. Run `@qa-specialist` validation before marking complete
4. Run `/sp.git.commit_pr` to commit and create PR
