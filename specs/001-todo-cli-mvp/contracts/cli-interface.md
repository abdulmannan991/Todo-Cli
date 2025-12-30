# CLI Interface Contract

**Feature**: 001-todo-cli-mvp
**Date**: 2025-12-30
**Component**: CLI Layer (User Interface)

## Overview

This document defines the contract for the CLI interface, which handles user input via argparse, delegates to the TodoStore, and formats output for the terminal. This is the View layer, containing NO business logic.

---

## Command Line Interface

**Entry Point**: `python todo.py <command> [arguments]`

**Commands**: add, list, complete, delete

---

## Command: `add`

**Syntax**:
```bash
python todo.py add <title>
```

**Purpose**: Add a new task with the given title

**Arguments**:
- `<title>` (str, required): The task description

**Behavior**:
1. Parse title from command line arguments
2. Call `store.add_task(title)`
3. On success: Print confirmation message to stdout
4. On failure: Print error message to stderr and exit with code 1

**Success Output Format**:
```
Task {id} added: {title}
```

**Error Cases**:
| Error Condition | Output (stderr) | Exit Code |
|-----------------|-----------------|-----------|
| Empty title | Error: Task title cannot be empty | 1 |
| Title too long (>1000 chars) | Error: Task title cannot exceed 1000 characters | 1 |
| No title provided | Error: the following arguments are required: title | 1 |

**Examples**:
```bash
$ python todo.py add "Buy groceries"
Task 1 added: Buy groceries

$ python todo.py add ""
Error: Task title cannot be empty

$ python todo.py add
Error: the following arguments are required: title
```

---

## Command: `list`

**Syntax**:
```bash
python todo.py list
```

**Purpose**: Display all tasks in a formatted table

**Arguments**: None

**Behavior**:
1. Call `store.list_tasks()`
2. If no tasks exist: Print "No tasks found" to stdout
3. If tasks exist: Format and print table to stdout

**Table Format**:
- **Columns**: ID, Title, Status
- **Alignment**: All columns left-aligned
- **Width**: Auto-adjust to content (no truncation)
- **Sorting**: By ID ascending (oldest to newest)
- **Separator**: Single line of dashes between header and rows

**Success Output Format (with tasks)**:
```
ID | Title                    | Status
-----------------------------------------
1  | Buy groceries            | pending
2  | Call dentist             | done
3  | Review Q4 budget proposal| pending
```

**Success Output Format (empty list)**:
```
No tasks found
```

**Error Cases**: None (list command cannot fail)

**Examples**:
```bash
$ python todo.py list
ID | Title         | Status
---------------------------------
1  | Buy groceries | pending

$ python todo.py list  # empty store
No tasks found
```

---

## Command: `complete`

**Syntax**:
```bash
python todo.py complete <id>
```

**Purpose**: Mark a task as done by its ID

**Arguments**:
- `<id>` (int, required): The task ID to complete

**Behavior**:
1. Parse ID from command line (argparse validates it's an integer)
2. Call `store.complete_task(id)`
3. If task found: Print confirmation message to stdout
4. If task not found: Print error message to stderr and exit with code 1

**Success Output Format**:
```
Task {id} marked as done
```

**Error Cases**:
| Error Condition | Output (stderr) | Exit Code |
|-----------------|-----------------|-----------|
| Non-integer ID (e.g., "abc") | Error: Invalid ID format. Please provide a positive integer. | 2 |
| Task not found (negative, zero, or non-existent ID) | Error: Task with ID {id} not found | 1 |
| No ID provided | Error: the following arguments are required: id | 1 |

**Idempotence**: Completing an already-done task succeeds with same message

**Examples**:
```bash
$ python todo.py complete 1
Task 1 marked as done

$ python todo.py complete 999
Error: Task with ID 999 not found

$ python todo.py complete abc
Error: Invalid ID format. Please provide a positive integer.

$ python todo.py complete
Error: the following arguments are required: id
```

---

## Command: `delete`

**Syntax**:
```bash
python todo.py delete <id>
```

**Purpose**: Remove a task from the list by its ID

**Arguments**:
- `<id>` (int, required): The task ID to delete

**Behavior**:
1. Parse ID from command line (argparse validates it's an integer)
2. Call `store.delete_task(id)`
3. If task found and deleted: Print confirmation message to stdout
4. If task not found: Print error message to stderr and exit with code 1

**Success Output Format**:
```
Task {id} deleted
```

**Error Cases**:
| Error Condition | Output (stderr) | Exit Code |
|-----------------|-----------------|-----------|
| Non-integer ID (e.g., "abc") | Error: Invalid ID format. Please provide a positive integer. | 2 |
| Task not found (negative, zero, or non-existent ID) | Error: Task with ID {id} not found | 1 |
| No ID provided | Error: the following arguments are required: id | 1 |

**Examples**:
```bash
$ python todo.py delete 1
Task 1 deleted

$ python todo.py delete 999
Error: Task with ID 999 not found

$ python todo.py delete abc
Error: Invalid ID format. Please provide a positive integer.
```

---

## Help System

**Global Help**:
```bash
$ python todo.py --help
usage: todo.py [-h] {add,list,complete,delete} ...

In-Memory Todo CLI

positional arguments:
  {add,list,complete,delete}
    add                 Add a new task
    list                List all tasks
    complete            Mark task as done
    delete              Delete a task

optional arguments:
  -h, --help            show this help message and exit
```

**Command-Specific Help**:
```bash
$ python todo.py add --help
usage: todo.py add [-h] title

positional arguments:
  title       Task title

optional arguments:
  -h, --help  show this help message and exit
```

---

## Error Handling

**Exit Codes**:
- **0**: Success
- **1**: Business logic error (task not found, empty title, etc.)
- **2**: Invalid input format (non-integer ID, etc.)

**Error Output**:
- All errors MUST be written to stderr (not stdout)
- Error messages MUST be prefixed with "Error: "
- Error messages MUST be clear and actionable

**argparse Error Handling**:
- argparse automatically handles missing required arguments
- argparse automatically handles invalid integer conversions
- Catch `argparse.ArgumentTypeError` for custom validation

---

## Table Formatting Specification

**Column Width Calculation**:
1. For each column, find max width of: header label and all cell values
2. Use that width for the column (no fixed width)
3. Left-align all text within column width

**Reference Implementation**:
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

    # Build header
    header = f"{'ID':<{id_width}} | {'Title':<{title_width}} | {'Status':<{status_width}}"
    separator = "-" * len(header)

    # Build rows (sorted by ID)
    rows = [
        f"{t.id:<{id_width}} | {t.title:<{title_width}} | {t.status:<{status_width}}"
        for t in sorted(tasks, key=lambda t: t.id)
    ]

    return "\n".join([header, separator] + rows)
```

---

## Testing Contract

**Manual Test Scenarios**:
1. Add task with simple title
2. Add task with multi-word title
3. Add task with special characters
4. List tasks (empty and populated)
5. Complete task by ID
6. Delete task by ID
7. Error: Add empty title
8. Error: Complete non-existent ID
9. Error: Complete non-integer ID
10. Error: Delete non-existent ID

**Integration Test Scenarios**:
1. Add → List → Verify task appears
2. Add → Complete → List → Verify status changed
3. Add → Delete → List → Verify task removed
4. Multiple adds → List → Verify sorted by ID ascending

---

## Implementation Notes

**@cli-expert Responsibility**:
- Implement argparse configuration per this contract
- Implement table formatting per specification
- Implement error handling and exit codes
- Ensure NO business logic in CLI layer (delegate to store)
- Format confirmation messages exactly as specified

**Store Dependency**:
- CLI layer MUST depend on TodoStore
- CLI layer MUST NOT implement task storage or ID generation
- All data operations delegated to store methods

**Type Safety**:
- All function signatures MUST have strict type hints
- Validate with `type-hint-enforcer` skill

---

## User Experience Requirements

**Performance** (per Success Criteria):
- Add command completes in under 5 seconds (SC-001)
- List command completes in under 3 seconds (SC-002, SC-005)
- Complete command completes in under 5 seconds (SC-003)
- Delete command completes in under 5 seconds (SC-004)

**Clarity** (per Success Criteria):
- 95% of user actions result in clear feedback (SC-006)
- All operations function without documentation (SC-007)

**Usability**:
- Error messages explain what went wrong and how to fix it
- Confirmation messages include relevant details (ID, title)
- Table output is human-readable and easy to scan
