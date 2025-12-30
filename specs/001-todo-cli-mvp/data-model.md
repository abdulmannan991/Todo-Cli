# Data Model: In-Memory Python CLI Todo App MVP

**Feature**: 001-todo-cli-mvp
**Date**: 2025-12-30
**Phase**: 1 - Data Model Design

## Overview

This document defines the data entities, their attributes, relationships, and validation rules for the Todo CLI MVP. The implementation uses Python dataclasses stored in-memory (per Constitution Principle II).

---

## Entity: Task

**Purpose**: Represents a single todo item that a user needs to track.

**Attributes**:

| Attribute | Type | Required | Default | Constraints | Description |
|-----------|------|----------|---------|-------------|-------------|
| `id` | `int` | Yes | Auto-assigned | Unique, positive, never reused | Unique identifier for the task |
| `title` | `str` | Yes | None | 1-1000 characters | Human-readable description of the task |
| `status` | `str` | Yes | `'pending'` | Must be `'pending'` or `'done'` | Current state of the task |

**Validation Rules**:

1. **ID Uniqueness**: Each task MUST have a unique ID within the application session
2. **ID Immutability**: Once assigned, a task's ID MUST never change
3. **ID Non-Reuse**: IDs MUST NOT be reused even after a task is deleted
4. **Title Non-Empty**: Title MUST contain at least 1 character (enforced at creation)
5. **Title Length**: Title SHOULD NOT exceed 1000 characters (reasonable limit for in-memory storage)
6. **Status Values**: Status MUST be either `'pending'` or `'done'` (no other values permitted)
7. **Status Default**: New tasks MUST default to `'pending'` status

**State Transitions**:

```
┌─────────┐
│ pending │────complete───>│ done │
└─────────┘                 └──────┘
     ▲                         │
     │                         │
     └──────────X──────────────┘
        (no reverse transition)
```

- **Forward Transition**: Tasks can transition from `pending` to `done` via the complete operation
- **No Reverse**: Tasks CANNOT transition from `done` back to `pending` (per clarification Q1)
- **Idempotent**: Completing an already-done task is allowed (no-op, returns success)

**Lifecycle**:

1. **Creation**: Task is created via `add` command with user-provided title
2. **Active**: Task exists in `pending` status, visible in list output
3. **Completion**: Task transitions to `done` status via `complete` command
4. **Deletion**: Task is removed from storage via `delete` command (ID is not reused)

---

## Entity: TodoStore

**Purpose**: Manages the collection of tasks and provides operations for task manipulation.

**Attributes**:

| Attribute | Type | Description |
|-----------|------|-------------|
| `_tasks` | `list[Task]` | In-memory storage for all tasks (private) |
| `_next_id` | `int` | Counter for generating unique IDs (private) |

**Invariants**:

1. **ID Uniqueness**: No two tasks in `_tasks` may have the same ID
2. **Sorted Access**: Tasks returned by `list_tasks()` MUST be sorted by ID ascending
3. **Next ID Monotonic**: `_next_id` MUST only increase, never decrease
4. **Next ID Validity**: `_next_id` MUST always be greater than any existing task ID

**Operations**:

See contracts/ directory for detailed operation signatures and behaviors.

---

## Data Relationships

**Single Entity Model**:
- This MVP has only one entity type (Task)
- No relationships between entities (tasks are independent)
- No dependencies or hierarchies

**Container Relationship**:
- `TodoStore` contains zero or more `Task` instances
- Relationship is composition (tasks don't exist outside the store)
- No sharing of tasks between stores (single store instance per application session)

---

## Data Constraints

**Memory Constraints**:
- **Target Capacity**: Support at least 100 tasks (per success criteria SC-005)
- **Practical Limit**: No hard limit enforced for MVP (in-memory storage can handle thousands)
- **Title Size**: 1000 character limit per title prevents unbounded memory growth

**Performance Constraints**:
- **List Operation**: MUST display all tasks in under 3 seconds (per SC-002, SC-005)
- **Lookup Operation**: MUST find task by ID efficiently (current linear search is O(n), acceptable for <1000 tasks)

---

## Implementation Notes

**Type Safety**:
- All fields MUST have explicit type hints (per Constitution Principle IV)
- Use Python 3.12+ type annotation syntax (`list[Task]` not `List[Task]`)
- The `type-hint-enforcer` skill will validate compliance

**Mutability**:
- Task instances are mutable (to allow status updates)
- Direct attribute modification is allowed (e.g., `task.status = 'done'`)
- No immutability constraints for MVP

**Persistence**:
- Data exists only in memory during application lifetime
- All data is lost when the application exits (per Constitution Principle II)
- No serialization, database, or file storage in Phase 1

---

## Schema Definition (Dataclass)

**Reference Implementation**:

```python
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
        """Validate task attributes after initialization."""
        if not self.title or len(self.title) == 0:
            raise ValueError("Task title cannot be empty")
        if len(self.title) > 1000:
            raise ValueError("Task title cannot exceed 1000 characters")
        if self.status not in ('pending', 'done'):
            raise ValueError(f"Invalid status: {self.status}")
```

---

## Testing Considerations

**Unit Test Scenarios**:
1. Task creation with valid title
2. Task creation with empty title (should fail)
3. Task creation with very long title (>1000 chars, should fail)
4. Task status defaults to 'pending'
5. Task status can be updated to 'done'
6. Task status cannot be set to invalid value

**Integration Test Scenarios**:
1. Store generates unique IDs for each task
2. Store never reuses IDs after deletion
3. Store maintains sorted order by ID
4. Store handles empty list gracefully
5. Store handles 100+ tasks without performance degradation

---

## Future Considerations (Out of Scope for MVP)

- Task priority levels
- Task due dates or timestamps
- Task categories or tags
- Task descriptions (multi-line)
- Persistent storage (database, files)
- Task history or audit log
- Subtasks or task dependencies
