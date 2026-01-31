<div align="center">

# Claude Code Portable Setup

### A production-ready, portable configuration for Claude Code CLI

[![Claude Code](https://img.shields.io/badge/Claude%20Code-CLI-blueviolet?style=for-the-badge&logo=anthropic)](https://claude.ai/claude-code)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge)](CONTRIBUTING.md)

---

**A comprehensive, batteries-included configuration framework for Claude Code**
*Skills • Agents • Hooks • Safety • Ralph Automation • Dev Docs*

[Quick Start](#-quick-start) • [Ralph Agent](#-ralph-autonomous-agent) • [Features](#-features) • [Documentation](#-documentation)

</div>

---

## About

This repository provides a **portable Claude Code configuration** that you can drop into any project to supercharge your AI-assisted development workflow. It includes pre-configured skills, specialized agents, safety hooks, and a persistent documentation pattern for maintaining context across sessions.

### Credits & Attribution

| | |
|---|---|
| **Author** | **Tomasz Gusciora** |
| **Based on** | [claude-code-infrastructure-showcase](https://github.com/diet103/claude-code-infrastructure-showcase) by diet103 |
| **Original Discussion** | [Claude Code is a Beast - Tips from 6 Months of Use](https://www.reddit.com/r/ClaudeAI/comments/1oivjvm/claude_code_is_a_beast_tips_from_6_months_of/) |
| **Hooks Guide** | [The Production-Ready Claude Code Hooks Guide](https://alirezarezvani.medium.com/the-production-ready-claude-code-hooks-guide-7-hooks-that-actually-matter-823587f9fc61) by Alireza Rezvani |
| **Frontend Skills** | [Anthropic Skills Repository](https://github.com/anthropics/skills) - `frontend-design`, `theme-factory`, `webapp-testing`, `web-artifacts-builder` |
| **React Best Practices** | [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills/tree/main) - Performance optimization rules for React/Next.js |
| **Vue Best Practices** | Adapted from React skill for Vue 3/Nuxt 3 ecosystem |

---

## Quick Start

### Installation

```bash
# Clone this repository
git clone https://github.com/YOUR_USERNAME/claude_code_common_base.git

# Or copy the .claude folder to your project
cp -r claude_code_common_base/.claude your-project/
cp claude_code_common_base/CLAUDE.md your-project/

# Make hooks and scripts executable
chmod +x .claude/hooks/*.py .claude/hooks/*.sh .claude/scripts/*.sh .claude/scripts/**/*.sh

# Configure git hooks
git config core.hooksPath .githooks
```

### The Idea-to-Implementation Pipeline

The recommended workflow transforms ideas into deployed code through three automated phases:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         IDEA-TO-IMPLEMENTATION PIPELINE                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   1. DISCOVERY          2. DEV DOCS           3. RALPH (terminal)           │
│   ─────────────         ─────────             ───────────────               │
│   /discovery     ──►    /dev-docs     ──►     ralph.sh                      │
│                                                                             │
│   Create PRD from       Create task           Run from terminal:            │
│   your idea through     documentation         .claude/scripts/              │
│   5 interactive         with plan,              ralph/ralph.sh              │
│   phases                context & tasks       (uses --dangerously-          │
│                                                skip-permissions)            │
│                                                                             │
│   Output:               Output:               Output:                       │
│   docs/discovery/       dev_docs/active/      Feature branch                │
│   └── 05-prd-final.md   └── NNNN_task/        ready to merge                │
│                             ├── *-plan.md                                   │
│                             ├── *-context.md                                │
│                             └── *-tasks.md                                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Step-by-Step Example

```bash
# Step 1: Create PRD from your idea
/discovery -d "A REST API for managing user subscriptions"
# Output: docs/discovery/subscription-api/05-prd-final.md

# Step 2: Create development task documentation
/dev-docs "Implement subscription API from PRD"
# Output: dev_docs/active/0001_subscription-api/

# Step 3: Let Ralph implement it autonomously
# IMPORTANT: Run from terminal (not IDE) to use --dangerously-skip-permissions
.claude/scripts/ralph/ralph.sh
# Ralph works in isolated worktree, commits to feature branch

# Step 4: Review and merge Ralph's work
git diff main..ralph/0001_subscription-api
git merge ralph/0001_subscription-api
```

---

## Ralph: Autonomous Agent

Ralph is a **test-driven, self-continuing agent** that automates implementation of tasks from `dev_docs/active/`. He works in an isolated git worktree, protecting your main branch while autonomously implementing features.

### How Ralph Works

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           RALPH'S ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   YOUR PROJECT ROOT                    WORKTREE (isolated)                  │
│   ─────────────────                    ────────────────────                 │
│        │                                     │                              │
│        │                               worktrees/ralph-worktree-0001/       │
│        │                                     │                              │
│   main branch ◄──────────────────────► ralph/0001_task-name branch          │
│   (protected)                          (all changes here)                   │
│        │                                     │                              │
│   Your active                          Ralph's workspace:                   │
│   development                          • Reads task docs                    │
│        │                               • Writes tests first                 │
│        │                               • Implements features                │
│        │                               • Commits progress                   │
│        │                                     │                              │
│        └──────── MERGE WHEN READY ───────────┘                              │
│                  (you review first)                                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Key Features

| Feature | Description |
|---------|-------------|
| **Git Worktree Isolation** | All changes in `worktrees/ralph-worktree-NNNN/` on feature branch |
| **Test-First Development** | Defines acceptance criteria → writes tests → implements → verifies |
| **Smart Task Selection** | Batches related tasks, respects priorities and dependencies |
| **Auto-Fix on Failure** | Analyzes test failures and attempts fixes before giving up |
| **Progress Tracking** | JSONL log in `ralph_progress.txt` for session continuity |
| **Conventional Commits** | Each iteration commits with proper message format |

### Ralph's Workflow Per Iteration

```
1. STARTUP           2. SELECT            3. TEST-FIRST         4. COMMIT
────────────         ──────────           ─────────────         ─────────
• Verify worktree    • Review [ ] items   • Define goals        • Update tasks.md
• Check branch       • Batch related      • Write tests (RED)   • Update context.md
• Read task docs     • Declare selection  • Implement (GREEN)   • Append progress
• Run baseline       • State rationale    • Verify & fix        • git commit
```

### Using Ralph

**Run from terminal using the shell script** (recommended):

```bash
# IMPORTANT: Run from terminal, not IDE (VS Code/Cursor)
# The shell script uses --dangerously-skip-permissions for autonomous operation
# IDE environments use .claude/settings.json which interrupts Ralph's workflow

# Run with default 20 iterations
.claude/scripts/ralph/ralph.sh

# Run with custom iteration limit
.claude/scripts/ralph/ralph.sh 10

# Preview what would happen
.claude/scripts/ralph/ralph.sh --dry-run

# Check current status
.claude/scripts/ralph/ralph.sh --status

# Clean up worktree and branch
.claude/scripts/ralph/ralph.sh --cleanup
```

### After Ralph Completes

```bash
# Review changes on the feature branch
git log main..ralph/0001_task-name
git diff main..ralph/0001_task-name

# Run tests in worktree
cd worktrees/ralph-worktree-0001 && pytest

# If satisfied, merge to main
git checkout main
git merge ralph/0001_task-name

# Or create a PR for team review
gh pr create --base main --head ralph/0001_task-name

# Clean up
git worktree remove worktrees/ralph-worktree-0001
git branch -D ralph/0001_task-name
```

### Ralph's Safety Features

1. **Worktree Isolation**: Changes never touch main branch directly
2. **Path-Restricted Tools**: Write/Edit only allowed in worktree directory
3. **Safety Hooks Active**: `safety_validator.py` still blocks dangerous operations
4. **Iteration Limit**: Maximum 20 iterations prevents runaway execution
5. **Test-Driven**: Tasks only marked complete when tests pass

### Environment Files in Worktrees

> **Note:** Ralph automatically copies all `.env*` and `.secret*` files to worktrees:
> - `.example` files (e.g., `.env.example`) - Claude CAN read these for structure reference
> - Actual secret files (e.g., `.env`, `.env.local`) - Copied but Claude CANNOT read them
>
> This allows your environment to be ready while keeping secrets protected by the safety hook.

---

## Features

<table>
<tr>
<td width="50%" valign="top">

### Skills System
Domain-specific knowledge modules that Claude loads when relevant:

| Skill | Purpose |
|-------|---------|
| `python-dev` | Python with KISS, YAGNI, SOLID + TDD |
| `k8s-dev` | Kubernetes cloud-agnostic patterns |
| `skill-developer` | Meta-skill for creating skills |
| `discovery` | Idea-to-PRD pipeline with 5 phases |
| `react-best-practices`** | 40+ React/Next.js performance rules |
| `vue-best-practices` | 40+ Vue 3/Nuxt 3 performance rules |
| `frontend-design`* | Production-grade UI with distinctive design |
| `theme-factory`* | Curated themes for artifacts |
| `webapp-testing`* | Playwright browser testing |
| `web-artifacts-builder`* | React/Tailwind HTML artifacts |

*From [Anthropic Skills](https://github.com/anthropics/skills) | **From [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills)

**Activation:** `/python-dev`, `/k8s-dev`, `/skill-dev`, `/discovery`, `/react-best-practices`, `/vue-best-practices`

</td>
<td width="50%" valign="top">

### 12 Specialized Agents
Autonomous sub-agents for complex tasks:

| Agent | Purpose |
|-------|---------|
| `test-writer` | TDD-driven test creation |
| `error-debugger` | Systematic debugging |
| `code-architecture-reviewer` | Code review |
| `refactor-planner` | Refactoring strategies |
| `api-tester` | API endpoint testing |
| `documentation-architect` | Create docs |
| `dependency-analyzer` | Audit dependencies |
| `performance-profiler` | Find bottlenecks |
| `plan-reviewer` | Review plans |
| `code-refactor-master` | Execute refactoring |
| `web-research-specialist` | Research online |
| `integration-verifier` | Verify feature integration |

</td>
</tr>
<tr>
<td width="50%" valign="top">

### Safety & Audit System
Built-in protection and logging:

| Hook | Function |
|------|----------|
| `safety_validator.py` | Blocks destructive commands |
| `audit_logger.py` | Full action audit trail |
| `skill-suggester.py` | Smart skill recommendations |
| `auto-format.sh` | Auto-format on save |

**Permission Tiers:**
- **ALLOW**: Read, Glob, Grep, tests, linters
- **ASK**: Edit, Write, rm, docker, git push
- **DENY**: .env files, secrets, credentials

</td>
<td width="50%" valign="top">

### Dev Docs Pattern
Persistent context across sessions:

```
dev_docs/
├── active/          # Work in progress
│   └── 0001_task/
│       ├── *-plan.md      # Strategy
│       ├── *-context.md   # State & decisions
│       ├── *-tasks.md     # Checklist
│       └── ralph_progress.txt
└── archive/         # Completed work
```

**Commands:** `/dev-docs`, `/dev-docs-update`, `/continue-dev`, `/ralph`, `/commit-git`

</td>
</tr>
</table>

---

## Available Commands

| Command | Description |
|---------|-------------|
| `/discovery` | Create PRD from idea through 5-phase pipeline |
| `/dev-docs` | Create task documentation from PRD or requirements |
| `/ralph` | Start autonomous implementation agent |
| `/continue-dev` | Resume task implementation (manual, with extended thinking) |
| `/commit-git` | Analyze changes, create conventional commits, push |
| `/python-dev` | Activate Python development skill |
| `/k8s-dev` | Activate Kubernetes development skill |
| `/skill-dev` | Activate skill development skill |
| `/frontend-design` | Activate frontend design skill |

---

## Directory Structure

```
.claude/
├── agents/                 # 11 specialized autonomous agents
│   ├── api-tester.md
│   ├── code-architecture-reviewer.md
│   ├── code-refactor-master.md
│   ├── dependency-analyzer.md
│   ├── documentation-architect.md
│   ├── error-debugger.md
│   ├── integration-verifier.md
│   ├── performance-profiler.md
│   ├── plan-reviewer.md
│   ├── refactor-planner.md
│   ├── test-writer.md
│   └── web-research-specialist.md
│
├── skills/                 # Domain knowledge modules
│   ├── python-dev/
│   ├── k8s-dev/
│   ├── skill-developer/
│   ├── react-best-practices/   # From Vercel (40+ perf rules)
│   ├── vue-best-practices/     # Vue/Nuxt adaptation (40+ rules)
│   ├── frontend-design/    # From Anthropic
│   ├── theme-factory/      # From Anthropic
│   ├── webapp-testing/     # From Anthropic
│   ├── web-artifacts-builder/  # From Anthropic
│   └── skill-rules.json
│
├── hooks/                  # Event-triggered automation
│   ├── safety_validator.py
│   ├── audit_logger.py
│   ├── skill-suggester.py
│   ├── skill-validator.py
│   └── auto-format.sh
│
├── commands/               # Slash commands
│   ├── discovery.md
│   ├── dev-docs.md
│   ├── ralph.md
│   ├── continue-dev.md
│   ├── commit-git.md
│   ├── python-dev.md
│   ├── k8s-dev.md
│   └── skill-dev.md
│
├── scripts/
│   ├── ralph/              # Ralph agent orchestrator
│   │   ├── ralph.sh        # Main script
│   │   └── prompts/        # Agent prompts
│   ├── discovery_agent/    # Discovery pipeline
│   └── next-task-number.sh
│
├── audit_logs/             # Action audit trail
│
├── plans/                  # Plan mode artifacts (plansDirectory)
│
└── settings.json           # Main configuration
```

---

## Discovery Pipeline

Transform ideas into structured Product Requirements Documents through a 5-phase pipeline.

### Phases

| Phase | Mode | Description |
|-------|------|-------------|
| 1. **Interview** | Interactive | Socratic questioning to understand your requirements |
| 2. **Research** | Autonomous | Web search to validate and expand findings |
| 3. **Synthesis** | Autonomous | Combine insights into structured PRD draft |
| 4. **Review** | Autonomous | Adversarial critical review with lens scoring |
| 5. **Consolidation** | Autonomous | Synthesize review into final PRD |

### Usage

```bash
# Start new discovery (interactive)
/discovery

# Start with description (skips prompt)
/discovery -d "A mobile app for tracking expenses"

# Resume from specific phase
/discovery --resume research
/discovery --resume synthesis

# List available phases
/discovery --list
```

### Output

All artifacts saved to `docs/discovery/<project-name>/`:
- `01-interview.md` - Interview notes
- `02-research.md` - Research findings
- `03-prd-draft.md` - PRD draft
- `04-prd-review.md` - Critical review with lens scores
- `05-prd-final.md` - Final consolidated PRD

---

## Documentation

| Document | Description |
|----------|-------------|
| [CLAUDE.md](CLAUDE.md) | Main guidelines (KISS, YAGNI, SOLID) |
| [.claude/skills/README.md](.claude/skills/README.md) | Skills system guide |
| [.claude/agents/README.md](.claude/agents/README.md) | Agents documentation |
| [.claude/hooks/README.md](.claude/hooks/README.md) | Hooks configuration |
| [.claude/dev_docs/README.md](.claude/dev_docs/README.md) | Dev docs pattern |
| [.claude/commands/ralph.md](.claude/commands/ralph.md) | Ralph agent guide |

---

## Customization

### Adding Custom Skills

1. Create directory: `.claude/skills/my-skill/`
2. Add `SKILL.md` with frontmatter
3. Register in `skill-rules.json`
4. Optionally add slash command

### Adding Custom Agents

1. Create `.claude/agents/my-agent.md`
2. Include YAML frontmatter (name, description, model, color)
3. Write detailed instructions

### Modifying Permissions

Edit `.claude/settings.json`:

```json
{
  "plansDirectory": ".claude/plans/",
  "permissions": {
    "allow": ["..."],
    "ask": ["..."],
    "deny": ["..."]
  }
}
```

> **Note:** The `plansDirectory` setting configures where Claude Code saves plan files when using plan mode. Plans are stored in `.claude/plans/` for better organization.

---

## Known Limitations

> **⚠️ Ralph Not Sandboxed**: Ralph currently runs with `--dangerously-skip-permissions` flag for autonomous operation. This means:
> - Ralph bypasses normal permission prompts (by design, for automation)
> - Safety hooks (`safety_validator.py`) still block dangerous operations
> - Worktree isolation protects your main branch
> - However, Ralph is **NOT** running in a true sandbox environment
>
> **Mitigation**: Always review Ralph's changes before merging. Consider running Ralph in a VM or container for sensitive projects.

---

## Connect With Me

<div align="center">

[![Blog](https://img.shields.io/badge/Blog-demystifAI.blog-FF5722?style=for-the-badge&logo=blogger&logoColor=white)](https://www.demystifAI.blog)
[![Substack](https://img.shields.io/badge/Substack-demystifAI-FF6719?style=for-the-badge&logo=substack&logoColor=white)](https://demystifAI.substack.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-tgusciora-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/tgusciora/)

</div>

---

## License

This project is available for personal and commercial use. Feel free to adapt it for your needs.

---

<div align="center">

**Built with Claude Code**

*Making AI-assisted development safer, smarter, and more productive*

</div>
