#!/usr/bin/env python3
"""
Discovery Pipeline Orchestrator
================================

Manages a 4-phase discovery-to-PRD pipeline:
1. Interview (interactive) - Socratic questioning with user
2. Research (autonomous) - Web research and validation
3. Synthesis (autonomous) - PRD generation
4. Review (autonomous) - Critical review

Each phase runs as a separate subprocess for context isolation.

Usage:
    python discovery_agent.py                    # Start new discovery
    python discovery_agent.py --resume research  # Resume from phase
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple


class Phase(NamedTuple):
    """Phase configuration."""

    name: str
    number: int
    output: str
    prompt_file: str
    inputs: tuple[str, ...]
    interactive: bool


# Phase definitions
PHASES: tuple[Phase, ...] = (
    Phase(
        name="interview",
        number=1,
        output="01-interview.md",
        prompt_file="PHASE_1_INTERVIEW.md",
        inputs=(),
        interactive=True,
    ),
    Phase(
        name="research",
        number=2,
        output="02-research.md",
        prompt_file="PHASE_2_RESEARCH.md",
        inputs=("01-interview.md",),
        interactive=False,
    ),
    Phase(
        name="synthesis",
        number=3,
        output="03-prd-draft.md",
        prompt_file="PHASE_3_SYNTHESIS.md",
        inputs=("01-interview.md", "02-research.md"),
        interactive=False,
    ),
    Phase(
        name="review",
        number=4,
        output="04-prd-review.md",
        prompt_file="PHASE_4_REVIEW.md",
        inputs=("03-prd-draft.md", "01-interview.md", "02-research.md"),
        interactive=False,
    ),
    Phase(
        name="consolidation",
        number=5,
        output="05-prd-final.md",
        prompt_file="PHASE_5_CONSOLIDATION.md",
        inputs=("03-prd-draft.md", "04-prd-review.md"),
        interactive=False,
    ),
)

PHASE_BY_NAME: dict[str, Phase] = {p.name: p for p in PHASES}


def sanitize_project_name(name: str) -> str:
    """Sanitize project name to prevent path traversal and ensure valid filename.

    Args:
        name: Raw project name input.

    Returns:
        Sanitized project name safe for use in file paths.
    """
    # Remove path separators and parent directory refs
    name = name.replace("/", "-").replace("\\", "-").replace("..", "")
    # Only keep alphanumeric and hyphens
    name = "".join(c if c.isalnum() or c == "-" else "-" for c in name)
    # Remove multiple consecutive hyphens
    while "--" in name:
        name = name.replace("--", "-")
    # Trim leading/trailing hyphens and limit length
    name = name.strip("-")[:50]
    # Ensure we have a valid name
    if not name or not any(c.isalnum() for c in name):
        return "discovery-project"
    return name


# Tools to allow without prompting during discovery phases
ALLOWED_TOOLS: tuple[str, ...] = (
    "Read(*)",
    "Write(*)",
    "Edit(*)",
    "WebSearch",
    "WebFetch",
    "Glob(*)",
    "Grep(*)",
)


def get_project_root() -> Path:
    """Find project root (where .claude/ exists)."""
    current = Path.cwd()
    while current != current.parent:
        if (current / ".claude").exists():
            return current
        current = current.parent
    return Path.cwd()


def get_prompts_dir() -> Path:
    """Get path to discovery prompts (relative to this script)."""
    return Path(__file__).parent / "prompts"


def get_output_dir(project_name: str) -> Path:
    """Get path to project output directory."""
    return get_project_root() / "docs" / "discovery" / project_name


def load_prompt(phase: Phase) -> str:
    """Load prompt content from file."""
    prompt_path = get_prompts_dir() / phase.prompt_file
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    return prompt_path.read_text()


def check_inputs_exist(project_name: str, phase: Phase) -> list[Path]:
    """Check required input files exist. Return paths."""
    output_dir = get_output_dir(project_name)
    missing: list[str] = []
    paths: list[Path] = []

    for input_file in phase.inputs:
        input_path = output_dir / input_file
        if not input_path.exists():
            missing.append(input_file)
        else:
            paths.append(input_path)

    if missing:
        raise FileNotFoundError(
            f"Missing inputs for phase '{phase.name}': {missing}\n"
            f"Run earlier phases first or check: {output_dir}"
        )
    return paths


def output_exists(project_name: str, phase: Phase) -> bool:
    """Check if phase output already exists."""
    return (get_output_dir(project_name) / phase.output).exists()


def get_completed_phases(project_name: str) -> list[str]:
    """Get list of completed phase names."""
    return [p.name for p in PHASES if output_exists(project_name, p)]


def ask_discovery_input() -> tuple[str, str]:
    """Ask for user description and derive project name."""
    print("\n" + "=" * 60)
    print("DISCOVERY PIPELINE - New Project")
    print("=" * 60)
    print("\nDescribe what you want to explore or build:")
    print("(e.g., 'A mobile app for tracking personal expenses')\n")

    while True:
        description = input("Description: ").strip()
        if not description:
            print("Please enter a description.")
            continue
        break

    # Derive project name using Claude (with fallback)
    print("\nDeriving project name...")
    project_name = derive_project_name(description)
    print(f"Derived project name: {project_name}")
    return project_name, description


def build_prompt(
    phase: Phase,
    project_name: str,
    input_paths: list[Path],
    description: str | None = None,
) -> str:
    """Build full prompt for a phase."""
    output_dir = get_output_dir(project_name)
    output_file = output_dir / phase.output

    parts: list[str] = [
        f"# Discovery Pipeline - Phase {phase.number}: {phase.name.title()}",
        f"\n## Project: {project_name}",
        f"\n## Output File: {output_file}",
        "",
        "IMPORTANT: When you complete this phase, save your output to the file above.",
        "",
    ]

    # Add user description for Phase 1 (interview)
    if description and phase.name == "interview":
        parts.append("## User Description\n")
        parts.append(f"The user wants to explore/build: {description}")
        parts.append("")

    parts.append("---")
    parts.append("")

    # Add input file contents
    if input_paths:
        parts.append("## Input Documents\n")
        for path in input_paths:
            parts.append(f"### {path.name}\n")
            parts.append("```markdown")
            parts.append(path.read_text())
            parts.append("```\n")
        parts.append("---\n")

    # Add phase instructions
    parts.append("## Phase Instructions\n")
    parts.append(load_prompt(phase))

    return "\n".join(parts)


def run_interactive_phase(
    phase: Phase, project_name: str, description: str | None = None
) -> int:
    """Run interview phase interactively."""
    output_dir = get_output_dir(project_name)
    output_dir.mkdir(parents=True, exist_ok=True)

    prompt = build_prompt(phase, project_name, [], description=description)

    print(f"\n{'=' * 60}")
    print(f"Phase {phase.number}: {phase.name.upper()} (Interactive)")
    print(f"Output: {output_dir / phase.output}")
    print("=" * 60)
    print("\nStarting interactive interview session...")
    print("Answer the questions. Type your responses when prompted.")
    print("The session will end when all requirements are gathered.\n")

    # Run claude interactively with initial prompt
    # Note: Do NOT use --print/-p flag - that's for non-interactive output mode
    result = subprocess.run(
        [
            "claude",
            "--allowedTools",
            ",".join(ALLOWED_TOOLS),
            prompt,
        ],
        cwd=get_project_root(),
    )

    return result.returncode


def run_autonomous_phase(phase: Phase, project_name: str) -> int:
    """Run autonomous phase as subprocess."""
    input_paths = check_inputs_exist(project_name, phase)
    output_dir = get_output_dir(project_name)
    output_dir.mkdir(parents=True, exist_ok=True)

    prompt = build_prompt(phase, project_name, input_paths)

    print(f"\n{'=' * 60}")
    print(f"Phase {phase.number}: {phase.name.upper()} (Autonomous)")
    print(f"Output: {output_dir / phase.output}")
    print("=" * 60)
    print("\nRunning autonomous phase... This may take a few minutes.\n")

    # Run claude with -p flag for autonomous execution
    # Pass prompt via stdin (required when -p is used with other flags)
    # Use --permission-mode acceptEdits to auto-approve file writes
    result = subprocess.run(
        [
            "claude",
            "-p",
            "--permission-mode",
            "bypassPermissions",
            "--allowedTools",
            " ".join(ALLOWED_TOOLS),
        ],
        input=prompt,
        text=True,
        cwd=get_project_root(),
    )

    return result.returncode


def run_phase(phase: Phase, project_name: str, description: str | None = None) -> int:
    """Run a single phase."""
    if phase.interactive:
        return run_interactive_phase(phase, project_name, description=description)
    return run_autonomous_phase(phase, project_name)


def _derive_project_name_fallback(description: str) -> str:
    """Fallback: simple derivation if Claude unavailable."""
    words = description.lower().split()
    skip_words = {
        "a",
        "an",
        "the",
        "for",
        "to",
        "of",
        "and",
        "or",
        "with",
        "in",
        "on",
        "at",
        "my",
        "i",
        "we",
        "our",
        "your",
        "their",
        "this",
        "that",
        "it",
        "is",
        "are",
        "want",
        "need",
        "would",
        "like",
        "idea",
        "plan",
        "project",
        "think",
        "create",
        "build",
        "make",
        "develop",
        "design",
        "implement",
        "add",
        "get",
    }
    key_words = [w for w in words if w.isalnum() and w not in skip_words][:4]
    project_name = "-".join(key_words)
    return sanitize_project_name(project_name)


def derive_project_name(description: str) -> str:
    """Use Claude to derive a meaningful project name from description."""
    prompt = f"""Given this project description, output ONLY a short kebab-case project name (2-4 words, lowercase, hyphens).
No explanation, just the name.

Description: {description}

Examples:
- "A mobile app for tracking expenses" -> "expense-tracker-app"
- "Website for selling handmade jewelry" -> "jewelry-store"
- "CLI tool for managing docker containers" -> "docker-manager-cli"

Output only the project name:"""

    try:
        result = subprocess.run(
            ["claude", "-p", prompt],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=get_project_root(),
        )
        if result.returncode == 0 and result.stdout.strip():
            name = result.stdout.strip().lower()
            name = sanitize_project_name(name)
            if name and name != "discovery-project":
                return name
    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        pass

    # Fallback to simple derivation if Claude fails
    return _derive_project_name_fallback(description)


def run_pipeline(
    project_name: str | None = None,
    resume_from: str | None = None,
    description: str | None = None,
) -> int:
    """Run phases 2-5 of discovery pipeline (Phase 1 handled by /discovery command)."""
    # Require --resume for this script (Phase 1 handled by /discovery command)
    if not resume_from:
        print("Error: --resume is required.")
        print("Phase 1 (interview) runs via /discovery command directly.")
        print("After Phase 1, use: --resume research --project <name>")
        return 1

    # Require --project with --resume
    if project_name is None:
        print("Error: --project is required with --resume")
        print(
            "Example: python discovery_agent.py --resume research --project myproject"
        )
        return 1

    # Validate phase name
    if resume_from not in PHASE_BY_NAME:
        print(f"Unknown phase: {resume_from}")
        print(f"Valid phases: {', '.join(PHASE_BY_NAME.keys())}")
        return 1

    output_dir = get_output_dir(project_name)
    start_phase = resume_from

    # Find starting index
    start_idx = next(i for i, p in enumerate(PHASES) if p.name == start_phase)

    # Run phases
    for phase in PHASES[start_idx:]:
        print(f"\n{'#' * 60}")
        print(f"# PHASE {phase.number}: {phase.name.upper()}")
        print("#" * 60)

        # Skip if already completed
        if output_exists(project_name, phase):
            print(f"Phase '{phase.name}' already completed. Skipping.")
            continue

        # Run phase (pass description only for interview phase)
        exit_code = run_phase(phase, project_name, description=description)

        if exit_code != 0:
            print(f"\nPhase '{phase.name}' failed with exit code {exit_code}")
            print("Pipeline halted. Resume with:")
            print(
                f"  python discovery_agent.py --project {project_name} --resume {phase.name}"
            )
            return exit_code

        # Verify output created
        if not output_exists(project_name, phase):
            print(f"\nWarning: Phase '{phase.name}' completed but output not found.")
            print(f"Expected: {output_dir / phase.output}")
            print("You may need to manually save the output and resume.")

    # Done
    print(f"\n{'=' * 60}")
    print("DISCOVERY PIPELINE COMPLETE")
    print("=" * 60)
    print(f"\nAll artifacts saved to: {output_dir}\n")

    print("Files created:")
    for phase in PHASES:
        path = output_dir / phase.output
        status = "OK" if path.exists() else "MISSING"
        print(f"  [{status}] {phase.output}")

    return 0


def list_phases() -> None:
    """Print phase information."""
    print("\nDiscovery Pipeline Phases:")
    print("-" * 50)
    for phase in PHASES:
        mode = "INTERACTIVE" if phase.interactive else "AUTONOMOUS"
        print(f"  {phase.number}. {phase.name.title()} ({mode})")
        print(f"     Output: {phase.output}")
        if phase.inputs:
            print(f"     Inputs: {', '.join(phase.inputs)}")
        print()


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Discovery-to-PRD Pipeline Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python discovery_agent.py                      # Start new discovery (interactive)
  python discovery_agent.py -d "Mobile expense tracker app"  # Start with description
  python discovery_agent.py --project myproj     # Start with project name
  python discovery_agent.py --resume research    # Resume from research
  python discovery_agent.py --list               # List all phases
        """,
    )

    parser.add_argument(
        "--project",
        "-p",
        help="Project name (prompted if not provided)",
    )
    parser.add_argument(
        "--description",
        "-d",
        help="Initial task description (prompted if not provided)",
    )
    parser.add_argument(
        "--resume",
        "-r",
        choices=[p.name for p in PHASES],
        help="Resume from specified phase",
    )
    parser.add_argument(
        "--list",
        "-l",
        action="store_true",
        help="List all phases",
    )

    args = parser.parse_args()

    if args.list:
        list_phases()
        return 0

    return run_pipeline(
        project_name=args.project,
        resume_from=args.resume,
        description=args.description,
    )


if __name__ == "__main__":
    sys.exit(main())
