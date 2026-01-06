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

**Purpose:** Kubernetes development with cloud-agnostic patterns

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

### frontend-design

> *Sourced from [Anthropic Skills Repository](https://github.com/anthropics/skills)*

**Purpose:** Create distinctive, production-grade frontend interfaces with high design quality

**Files:**
- `SKILL.md` - Main guide with design thinking and aesthetics guidelines

**Triggers:**
- Keywords: `frontend design`, `ui design`, `landing page`, `dashboard`, etc.
- File patterns: `**/components/**/*.tsx`, `**/pages/**/*.tsx`, `**/*.css`

**Use when:**
- Building web components, pages, or applications
- Creating landing pages or dashboards
- Styling/beautifying any web UI
- Need distinctive design that avoids generic AI aesthetics

**Key Principles:**
- Bold aesthetic direction (minimalist, maximalist, retro-futuristic, etc.)
- Distinctive typography choices (avoid generic fonts like Inter, Arial)
- Cohesive color themes with CSS variables
- Creative motion and micro-interactions

**[View Skill](frontend-design/)**

---

### theme-factory

> *Sourced from [Anthropic Skills Repository](https://github.com/anthropics/skills)*

**Purpose:** Apply professional themes with curated color palettes and font pairings to artifacts

**Files:**
- `SKILL.md` - Main guide
- `themes/` - 10 pre-built theme definitions (Ocean Depths, Sunset Boulevard, etc.)

**Triggers:**
- Keywords: `theme`, `color palette`, `font pairing`, `apply theme`
- Intent patterns: `(apply|choose|select|use).*?theme`

**Use when:**
- Styling presentation slides, docs, or HTML artifacts
- Need consistent professional color/font choices
- Want to apply pre-built themes or create custom ones

**Available Themes:**
1. Ocean Depths - Professional maritime theme
2. Sunset Boulevard - Warm sunset colors
3. Forest Canopy - Natural earth tones
4. Modern Minimalist - Clean grayscale
5. Golden Hour - Autumnal palette
6. Arctic Frost - Winter-inspired
7. Desert Rose - Dusty sophisticated tones
8. Tech Innovation - Bold tech aesthetic
9. Botanical Garden - Fresh garden colors
10. Midnight Galaxy - Cosmic deep tones

**[View Skill](theme-factory/)**

---

### webapp-testing

> *Sourced from [Anthropic Skills Repository](https://github.com/anthropics/skills)*

**Purpose:** Test local web applications using Playwright for browser automation

**Files:**
- `SKILL.md` - Main guide with patterns and examples
- `scripts/with_server.py` - Server lifecycle management

**Triggers:**
- Keywords: `playwright`, `browser test`, `e2e test`, `ui testing`
- File patterns: `**/tests/e2e/**`, `**/playwright/**`

**Use when:**
- Testing frontend functionality
- Debugging UI behavior
- Capturing browser screenshots
- End-to-end testing of web applications

**Key Patterns:**
- Reconnaissance-then-action pattern
- Server lifecycle management (single or multiple servers)
- Proper wait handling for dynamic content

**[View Skill](webapp-testing/)**

---

### web-artifacts-builder

> *Sourced from [Anthropic Skills Repository](https://github.com/anthropics/skills)*

**Purpose:** Build complex multi-component HTML artifacts with React, Tailwind CSS, and shadcn/ui

**Files:**
- `SKILL.md` - Main guide
- `scripts/init-artifact.sh` - Project initialization
- `scripts/bundle-artifact.sh` - Bundle to single HTML file

**Triggers:**
- Keywords: `html artifact`, `react artifact`, `shadcn`, `complex artifact`
- Intent patterns: `(create|build).*?(complex|elaborate).*?artifact`

**Use when:**
- Building elaborate, multi-component claude.ai artifacts
- Need state management or routing in artifacts
- Using shadcn/ui components
- NOT for simple single-file HTML/JSX artifacts

**Stack:**
- React 18 + TypeScript + Vite
- Tailwind CSS + shadcn/ui (40+ components pre-installed)
- Parcel for bundling to single HTML

**[View Skill](web-artifacts-builder/)**

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
├── python-dev/            # Python + TDD + SOLID
│   ├── SKILL.md
│   └── resources/
├── skill-developer/       # Meta-skill for creating skills
│   ├── SKILL.md
│   └── resources/
├── k8s-dev/               # Kubernetes patterns
│   ├── SKILL.md
│   └── resources/
├── frontend-design/       # Frontend UI design (from Anthropic)
│   └── SKILL.md
├── theme-factory/         # Artifact theming (from Anthropic)
│   ├── SKILL.md
│   └── themes/            # 10 pre-built themes
├── webapp-testing/        # Playwright testing (from Anthropic)
│   ├── SKILL.md
│   └── scripts/
└── web-artifacts-builder/ # React/Tailwind artifacts (from Anthropic)
    ├── SKILL.md
    └── scripts/
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
