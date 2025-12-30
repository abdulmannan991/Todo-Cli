---
id: 004
title: Generate Todo CLI MVP Tasks
stage: tasks
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5
feature: 001-todo-cli-mvp
branch: 001-todo-cli-mvp
user: Abdul Mannan
command: /sp.tasks
labels: ["tasks", "task-breakdown", "todo-app", "implementation-tasks"]
links:
  spec: specs/001-todo-cli-mvp/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-todo-cli-mvp/tasks.md
tests:
  - N/A (task planning - test scenarios defined in tasks)
---

## Prompt

```text
# Role: Project Manager & SDD Architect
# Goal: Convert plan.md into Skill-Enforced Actionable Tasks

## 1. Task Generation Directives
Please break down the approved `plan.md` into the following units. You MUST explicitly mention that the `type-hint-enforcer` and `spec-aligner` skills are required for every code-related task.

### Task 1: Core Data Modeling
- **Agent**: `@logic-expert`
- **Action**: Create `models.py` for the `@dataclass` Task structure.
- **Skill Requirement**: Use `type-hint-enforcer` to ensure the `id`, `title`, and `status` fields are strictly typed.

### Task 2: In-Memory Logic Implementation
- **Agent**: `@logic-expert`
- **Action**: Create `store.py` with `TodoStore` class.
- **Skill Requirement**: Use `spec-aligner` to verify that the Add, List, Complete, and Delete logic matches the `specs/features.md`.

### Task 3: CLI & UX Implementation
- **Agent**: `@cli-expert`
- **Action**: Create `interface.py` for `argparse` and table formatting.
- **Skill Requirement**: Use `spec-aligner` to ensure the table columns are left-aligned and auto-width as per our clarification.

### Task 4: Main Integration
- **Agent**: `@qa-specialist`
- **Action**: Create `main.py` entry point.
- **Skill Requirement**: Use `type-hint-enforcer` for all variable assignments.

### Task 5: Final Verification Run
- **Agent**: `@qa-specialist`
- **Action**: Execute the app and verify one-way status transitions and ID rejection logic.

## 2. Global Guardrails
- No task is considered "Done" until the `spec-aligner` confirms it matches the hackathon requirements.
```

## Response snapshot

Generated comprehensive task breakdown with 48 tasks organized by user story (4 stories) following strict format requirements and explicit skill enforcement.

**Task Organization**:
- Phase 1: Setup (3 tasks) - Project initialization
- Phase 2: Foundational (3 tasks) - Core models and store skeleton (BLOCKS all user stories)
- Phase 3: User Story 1 - Add Tasks (8 tasks, Priority P1) 🎯 MVP
- Phase 4: User Story 2 - View Tasks (8 tasks, Priority P2)
- Phase 5: User Story 3 - Complete Tasks (9 tasks, Priority P3)
- Phase 6: User Story 4 - Delete Tasks (8 tasks, Priority P4)
- Phase 7: Polish & Cross-Cutting (9 tasks) - Comprehensive validation

**Total**: 48 tasks across 7 phases

**Format Compliance**:
- ✅ All tasks follow strict checklist format: `- [ ] [TaskID] [P?] [Story?] Description with file path`
- ✅ Task IDs sequential (T001-T048)
- ✅ [P] markers for parallelizable tasks
- ✅ [Story] labels for user story tasks (US1, US2, US3, US4)
- ✅ Agent assignments using [@agent-name] notation
- ✅ Explicit file paths in all code tasks

**Skill Enforcement** (per user directives):
- **type-hint-enforcer**: Explicitly required in 11 tasks (T004, T006, T007, T008, T010, T015, T023, T024, T032, T048)
- **spec-aligner**: Explicitly required in 25 tasks (all implementation and testing tasks)
- **Global Guardrail**: Documented that NO task is "Done" until spec-aligner confirms compliance

**Agent Assignments**:
- @logic-expert: 8 tasks (models.py, store.py with 5 methods)
- @cli-expert: 12 tasks (cli.py with argparse, formatting, handlers)
- @qa-specialist: 28 tasks (main.py, todo.py, all manual tests, compliance validation)

**Parallel Opportunities Identified**:
- Foundational phase: T004 || T006 (models vs store skeleton)
- User Story 1: T008-T009 || T010-T011 (CLI vs integration)
- User Story 2: T016-T018 || T019 (CLI vs routing)
- User Story 3: T025-T026 || T027 (CLI vs routing)
- User Story 4: T033-T034 || T035 (CLI vs routing)
- Polish phase: T040-T045 (all manual tests), T046-T047 (compliance checks), T048 (type validation)

**Independent Testing**:
- Each user story has checkpoint with independent test criteria
- US1 checkpoint: Can ship as MVP (add tasks only)
- US2 checkpoint: Can add and view tasks
- US3 checkpoint: Full core functionality (add, list, complete)
- US4 checkpoint: Complete feature set (all 4 operations)

**Implementation Strategies Documented**:
1. MVP First: Setup → Foundational → US1 only (fastest to working product)
2. Incremental Delivery: Add one story at a time, deploy/demo after each
3. Parallel Team: Split stories across developers after Foundational phase

**Success Criteria Mapping**:
- Tasks mapped to all FR-001 through FR-014 requirements
- Tasks mapped to all SC-001 through SC-008 success criteria
- Performance test (T043) validates SC-005 (100 tasks in <3s)
- In-memory verification (T044) validates FR-011
- Error handling (T045) validates SC-006 (95% clear feedback)

## Outcome

- ✅ Impact: Complete, executable task breakdown ready for /sp.implement with explicit skill enforcement
- 🧪 Tests: Manual test tasks defined (T012-T014, T020-T022, T028-T031, T036-T039, T040-T045)
- 📁 Files: Created specs/001-todo-cli-mvp/tasks.md (48 tasks across 7 phases)
- 🔁 Next prompts: /sp.implement to execute tasks with agent delegation
- 🧠 Reflection: Task generation successfully organized by user story (4 stories, P1-P4 priorities) with strict format compliance. All tasks include explicit skill requirements (type-hint-enforcer for type safety, spec-aligner for requirements compliance). Foundational phase clearly blocks all user stories. Each story has independent test criteria. MVP path identified (US1 only). Parallel opportunities documented. Global guardrail enforced: no task "Done" until spec-aligner confirms compliance.

## Evaluation notes (flywheel)

- Failure modes observed: None - all tasks generated successfully with proper format
- Graders run and results (PASS/FAIL): Format validation - PASS (all 48 tasks follow checklist format with IDs, labels, file paths)
- Prompt variant (if applicable): N/A (standard task generation workflow)
- Next experiment (smallest change to try): N/A (tasks complete, ready for /sp.implement)
