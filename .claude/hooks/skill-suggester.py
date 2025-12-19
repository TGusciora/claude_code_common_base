#!/usr/bin/env python3
"""
Skill Suggester Hook for Claude Code
=====================================

Analyzes user prompts and file context to suggest relevant skills.
Implements soft enforcement - suggests but never blocks.

Exit Codes:
    0 - Always (suggestions are advisory, never blocking)

Output:
    Skill suggestions via stdout to inject into Claude context.

Integration:
    Configured as UserPromptSubmit hook in .claude/settings.json

Performance Target:
    < 100ms execution time
"""

import json
import re
import sys
from pathlib import Path
from typing import Any


def load_skill_rules() -> dict[str, Any]:
    """Load skill-rules.json from skills directory."""
    # Try relative to this hook file
    hook_dir = Path(__file__).parent
    rules_path = hook_dir.parent / "skills" / "skill-rules.json"

    if rules_path.exists():
        try:
            return json.loads(rules_path.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def match_keywords(prompt: str, keywords: list[str]) -> list[str]:
    """Check if prompt contains any trigger keywords. Returns matched keywords."""
    prompt_lower = prompt.lower()
    return [kw for kw in keywords if kw.lower() in prompt_lower]


def match_intent_patterns(prompt: str, patterns: list[str]) -> list[str]:
    """Check if prompt matches any intent patterns. Returns matched patterns."""
    matches = []
    for pattern in patterns:
        try:
            if re.search(pattern, prompt, re.IGNORECASE):
                matches.append(pattern)
        except re.error:
            # Invalid regex, skip
            continue
    return matches


def match_path_patterns(
    file_paths: list[str],
    patterns: list[str],
    exclusions: list[str] | None = None
) -> list[str]:
    """Check if any file paths match trigger patterns. Returns matched paths."""
    from fnmatch import fnmatch

    exclusions = exclusions or []
    matches = []

    for path in file_paths:
        # Check exclusions first
        excluded = any(fnmatch(path, excl) for excl in exclusions)
        if excluded:
            continue

        # Check inclusions
        for pattern in patterns:
            if fnmatch(path, pattern):
                matches.append(path)
                break

    return matches


def find_matching_skills(
    prompt: str,
    file_paths: list[str],
    rules: dict[str, Any]
) -> list[dict[str, Any]]:
    """Find all skills that match current context."""
    matches = []

    # Handle nested structure: rules may have "skills" key or be flat
    skills = rules.get("skills", rules)

    for skill_name, config in skills.items():
        # Skip non-skill entries (version, notes, etc.)
        if not isinstance(config, dict) or "promptTriggers" not in config:
            continue
        score = 0
        reasons = []

        # Check prompt triggers
        prompt_triggers = config.get("promptTriggers", {})

        keywords = prompt_triggers.get("keywords", [])
        matched_keywords = match_keywords(prompt, keywords)
        if matched_keywords:
            score += 2
            reasons.append(f"keyword: {matched_keywords[0]}")

        intent_patterns = prompt_triggers.get("intentPatterns", [])
        matched_intents = match_intent_patterns(prompt, intent_patterns)
        if matched_intents:
            score += 1
            reasons.append("intent match")

        # Check file triggers
        file_triggers = config.get("fileTriggers", {})
        path_patterns = file_triggers.get("pathPatterns", [])
        path_exclusions = file_triggers.get("pathExclusions", [])

        if path_patterns:
            matched_paths = match_path_patterns(
                file_paths,
                path_patterns,
                path_exclusions
            )
            if matched_paths:
                score += 1
                reasons.append("file context")

        if score > 0:
            matches.append({
                "skill": skill_name,
                "score": score,
                "reasons": reasons,
                "priority": config.get("priority", "medium"),
                "description": config.get("description", ""),
                "enforcement": config.get("enforcement", "suggest")
            })

    # Sort by score (descending), then priority
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    matches.sort(
        key=lambda x: (-x["score"], priority_order.get(x["priority"], 2))
    )

    return matches


def format_all_suggestions(matches: list[dict[str, Any]]) -> str:
    """Format all skill matches as a visually prominent suggestion block."""
    if not matches:
        return ""

    # Group matches by priority
    priority_groups: dict[str, list[dict[str, Any]]] = {
        "critical": [],
        "high": [],
        "medium": [],
        "low": [],
    }

    for match in matches:
        priority = match.get("priority", "medium")
        if priority in priority_groups:
            priority_groups[priority].append(match)

    # Build output
    lines = [
        "",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "  SKILL ACTIVATION CHECK",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
    ]

    # Critical skills
    if priority_groups["critical"]:
        lines.append("!! CRITICAL SKILLS (REQUIRED):")
        for m in priority_groups["critical"]:
            reasons = ", ".join(m["reasons"])
            lines.append(f"   -> /{m['skill']} ({reasons})")
        lines.append("")

    # High priority skills
    if priority_groups["high"]:
        lines.append(">> RECOMMENDED SKILLS:")
        for m in priority_groups["high"]:
            reasons = ", ".join(m["reasons"])
            lines.append(f"   -> /{m['skill']} ({reasons})")
        lines.append("")

    # Medium priority skills
    if priority_groups["medium"]:
        lines.append("-- SUGGESTED SKILLS:")
        for m in priority_groups["medium"]:
            reasons = ", ".join(m["reasons"])
            lines.append(f"   -> /{m['skill']} ({reasons})")
        lines.append("")

    # Low priority skills
    if priority_groups["low"]:
        lines.append(".. OPTIONAL SKILLS:")
        for m in priority_groups["low"]:
            reasons = ", ".join(m["reasons"])
            lines.append(f"   -> /{m['skill']} ({reasons})")
        lines.append("")

    lines.append("ACTION: Use slash command to activate skill")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    """Main entry point."""
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    prompt = data.get("prompt", "")
    if not prompt:
        sys.exit(0)

    # Get file context if available
    file_paths = data.get("active_files", [])
    if isinstance(file_paths, str):
        file_paths = [file_paths]

    rules = load_skill_rules()
    if not rules:
        sys.exit(0)

    matches = find_matching_skills(prompt, file_paths, rules)

    if matches:
        # Output all matching skills grouped by priority
        output = format_all_suggestions(matches)
        print(output)

    # Always exit 0 - suggestions are advisory only
    sys.exit(0)


if __name__ == "__main__":
    main()
