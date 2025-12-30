# Edit Task Title Feature - User Guide

## Overview
The Todo CLI now includes a **Edit Task Title** feature that allows you to modify the title of existing tasks without affecting their status or ID.

## Updated Interactive Menu

```
==============================
   TODO APPLICATION
==============================

1. Add Task
2. View Tasks
3. Update Task (Complete)
4. Delete Task
5. Edit Task Title          ← NEW FEATURE
6. Exit
```

## How to Use Edit Task Title

### Step-by-Step Instructions

1. **Start the interactive menu:**
   ```bash
   python todo.py
   ```

2. **Select option 5:**
   ```
   Enter your choice: 5
   ```

3. **Enter the task ID you want to edit:**
   ```
   Enter task ID to edit: 1
   ```

4. **Enter the new title:**
   ```
   Enter new title: Updated task title
   ```

5. **See success confirmation:**
   ```
   Task 1 title updated successfully!
   ```

## Example Session

```
==============================
   TODO APPLICATION
==============================

1. Add Task
2. View Tasks
3. Update Task (Complete)
4. Delete Task
5. Edit Task Title
6. Exit

Enter your choice: 1
Enter task title: Buy groceries
Task 1 added successfully: Buy groceries

==============================
   TODO APPLICATION
==============================

1. Add Task
2. View Tasks
3. Update Task (Complete)
4. Delete Task
5. Edit Task Title
6. Exit

Enter your choice: 5
Enter task ID to edit: 1
Enter new title: Buy groceries and milk
Task 1 title updated successfully!

==============================
   TODO APPLICATION
==============================

1. Add Task
2. View Tasks
3. Update Task (Complete)
4. Delete Task
5. Edit Task Title
6. Exit

Enter your choice: 2

ID | Title                    | Status
═════════════════════════════════════
1  | Buy groceries and milk   | pending

==============================
   TODO APPLICATION
==============================

1. Add Task
2. View Tasks
3. Update Task (Complete)
4. Delete Task
5. Edit Task Title
6. Exit

Enter your choice: 6
Goodbye!
```

## Features

### ✅ What Edit Task Does
- Updates the title of an existing task
- Preserves the task ID (no ID changes)
- Preserves the task status (done/pending unchanged)
- Validates the new title (same rules as task creation)
- Works with tasks in any status (pending or done)

### ❌ What Edit Task Does NOT Do
- Does NOT change the task ID
- Does NOT change the task status (use option 3 to mark complete)
- Does NOT delete the task (use option 4 to delete)
- Does NOT accept empty titles
- Does NOT accept titles longer than 1000 characters

## Validation & Error Handling

### Empty Title
```
Enter task ID to edit: 1
Enter new title:
Error: Task title cannot be empty
```

### Non-Existent Task ID
```
Enter task ID to edit: 999
Enter new title: Some title
Error: Task with ID 999 not found
```

### Invalid ID Format
```
Enter task ID to edit: abc
Error: Invalid ID format. Please provide a positive integer.
```

### Title Too Long (>1000 characters)
```
Enter task ID to edit: 1
Enter new title: [1001 character string]
Error: Task title cannot exceed 1000 characters
```

## Technical Details

### Implementation
- **Method**: `update_task_title(task_id: int, new_title: str) -> Optional[Task]` in `src/store.py`
- **Type Safety**: All functions include strict type hints
- **Validation**: Enforces same title rules as task creation
- **In-Memory**: Changes persist within the session (in-memory store)
- **Separation**: Completely separate from "Mark Complete" operation

### Color Scheme
- **Prompts**: Bold Yellow (matches existing theme)
- **Success Messages**: Bright Green
- **Error Messages**: Bright Red

### Return Values
- **Success**: Returns updated Task object
- **Not Found**: Returns None
- **Invalid Title**: Raises ValueError

## Use Cases

1. **Fix Typos**
   ```
   Original: "Buy groseries"
   Updated:  "Buy groceries"
   ```

2. **Add Details**
   ```
   Original: "Call dentist"
   Updated:  "Call dentist for 3pm appointment"
   ```

3. **Clarify Tasks**
   ```
   Original: "Work on report"
   Updated:  "Complete Q4 financial report"
   ```

4. **Update Requirements**
   ```
   Original: "Buy 2 notebooks"
   Updated:  "Buy 5 notebooks"
   ```

## Important Notes

- ✅ **Preserves Status**: Editing a "done" task keeps it marked as done
- ✅ **Preserves ID**: Task IDs never change, even after editing
- ✅ **Immediate Feedback**: Success/error messages display instantly
- ✅ **Special Characters**: Supports special characters (@, #, ', etc.)
- ✅ **Backward Compatible**: All existing features (Add, View, Complete, Delete) work unchanged

## Testing

Comprehensive test suite included:
- ✅ 14 edit-specific tests (all pass)
- ✅ 9 regression tests (all pass)
- ✅ Validates no breaking changes to existing functionality

## Comparison: Edit vs Complete

| Feature | Edit Task Title (Option 5) | Update Task Complete (Option 3) |
|---------|---------------------------|----------------------------------|
| Purpose | Change task description | Mark task as done |
| Prompts | ID + New Title | ID only |
| Changes Title | ✅ Yes | ❌ No |
| Changes Status | ❌ No | ✅ Yes (to "done") |
| Changes ID | ❌ No | ❌ No |
| Validation | Title rules | ID only |

Both operations are completely separate and serve different purposes.
