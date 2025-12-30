# TodoStore Interface Contract

**Feature**: 001-todo-cli-mvp
**Date**: 2025-12-30
**Component**: Store Layer (Business Logic)

## Overview

This document defines the contract for the `TodoStore` class, which manages in-memory task storage and provides operations for task manipulation. This is the core business logic layer, CLI-agnostic and independently testable.

---

## Class: TodoStore

**Responsibility**: Manage the lifecycle of Task objects in memory

**Dependencies**: Task dataclass (from models module)

**State**:
- `_tasks: list[Task]` - In-memory storage of all tasks
- `_next_id: int` - Counter for generating unique task IDs

---

## Method: `__init__`

**Signature**:
```python
def __init__(self) -> None:
    ...
```

**Purpose**: Initialize an empty TodoStore

**Parameters**: None

**Returns**: None

**Side Effects**:
- Initializes `_tasks` as empty list
- Initializes `_next_id` to 1

**Postconditions**:
- `len(self._tasks) == 0`
- `self._next_id == 1`

**Exceptions**: None

---

## Method: `add_task`

**Signature**:
```python
def add_task(self, title: str) -> Task:
    ...
```

**Purpose**: Create a new task with the given title

**Parameters**:
- `title` (str): The task description (must be non-empty, 1-1000 characters)

**Returns**: The newly created Task object

**Behavior**:
1. Validate title is non-empty (length >= 1)
2. Validate title length <= 1000 characters
3. Create new Task with:
   - `id = self._next_id`
   - `title = title` (exact copy, no trimming)
   - `status = 'pending'` (default)
4. Increment `self._next_id` by 1
5. Append task to `self._tasks`
6. Return the created task

**Side Effects**:
- Adds one task to `_tasks`
- Increments `_next_id` by 1

**Postconditions**:
- Task exists in `_tasks` with unique ID
- `_next_id` is greater than the returned task's ID

**Exceptions**:
- `ValueError`: If title is empty string
- `ValueError`: If title exceeds 1000 characters

**Example**:
```python
store = TodoStore()
task = store.add_task("Buy groceries")
# task.id == 1
# task.title == "Buy groceries"
# task.status == "pending"
```

---

## Method: `list_tasks`

**Signature**:
```python
def list_tasks(self) -> list[Task]:
    ...
```

**Purpose**: Retrieve all tasks sorted by ID in ascending order

**Parameters**: None

**Returns**: List of all tasks, sorted by ID (oldest first)

**Behavior**:
1. Return a sorted copy of `_tasks` ordered by ID ascending
2. Empty list if no tasks exist

**Side Effects**: None (read-only operation)

**Postconditions**:
- Returned list contains all tasks from `_tasks`
- Returned list is sorted by ID (ascending)
- Original `_tasks` is unmodified

**Exceptions**: None

**Complexity**: O(n log n) for sorting

**Example**:
```python
store = TodoStore()
store.add_task("Task A")  # ID 1
store.add_task("Task B")  # ID 2
tasks = store.list_tasks()
# tasks[0].id < tasks[1].id  # True
```

---

## Method: `get_task`

**Signature**:
```python
def get_task(self, task_id: int) -> Task | None:
    ...
```

**Purpose**: Retrieve a task by its unique ID

**Parameters**:
- `task_id` (int): The ID of the task to retrieve

**Returns**:
- The Task object if found
- `None` if no task with the given ID exists

**Behavior**:
1. Search `_tasks` for a task with `id == task_id`
2. Return the task if found
3. Return `None` if not found

**Side Effects**: None (read-only operation)

**Postconditions**:
- Original `_tasks` is unmodified

**Exceptions**: None (returns None instead of raising exceptions)

**Complexity**: O(n) linear search

**Example**:
```python
store = TodoStore()
task = store.add_task("Task A")  # ID 1
found = store.get_task(1)  # Returns task
missing = store.get_task(999)  # Returns None
```

---

## Method: `complete_task`

**Signature**:
```python
def complete_task(self, task_id: int) -> Task | None:
    ...
```

**Purpose**: Mark a task as done by its ID

**Parameters**:
- `task_id` (int): The ID of the task to complete

**Returns**:
- The updated Task object if found
- `None` if no task with the given ID exists

**Behavior**:
1. Find task with `id == task_id`
2. If not found, return `None`
3. If found, set `task.status = 'done'`
4. Return the updated task

**Idempotence**:
- Calling on an already-done task succeeds (no-op)
- Returns the task with status='done' without error

**Side Effects**:
- Modifies the status field of the task in `_tasks`

**Postconditions**:
- If task found: `task.status == 'done'`
- Task ID and title remain unchanged

**Exceptions**: None (returns None instead of raising exceptions)

**Irreversibility**:
- No method exists to revert status from 'done' to 'pending' (per Constitution)

**Example**:
```python
store = TodoStore()
task = store.add_task("Task A")  # status='pending'
result = store.complete_task(task.id)
# result.status == 'done'
# Idempotent:
result2 = store.complete_task(task.id)
# result2.status == 'done' (no error)
```

---

## Method: `delete_task`

**Signature**:
```python
def delete_task(self, task_id: int) -> bool:
    ...
```

**Purpose**: Remove a task from storage by its ID

**Parameters**:
- `task_id` (int): The ID of the task to delete

**Returns**:
- `True` if task was found and deleted
- `False` if no task with the given ID exists

**Behavior**:
1. Search `_tasks` for task with `id == task_id`
2. If found, remove it from `_tasks`
3. Return `True` if deleted, `False` if not found

**Side Effects**:
- Removes task from `_tasks` if found
- `_next_id` is NOT decremented (IDs are never reused)

**Postconditions**:
- Task no longer exists in `_tasks`
- `_next_id` remains unchanged (ID is not reused)

**Exceptions**: None (returns False instead of raising exceptions)

**Example**:
```python
store = TodoStore()
task = store.add_task("Task A")  # ID 1
success = store.delete_task(1)  # Returns True
# Task 1 no longer exists
retry = store.delete_task(1)  # Returns False (already deleted)
```

---

## Invariants

The TodoStore class MUST maintain these invariants at all times:

1. **ID Uniqueness**: No two tasks in `_tasks` have the same ID
2. **ID Sequential**: IDs are assigned sequentially starting from 1
3. **No ID Reuse**: `_next_id` only increases, never decreases
4. **Next ID Valid**: `_next_id` is always greater than any existing task ID
5. **Valid Status**: All tasks in `_tasks` have status of 'pending' or 'done'

---

## Thread Safety

**Not Thread-Safe**: This implementation is designed for single-threaded use (per Constitution - single-user, single-process application). No synchronization mechanisms are provided.

---

## Testing Contract

**Unit Tests Required**:
1. Empty store operations (list, get, complete, delete on empty store)
2. Add single task (verify ID assignment, default status)
3. Add multiple tasks (verify ID increment, uniqueness)
4. List tasks (verify sorting, completeness)
5. Get task (verify found/not-found cases)
6. Complete task (verify status change, idempotence, not-found case)
7. Delete task (verify removal, ID non-reuse, not-found case)
8. Edge cases (empty titles, long titles, negative/zero IDs, large ID values)

**Integration Tests Required**:
1. Add → List → Verify presence
2. Add → Complete → List → Verify status change
3. Add → Delete → List → Verify removal
4. Add → Delete → Add → Verify new task gets non-reused ID
5. Performance test with 100+ tasks

---

## Implementation Notes

**@logic-expert Responsibility**:
- Implement all methods per this contract
- Ensure strict type hints on all signatures
- Validate with `type-hint-enforcer` skill
- Maintain all invariants
- Handle edge cases gracefully (no crashes)

**CLI Separation**:
- This module MUST NOT import or depend on CLI/argparse code
- All validation errors return gracefully (None or False)
- CLI layer handles user-facing error messages
