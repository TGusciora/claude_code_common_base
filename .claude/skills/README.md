# Skills

Skills are modular knowledge bases that Claude loads when relevant. They provide domain-specific guidelines, best practices, and code examples.

---

## How Skill Activation Works

### Automatic Flow

1. **User submits prompt** (e.g., "write a Python function")
2. **skill-suggester.py hook** analyzes the prompt
3. **Matches against skill-rules.json** triggers (keywords, patterns, file paths)
4. **Suggests matching skills** with priority levels
5. **User invokes slash command** (e.g., `/python-dev`)
6. **Claude reads SKILL.md** and applies guidance

### Manual Activation

Use slash commands directly:
```
/python-dev    # Activate Python development skill
/skill-dev     # Activate skill developer skill
/k8s-dev       # Activate Kubernetes development skill
```

---

## Available Skills

### python-dev

**Purpose:** Python development with KISS, YAGNI, SOLID principles and TDD

**Files:**
- `SKILL.md` - Main guide (400+ lines)
- `resources/SOLID_PRINCIPLES.md` - Detailed SOLID patterns
- `resources/TDD_PATTERNS.md` - Testing patterns and pytest fixtures
- `resources/ANTI_PATTERNS.md` - Common mistakes to avoid

**Triggers:**
- Keywords: `python`, `pytest`, `tdd`, `type hints`, `ruff`, etc.
- File patterns: `*.py`, `**/*.py`, `**/conftest.py`

**Use when:**
- Writing Python functions, classes, or modules
- Writing/improving pytest tests
- Refactoring Python code
- Code review

**[View Skill](python-dev/)**

---

### skill-developer

**Purpose:** Meta-skill for creating Claude Code skills

**Files:**
- `SKILL.md` - Main guide
- `resources/FIRST_PRINCIPLES.md` - KISS, YAGNI, DRY foundations
- `resources/SKILL_ARCHITECTURE.md` - Structural patterns
- `resources/BEST_PRACTICES.md` - Writing guidelines
- `resources/ANTI_PATTERNS.md` - Mistakes to avoid
- `resources/TEMPLATES.md` - Starter templates

**Triggers:**
- Keywords: `skill system`, `create skill`, `skill triggers`, etc.
- File patterns: `.claude/skills/**`, `**/SKILL.md`

**Use when:**
- Creating new skills
- Understanding skill structure
- Working with skill-rules.json
- Debugging skill activation

**[View Skill](skill-developer/)**

---

### k8s-dev

**Purpose:** Kubernetes development with cloud-agnostic patterns (Azure Phase 1)

**Files:**
- `SKILL.md` - Main guide with patterns and templates
- `resources/MANIFEST_TEMPLATES.md` - Complete manifest examples
- `resources/LABEL_STANDARDS.md` - Labeling conventions
- `resources/COMMON_ISSUES.md` - Troubleshooting guide

**Triggers:**
- Keywords: `kubernetes`, `k8s`, `deployment`, `helm`, `manifest`, etc.
- File patterns: `**/k8s/**`, `**/helm/**`, `**/infra/**/*.yaml`

**Use when:**
- Creating K8s manifests (Deployments, Services, etc.)
- Setting up Helm charts
- Reviewing K8s configurations
- Troubleshooting K8s deployments

**Key Standards:**
- ClusterIP services only
- Resource limits required
- 5 required labels (app, system, component, owner, version)
- Database in separate Pod

**[View Skill](k8s-dev/)**

---

## skill-rules.json Configuration

### Location

`.claude/skills/skill-rules.json`

### Format

```json
{
  "skills": {
    "skill-name": {
      "type": "domain",
      "enforcement": "suggest",
      "priority": "high",
      "promptTriggers": {
        "keywords": ["python", "pytest"],
        "intentPatterns": ["(write|create).*python"]
      },
      "fileTriggers": {
        "pathPatterns": ["**/*.py"],
        "pathExclusions": ["**/.venv/**"]
      }
    }
  }
}
```

### Enforcement Levels

| Level | Behavior |
|-------|----------|
| `suggest` | Skill appears as suggestion, doesn't block |
| `warn` | Shows warning but allows proceeding |
| `block` | Must use skill before proceeding (guardrail) |

### Priority Levels

| Priority | When to Use |
|----------|-------------|
| `critical` | Always trigger when matched |
| `high` | Trigger for most matches |
| `medium` | Trigger for clear matches |
| `low` | Trigger only for explicit matches |

---

## Creating New Skills

### Quick Start

1. **Create skill directory:**
   ```bash
   mkdir -p .claude/skills/my-skill/resources
   ```

2. **Create SKILL.md:**
   ```markdown
   ---
   name: my-skill
   description: What this skill does
   ---

   # My Skill

   ## Purpose
   [Why this skill exists]

   ## When to Use
   [Scenarios]

   ## Quick Reference
   [Key patterns]
   ```

3. **Add to skill-rules.json:**
   ```json
   {
     "skills": {
       "my-skill": {
         "type": "domain",
         "enforcement": "suggest",
         "priority": "high",
         "promptTriggers": {
           "keywords": ["keyword1", "keyword2"]
         },
         "fileTriggers": {
           "pathPatterns": ["src/**/*.py"]
         }
       }
     }
   }
   ```

4. **Create slash command** (optional):
   ```bash
   touch .claude/commands/my-skill.md
   ```

See **skill-developer** skill for comprehensive guidance.

---

## Troubleshooting

### Skill isn't activating

**Check:**
1. Is skill directory in `.claude/skills/`?
2. Is skill listed in `skill-rules.json`?
3. Do `pathPatterns` match your files?
4. Is skill-suggester.py hook enabled in settings.json?

**Debug:**
```bash
# Check skill exists
ls -la .claude/skills/

# Validate skill-rules.json
cat .claude/skills/skill-rules.json | jq .

# Check hooks are executable
ls -la .claude/hooks/*.py
```

### Skill activates too often

- Make keywords more specific in skill-rules.json
- Narrow `pathPatterns`
- Add `pathExclusions`

### Skill never activates

- Add more keywords
- Broaden `pathPatterns`
- Check that skill-suggester.py hook is configured

---

## File Structure

```
.claude/skills/
├── README.md              # This file
├── skill-rules.json       # Trigger configuration
├── python-dev/
│   ├── SKILL.md           # Main skill file
│   └── resources/         # Deep-dive reference files
├── skill-developer/
│   ├── SKILL.md
│   └── resources/
└── k8s-dev/
    ├── SKILL.md           # Main K8s guide
    └── resources/
        ├── MANIFEST_TEMPLATES.md
        ├── LABEL_STANDARDS.md
        └── COMMON_ISSUES.md
```

---

## Related Files

| File | Purpose |
|------|---------|
| `skill-rules.json` | Trigger configuration |
| `.claude/hooks/skill-suggester.py` | Analyzes prompts, suggests skills |
| `.claude/commands/python-dev.md` | Python skill activation command |
| `.claude/commands/skill-dev.md` | Skill developer activation command |
| `.claude/commands/k8s-dev.md` | Kubernetes skill activation command |
| `.claude/repo_specific/K8S_OPERATIONS.md` | K8s operational standards reference |
