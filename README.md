<div align="center">

# 🤖 Claude Code Portable Setup

### A production-ready, portable configuration for Claude Code CLI

[![Claude Code](https://img.shields.io/badge/Claude%20Code-CLI-blueviolet?style=for-the-badge&logo=anthropic)](https://claude.ai/claude-code)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge)](CONTRIBUTING.md)

---

**A comprehensive, batteries-included configuration framework for Claude Code**
*Skills • Agents • Hooks • Safety • Audit Logging • Dev Docs*

[Features](#-features) • [Quick Start](#-quick-start) • [Directory Structure](#-directory-structure) • [Documentation](#-documentation)

</div>

---

## 📖 About

This repository provides a **portable Claude Code configuration** that you can drop into any project to supercharge your AI-assisted development workflow. It includes pre-configured skills, specialized agents, safety hooks, and a persistent documentation pattern for maintaining context across sessions.

### 🙏 Credits & Attribution

| | |
|---|---|
| **Author** | **Tomasz Guściora** |
| **Based on** | [claude-code-infrastructure-showcase](https://github.com/diet103/claude-code-infrastructure-showcase) by diet103 |
| **Original Discussion** | [Claude Code is a Beast - Tips from 6 Months of Use](https://www.reddit.com/r/ClaudeAI/comments/1oivjvm/claude_code_is_a_beast_tips_from_6_months_of/) |

---

## ✨ Features

<table>
<tr>
<td width="50%" valign="top">

### 🎯 Skills System
Domain-specific knowledge modules that Claude loads when relevant:

| Skill | Purpose |
|-------|---------|
| `python-dev` | Python with KISS, YAGNI, SOLID + TDD |
| `k8s-dev` | Kubernetes cloud-agnostic patterns |
| `skill-developer` | Meta-skill for creating skills |

**Activation:** `/python-dev`, `/k8s-dev`, `/skill-dev`

</td>
<td width="50%" valign="top">

### 🤖 11 Specialized Agents
Autonomous sub-agents for complex tasks:

| Agent | Purpose |
|-------|---------|
| `test-writer` | TDD-driven test creation |
| `error-debugger` | Systematic debugging |
| `code-architecture-reviewer` | Code review |
| `refactor-planner` | Refactoring strategies |
| `api-tester` | API endpoint testing |
| `+ 6 more...` | See full list below |

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 🛡️ Safety & Audit System
Built-in protection and logging:

| Hook | Function |
|------|----------|
| `safety_validator.py` | Blocks destructive commands |
| `audit_logger.py` | Full action audit trail |
| `skill-suggester.py` | Smart skill recommendations |
| `auto-format.sh` | Auto-format on save |

</td>
<td width="50%" valign="top">

### 📚 Dev Docs Pattern
Persistent context across sessions:

```
dev_docs/
├── active/          # Work in progress
│   └── 0001_task/
│       ├── *-plan.md
│       ├── *-context.md
│       └── *-tasks.md
└── archive/         # Completed work
```

**Commands:** `/dev-docs`, `/dev-docs-update`

</td>
</tr>
</table>

---

## 🚀 Quick Start

### 1. Clone or Copy

```bash
# Clone this repository
git clone https://github.com/YOUR_USERNAME/claude_code_common_base.git

# Or copy the .claude folder to your project
cp -r claude_code_common_base/.claude your-project/
cp claude_code_common_base/CLAUDE.md your-project/
```

### 2. Make Hooks Executable

```bash
chmod +x .claude/hooks/*.py
chmod +x .claude/hooks/*.sh
chmod +x .claude/scripts/*.sh
```

### 3. Start Using

```bash
# Launch Claude Code in your project
claude

# Use skills
/python-dev    # Activate Python development skill

# Use agents
"Use the test-writer agent to write tests for my function"
```

---

## 📁 Directory Structure

```
.claude/
├── 📂 agents/              # 11 specialized autonomous agents
│   ├── api-tester.md
│   ├── code-architecture-reviewer.md
│   ├── code-refactor-master.md
│   ├── dependency-analyzer.md
│   ├── documentation-architect.md
│   ├── error-debugger.md
│   ├── performance-profiler.md
│   ├── plan-reviewer.md
│   ├── refactor-planner.md
│   ├── test-writer.md
│   └── web-research-specialist.md
│
├── 📂 skills/              # Domain knowledge modules
│   ├── python-dev/         # Python + TDD + SOLID
│   ├── k8s-dev/            # Kubernetes patterns
│   ├── skill-developer/    # Meta-skill for creating skills
│   └── skill-rules.json    # Trigger configuration
│
├── 📂 hooks/               # Event-triggered automation
│   ├── safety_validator.py # Block dangerous commands
│   ├── audit_logger.py     # Action logging
│   ├── skill-suggester.py  # Smart skill suggestions
│   ├── skill-validator.py  # Skill file validation
│   └── auto-format.sh      # Auto-formatting
│
├── 📂 commands/            # Slash commands
│   ├── python-dev.md
│   ├── k8s-dev.md
│   ├── skill-dev.md
│   ├── dev-docs.md
│   └── dev-docs-update.md
│
├── 📂 scripts/             # Helper scripts
│   └── next-task-number.sh
│
├── 📂 audit_logs/          # Action audit trail
│
└── ⚙️ settings.json         # Main configuration
```

---

## 🎯 Available Agents

| Agent | Purpose | Use Case |
|-------|---------|----------|
| 🧪 `test-writer` | TDD test creation | "Write tests for my validation function" |
| 🔴 `error-debugger` | Debug errors systematically | "Debug this KeyError" |
| 🔵 `code-architecture-reviewer` | Code & architecture review | "Review my new API endpoint" |
| 🟣 `refactor-planner` | Plan refactoring strategies | "Plan how to split this large module" |
| 🟣 `performance-profiler` | Find bottlenecks | "Profile this slow function" |
| 🟡 `plan-reviewer` | Review implementation plans | "Review my authentication plan" |
| 🟡 `dependency-analyzer` | Audit dependencies | "Check for security vulnerabilities" |
| 🟠 `api-tester` | Test API endpoints | "Test the /users endpoint" |
| 🔵 `documentation-architect` | Create documentation | "Document this feature" |
| 🔵 `web-research-specialist` | Research online | "Find solutions for this error" |
| 🟢 `code-refactor-master` | Execute refactoring | "Reorganize the components folder" |

**Usage:** `Use the [agent-name] agent to [your task]`

---

## 🛡️ Safety Features

### Permission Tiers

```
✅ ALLOW (no confirmation)
   Read, Glob, Grep, git status, git log, tests, linters

⚠️ ASK (requires confirmation)
   Edit, Write, rm, docker, kubectl delete, git push, installs

🚫 DENY (always blocked)
   .env files, secrets, credentials, rm -rf /
```

### Built-in Protections

- **Destructive Command Blocking** - `rm -rf /`, `rm -rf ~` are blocked
- **Sensitive File Protection** - `.env`, `credentials`, `id_rsa` access denied
- **Full Audit Trail** - Every action logged to `.claude/audit_logs/`

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [CLAUDE.md](CLAUDE.md) | Main guidelines (KISS, YAGNI, SOLID) |
| [.claude/skills/README.md](.claude/skills/README.md) | Skills system guide |
| [.claude/agents/README.md](.claude/agents/README.md) | Agents documentation |
| [.claude/hooks/README.md](.claude/hooks/README.md) | Hooks configuration |
| [.claude/dev_docs/README.md](.claude/dev_docs/README.md) | Dev docs pattern |

---

## 🔧 Customization

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
  "permissions": {
    "allow": ["..."],
    "ask": ["..."],
    "deny": ["..."]
  }
}
```

---

## 🌐 Connect With Me

<div align="center">

[![Blog](https://img.shields.io/badge/Blog-demystifAI.blog-FF5722?style=for-the-badge&logo=blogger&logoColor=white)](https://www.demystifAI.blog)
[![Substack](https://img.shields.io/badge/Substack-demystifAI-FF6719?style=for-the-badge&logo=substack&logoColor=white)](https://demystifAI.substack.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-tgusciora-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/tgusciora/)

</div>

---

## 📜 License

This project is available for personal and commercial use. Feel free to adapt it for your needs.

---

<div align="center">

**Built with 🤖 Claude Code**

*Making AI-assisted development safer, smarter, and more productive*

</div>