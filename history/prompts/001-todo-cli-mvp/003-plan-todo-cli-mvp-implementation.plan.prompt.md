---
id: 003
title: Plan Todo CLI MVP Implementation
stage: plan
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5
feature: 001-todo-cli-mvp
branch: 001-todo-cli-mvp
user: Abdul Mannan
command: /sp.plan
labels: ["planning", "architecture", "todo-app", "implementation-design"]
links:
  spec: specs/001-todo-cli-mvp/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-todo-cli-mvp/plan.md
  - specs/001-todo-cli-mvp/research.md
  - specs/001-todo-cli-mvp/data-model.md
  - specs/001-todo-cli-mvp/quickstart.md
  - specs/001-todo-cli-mvp/contracts/store-interface.md
  - specs/001-todo-cli-mvp/contracts/cli-interface.md
tests:
  - N/A (planning phase - test scenarios defined in contracts)
---

## Prompt

```text
# Topic: Finalized Implementation Plan for In-Memory Todo App

## Goal
Establish a 4-Phase implementation roadmap that utilizes our specialized sub-agents and skills to build the MVP.

## Phase 1: Foundation & Data Model
- **@logic-expert**: Create `models.py` defining the `@dataclass` for `Task` with fields: `id: int`, `title: str`, and `status: str`.
- **@logic-expert**: Ensure the default status is 'pending'.
- **Skill Check**: `type-hint-enforcer` must validate all dataclass types.

## Phase 2: In-Memory Logic Layer
- **@logic-expert**: Create `store.py` containing a `TodoStore` class.
- **Methods**: Implement `add_task`, `list_tasks`, `complete_task` (one-way only), and `delete_task`.
- **Validation**: Implement ID lookup logic following the "Reject non-integers, report missing for negative/zero" rule.

## Phase 3: CLI & User Interface
- **@cli-expert**: Create `interface.py` using `argparse` to handle CLI commands.
- **Formatting**: Implement the table view using left-aligned, auto-width columns.
- **Messages**: Implement the descriptive confirmation messages (e.g., "Task [ID] marked as done").

## Phase 4: Integration & QA
- **@qa-specialist**: Create a `main.py` entry point that connects the CLI to the Store.
- **Verification**: Run a full suite of manual/automated tests for all 4 features to ensure 100% In-Memory persistence during the session.

## Deliverables
Update `.specify/memory/plan.md` with these steps. Each step must be marked as 'Pending' for the `/sp.implement` phase.
```

## Response snapshot

Created comprehensive implementation plan with Phase 0 research, Phase 1 design artifacts, and detailed 4-phase implementation roadmap per user requirements.

**Planning Artifacts Generated**:

1. **research.md** (Phase 0 - Technical Decisions)
   - 5 research questions resolved: dataclass configuration, ID generation strategy, table formatting approach, argparse structure, error handling pattern
   - All decisions prioritize simplicity, Constitution compliance, and performance
   - Zero external dependencies required (standard library only)

2. **data-model.md** (Phase 1 - Data Model Design)
   - Task entity specification with validation rules and state transitions
   - TodoStore entity with invariants and operations
   - Schema definition with reference dataclass implementation
   - Testing considerations and future scope boundaries

3. **contracts/store-interface.md** (Phase 1 - Store Layer Contract)
   - TodoStore class specification with 6 methods
   - Detailed signatures, preconditions, postconditions, side effects
   - Invariants: ID uniqueness, sequential assignment, no reuse
   - Testing contract with 15+ required test scenarios

4. **contracts/cli-interface.md** (Phase 1 - CLI Layer Contract)
   - Command specifications for add, list, complete, delete
   - Table formatting specification (left-aligned, auto-width, ID-sorted)
   - Error handling and exit codes (0=success, 1=business error, 2=format error)
   - Confirmation message formats per clarification Q5

5. **quickstart.md** (Phase 1 - Implementation Guide)
   - Phase-by-phase implementation workflow with reference code
   - Complete reference implementations for all modules (~250 LOC total)
   - Validation steps and troubleshooting guide
   - Constitution compliance checklist

6. **plan.md** (Main Planning Document)
   - Technical context and Constitution Check (all principles PASS)
   - Project structure (single project, ~250 LOC)
   - 4-phase implementation roadmap per user input
   - Success criteria mapping, risks, ADR suggestions

**Constitution Validation** (Post-Design):
- ✅ Agentic Delegation: Explicit agent assignments (40% @logic-expert, 40% @cli-expert, 20% @qa-specialist)
- ✅ In-Memory State: Confirmed no databases, no file I/O in any contract
- ✅ Modular Architecture: Store layer has zero CLI dependencies per contracts
- ✅ Strict Type Safety: All reference implementations include full type hints
- ✅ Spec-Driven Development: Design traces directly to FR-001 through FR-014
- ✅ No Feature Creep: Only 4 operations (add, list, complete, delete)

**Architecture Decisions Identified**:
1. Dataclass-based Task model (mutable, type-safe)
2. Sequential ID generation (O(1), never reused)
3. Manual table formatting (no external dependencies)

Suggested creating ADRs for decisions 1-2 (awaiting user consent per Constitution).

**Implementation Phases**:
- Phase 1: @logic-expert creates models.py with Task dataclass
- Phase 2: @logic-expert creates store.py with TodoStore class (5 methods)
- Phase 3: @cli-expert creates cli.py with argparse + table formatting
- Phase 4: @qa-specialist creates main.py + validation suite

**Estimated Scope**: ~250 lines of production code across 4 modules

## Outcome

- ✅ Impact: Complete implementation plan ready for task generation and execution
- 🧪 Tests: N/A (planning phase - test scenarios defined in contracts, execution in Phase 4)
- 📁 Files: Created 6 planning artifacts (plan.md, research.md, data-model.md, quickstart.md, 2 contract files)
- 🔁 Next prompts: /sp.tasks to generate detailed task breakdown, then /sp.implement
- 🧠 Reflection: Planning successfully addressed all user-specified phases while maintaining Constitution compliance. Research phase resolved all technical unknowns (dataclass config, ID strategy, table formatting, argparse structure, error handling). Design artifacts provide clear contracts for each agent. Ready for user approval and task generation.

## Evaluation notes (flywheel)

- Failure modes observed: None - all planning artifacts generated successfully
- Graders run and results (PASS/FAIL): Constitution Check (post-design) - PASS (all 6 principles satisfied)
- Prompt variant (if applicable): N/A (standard planning workflow)
- Next experiment (smallest change to try): N/A (planning complete, ready for /sp.tasks)
