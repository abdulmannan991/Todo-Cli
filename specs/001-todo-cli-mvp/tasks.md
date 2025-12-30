# Tasks: In-Memory Python CLI Todo App MVP

**Input**: Design documents from `/specs/001-todo-cli-mvp/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL for this MVP - not included unless explicitly requested.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below use single project structure per plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directory structure with src/ and tests/ folders
- [X] T002 Create src/__init__.py to make src a Python package
- [X] T003 Verify Python 3.12+ installation with `python --version`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 [@logic-expert] Create Task dataclass in src/models.py with id: int, title: str, status: str fields and __post_init__ validation (SKILL: type-hint-enforcer)
- [X] T005 [@logic-expert] Verify Task dataclass default status is 'pending' and validation rejects empty titles (SKILL: spec-aligner against FR-003, FR-007)
- [X] T006 [@logic-expert] Create TodoStore class skeleton in src/store.py with _tasks: list[Task] and _next_id: int attributes (SKILL: type-hint-enforcer)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to add tasks with auto-generated IDs and pending status

**Independent Test**: Run add command with various titles, verify unique IDs and pending status

**Why This Is MVP**: Task creation is the foundational capability - without it, no other functionality has value.

### Implementation for User Story 1

- [X] T007 [@logic-expert] Implement TodoStore.add_task(title: str) -> Task in src/store.py with ID generation and task appending (SKILL: type-hint-enforcer, spec-aligner against FR-001, FR-002, FR-003)
- [X] T008 [@cli-expert] Create argparse parser skeleton in src/cli.py with add subcommand accepting title argument (SKILL: type-hint-enforcer against FR-010)
- [X] T009 [@cli-expert] Implement handle_add function in src/cli.py that calls store.add_task and prints confirmation message "Task {id} added: {title}" (SKILL: spec-aligner against FR-014)
- [X] T010 [@qa-specialist] Create src/main.py entry point that initializes TodoStore and routes add command to handle_add (SKILL: type-hint-enforcer)
- [X] T011 [@qa-specialist] Create todo.py executable script in project root that imports and calls src.main.main()
- [X] T012 [@qa-specialist] Manual test: Add task with simple title, verify ID=1, status=pending, confirmation message
- [X] T013 [@qa-specialist] Manual test: Add task with multi-word title, verify entire title captured without truncation
- [X] T014 [@qa-specialist] Manual test: Attempt to add empty title, verify error message and task not created (SKILL: spec-aligner against acceptance scenario US1.4)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. You can ship this as a minimal viable product!

---

## Phase 4: User Story 2 - View All Tasks (Priority: P2)

**Goal**: Display all tasks in a formatted table with ID, Title, and Status columns

**Independent Test**: Pre-populate tasks, run list command, verify table format with sorted tasks

**Why P2**: Viewing is essential to make captured tasks visible and useful.

### Implementation for User Story 2

- [X] T015 [@logic-expert] Implement TodoStore.list_tasks() -> list[Task] in src/store.py that returns tasks sorted by ID ascending (SKILL: type-hint-enforcer, spec-aligner against FR-004)
- [X] T016 [@cli-expert] Implement format_table function in src/cli.py with left-aligned columns, auto-width calculation, and ID sorting (SKILL: spec-aligner against FR-004 and clarification Q4)
- [X] T017 [@cli-expert] Add list subcommand to argparse parser in src/cli.py (no arguments required)
- [X] T018 [@cli-expert] Implement handle_list function in src/cli.py that calls store.list_tasks and prints formatted table (SKILL: spec-aligner against FR-004)
- [X] T019 [@qa-specialist] Update src/main.py to route list command to handle_list
- [X] T020 [@qa-specialist] Manual test: Add 5 tasks (3 pending, 2 done), run list, verify table format with all tasks sorted by ID
- [X] T021 [@qa-specialist] Manual test: Run list on empty store, verify "No tasks found" message
- [X] T022 [@qa-specialist] Manual test: Add tasks with varying title lengths, verify auto-width with no truncation (SKILL: spec-aligner against acceptance scenario US2.3)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. You can now add and view tasks!

---

## Phase 5: User Story 3 - Mark Tasks as Complete (Priority: P3)

**Goal**: Allow users to mark tasks as done by ID with one-way transition

**Independent Test**: Create pending task, mark complete, verify status changes to 'done'

**Why P3**: Completion tracking is core todo list value but depends on add and list being functional.

### Implementation for User Story 3

- [X] T023 [@logic-expert] Implement TodoStore.get_task(task_id: int) -> Task | None in src/store.py for ID lookup (SKILL: type-hint-enforcer)
- [X] T024 [@logic-expert] Implement TodoStore.complete_task(task_id: int) -> Task | None in src/store.py with one-way transition logic (SKILL: type-hint-enforcer, spec-aligner against FR-005 and clarification Q1)
- [X] T025 [@cli-expert] Add complete subcommand to argparse parser in src/cli.py with id argument (type=int for validation) (SKILL: spec-aligner against FR-013)
- [X] T026 [@cli-expert] Implement handle_complete function in src/cli.py that calls store.complete_task and prints "Task {id} marked as done" or error (SKILL: spec-aligner against FR-014)
- [X] T027 [@qa-specialist] Update src/main.py to route complete command to handle_complete
- [X] T028 [@qa-specialist] Manual test: Mark pending task as done, verify status changes and confirmation message
- [X] T029 [@qa-specialist] Manual test: Mark already-done task as done again, verify idempotent (no error) (SKILL: spec-aligner against acceptance scenario US3.2)
- [X] T030 [@qa-specialist] Manual test: Attempt to complete non-existent ID, verify "Task with ID X not found" error
- [X] T031 [@qa-specialist] Manual test: Attempt to complete with non-integer ID (e.g., "abc"), verify "Invalid ID format" error (SKILL: spec-aligner against FR-013 and clarification Q3)

**Checkpoint**: All core functionality (add, list, complete) should now be independently functional. This is a fully usable todo app!

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P4)

**Goal**: Enable task deletion by ID without reusing IDs

**Independent Test**: Create tasks, delete by ID, verify removal and ID non-reuse

**Why P4**: Deletion is nice-to-have for list maintenance but less critical than core features.

### Implementation for User Story 4

- [X] T032 [@logic-expert] Implement TodoStore.delete_task(task_id: int) -> bool in src/store.py that removes task but never reuses ID (SKILL: type-hint-enforcer, spec-aligner against FR-006, FR-012)
- [X] T033 [@cli-expert] Add delete subcommand to argparse parser in src/cli.py with id argument (type=int)
- [X] T034 [@cli-expert] Implement handle_delete function in src/cli.py that calls store.delete_task and prints "Task {id} deleted" or error (SKILL: spec-aligner against FR-014)
- [X] T035 [@qa-specialist] Update src/main.py to route delete command to handle_delete
- [X] T036 [@qa-specialist] Manual test: Delete task by ID, verify removal and confirmation message
- [X] T037 [@qa-specialist] Manual test: Delete task, add new task, verify new task gets non-reused ID (SKILL: spec-aligner against FR-012)
- [X] T038 [@qa-specialist] Manual test: Attempt to delete non-existent ID, verify "Task with ID X not found" error
- [X] T039 [@qa-specialist] Manual test: Delete single task, verify empty list shows "No tasks found" (SKILL: spec-aligner against acceptance scenario US4.3)

**Checkpoint**: All user stories should now be independently functional. Complete todo app with add, list, complete, and delete!

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements that affect multiple user stories and comprehensive validation

- [X] T040 [@qa-specialist] Comprehensive smoke test: Add 3 tasks, list, complete one, delete one, list again - verify all operations work correctly
- [X] T041 [@qa-specialist] Edge case test: Add task with special characters (e.g., "@john's code #urgent!"), verify stored correctly
- [X] T042 [@qa-specialist] Edge case test: Add task with 500+ character title, verify accepted (up to 1000 char limit)
- [X] T043 [@qa-specialist] Performance test: Add 100 tasks, run list command, verify completes in <3 seconds (SKILL: spec-aligner against SC-005)
- [X] T044 [@qa-specialist] In-memory verification test: Add tasks, exit app, restart, run list - verify data lost as expected (SKILL: spec-aligner against FR-011)
- [X] T045 [@qa-specialist] Error handling test: Test all error scenarios (empty title, negative IDs, non-integer IDs) - verify clear error messages (SKILL: spec-aligner against SC-006)
- [ ] T046 [@qa-specialist] Final spec compliance check: Verify all FR-001 through FR-014 satisfied using spec-aligner skill
- [ ] T047 [@qa-specialist] Final success criteria check: Verify all SC-001 through SC-008 met using spec-aligner skill
- [ ] T048 [@logic-expert] Final type-hint validation: Run type-hint-enforcer skill on all modules (models.py, store.py, cli.py, main.py)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1 - Add Tasks)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2 - View Tasks)**: Can start after Foundational (Phase 2) - Technically independent but more useful after US1
- **User Story 3 (P3 - Complete Tasks)**: Can start after Foundational (Phase 2) - Technically independent but requires US1+US2 for practical testing
- **User Story 4 (P4 - Delete Tasks)**: Can start after Foundational (Phase 2) - Technically independent but requires US1+US2 for practical testing

**Note**: While stories are technically independent after Foundational phase, practical value increases when implemented in priority order (P1→P2→P3→P4).

### Within Each User Story

- Implementation tasks can be partially parallel (models vs CLI in different files)
- Integration tasks depend on implementation completion
- Manual tests depend on integration being complete

### Parallel Opportunities

**Phase 2 (Foundational)**:
- T004 and T006 can run in parallel (different files: models.py vs store.py)

**Phase 3 (User Story 1)**:
- After T007 completes: T008-T009 can run in parallel with T010-T011 (CLI vs integration, different concerns)

**Phase 4 (User Story 2)**:
- After T015 completes: T016-T018 can run in parallel with T019 (CLI implementation vs main.py routing)

**Phase 5 (User Story 3)**:
- After T023-T024 complete: T025-T026 can run in parallel with T027 (CLI vs integration)

**Phase 6 (User Story 4)**:
- After T032 completes: T033-T034 can run in parallel with T035 (CLI vs integration)

**Phase 7 (Polish)**:
- T040-T045 (manual tests) can run in parallel
- T046-T047 (compliance checks) can run in parallel
- T048 (type validation) can run independently

---

## Parallel Example: User Story 1 Implementation

```bash
# After T007 (store.add_task) completes:

# Developer A can work on CLI:
Task: "T008 - Create argparse parser with add subcommand"
Task: "T009 - Implement handle_add function with confirmation message"

# WHILE Developer B works on integration:
Task: "T010 - Create main.py entry point with TodoStore initialization"
Task: "T011 - Create todo.py executable script"

# Then both converge for testing:
Task: "T012-T014 - Manual tests for User Story 1"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

**Fastest path to working product**:
1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T006) - CRITICAL
3. Complete Phase 3: User Story 1 (T007-T014)
4. **STOP and VALIDATE**: Test adding tasks independently
5. Ship as MVP if needed

**Result**: Basic todo app that can capture tasks (minimal but functional)

### Incremental Delivery (Recommended)

**Build value incrementally**:
1. Setup + Foundational (T001-T006) → Foundation ready
2. Add User Story 1 (T007-T014) → Test independently → **Deploy/Demo MVP!**
3. Add User Story 2 (T015-T022) → Test independently → **Deploy/Demo (now can view tasks!)**
4. Add User Story 3 (T023-T031) → Test independently → **Deploy/Demo (now can complete!)**
5. Add User Story 4 (T032-T039) → Test independently → **Deploy/Demo (full feature set!)**
6. Polish & Validate (T040-T048) → **Final production release**

Each story adds value without breaking previous stories.

### Parallel Team Strategy

**With multiple developers**:
1. Team completes Setup + Foundational together (T001-T006)
2. Once Foundational is done (after T006):
   - Developer A: User Story 1 (T007-T014)
   - Developer B: User Story 2 (T015-T022)
   - Developer C: User Story 3 (T023-T031)
   - Developer D: User Story 4 (T032-T039)
3. Stories complete and integrate independently
4. Team completes Polish together (T040-T048)

**Note**: While parallel development is possible, sequential (P1→P2→P3→P4) is recommended for solo developers to build and test incrementally.

---

## Skill Enforcement Summary

**CRITICAL**: The following skills are MANDATORY and must be explicitly invoked:

### type-hint-enforcer Skill (Type Safety Validation)

**Required for ALL code tasks**:
- T004: Task dataclass type hints
- T006: TodoStore class type hints
- T007: add_task method type hints
- T008: argparse parser type hints
- T010: main.py type hints
- T015: list_tasks method type hints
- T023: get_task method type hints
- T024: complete_task method type hints
- T032: delete_task method type hints
- T048: Final comprehensive type validation

### spec-aligner Skill (Requirements Compliance)

**Required for ALL implementation and testing tasks**:
- T005: Verify Task defaults and validation against FR-003, FR-007
- T007: Verify add_task against FR-001, FR-002, FR-003
- T009: Verify confirmation messages against FR-014
- T014: Verify error handling against acceptance scenario US1.4
- T015: Verify list_tasks against FR-004
- T016: Verify table formatting against FR-004 and clarification Q4
- T018: Verify list output against FR-004
- T022: Verify table auto-width against acceptance scenario US2.3
- T024: Verify one-way transition against FR-005 and clarification Q1
- T025: Verify ID validation against FR-013
- T026: Verify complete messages against FR-014
- T029: Verify idempotence against acceptance scenario US3.2
- T031: Verify error handling against FR-013 and clarification Q3
- T032: Verify ID non-reuse against FR-006, FR-012
- T034: Verify delete messages against FR-014
- T037: Verify ID non-reuse against FR-012
- T039: Verify empty list handling against acceptance scenario US4.3
- T043: Verify performance against SC-005
- T044: Verify in-memory behavior against FR-011
- T045: Verify error messages against SC-006
- T046: Final check of ALL FR-001 through FR-014
- T047: Final check of ALL SC-001 through SC-008

**Global Guardrail**: No task is considered "Done" until the `spec-aligner` skill confirms it matches the hackathon requirements (as specified in user input).

---

## Notes

- Tasks use strict checklist format: `- [ ] [TaskID] [P?] [Story?] Description with file path`
- [P] tasks can run in parallel (different files, no dependencies)
- [Story] labels (US1-US4) map to user stories from spec.md
- Each user story is independently completable and testable
- File paths are explicit for all code tasks
- Manual tests verify acceptance scenarios from spec.md
- Skills (type-hint-enforcer, spec-aligner) are explicitly referenced per user directives
- Tests are OPTIONAL for MVP (not included by default)
- Commit after completing each user story phase for clean history
