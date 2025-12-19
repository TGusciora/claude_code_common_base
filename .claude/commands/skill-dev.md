Activate the skill-developer skill to help with Claude Code skill development.

Read the skill file at `.claude/skills/skill-developer/SKILL.md` and apply its guidance to help the user with their skill development task.

## Task Detection

Determine what the user needs:

**Creating a new skill:**
- Guide them through the 5-step process in SKILL.md
- Help choose appropriate template from TEMPLATES.md
- Assist with trigger pattern design

**Debugging a skill:**
- Check skill-rules.json configuration
- Verify trigger patterns match expected prompts
- Review ANTI_PATTERNS.md for common issues

**Improving a skill:**
- Review against BEST_PRACTICES.md guidelines
- Check for FIRST_PRINCIPLES.md compliance
- Verify SKILL_ARCHITECTURE.md patterns

**Understanding skills:**
- Explain concepts from the skill developer skill
- Provide examples from templates
- Reference appropriate resource files

## Resource Files

Reference these for deeper guidance:

- `.claude/skills/skill-developer/resources/FIRST_PRINCIPLES.md` - KISS, YAGNI, DRY foundations
- `.claude/skills/skill-developer/resources/SKILL_ARCHITECTURE.md` - Structural patterns
- `.claude/skills/skill-developer/resources/BEST_PRACTICES.md` - Writing guidelines
- `.claude/skills/skill-developer/resources/ANTI_PATTERNS.md` - Mistakes to avoid
- `.claude/skills/skill-developer/resources/TEMPLATES.md` - Starter templates

## Key Files

- `.claude/skills/skill-rules.json` - Where trigger configuration lives
- `.claude/skills/[skill-name]/SKILL.md` - Main skill files
- `.claude/commands/` - Slash command definitions
