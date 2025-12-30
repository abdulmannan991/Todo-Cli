---
id: 007
title: Add Edit Task Title Feature
stage: green
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5
feature: 001-todo-cli-mvp
branch: 001-todo-cli-mvp
user:  Abdul Mannan
command: sp.implement
labels: ["edit-feature", "task-update", "cli-enhancement", "type-hints", "validation"]
links:
  spec: specs/001-todo-cli-mvp/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - src/store.py
  - src/cli.py
  - test_edit_task.py
tests:
  - Test 1: Tasks added successfully
  - Test 2: Task title updated successfully
  - Test 3: Update persisted correctly
  - Test 4: Non-existent task handled correctly
  - Test 5: Empty title rejected
  - Test 6: Title length validation works
  - Test 7: Multiple updates work correctly
  - Test 8: Update doesn't affect status
  - Test 9: Update doesn't affect ID
  - Test 10: Special characters work
  - Test 11: Edit Task option appears in menu
  - Test 12: Edit success message displayed
  - Test 13: Updated title appears in task list
  - Test 14: Exit code is 0
  - Regression: All 9 existing tests still pass
---

## Prompt

Add a 'Full Edit' feature to the Todo App with a new menu option separate from "Mark Complete".

**Functional Requirements:**
- Add new menu option: "6. Edit Task Title" (separate from Mark Complete)

**Logic Implementation (@logic-expert):**
- Method: Create `update_task_title(task_id: int, new_title: str)` in `store.py`
- Validation: If ID not found, return None; display error in Bright Red
- Persistence: Ensure change is updated in in-memory dataclass list
- Title validation: Apply same rules as task creation (non-empty, 1-1000 chars)

**UI Implementation (@cli-expert):**
- Menu Update: Add "5. Edit Task Title" to main interactive loop
- Renumber "Exit" option to "6. Exit"
- User Flow:
  1. Prompt: "Enter task ID to edit:" (Bold Yellow)
  2. Prompt: "Enter new title:" (Bold Yellow)
  3. Success message in Bright Green: "Task [ID] title updated successfully!"
  4. Error messages in Bright Red for invalid ID or empty title
- Styling: Input prompts in Bold Yellow to match existing theme

**Skill Enforcement:**
- type-hint-enforcer: Apply strict typing to new update method
- spec-aligner: Ensure new feature doesn't break existing "Mark Complete" or "Delete" logic

## Response snapshot

Successfully implemented Edit Task Title feature with comprehensive validation and testing:

**@logic-expert Implementation:**
- Created `update_task_title(task_id: int, new_title: str) -> Optional[Task]` in src/store.py
- Method signature includes strict type hints per type-hint-enforcer
- Validation logic:
  - Returns None if task_id not found (consistent with complete_task)
  - Raises ValueError if new_title is empty
  - Raises ValueError if new_title exceeds 1000 characters
  - Applies same validation rules as Task.__post_init__
- Implementation details:
  - Calls get_task(task_id) to retrieve task
  - Validates new_title before applying
  - Updates task.title directly (in-memory modification)
  - Returns updated Task object for success confirmation
- In-memory persistence verified: Changes persist within TodoStore instance
- Does not affect task.id or task.status (only modifies task.title)

**@cli-expert Implementation:**
- Updated interactive menu in src/cli.py:
  - Changed menu from 1-5 options to 1-6 options
  - Added "5. Edit Task Title" option
  - Renumbered "Exit" from option 5 to option 6
  - Updated validation message: "Please select 1-6" (was 1-5)
- User flow implementation:
  - Prompt 1: "Enter task ID to edit:" with Bold Yellow styling
  - Prompt 2: "Enter new title:" with Bold Yellow styling
  - Success: "Task {id} title updated successfully!" in Bright Green
  - Error handling:
    - Empty title: "Error: Task title cannot be empty" in Bright Red
    - Non-existent ID: "Error: Task with ID {id} not found" in Bright Red
    - Invalid ID format: "Error: Invalid ID format. Please provide a positive integer." in Bright Red
    - Title > 1000 chars: "Error: Task title cannot exceed 1000 characters" in Bright Red
- Input validation:
  - Empty titles caught before calling store method (immediate feedback)
  - Invalid ID formats caught with try/except ValueError
  - ValueError messages from store.update_task_title() properly displayed
- Strict type hints applied throughout:
  - `task_id_str: str`
  - `task_id: int`
  - `new_title: str`
  - `result: Optional[Task]`

**@qa-specialist Testing:**
- Created comprehensive test_edit_task.py with 14 test scenarios:
  1. Tasks added successfully ✓
  2. Task title updated successfully ✓
  3. Update persisted correctly ✓
  4. Non-existent task handled correctly ✓
  5. Empty title rejected with ValueError ✓
  6. Title length validation (>1000 chars) works ✓
  7. Multiple updates work correctly ✓
  8. Update doesn't affect task status ✓
  9. Update doesn't affect task ID ✓
  10. Special characters in title work ✓
  11. Edit Task option appears in menu ✓
  12. Edit success message displayed ✓
  13. Updated title appears in task list ✓
  14. Exit code is 0 ✓
- All 14 tests passed successfully
- Regression testing: Ran existing test_todo.py - all 9 tests still pass ✓
- Verified existing functionality unaffected:
  - Add Task: Still works ✓
  - View Tasks: Still works ✓
  - Mark Complete: Still works ✓
  - Delete Task: Still works ✓
  - Command-line mode: Still works ✓

**Key Technical Decisions:**
- Edit is separate operation from Complete (different menu option)
- Title validation reuses same rules as task creation (consistency)
- Returns Optional[Task] to match pattern of complete_task()
- Empty title check done in CLI before calling store (better UX)
- ValueError exceptions properly caught and displayed to user
- In-memory modification of existing Task dataclass instance
- No ID reuse, no status change, only title modification

**Verification Results:**
✅ update_task_title method created with strict type hints
✅ Title validation enforces non-empty and ≤1000 chars
✅ Non-existent task IDs return None (not crash)
✅ Interactive menu shows option "5. Edit Task Title"
✅ Exit option correctly renumbered to 6
✅ Bold Yellow prompts for user input
✅ Bright Green success message for successful edit
✅ Bright Red error messages for all error cases
✅ Update persists in memory within session
✅ Update doesn't affect task ID or status
✅ Special characters handled correctly
✅ Multiple edits work correctly
✅ Empty titles rejected before store call
✅ All existing tests still pass (no regression)

## Outcome

- ✅ Impact: Added full task title editing capability as new menu option (separate from Mark Complete). Users can now correct typos, update task descriptions, and refine task titles without deleting and recreating tasks. Feature maintains strict validation and error handling consistent with existing operations.
- 🧪 Tests: Created test_edit_task.py with 14 comprehensive test scenarios covering update success, validation, persistence, edge cases, and interactive menu integration. All tests passed. Regression testing confirmed all 9 existing tests still pass.
- 📁 Files: 3 files modified/created (src/store.py: added update_task_title() method, src/cli.py: added menu option 5 and handler, test_edit_task.py: comprehensive tests).
- 🔁 Next prompts: Optional: Add bulk edit capability (edit multiple tasks). Optional: Add confirmation prompt before editing. Optional: Show previous title before prompting for new title.
- 🧠 Reflection: Implementation successfully adds edit functionality without breaking existing features. Strict separation between Edit and Complete operations maintains clarity. Type hints and validation ensure robustness. In-memory constraint preserved. All error cases handled gracefully with user-friendly messages.

## Evaluation notes (flywheel)

- Failure modes observed: None. Implementation worked correctly on first attempt. All tests passed including regression tests.
- Graders run and results (PASS/FAIL): Type-hint-enforcer: PASS (all new functions include strict type hints). Spec-aligner: PASS (no regression - existing Complete and Delete logic unaffected, all 9 original tests still pass). Validation tests: 14/14 PASS.
- Prompt variant (if applicable): Original prompt from sp.implement command with edit task requirements
- Next experiment (smallest change to try): Consider adding undo/redo functionality for edits. Consider adding edit history tracking (store previous titles). Consider adding "preview changes" before confirming edit.
