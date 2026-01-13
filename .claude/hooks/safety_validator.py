#!/usr/bin/env python3
"""
Safety Validator Hook for Claude Code
======================================

Purpose:
    Pre-tool-use validation layer that blocks potentially destructive operations
    before they execute. Acts as a safety gate for Bash, Read, Write, and Edit tools.

Protected Against:
    - Recursive deletion of root filesystem (rm -rf /)
    - Recursive deletion of all files (rm -rf *)
    - Recursive deletion of home directory (rm -rf ~)
    - Disk wiping operations (dd if=/dev/zero)
    - Access to environment files (.env, .env.local, .env.production, etc.)
    - Access to secret files (.secret, .secret.local, etc.)
    - Access to SSH private keys (id_rsa, id_ed25519, id_ecdsa)
    - Access to credential files (.pem, credentials)
    - Bash access to sensitive files (cat/head/tail/cp on .env, .secret, keys)

Exceptions:
    - Files ending with .example are allowed (safe template files)
    - e.g., .env.example, .secret.example can be read for structure reference

Exit Codes:
    0 - Tool use permitted (validation passed)
    2 - Tool use blocked (dangerous operation detected)

Integration:
    Configured as PreToolUse hook in .claude/settings.json
    Receives tool call JSON via stdin from Claude Code
"""

import json
import sys
import re

data = json.load(sys.stdin)
tool_name = data.get("tool_name", "")
tool_input = data.get("tool_input", {})

# Block dangerous bash commands
if tool_name == "Bash":
    command = tool_input.get("command", "")

    dangerous_patterns = [
        # rm -rf variations: handles -rf, -r -f, --recursive --force, etc.
        r"rm\s+(-[a-zA-Z]*r[a-zA-Z]*\s+-[a-zA-Z]*f[a-zA-Z]*|-[a-zA-Z]*f[a-zA-Z]*\s+-[a-zA-Z]*r[a-zA-Z]*|-[a-zA-Z]*rf[a-zA-Z]*|-[a-zA-Z]*fr[a-zA-Z]*|--recursive\s+--force|--force\s+--recursive)\s+/\s*$",
        # rm -rf /* or rm -rf *
        r"rm\s+(-[a-zA-Z]*r[a-zA-Z]*\s+-[a-zA-Z]*f[a-zA-Z]*|-[a-zA-Z]*f[a-zA-Z]*\s+-[a-zA-Z]*r[a-zA-Z]*|-[a-zA-Z]*rf[a-zA-Z]*|-[a-zA-Z]*fr[a-zA-Z]*|--recursive\s+--force|--force\s+--recursive)\s+(/\*)?\*",
        # rm -rf ~ (home directory)
        r"rm\s+(-[a-zA-Z]*r[a-zA-Z]*\s+-[a-zA-Z]*f[a-zA-Z]*|-[a-zA-Z]*f[a-zA-Z]*\s+-[a-zA-Z]*r[a-zA-Z]*|-[a-zA-Z]*rf[a-zA-Z]*|-[a-zA-Z]*fr[a-zA-Z]*|--recursive\s+--force|--force\s+--recursive)\s+~",
        # rm -rf $HOME
        r"rm\s+(-[a-zA-Z]*r[a-zA-Z]*\s+-[a-zA-Z]*f[a-zA-Z]*|-[a-zA-Z]*f[a-zA-Z]*\s+-[a-zA-Z]*r[a-zA-Z]*|-[a-zA-Z]*rf[a-zA-Z]*|-[a-zA-Z]*fr[a-zA-Z]*|--recursive\s+--force|--force\s+--recursive)\s+\$HOME",
        # dd disk operations
        r"dd\s+.*if=/dev/(zero|random|urandom).*of=/dev/",
        r"dd\s+.*of=/dev/[a-z]+\s",
    ]

    for pattern in dangerous_patterns:
        if re.search(pattern, command, re.IGNORECASE):
            print("BLOCKED: Dangerous command pattern detected", file=sys.stderr)
            sys.exit(2)

    # Additional simple checks for common dangerous patterns
    dangerous_simple = [
        ("rm -rf /", "recursive delete root"),
        ("rm -rf /*", "recursive delete root contents"),
        ("rm -rf ~", "recursive delete home"),
        ("rm -rf $HOME", "recursive delete home"),
        ("> /dev/sda", "overwrite disk"),
        ("mkfs.", "format filesystem"),
        (":(){ :|:& };:", "fork bomb"),
    ]

    for pattern, description in dangerous_simple:
        if pattern in command:
            print(f"BLOCKED: {description}", file=sys.stderr)
            sys.exit(2)

    # Block Bash access to sensitive files (but allow .example files)
    # First check if it's an .example file - those are safe
    if not re.search(r"\.example\b", command, re.IGNORECASE):
        sensitive_file_patterns = [
            r"\bcat\s+.*\.env\b",
            r"\bhead\s+.*\.env\b",
            r"\btail\s+.*\.env\b",
            r"\bcp\s+.*\.env\b",
            r"\bcat\s+.*\.secret",
            r"\bhead\s+.*\.secret",
            r"\btail\s+.*\.secret",
            r"\bcp\s+.*\.secret",
            r"\bcat\s+.*id_rsa",
            r"\bcat\s+.*id_ed25519",
            r"\bcat\s+.*\.pem",
            r"\bcat\s+.*credentials",
        ]

        for pattern in sensitive_file_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                print("BLOCKED: Cannot access sensitive file via Bash", file=sys.stderr)
                sys.exit(2)

# Block access to sensitive files
if tool_name in ["Read", "Write", "Edit"]:
    file_path = tool_input.get("file_path", "")

    # Allow .example files (they're safe templates without secrets)
    if file_path.endswith(".example"):
        sys.exit(0)

    sensitive_patterns = [
        ".env",
        ".secret",
        "id_rsa",
        "id_ed25519",
        "id_ecdsa",
        ".pem",
        "credentials",
    ]

    for blocked in sensitive_patterns:
        if blocked in file_path:
            print(
                f"BLOCKED: Cannot modify sensitive file: {file_path}", file=sys.stderr
            )
            sys.exit(2)

sys.exit(0)
