Activate the python-dev skill to help with Python development following KISS, YAGNI, SOLID principles and TDD.

Read the skill file at `.claude/skills/python-dev/SKILL.md` and apply its guidance.

## Task Detection

Determine what the user needs:

**Writing new code:**
- Guide with KISS principles (one function = one task)
- Suggest TDD approach (test first)
- Apply type hints

**Writing tests:**
- Follow TDD red-green-refactor cycle
- Use Arrange-Act-Assert structure
- Apply proper test naming: test_<function>_<scenario>_<expected>

**Refactoring:**
- Check against SOLID principles
- Identify anti-patterns
- Suggest incremental improvements

**Code review:**
- Review against anti-patterns
- Check for proper test coverage
- Verify type hints and documentation

## Resource Files

Reference these for deeper guidance:

- `.claude/skills/python-dev/resources/SOLID_PRINCIPLES.md` - Detailed SOLID patterns
- `.claude/skills/python-dev/resources/TDD_PATTERNS.md` - Testing patterns and pytest fixtures
- `.claude/skills/python-dev/resources/ANTI_PATTERNS.md` - Common mistakes to avoid

## Key Principles

- **KISS**: Keep functions focused, avoid clever code
- **YAGNI**: Only implement what's needed now
- **SOLID**: Single responsibility, dependency injection
- **TDD**: Write test first, then minimal code, then refactor
