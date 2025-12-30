# Implementation Plan: In-Memory Python CLI Todo App MVP

**Branch**: `001-todo-cli-mvp` | **Date**: 2025-12-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-todo-cli-mvp/spec.md`

## Summary

Build a minimal viable product (MVP) todo application with an in-memory Python CLI interface supporting four core operations: add, list, complete, and delete tasks. The implementation follows a strict Store-View separation pattern with dataclass-based models, leveraging specialized agents (@logic-expert, @cli-expert, @qa-specialist) for domain-specific implementation tasks. All data persists in memory only (no databases or file storage), meeting Hackathon Phase 1 requirements.

**Primary Requirement**: Enable users to manage todo tasks via command-line interface with instant feedback and zero setup requirements.

**Technical Approach**:
- **Data Layer**: Python dataclasses (@dataclass) for Task model with strict type hints
- **Business Logic**: TodoStore class managing in-memory list of tasks with auto-incrementing IDs
- **Interface Layer**: argparse-based CLI with subcommands and formatted table output
- **Integration**: Main entry point connecting CLI to Store with proper error handling

---

## Technical Context

**Language/Version**: Python 3.12 or higher
**Primary Dependencies**: Standard library only (argparse, dataclasses, typing, sys)
**Storage**: In-memory (list and dataclass instances, no external persistence)
**Testing**: pytest (optional for MVP), manual testing required
**Target Platform**: Cross-platform (Windows, macOS, Linux with Python 3.12+)
**Project Type**: Single project (CLI application)
**Performance Goals**: <5s for add/complete/delete, <3s for list with 100 tasks
**Constraints**: No external dependencies, no databases, no file persistence, data loss on restart acceptable
**Scale/Scope**: Support 100+ tasks in-memory without performance degradation

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Agentic Delegation Pattern ✅ PASS
- **@logic-expert**: Responsible for `models.py` (Task dataclass) and `store.py` (TodoStore class, ID generation, state management)
- **@cli-expert**: Responsible for `cli.py` (argparse configuration, table formatting, confirmation messages)
- **@qa-specialist**: Responsible for `main.py` (integration), validation against spec, comprehensive testing

**Status**: Plan explicitly delegates tasks to specialized agents per Constitution

### Principle II: In-Memory State Management ✅ PASS
- Task storage: `list[Task]` in TodoStore._tasks (Python list, in-memory)
- ID counter: `int` in TodoStore._next_id (Python integer, in-memory)
- No databases: Confirmed (no SQLite, PostgreSQL, MySQL, etc.)
- No file persistence: Confirmed (no JSON, CSV, pickle, etc.)
- No third-party state libraries: Confirmed (standard library only)
- Data loss on restart: Explicitly documented and accepted (per FR-011)

**Status**: All data strictly in-memory per Constitution

### Principle III: Modular Architecture (Store-View Separation) ✅ PASS
- **Store Layer**: `src/store.py` and `src/models.py` (CLI-agnostic, independently testable)
- **View Layer**: `src/cli.py` (no business logic, delegates to store)
- **Command Pattern**: Each subcommand (add, list, complete, delete) has dedicated handler function
- **Integration**: `src/main.py` routes commands to handlers

**Status**: Clean separation enforced, Store has zero CLI dependencies

### Principle IV: Strict Type Safety ✅ PASS
- All function signatures include type hints (per quickstart reference implementations)
- Python 3.12+ type syntax used (`list[Task]` not `List[Task]`)
- `type-hint-enforcer` skill will validate compliance during implementation
- Dataclass fields have explicit types (id: int, title: str, status: str)

**Status**: Type hints mandatory on all signatures, validation planned

### Principle V: Spec-Driven Development (SDD) ✅ PASS
- Workflow followed: `/sp.constitution` → `/sp.specify` → `/sp.clarify` → `/sp.plan` (current step)
- Next steps: User approval → `/sp.tasks` → `/sp.implement` → validation → `/sp.git.commit_pr`
- No code written yet (design phase only)

**Status**: SDD workflow adhered to, awaiting user approval before code generation

### Principle VI: No Feature Creep ✅ PASS
- Only spec-defined features included: add, list, complete, delete (FR-001 through FR-014)
- No additional features: No priorities, no due dates, no categories, no persistence, no undo
- `spec-aligner` skill will validate implementation against spec.md

**Status**: Scope limited to explicit spec requirements

**GATE RESULT**: ✅ ALL CHECKS PASSED - Proceed to Phase 0

---

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-cli-mvp/
├── spec.md                    # Feature specification (user requirements)
├── plan.md                    # This file (architecture and design)
├── research.md                # Phase 0 output (technical decisions)
├── data-model.md              # Phase 1 output (entity definitions)
├── quickstart.md              # Phase 1 output (implementation guide)
├── contracts/                 # Phase 1 output (interface contracts)
│   ├── store-interface.md     # TodoStore method signatures and behaviors
│   └── cli-interface.md       # CLI command specifications
├── checklists/                # Quality validation
│   └── requirements.md        # Spec quality checklist (complete)
└── tasks.md                   # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
todo-app/
├── src/
│   ├── models.py              # Task dataclass (@logic-expert)
│   ├── store.py               # TodoStore class (@logic-expert)
│   ├── cli.py                 # CLI interface (@cli-expert)
│   └── main.py                # Entry point (@qa-specialist)
├── tests/                     # Optional for MVP
│   ├── test_models.py
│   ├── test_store.py
│   └── test_cli.py
├── todo.py                    # Executable script (imports src.main)
├── specs/                     # This directory
│   └── 001-todo-cli-mvp/
├── .specify/                  # SpecKit Plus templates and tools
└── history/                   # PHRs and ADRs
```

**Structure Decision**: Single project structure selected because:
- CLI application (not web or mobile)
- Single language (Python)
- All code in one repository
- No frontend/backend split needed

**Module Layout**:
- `src/models.py`: 30-40 lines (Task dataclass with validation)
- `src/store.py`: 60-80 lines (TodoStore class with 5 methods)
- `src/cli.py`: 100-120 lines (argparse + handlers + formatting)
- `src/main.py`: 30-40 lines (routing and initialization)
- `todo.py`: 10 lines (executable entry point)

**Total Estimated LOC**: ~250 lines of production code

---

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations detected**. All Constitution principles satisfied.

---

## Phase 0: Research & Technical Decisions

**Status**: ✅ COMPLETE

**Output**: `research.md` (5 technical decisions resolved)

**Key Decisions**:
1. **Dataclass Configuration**: Mutable dataclass with explicit defaults (allows status updates)
2. **ID Generation**: Simple incrementing counter (O(1), guarantees uniqueness, never reuses)
3. **Table Formatting**: Manual f-string formatting (no external dependencies, full control)
4. **argparse Structure**: Subparsers pattern (standard for multi-command CLIs)
5. **Error Handling**: Two-tier validation (argparse for format, store for existence)

**Rationale**: All decisions prioritize simplicity, Constitution compliance (standard library only), and performance (O(1) ID generation, O(n log n) sorting).

---

## Phase 1: Design & Contracts

**Status**: ✅ COMPLETE

### Artifacts Generated

1. **data-model.md** (Data Model Design)
   - Task entity definition with attributes, validation rules, state transitions
   - TodoStore entity with invariants and operations
   - Schema definition (dataclass reference implementation)

2. **contracts/store-interface.md** (Store Layer Contract)
   - TodoStore class specification
   - Method signatures: `__init__`, `add_task`, `list_tasks`, `get_task`, `complete_task`, `delete_task`
   - Preconditions, postconditions, side effects, exceptions
   - Invariants and testing requirements

3. **contracts/cli-interface.md** (CLI Layer Contract)
   - Command specifications: add, list, complete, delete
   - Argument parsing rules
   - Output formats (success and error messages)
   - Table formatting specification
   - Error handling and exit codes

4. **quickstart.md** (Implementation Guide)
   - Project structure
   - Phase-by-phase implementation workflow
   - Reference code for each module
   - Validation steps and troubleshooting

### Design Highlights

**Task Model**:
```python
@dataclass
class Task:
    id: int
    title: str
    status: str = field(default='pending')
```

**Store Interface**:
- `add_task(title: str) -> Task`: Create task with auto-ID
- `list_tasks() -> list[Task]`: Return sorted tasks
- `get_task(task_id: int) -> Task | None`: Lookup by ID
- `complete_task(task_id: int) -> Task | None`: Mark as done
- `delete_task(task_id: int) -> bool`: Remove task

**CLI Commands**:
- `python todo.py add "title"` → "Task {id} added: {title}"
- `python todo.py list` → Table with ID | Title | Status
- `python todo.py complete <id>` → "Task {id} marked as done"
- `python todo.py delete <id>` → "Task {id} deleted"

---

## Constitution Check (Post-Design)

**Re-evaluation after Phase 1 design completion**:

### Principle I: Agentic Delegation Pattern ✅ PASS
- Contracts explicitly define responsibilities for each agent
- Store layer (40% of code) → @logic-expert
- CLI layer (40% of code) → @cli-expert
- Integration (20% of code) → @qa-specialist

### Principle II: In-Memory State Management ✅ PASS
- Design confirms: `_tasks: list[Task]` (in-memory list)
- No database schemas, no file I/O operations in any contract
- Data model explicitly states "Data exists only in memory during application lifetime"

### Principle III: Modular Architecture ✅ PASS
- Store interface has zero CLI dependencies (confirmed in contracts)
- CLI interface delegates all business logic to store (confirmed in contracts)
- Clear boundaries: models.py, store.py (business) | cli.py (view) | main.py (integration)

### Principle IV: Strict Type Safety ✅ PASS
- All reference implementations in quickstart.md include full type hints
- Contracts specify type signatures for all methods
- Validation step included in each phase

### Principle V: Spec-Driven Development ✅ PASS
- Design artifacts directly trace to spec requirements (FR-001 through FR-014)
- No features added beyond spec

### Principle VI: No Feature Creep ✅ PASS
- Zero features beyond the spec's four operations
- Quickstart explicitly lists "Future Considerations (Out of Scope for MVP)"

**FINAL GATE RESULT**: ✅ ALL CHECKS PASSED - Ready for `/sp.tasks`

---

## Implementation Phases (from User Input)

The user requested a specific 4-phase implementation plan. These phases will be converted to detailed tasks by `/sp.tasks`:

### Phase 1: Foundation & Data Model
**Agent**: @logic-expert
- **Task 1.1**: Create `src/models.py` defining Task dataclass
  - Fields: `id: int`, `title: str`, `status: str`
  - Default status: `'pending'`
  - Validation in `__post_init__`
- **Validation**: Run `type-hint-enforcer` skill

### Phase 2: In-Memory Logic Layer
**Agent**: @logic-expert
- **Task 2.1**: Create `src/store.py` containing TodoStore class
- **Task 2.2**: Implement `add_task(title: str) -> Task`
  - ID generation (auto-increment from `_next_id`)
  - Append to `_tasks` list
- **Task 2.3**: Implement `list_tasks() -> list[Task]`
  - Return sorted by ID ascending
- **Task 2.4**: Implement `complete_task(task_id: int) -> Task | None`
  - One-way transition (pending → done only)
  - Return None if not found
- **Task 2.5**: Implement `delete_task(task_id: int) -> bool`
  - Remove from list, never reuse ID
- **Validation**: ID lookup follows "Reject non-integers (argparse), report missing for negative/zero"

### Phase 3: CLI & User Interface
**Agent**: @cli-expert
- **Task 3.1**: Create `src/cli.py` using argparse
  - Subcommands: add, list, complete, delete
  - Type validation: `type=int` for ID arguments
- **Task 3.2**: Implement table formatter
  - Left-aligned columns
  - Auto-width (no truncation)
  - Sorted by ID ascending
- **Task 3.3**: Implement confirmation messages
  - Add: "Task {id} added: {title}"
  - Complete: "Task {id} marked as done"
  - Delete: "Task {id} deleted"
- **Task 3.4**: Implement error handling
  - stderr for errors
  - Exit code 1 for business errors
  - Exit code 2 for format errors

### Phase 4: Integration & QA
**Agent**: @qa-specialist
- **Task 4.1**: Create `src/main.py` entry point
  - Initialize TodoStore (fresh each run)
  - Route subcommands to handlers
  - Return exit codes
- **Task 4.2**: Create `todo.py` executable script
- **Task 4.3**: Manual test suite execution
  - Smoke tests (all commands with valid input)
  - Error cases (empty title, non-existent ID, non-integer ID)
  - In-memory verification (data loss on restart)
  - Performance test (100 tasks, list in <3s)
- **Task 4.4**: Spec compliance validation
  - Verify all FR-001 through FR-014 satisfied
  - Verify all SC-001 through SC-008 met
  - Verify all acceptance scenarios pass

---

## Architecture Decision Record (ADR) Suggestions

📋 **Potential ADRs Identified** (awaiting user consent per Constitution):

1. **ADR-001: Dataclass-Based Task Model**
   - Decision: Use mutable dataclass for Task entity
   - Context: Need type-safe, simple data structure
   - Alternatives: NamedTuple (immutable), dict (no types), custom class (boilerplate)
   - Rationale: Dataclass provides type safety + mutability for status updates

2. **ADR-002: Sequential ID Generation Strategy**
   - Decision: Use simple incrementing counter
   - Context: Need unique, never-reused IDs
   - Alternatives: UUID (complex), hash-based (collision risk), max+1 (O(n) cost)
   - Rationale: O(1) generation, guaranteed uniqueness, user-friendly integers

3. **ADR-003: Manual Table Formatting**
   - Decision: Implement table formatting with f-strings
   - Context: Need formatted output, no external dependencies allowed
   - Alternatives: tabulate library (violates Constitution), CSV output (less readable)
   - Rationale: Full control, zero dependencies, ~20 lines of code

**Recommendation**: Document ADR-001 and ADR-002 as they represent significant architectural choices with long-term implications. ADR-003 is less critical (implementation detail).

**User**: Would you like me to create ADRs for these decisions? Reply with `/sp.adr <title>` to proceed.

---

## Risks & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Type hint errors during validation | Low | Medium | `type-hint-enforcer` skill used in each phase |
| argparse not catching non-integer IDs | Low | Medium | Explicit `type=int` in parser configuration |
| Table formatting breaks with edge cases | Medium | Low | Test with empty list, long titles, 100+ tasks |
| Performance degradation with many tasks | Low | Medium | O(n log n) sort acceptable for <1000 tasks per spec |
| ID counter overflow | Very Low | Low | Python int has unlimited precision |

---

## Success Criteria Mapping

All success criteria from spec.md mapped to implementation phases:

- **SC-001** (Add in <5s): Phase 2 (O(1) add_task)
- **SC-002** (List in <3s): Phase 3 (O(n log n) format_table)
- **SC-003** (Complete in <5s): Phase 2 (O(n) complete_task)
- **SC-004** (Delete in <5s): Phase 2 (O(n) delete_task)
- **SC-005** (100 tasks, list <3s): Phase 4 (performance test)
- **SC-006** (95% clear feedback): Phase 3 (confirmation messages)
- **SC-007** (Works without docs): Phase 4 (manual testing)
- **SC-008** (No external setup): Phases 1-2 (standard library only)

---

## Next Steps

1. ✅ **Phase 0 Complete**: research.md generated with 5 technical decisions
2. ✅ **Phase 1 Complete**: data-model.md, contracts/, quickstart.md generated
3. ⏸️ **Awaiting User Approval**: Review this plan before proceeding
4. ⏭️ **Next Command**: `/sp.tasks` to generate detailed task breakdown from this plan
5. ⏭️ **Then**: `/sp.implement` to execute tasks with agent delegation

**Plan Status**: ✅ READY FOR USER REVIEW AND APPROVAL
