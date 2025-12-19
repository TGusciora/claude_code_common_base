# Agents

Specialized agents for complex, multi-step tasks.

---

## How to Trigger an Agent

**Agents require explicit invocation.** They are NOT automatically triggered like skills.

### Invocation Pattern

Ask Claude to use a specific agent:

```
Use the [agent-name] agent to [your task]
```

### Examples

```
Use the test-writer agent to write tests for my validation function
Use the error-debugger agent to investigate this KeyError in user_service.py
Use the plan-reviewer agent to review my authentication implementation plan
Use the code-architecture-reviewer agent to review my new API endpoint
Use the dependency-analyzer agent to check for security vulnerabilities
```

### Tips for Best Results

- **Be specific** about what you want the agent to do
- **Provide context** - mention relevant files, error messages, or requirements
- **One task per invocation** - agents work best with focused objectives

---

## What Are Agents?

Agents are autonomous Claude instances that handle specific complex tasks. Unlike skills (which provide inline guidance), agents:
- Run as separate sub-tasks
- Work autonomously with minimal supervision
- Have specialized tool access
- Return comprehensive reports when complete

**Key advantage:** Agents are **standalone** - just copy the `.md` file and use immediately!

---

## Available Agents (11)

### api-tester
**Purpose:** Test API endpoints and validate request/response contracts

**When to use:**
- Testing new API endpoints
- Validating external API integrations
- Ensuring API contract compliance
- Testing error handling and edge cases

**Model:** Opus | **Color:** Orange

---

### code-architecture-reviewer
**Purpose:** Review code for architectural consistency and best practices

**When to use:**
- After implementing a new feature
- Before merging significant changes
- When refactoring code
- To validate architectural decisions

**Model:** Opus | **Color:** Blue

---

### code-refactor-master
**Purpose:** Plan and execute comprehensive refactoring

**When to use:**
- Reorganizing file structures
- Breaking down large components
- Updating import paths after moves
- Improving code maintainability

**Model:** Opus | **Color:** Cyan

---

### dependency-analyzer
**Purpose:** Analyze, audit, and manage project dependencies

**When to use:**
- Checking for outdated packages
- Scanning for security vulnerabilities
- Resolving version conflicts
- Finding unused dependencies

**Model:** Opus | **Color:** Yellow

---

### documentation-architect
**Purpose:** Create comprehensive documentation

**When to use:**
- Documenting new features
- Creating API documentation
- Writing developer guides
- Generating architectural overviews

**Model:** Opus | **Color:** Blue

---

### error-debugger
**Purpose:** Systematically debug errors and unexpected behavior

**When to use:**
- Cryptic error messages
- Intermittent/flaky failures
- Silent failures (wrong results, no error)
- Stack trace analysis

**Model:** Opus | **Color:** Red

---

### performance-profiler
**Purpose:** Identify bottlenecks and optimize code performance

**When to use:**
- Slow-running functions
- High memory usage
- Database query optimization
- Profiling CPU/memory usage

**Model:** Opus | **Color:** Purple

---

### plan-reviewer
**Purpose:** Review development plans before implementation

**When to use:**
- Before starting complex features
- Validating architectural plans
- Identifying potential issues early
- Getting second opinion on approach

**Model:** Opus | **Color:** Yellow

---

### refactor-planner
**Purpose:** Create comprehensive refactoring strategies

**When to use:**
- Planning code reorganization
- Modernizing legacy code
- Breaking down large files
- Improving code structure

**Model:** Opus | **Color:** Purple

---

### test-writer
**Purpose:** Write tests following TDD principles

**When to use:**
- Creating tests for new functions
- Adding test coverage to existing modules
- TDD approach (tests first)
- Ensuring atomic, isolated tests

**Model:** Opus | **Color:** Green

---

### web-research-specialist
**Purpose:** Research technical issues online

**When to use:**
- Debugging obscure errors
- Finding solutions to problems
- Researching best practices
- Comparing implementation approaches

**Model:** Opus | **Color:** Blue

---

## When to Use Agents vs Skills

| Use Agents When... | Use Skills When... |
|-------------------|-------------------|
| Task requires multiple steps | Need inline guidance |
| Complex analysis needed | Checking best practices |
| Autonomous work preferred | Want to maintain control |
| Task has clear end goal | Ongoing development work |
| Example: "Review all controllers" | Example: "Creating a new route" |

**Both can work together:**
- Skill provides patterns during development
- Agent reviews the result when complete

---

## Agent Quick Reference

| Agent | Purpose | Model | Color |
|-------|---------|-------|-------|
| api-tester | Test API endpoints | Opus | Orange |
| code-architecture-reviewer | Code review & architecture | Opus | Blue |
| code-refactor-master | Execute refactoring | Opus | Cyan |
| dependency-analyzer | Audit dependencies | Opus | Yellow |
| documentation-architect | Create documentation | Opus | Blue |
| error-debugger | Debug errors | Opus | Red |
| performance-profiler | Profile & optimize | Opus | Purple |
| plan-reviewer | Review plans | Opus | Yellow |
| refactor-planner | Plan refactoring | Opus | Purple |
| test-writer | Write TDD tests | Opus | Green |
| web-research-specialist | Web research | Opus | Blue |

---

## Creating Your Own Agents

Agents are markdown files with YAML frontmatter:

```markdown
---
name: agent-name
description: When to use this agent with examples
model: opus
color: blue
---

You are [role description]...

**Core Responsibilities:**
1. First responsibility
2. Second responsibility
...

**Output Format:**
- How to structure and save results
```

**Tips:**
- Be very specific in instructions
- Break complex tasks into numbered steps
- Specify exactly what to return
- Include examples of good output
- List available tools explicitly

---

## Troubleshooting

### Agent not found

```bash
# Check if agent file exists
ls -la .claude/agents/[agent-name].md
```

### Agent produces inconsistent results

- Review the agent's instructions for clarity
- Add more specific examples in the description
- Consider specifying a more capable model (opus vs sonnet)

---

## Next Steps

1. **Browse agents above** - Find ones useful for your work
2. **Ask Claude to use them** - "Use [agent] to [task]"
3. **Create your own** - Follow the pattern for your specific needs
