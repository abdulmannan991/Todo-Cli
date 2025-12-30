
---
id: 001
title: Todo App Hackathon Constitution
stage: constitution
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5
feature: none
branch: 001-humanoid-control-chapters
user: Abdul Mannan
command: /sp.constitution
labels: ["constitution", "hackathon", "python", "cli", "agentic-delegation"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (documentation only)
---

## Prompt

```text
# Role: Lead Architect & Spec-Driven Development Orchestrator

## Project Objective
Develop a professional-grade, in-memory Python CLI Todo application for Hackathon 2 Phase 1.

## Core Directives
1. **Agentic Delegation**:
   - ALWAYS delegate state and data structure tasks to the `@logic-expert`.
   - ALWAYS delegate UI, `argparse`, and terminal formatting to the `@cli-expert`.
   - Use the `@qa-specialist` to validate every implementation against the specs.

2. **Skill Enforcement**:
   - Utilize the `type-hint-enforcer` skill for every line of Python code.
   - Utilize the `spec-aligner` skill to ensure no "feature creep" outside of the hackathon requirements.

3. **Technical Constraints**:
   - **Language**: Python 3.12+.
   - **Persistence**: STRICTLY In-Memory. No SQLite, JSON files, or external DBs for Phase 1.
   - **CLI Framework**: Standard library `argparse` for command parsing.

4. **Architectural Pattern**:
   - Implement a modular design separating the "Store" (logic) from the "View" (CLI).
   - Follow the Command Pattern for actions: `add`, `list`, `delete`, `complete`.

5. **Speckit Plus Workflow**:
   - All architecture decisions must be recorded in `.specify/memory/`.
   - Code must not be written until the `/sp.plan` is approved.
```

## Response snapshot

Created the Todo App Constitution v1.0.0 with six core principles:

1. **Agentic Delegation Pattern**: Mandates specialized agents (@logic-expert for state, @cli-expert for UI, @qa-specialist for validation)
2. **In-Memory State Management**: Strictly in-memory storage using Python lists/dicts, no external persistence
3. **Modular Architecture**: Store-View separation with Command Pattern for user actions
4. **Strict Type Safety**: Mandatory type hints for all function signatures using Python 3.12+ features
5. **Spec-Driven Development**: Non-negotiable workflow requiring user approval before coding
6. **No Feature Creep**: Implement only spec-defined features using spec-aligner skill

Additional sections defined:
- **Technical Constraints**: Python 3.12+, standard library only, argparse for CLI
- **Development Workflow**: Command execution order and agent delegation protocol
- **Governance**: Constitution authority, amendment process, compliance review

All placeholders filled, version set to 1.0.0 (initial ratification), templates validated for consistency.

## Outcome

- ✅ Impact: Constitution ratified, establishes governance framework and technical standards for Hackathon 2 Phase 1
- 🧪 Tests: N/A (documentation artifact)
- 📁 Files: Created/updated .specify/memory/constitution.md (157 lines)
- 🔁 Next prompts: /sp.specify to create feature specification following defined principles
- 🧠 Reflection: Constitution successfully captures all user requirements including agentic delegation, technical constraints, and SDD workflow. Clear separation between Store and View layers will enable parallel development by specialized agents.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual validation - PASS (all placeholders filled, version coherent, templates aligned)
- Prompt variant (if applicable): N/A (first iteration)
- Next experiment (smallest change to try): N/A (constitution complete)
