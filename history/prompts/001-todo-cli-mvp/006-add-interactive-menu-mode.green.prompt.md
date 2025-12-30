---
id: 006
title: Add Interactive Menu Mode to Todo CLI
stage: green
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5
feature: 001-todo-cli-mvp
branch: 001-todo-cli-mvp
user: wajiz.pk
command: sp.implement
labels: ["interactive-mode", "menu-ui", "ux-enhancement", "ansi-colors", "type-hints"]
links:
  spec: specs/001-todo-cli-mvp/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - src/cli.py
  - src/main.py
  - test_interactive.py
tests:
  - Test 1: Interactive mode started successfully
  - Test 2: Menu header displayed
  - Test 3: Task 1 added successfully
  - Test 4: Task 2 added successfully
  - Test 5: Task list shows 'Buy groceries'
  - Test 6: Task completion message shown
  - Test 7: Task deletion message shown
  - Test 8: Exit message displayed
  - Test 9: Exit code is 0 (success)
  - Test 10: Command-line mode still works with arguments
---

## Prompt

Implement an "Interactive Mode" that mimics a menu-driven structure for the Todo App.

**Feature Requirement:**
- Add Interactive Menu Mode with continuous loop until user exits

**UI Design Specifications:**
- Menu Display: Header labeled "=== TODO APPLICATION ==="
- Numbered Options:
  1. Add Task
  2. View Tasks
  3. Update Task (Optional/Complete)
  4. Delete Task
  5. Exit
- Styling:
  - Cyan or Bold White for menu headers
  - Bright Green for success messages ("Task added successfully")
  - Bold Yellow for "Enter your choice" prompt
  - Use existing ANSI color logic from Colors class

**Implementation Instructions:**
- @cli-expert: Create `start_interactive_mode()` function in `cli.py` with `while True` loop
- @logic-expert: Ensure TodoStore methods are correctly called by menu choices
- @qa-specialist: Update `main.py` so that if no command-line arguments are provided, the app automatically starts Interactive Menu

**Skill Enforcement:**
- type-hint-enforcer: Apply strict typing to menu handling functions
- spec-aligner: Ensure interactive mode follows In-Memory constraint from Constitution

## Response snapshot

Successfully implemented Interactive Menu Mode with all required features:

**@cli-expert Implementation:**
- Added CYAN color constant to Colors class: '\033[96m' (Bright Cyan)
- Created `start_interactive_mode(store: TodoStore) -> int` function in src/cli.py
- Implemented continuous menu loop with 5 options:
  1. Add Task: Prompts for title, validates non-empty, calls store.add_task()
  2. View Tasks: Calls store.list_tasks() and displays formatted table
  3. Update Task (Complete): Prompts for ID, validates integer, calls store.complete_task()
  4. Delete Task: Prompts for ID, validates integer, calls store.delete_task()
  5. Exit: Displays "Goodbye!" and returns 0
- Menu styling:
  - Cyan bold header with "===" borders (30 characters wide)
  - Yellow prompt for "Enter your choice"
  - Green success messages ("Task X added successfully")
  - Red error messages for invalid input
- Input validation:
  - Empty titles rejected with error message
  - Invalid ID formats caught with try/except ValueError
  - Invalid menu choices (not 1-5) display error
- All methods include strict type hints per type-hint-enforcer skill

**@logic-expert Verification:**
- TodoStore methods correctly integrated:
  - add_task(title: str) -> Task: Called on option 1
  - list_tasks() -> list[Task]: Called on option 2
  - complete_task(task_id: int) -> Optional[Task]: Called on option 3
  - delete_task(task_id: int) -> bool: Called on option 4
- All return values properly handled (None checks for get/complete, bool for delete)
- In-memory constraint maintained: Same TodoStore instance persists across menu loop

**@qa-specialist Implementation:**
- Updated src/main.py to detect no arguments: `if len(sys.argv) == 1:`
- When no args: Automatically calls `start_interactive_mode(store)`
- When args present: Uses existing argparse command-line mode
- Store initialization moved before argument check (single instance for both modes)
- Created comprehensive test_interactive.py with 10 test scenarios
- All 10 tests passed:
  ✓ Interactive mode starts
  ✓ Menu header displays
  ✓ Tasks added successfully
  ✓ Task list displays correctly
  ✓ Task completion works
  ✓ Task deletion works
  ✓ Exit message shows
  ✓ Exit code is 0
  ✓ Command-line mode still functional

**Key Technical Decisions:**
- Menu loop continues until user chooses option 5 (Exit)
- Each operation provides immediate feedback (success/error message)
- Invalid choices display error but don't exit (user-friendly)
- Store persists across all menu operations within single session
- Command-line mode remains fully functional when arguments provided
- Backward compatible: Existing CLI commands work unchanged

**Verification Results:**
✅ Interactive mode starts when `python todo.py` run with no args
✅ Menu displays with cyan header and 5 options
✅ Add task validates empty titles
✅ View tasks shows formatted table with colors
✅ Complete task validates ID format and existence
✅ Delete task validates ID format and existence
✅ Exit displays goodbye message and returns 0
✅ Invalid menu choices handled gracefully
✅ Command-line mode (`python todo.py add "task"`) still works
✅ All type hints enforced throughout

## Outcome

- ✅ Impact: Added user-friendly Interactive Menu Mode that automatically starts when no arguments provided. Menu-driven interface provides better UX for users unfamiliar with CLI arguments. Both interactive and command-line modes coexist seamlessly.
- 🧪 Tests: Created test_interactive.py with 10 comprehensive test scenarios covering menu display, all operations, error handling, and backward compatibility. All tests passed successfully.
- 📁 Files: 3 files modified/created (src/cli.py: added start_interactive_mode() + CYAN color, src/main.py: added auto-detect logic, test_interactive.py: comprehensive tests).
- 🔁 Next prompts: Optional: Add confirmation prompts for destructive operations (delete). Optional: Add option to return to menu after viewing tasks. Optional: Add help text for each menu option.
- 🧠 Reflection: Implementation successfully enhances UX while maintaining backward compatibility. The menu-driven approach makes the app more accessible to non-technical users. Strict type hints and error handling ensure robustness. In-memory constraint preserved as required by Constitution.

## Evaluation notes (flywheel)

- Failure modes observed: None. Implementation worked correctly on first attempt. All tests passed.
- Graders run and results (PASS/FAIL): Type-hint-enforcer: PASS (all new functions include strict type hints). Spec-aligner: PASS (in-memory constraint maintained, no external persistence). Integration tests: 10/10 PASS.
- Prompt variant (if applicable): Original prompt from sp.implement command with interactive menu requirements
- Next experiment (smallest change to try): Consider adding color customization options via environment variables. Consider adding readline support for better input editing (up/down arrow for history).
