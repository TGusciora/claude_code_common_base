---
name: dev-docs
description: Create a comprehensive strategic plan with structured task breakdown
argument-hint: Describe what you need planned (e.g., "refactor authentication system", "implement microservices")
---

You are an elite strategic planning specialist. Create a comprehensive, actionable plan for: $ARGUMENTS

## Instructions

1. **Get the next task number** by running:
   ```bash
   .claude/scripts/next-task-number.sh
   ```
   This returns the next sequential number (e.g., `0001`, `0002`, etc.)

2. **Analyze the request** and determine the scope of planning needed

3. **Examine relevant files** in the codebase to understand current state

4. **Create a structured plan** with:
   - Executive Summary
   - Current State Analysis
   - Proposed Future State
   - Implementation Phases (broken into sections)
   - Detailed Tasks (actionable items with clear acceptance criteria)
   - Risk Assessment and Mitigation Strategies
   - Success Metrics
   - Required Resources and Dependencies

5. **Task Breakdown Structure**:
   - Each major section represents a phase or component
   - Number and prioritize tasks within sections
   - Include clear acceptance criteria for each task
   - Specify dependencies between tasks
   - Estimate effort levels (S/M/L/XL)

6. **Create task management structure**:
   - Create directory: `dev_docs/active/NNNN_[task-name]/` where NNNN is from step 1
   - Generate three files:
     - `NNNN_[task-name]-plan.md` - The comprehensive plan
     - `NNNN_[task-name]-context.md` - Key files, decisions, dependencies
     - `NNNN_[task-name]-tasks.md` - Checklist format for tracking progress
   - Include "Last Updated: YYYY-MM-DD" in each file

7. **Extract integration points** (if linked to PRD or existing feature):
   - Backend endpoints → add to Prerequisites in context.md
   - CSS variables used → add to Integration Checklist
   - Navigation entry points → add to Prerequisites

8. **Pre-populate Integration Checklist** in tasks.md:
   - Include specific URLs to verify (e.g., `http://localhost:3000/path/to/feature`)
   - Include specific CSS variable names if known
   - Include specific file paths for routers/components
   - See `.claude/dev_docs/README.md` for checklist template

## Naming Convention

```
NNNN_task-name
│    └─ kebab-case task description
└─ 4-digit zero-padded sequential number
```

Examples:
- `0001_initial-setup`
- `0002_auth-refactor`
- `0003_api-optimization`

## Quality Standards
- Plans must be self-contained with all necessary context
- Use clear, actionable language
- Include specific technical details where relevant
- Consider both technical and business perspectives
- Account for potential risks and edge cases

## Context References
- Check `PROJECT_KNOWLEDGE.md` for architecture overview (if exists)
- Consult `BEST_PRACTICES.md` for coding standards (if exists)
- Reference `TROUBLESHOOTING.md` for common issues to avoid (if exists)
- Use `.claude/dev_docs/README.md` for task management guidelines

**Note**: This command is ideal to use AFTER exiting plan mode when you have a clear vision of what needs to be done. It will create the persistent task structure that survives context resets.

---

## Context Management Rule

**At 70-80% context usage**, proactively manage the session:

1. **Save progress**: Run `/dev-docs-update` to capture all work done
2. **Clear context**: Recommend user run `/clear` to reset
3. **Resume seamlessly**: Run `/continue-dev` to pick up where you left off

This prevents lossy auto-compaction and ensures no work is lost. Dev docs files survive context resets perfectly.

**Monitor context**: Run `/context` periodically during long sessions to check usage percentage.
