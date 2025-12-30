# Todo App (Hackathon 2 Phase 1) Constitution

<!--
SYNC IMPACT REPORT
Version: 1.0.0 → 1.0.0 (Initial ratification)
Ratification Date: 2025-12-30
Principles Defined:
  - I. Agentic Delegation Pattern
  - II. In-Memory State Management
  - III. Modular Architecture (Store-View Separation)
  - IV. Strict Type Safety
  - V. Spec-Driven Development (SDD)
  - VI. No Feature Creep

Templates Status:
  ✅ plan-template.md - Constitution Check section references this file
  ✅ spec-template.md - Requirements align with defined principles
  ✅ tasks-template.md - Task categorization supports principle-driven workflow

Follow-up Actions: None
-->

## Core Principles

### I. Agentic Delegation Pattern

**Specialized agents handle domain-specific tasks:**
- State management and data structures → `@logic-expert` agent (MANDATORY for all in-memory storage, ID generation, data integrity)
- CLI interface and terminal formatting → `@cli-expert` agent (MANDATORY for all argparse, command handling, terminal output)
- Quality assurance and spec validation → `@qa-specialist` agent (MANDATORY before marking any feature complete)

**Rationale**: Complex systems benefit from specialized expertise. Delegating to domain experts ensures correctness, consistency, and prevents architectural drift. The lead architect coordinates but does not implement cross-cutting concerns alone.

### II. In-Memory State Management

**Data persistence requirements for Phase 1:**
- ALL data MUST be stored in Python lists and dictionaries in-memory
- NO external databases (SQLite, PostgreSQL, MySQL, etc.) permitted
- NO file-based persistence (JSON, CSV, pickle, etc.) permitted
- NO third-party state management libraries
- State resets on application restart (acceptable for Phase 1)

**Rationale**: Hackathon Phase 1 focuses on core functionality and user experience. In-memory storage eliminates setup complexity, ensures fast iteration, and provides instant feedback. Persistence can be added in Phase 2 if needed.

### III. Modular Architecture (Store-View Separation)

**Separation of concerns enforced:**
- **Store Layer** (`src/store/` or equivalent): Manages state, business logic, and data operations. MUST be CLI-agnostic and independently testable.
- **View Layer** (`src/cli/` or equivalent): Handles user input, command parsing, and terminal output. MUST NOT contain business logic.
- **Command Pattern**: Each user action (add, list, delete, complete) implemented as a discrete command with clear interface.

**Rationale**: Modular design enables independent testing, easier debugging, and future extensibility (e.g., adding a web UI later). Store-View separation is a proven pattern for maintainable applications.

### IV. Strict Type Safety

**Type annotations mandatory:**
- EVERY function signature MUST include type hints for parameters and return values
- Use Python 3.12+ type annotation features (`list[Task]`, `dict[str, Any]`, etc.)
- Utilize `type-hint-enforcer` skill to validate compliance
- Type hints serve as inline documentation and enable IDE support

**Rationale**: Type hints catch bugs early, improve code readability, and enable powerful refactoring tools. They are especially critical in a team environment where code is shared and reviewed.

### V. Spec-Driven Development (SDD)

**Development workflow (non-negotiable):**
1. User provides feature description
2. `/sp.specify` → Create/update `spec.md` with requirements and acceptance criteria
3. `/sp.plan` → Generate architectural design in `plan.md`
4. **GATE**: User approves `plan.md` before ANY code is written
5. `/sp.tasks` → Generate actionable task list in `tasks.md`
6. `/sp.implement` → Execute tasks in dependency order
7. `/sp.git.commit_pr` → Commit and create PR only after all tasks pass validation

**Rationale**: Writing code before understanding requirements leads to rework, scope creep, and misaligned deliverables. SDD ensures alignment between user intent and implementation.

### VI. No Feature Creep

**Scope discipline:**
- Implement ONLY features explicitly defined in `spec.md`
- Utilize `spec-aligner` skill to validate all code against specifications
- Reject "nice to have" additions unless user explicitly adds them to the spec
- Hackathon constraints prioritize core functionality over polish

**Rationale**: Feature creep derails timelines and dilutes focus. Hackathon success requires ruthless prioritization of core value delivery.

## Technical Constraints

### Language and Platform
- **Language**: Python 3.12 or higher (REQUIRED)
- **Standard Library Only**: argparse for CLI, typing for type hints, dataclasses for models
- **No External Dependencies**: Phase 1 uses only Python standard library (except pytest for testing if needed)

### CLI Framework
- **argparse**: Standard library command-line parser (MANDATORY)
- **Subcommands**: add, list, delete, complete (minimum viable set)
- **Output Format**: Human-readable text (tables preferred), errors to stderr

### Testing (Optional for Phase 1)
- If tests are written, use pytest or unittest
- Tests focus on Store layer (business logic), not CLI formatting
- CLI layer tested manually or via integration tests

## Development Workflow

### Command Execution Order
1. **Constitution Definition**: `/sp.constitution` (this command) - Define project principles
2. **Feature Specification**: `/sp.specify` - Capture user requirements
3. **Implementation Planning**: `/sp.plan` - Design architecture and validate against constitution
4. **Task Generation**: `/sp.tasks` - Break design into actionable tasks
5. **Implementation**: `/sp.implement` - Execute tasks with agent delegation
6. **Quality Assurance**: `@qa-specialist` validation before completion
7. **Version Control**: `/sp.git.commit_pr` - Commit and create PR

### Agent Delegation Protocol
- **Before implementing state logic**: Invoke `@logic-expert` to design/review data structures
- **Before implementing CLI**: Invoke `@cli-expert` to design/review command interface
- **Before marking feature complete**: Invoke `@qa-specialist` to validate against spec

### Prompt History Records (PHR)
- **MANDATORY**: Create PHR after every user interaction that results in work (planning, implementation, debugging)
- **Location**: `history/prompts/<stage>/` where stage is constitution | spec | plan | tasks | implementation | etc.
- **Content**: Full user prompt (verbatim), key assistant response, files modified, tests run
- **Purpose**: Traceability, learning, and accountability

### Architecture Decision Records (ADR)
- **Trigger**: Significant decisions during `/sp.plan` or `/sp.tasks` (e.g., data structure choice, ID generation strategy)
- **Process**: Suggest ADR creation to user with `/sp.adr <title>`, WAIT for consent
- **Content**: Context, decision, consequences, alternatives considered
- **Location**: `history/adr/`

## Governance

### Constitution Authority
- This constitution SUPERSEDES all other development practices
- All PRs, code reviews, and implementations MUST verify compliance with these principles
- Violations require explicit justification documented in `plan.md` Complexity Tracking section

### Amendment Process
1. Proposed changes discussed with user
2. Constitution updated via `/sp.constitution`
3. Version incremented per semantic versioning:
   - MAJOR: Principle removed or redefined (backward incompatible)
   - MINOR: New principle added or section expanded
   - PATCH: Clarifications, wording fixes, non-semantic changes
4. All dependent templates (plan, spec, tasks) synchronized
5. PHR created documenting the amendment rationale

### Compliance Review
- Lead architect validates every implementation against principles
- `@qa-specialist` performs final compliance check before feature completion
- Deviations logged in `plan.md` with justification and mitigation plan

---

**Version**: 1.0.0 | **Ratified**: 2025-12-30 | **Last Amended**: 2025-12-30
