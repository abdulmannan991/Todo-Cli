# Feature Specification: In-Memory Python CLI Todo App MVP

**Feature Branch**: `001-todo-cli-mvp`
**Created**: 2025-12-30
**Status**: Draft
**Input**: User description: "In-Memory Python CLI Todo App with task creation, retrieval, completion, and deletion capabilities for Hackathon 2 Phase 1"

## Clarifications

### Session 2025-12-30

- Q: Can users mark a 'done' task back to 'pending' (e.g., if they uncomplete a task by mistake or need to redo it)? → A: One-way transition only (pending → done, no reversal)
- Q: Which data structure approach should @logic-expert use for storing tasks in memory? → A: Dataclass-based approach (e.g., `@dataclass class Task` with typed fields)
- Q: How should the system handle invalid ID inputs (non-integer values, negative numbers, or zero)? → A: Reject non-integers with error; accept negative/zero but report "not found"
- Q: How should the table be formatted when listing tasks? → A: Left-aligned columns, auto-width, sorted by ID ascending (oldest first)
- Q: What format should confirmation messages use for successful operations? → A: Simple descriptive format with key details (e.g., "Task [ID] added: [Title]")

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add New Tasks (Priority: P1)

As a user, I want to quickly add tasks to my todo list so that I can capture things I need to do without interrupting my workflow.

**Why this priority**: Task creation is the foundational capability. Without the ability to add tasks, no other functionality has value. This is the absolute minimum for a viable todo application.

**Independent Test**: Can be fully tested by running the add command with various task titles and verifying each task receives a unique ID and appears with 'pending' status. Delivers immediate value as a task capture tool.

**Acceptance Scenarios**:

1. **Given** an empty todo list, **When** I add a task with title "Buy groceries", **Then** the system assigns a unique ID (e.g., 1), sets status to 'pending', and displays confirmation "Task 1 added: Buy groceries"
2. **Given** a todo list with 3 existing tasks, **When** I add a task with title "Call dentist", **Then** the system assigns the next sequential ID (e.g., 4), sets status to 'pending', and displays confirmation "Task 4 added: Call dentist"
3. **Given** the command prompt, **When** I add a task with a multi-word title "Review Q4 budget proposal", **Then** the entire title is captured correctly without truncation
4. **Given** the command prompt, **When** I attempt to add a task with an empty title, **Then** the system displays an error message and does not create the task

---

### User Story 2 - View All Tasks (Priority: P2)

As a user, I want to see all my tasks in a clean, readable format so that I can quickly understand what I need to do and track my progress.

**Why this priority**: Viewing tasks is the second most critical feature. Users need to see what they've captured to make the todo list useful. Without this, tasks are added but invisible.

**Independent Test**: Can be tested by pre-populating the list with sample tasks and verifying the list command displays all tasks in a formatted table with ID, title, and status columns. Delivers value as a task overview tool.

**Acceptance Scenarios**:

1. **Given** a todo list with 5 tasks (3 pending, 2 done), **When** I run the list command, **Then** I see all 5 tasks displayed in a table format with columns for ID, Title, and Status, sorted by ID in ascending order
2. **Given** an empty todo list, **When** I run the list command, **Then** I see a message indicating "No tasks found" or an empty table with headers
3. **Given** a todo list with tasks of varying title lengths, **When** I run the list command, **Then** the table columns auto-adjust width to display all titles clearly (left-aligned, no truncation)
4. **Given** a todo list with both pending and done tasks, **When** I run the list command, **Then** I can easily distinguish between pending and done tasks based on the status column, with tasks ordered by ID (oldest to newest)

---

### User Story 3 - Mark Tasks as Complete (Priority: P3)

As a user, I want to mark tasks as done when I complete them so that I can track my progress and feel a sense of accomplishment.

**Why this priority**: Marking tasks complete provides the core value of a todo list - tracking what's been accomplished. This is essential but depends on P1 (adding) and P2 (viewing) being functional first.

**Independent Test**: Can be tested by creating a pending task, marking it complete by ID, and verifying the status changes to 'done' when viewing the list. Delivers value as a progress tracking tool.

**Acceptance Scenarios**:

1. **Given** a todo list with a pending task (ID: 2, Title: "Write report"), **When** I run the complete command with ID 2, **Then** the task status changes to 'done' and the system displays "Task 2 marked as done"
2. **Given** a todo list with a task already marked as 'done' (ID: 5), **When** I attempt to mark it complete again, **Then** the system confirms it's already done (idempotent operation, no error)
3. **Given** a todo list, **When** I attempt to mark a non-existent task ID (e.g., 999) as complete, **Then** the system displays an error message "Task with ID 999 not found"
4. **Given** a todo list, **When** I run the complete command without providing an ID, **Then** the system displays an error message explaining the required ID parameter

---

### User Story 4 - Delete Tasks (Priority: P4)

As a user, I want to remove tasks from my list so that I can keep my todo list focused on relevant items and clean up mistakes or obsolete tasks.

**Why this priority**: Deletion is a nice-to-have for the MVP but less critical than adding, viewing, and completing tasks. Users can work around its absence temporarily but it's valuable for list maintenance.

**Independent Test**: Can be tested by creating tasks, deleting them by ID, and verifying they no longer appear in the list. Delivers value as a list maintenance tool.

**Acceptance Scenarios**:

1. **Given** a todo list with 4 tasks, **When** I delete task ID 3, **Then** the task is removed from the list, the system displays "Task 3 deleted", and the remaining tasks (1, 2, 4) are still present with their original IDs
2. **Given** a todo list, **When** I attempt to delete a non-existent task ID (e.g., 888), **Then** the system displays an error message "Task with ID 888 not found"
3. **Given** a todo list with a single task (ID: 1), **When** I delete that task, **Then** the list becomes empty and subsequent list commands show "No tasks found"
4. **Given** a todo list, **When** I run the delete command without providing an ID, **Then** the system displays an error message explaining the required ID parameter

---

### Edge Cases

- What happens when a user adds a task with special characters (e.g., "Review @john's code #urgent!")?
  - Expected: The system accepts and stores the full title including special characters
- What happens when a user tries to add a very long task title (e.g., 500+ characters)?
  - Expected: The system accepts the title (reasonable assumption: no arbitrary limits for MVP, or accept up to 1000 characters)
- What happens when the user provides invalid input format for commands?
  - Expected: The system displays helpful error messages explaining correct usage
- What happens when the user provides non-integer ID values (e.g., "abc", "1.5")?
  - Expected: The system rejects with error message "Invalid ID format. Please provide a positive integer."
- What happens when the user provides negative or zero IDs (e.g., -1, 0)?
  - Expected: The system accepts the input but reports "Task with ID [X] not found"
- What happens when operations are performed on an empty list?
  - Expected: The system handles gracefully with appropriate messages (e.g., "No tasks to display")
- What happens if the user restarts the application?
  - Expected: All data is lost (acceptable for Phase 1 in-memory implementation, clearly documented)
- What happens when ID numbers get very large after many add/delete cycles?
  - Expected: IDs continue incrementing sequentially; system handles large integers without issues

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to add a new task with a title via command-line interface
- **FR-002**: System MUST assign a unique, auto-incrementing integer ID to each newly created task
- **FR-003**: System MUST set the default status of newly created tasks to 'pending'
- **FR-004**: System MUST display all tasks in a formatted table showing ID, Title, and Status columns (left-aligned, auto-width columns, sorted by ID in ascending order)
- **FR-005**: System MUST allow users to mark a task as 'done' by providing its unique ID (one-way transition only; tasks cannot be marked back to 'pending')
- **FR-006**: System MUST allow users to delete a task by providing its unique ID
- **FR-007**: System MUST validate that task titles are not empty (minimum 1 character) before creating a task
- **FR-008**: System MUST display clear error messages when operations fail (e.g., task not found, invalid ID format for non-integer inputs, empty title)
- **FR-009**: System MUST store all task data in-memory using Python data structures (no external databases or file persistence)
- **FR-010**: System MUST implement command-line interface using Python's argparse library with subcommands: add, list, complete, delete
- **FR-011**: System MUST handle the application lifecycle such that all data is lost when the program terminates (acceptable for Phase 1)
- **FR-012**: System MUST preserve ID uniqueness even after tasks are deleted (IDs should not be reused)
- **FR-013**: System MUST validate ID inputs for complete and delete operations: reject non-integer values with "Invalid ID format" error; accept negative/zero values but report "Task with ID [X] not found"
- **FR-014**: System MUST display confirmation messages for successful operations using the format: "Task [ID] added: [Title]" for add, "Task [ID] marked as done" for complete, "Task [ID] deleted" for delete

### Key Entities

- **Task**: Represents a single todo item with the following attributes:
  - **ID**: Unique integer identifier, auto-assigned, never reused
  - **Title**: Text description of the task (minimum 1 character, reasonable maximum 1000 characters assumed)
  - **Status**: Current state of the task, either 'pending' (default) or 'done'. Transitions are one-way only (pending → done); tasks cannot be reverted to pending once marked done

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add a new task in under 5 seconds by typing a single command
- **SC-002**: Users can view their complete task list in under 3 seconds with a single command
- **SC-003**: Users can mark a task complete in under 5 seconds by providing the task ID
- **SC-004**: Users can delete a task in under 5 seconds by providing the task ID
- **SC-005**: The application handles at least 100 tasks without performance degradation (list displays in under 3 seconds)
- **SC-006**: 95% of user actions result in clear, unambiguous feedback (success confirmations or error messages)
- **SC-007**: All core operations (add, list, complete, delete) function correctly on first use without requiring documentation
- **SC-008**: The application operates without requiring any external setup (databases, configuration files, etc.)

## Assumptions

The following assumptions were made to fill gaps in the requirements:

1. **Task Title Length**: Maximum task title length of 1000 characters is reasonable for typical use cases. No explicit limit was specified, so this prevents potential memory issues while being generous.

2. **ID Generation Strategy**: IDs increment sequentially starting from 1 and are never reused, even after deletion. This is the simplest approach for MVP and ensures uniqueness.

3. **Status Values**: Only two status values are needed for MVP: 'pending' and 'done'. Additional statuses (in-progress, blocked, etc.) are not required for hackathon Phase 1.

4. **Command Syntax**: Standard CLI patterns will be used:
   - `python todo.py add "Task title"`
   - `python todo.py list`
   - `python todo.py complete <id>`
   - `python todo.py delete <id>`

5. **Error Handling**: User-friendly error messages are sufficient; no logging to files or advanced error tracking needed for MVP.

6. **Performance**: Target response times assume local execution on modern hardware (last 5 years). The in-memory approach should easily meet performance criteria with <1000 tasks.

7. **Character Encoding**: UTF-8 encoding is assumed for task titles to support international characters and emojis.

8. **Concurrency**: No concurrent access patterns need to be handled (single-user, single-process application).

## Agentic Delegation Notes

This specification defines WHAT users need. The HOW will be delegated as follows during implementation planning and execution:

- **@logic-expert**: Will design the in-memory data structures using a dataclass-based approach (`@dataclass class Task` with typed fields stored in a `List[Task]`), ID generation logic, and state transition rules to ensure strict adherence to in-memory storage requirements per the Constitution.

- **@cli-expert**: Will design the argparse command structure, help messages, and table formatting for the list output (left-aligned columns, auto-width adjustment, sorted by ID ascending) using appropriate terminal formatting techniques.

- **@qa-specialist**: Will validate the implementation against this specification, test edge cases (empty titles, non-existent IDs, special characters), and ensure all functional requirements and success criteria are met before marking the feature complete.

All function signatures in the implementation MUST include strict type hints validated by the `type-hint-enforcer` skill as mandated by the Constitution.
