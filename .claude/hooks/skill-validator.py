#!/usr/bin/env python3
"""
Skill Validator Hook for Claude Code
=====================================

Validates skill-related operations and provides warnings (not blocks).
Implements soft enforcement per requirements.

Exit Codes:
    0 - Always (warnings only, never blocks)

Output:
    Warnings to stderr when potential issues detected.

Checks:
    - SKILL.md exceeds 500 lines
    - Missing required sections in SKILL.md
    - Invalid frontmatter format
    - skill-rules.json syntax errors
    - Missing trigger configuration

Integration:
    Configured as PreToolUse hook in .claude/settings.json

Performance Target:
    < 200ms execution time
"""

import json
import re
import sys
from typing import Any


def warn(message: str) -> None:
    """Output warning to stderr (does not block)."""
    print(f"[Skill Warning] {message}", file=sys.stderr)


def check_skill_file_length(file_path: str, content: str) -> None:
    """Warn if SKILL.md exceeds 500 lines."""
    if not file_path.endswith("SKILL.md"):
        return

    line_count = content.count("\n") + 1

    if line_count > 500:
        warn(
            f"SKILL.md has {line_count} lines (exceeds 500-line guideline). "
            "Consider moving detailed content to resource files."
        )
    elif line_count > 400:
        warn(
            f"SKILL.md has {line_count} lines (approaching 500-line limit). "
            "Plan for resource files if adding more content."
        )


def check_required_sections(file_path: str, content: str) -> None:
    """Warn if SKILL.md missing required sections."""
    if not file_path.endswith("SKILL.md"):
        return

    required_sections = [
        ("## Purpose", "Purpose"),
        ("## When to Use", "When to Use This Skill"),
    ]

    missing = []
    for marker, name in required_sections:
        if marker not in content:
            missing.append(name)

    if missing:
        warn(f"SKILL.md missing recommended sections: {', '.join(missing)}")


def check_frontmatter(file_path: str, content: str) -> None:
    """Warn if SKILL.md has invalid frontmatter."""
    if not file_path.endswith("SKILL.md"):
        return

    # Check for frontmatter presence
    if not content.startswith("---"):
        warn("SKILL.md should start with YAML frontmatter (---)")
        return

    # Check for closing frontmatter
    if content.count("---") < 2:
        warn("SKILL.md frontmatter not properly closed (needs two ---)")
        return

    # Extract and check frontmatter content
    frontmatter_match = re.search(
        r"^---\s*\n(.*?)\n---",
        content,
        re.DOTALL
    )

    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)

        if "name:" not in frontmatter:
            warn("SKILL.md frontmatter missing 'name' field")

        if "description:" not in frontmatter:
            warn("SKILL.md frontmatter missing 'description' field")


def check_skill_rules_syntax(file_path: str, content: str) -> None:
    """Warn if skill-rules.json has syntax or structure issues."""
    if not file_path.endswith("skill-rules.json"):
        return

    try:
        rules = json.loads(content)
    except json.JSONDecodeError as e:
        warn(f"skill-rules.json has invalid JSON: {e}")
        return

    if not isinstance(rules, dict):
        warn("skill-rules.json should be an object with skill names as keys")
        return

    for skill_name, config in rules.items():
        if not isinstance(config, dict):
            warn(f"Skill '{skill_name}' should be an object")
            continue

        # Check required fields
        if "type" not in config:
            warn(
                f"Skill '{skill_name}' missing 'type' field "
                "(should be 'domain', 'guardrail', or 'workflow')"
            )

        # Check for triggers
        has_prompt_triggers = bool(config.get("promptTriggers"))
        has_file_triggers = bool(config.get("fileTriggers"))

        if not has_prompt_triggers and not has_file_triggers:
            warn(
                f"Skill '{skill_name}' has no triggers defined - "
                "will never auto-activate"
            )

        # Check enforcement for guardrails
        if config.get("type") == "guardrail":
            enforcement = config.get("enforcement")
            if enforcement == "block" and "blockMessage" not in config:
                warn(
                    f"Guardrail '{skill_name}' uses 'block' enforcement "
                    "but has no 'blockMessage'"
                )


def check_resource_file_naming(file_path: str, content: str) -> None:
    """Warn if resource file doesn't follow naming convention."""
    if "/resources/" not in file_path:
        return

    if not file_path.endswith(".md"):
        return

    # Get filename without path and extension
    filename = file_path.split("/")[-1]
    name_without_ext = filename.replace(".md", "")

    # Check if UPPERCASE_SNAKE_CASE
    if not re.match(r"^[A-Z][A-Z0-9_]*$", name_without_ext):
        warn(
            f"Resource file '{filename}' should use UPPERCASE_SNAKE_CASE "
            "(e.g., BEST_PRACTICES.md)"
        )


def main() -> None:
    """Main entry point."""
    try:
        data: dict[str, Any] = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    # Only validate Write/Edit operations on skill files
    if tool_name not in ["Write", "Edit"]:
        sys.exit(0)

    file_path = tool_input.get("file_path", "")

    # Only check files in .claude/skills/
    if ".claude/skills/" not in file_path:
        sys.exit(0)

    # Get content based on tool type
    if tool_name == "Write":
        content = tool_input.get("content", "")
    else:  # Edit
        content = tool_input.get("new_string", "")
        # For Edit, we might not have full file content
        # Run more limited checks

    if not content:
        sys.exit(0)

    # Run checks
    check_skill_file_length(file_path, content)
    check_required_sections(file_path, content)
    check_frontmatter(file_path, content)
    check_skill_rules_syntax(file_path, content)
    check_resource_file_naming(file_path, content)

    # Always exit 0 - warnings only, never block
    sys.exit(0)


if __name__ == "__main__":
    main()
