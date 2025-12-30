# Interactive Menu Mode - Demo Guide

## Overview
The Todo CLI now supports an **Interactive Menu Mode** that automatically starts when you run the application without arguments.

## How to Use

### Start Interactive Mode
Simply run the application without any arguments:
```bash
python todo.py
```

### Menu Display
You'll see a stylized menu:
```
==============================
   TODO APPLICATION
==============================

1. Add Task
2. View Tasks
3. Update Task (Complete)
4. Delete Task
5. Exit

Enter your choice:
```

### Menu Options

#### 1. Add Task
- Prompts: `Enter task title:`
- Enter any non-empty task title
- Success: `Task 1 added successfully: Your task title` (in green)
- Error: `Error: Task title cannot be empty` (in red)

#### 2. View Tasks
- Displays formatted table with all tasks
- Shows ID, Title, and Status columns
- Status color-coded:
  - **pending**: Bold Yellow
  - **done**: Dim Gray
- Empty list: `No tasks found`

#### 3. Update Task (Complete)
- Prompts: `Enter task ID to complete:`
- Enter task ID number
- Success: `Task 1 marked as done` (in green)
- Error: `Error: Task with ID X not found` (in red)
- Invalid ID: `Error: Invalid ID format. Please provide a positive integer.` (in red)

#### 4. Delete Task
- Prompts: `Enter task ID to delete:`
- Enter task ID number
- Success: `Task 1 deleted successfully` (in green)
- Error: `Error: Task with ID X not found` (in red)
- Invalid ID: `Error: Invalid ID format. Please provide a positive integer.` (in red)

#### 5. Exit
- Displays: `Goodbye!` (in green)
- Returns to command prompt

## Color Scheme

- **Menu Headers**: Cyan Bold
- **Success Messages**: Bright Green
- **Error Messages**: Bright Red
- **Prompts**: Bold Yellow
- **Done Tasks**: Dim Gray
- **Pending Tasks**: Bold Yellow

## Example Session

```
==============================
   TODO APPLICATION
==============================

1. Add Task
2. View Tasks
3. Update Task (Complete)
4. Delete Task
5. Exit

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
5. Exit

Enter your choice: 1
Enter task title: Call dentist
Task 2 added successfully: Call dentist

==============================
   TODO APPLICATION
==============================

1. Add Task
2. View Tasks
3. Update Task (Complete)
4. Delete Task
5. Exit

Enter your choice: 2

ID | Title          | Status
════════════════════════════════
1  | Buy groceries  | pending
2  | Call dentist   | pending

==============================
   TODO APPLICATION
==============================

1. Add Task
2. View Tasks
3. Update Task (Complete)
4. Delete Task
5. Exit

Enter your choice: 3
Enter task ID to complete: 1
Task 1 marked as done

==============================
   TODO APPLICATION
==============================

1. Add Task
2. View Tasks
3. Update Task (Complete)
4. Delete Task
5. Exit

Enter your choice: 2

ID | Title          | Status
════════════════════════════════
1  | Buy groceries  | done (gray)
2  | Call dentist   | pending (yellow)

==============================
   TODO APPLICATION
==============================

1. Add Task
2. View Tasks
3. Update Task (Complete)
4. Delete Task
5. Exit

Enter your choice: 5
Goodbye!
```

## Command-Line Mode Still Available

The traditional command-line mode is still fully functional:

```bash
# Add a task
python todo.py add "Write report"

# List all tasks
python todo.py list

# Complete a task
python todo.py complete 1

# Delete a task
python todo.py delete 2
```

## Technical Details

### Implementation
- **Function**: `start_interactive_mode(store: TodoStore) -> int` in `src/cli.py`
- **Auto-detect**: `main.py` checks `len(sys.argv) == 1` to trigger interactive mode
- **Type Safety**: All functions include strict type hints
- **In-Memory**: Store persists across menu operations within single session
- **Backward Compatible**: Command-line mode works unchanged

### Error Handling
- Empty task titles rejected
- Invalid ID formats caught (non-integers)
- Non-existent task IDs handled gracefully
- Invalid menu choices prompt re-entry (no crash)

### Testing
- Comprehensive test suite: `test_interactive.py`
- 10 test scenarios covering all operations
- All tests passing ✅
