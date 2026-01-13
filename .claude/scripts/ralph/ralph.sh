#!/bin/bash
#
# ralph.sh - Self-Continuing Agent for dev_docs Tasks
# ====================================================
#
# Ralph automates work on dev_docs/active/ tasks through an iterative loop.
# Uses git worktree isolation - all changes happen on a feature branch.
#
# Usage:
#   .claude/scripts/ralph/ralph.sh [iterations]    # Default: 20 iterations
#   .claude/scripts/ralph/ralph.sh 5               # Run 5 iterations
#   .claude/scripts/ralph/ralph.sh --dry-run       # Show what would happen
#   .claude/scripts/ralph/ralph.sh --status        # Show current status
#   .claude/scripts/ralph/ralph.sh --cleanup       # Remove worktree and branch
#
# Safety:
#   - All changes on feature branch (main protected)
#   - Write/Edit restricted to worktree path via --allowedTools
#   - Safety hooks remain active (safety_validator.py)
#   - Maximum iterations prevent runaway execution
#

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
PROMPTS_DIR="$SCRIPT_DIR/prompts"

# Completion markers
TASK_ITEM_DONE="<ralph>TASK_ITEM_DONE</ralph>"
ALL_TASKS_DONE="<ralph>ALL_TASKS_DONE</ralph>"
ERROR_STOP="<ralph>ERROR_STOP</ralph>"

# Logging functions
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Find active task in dev_docs/active/
find_active_task() {
    ls -1 "$PROJECT_ROOT/dev_docs/active/" 2>/dev/null | grep -E '^[0-9]{4}_' | sort | head -1
}

# Worktrees directory (inside project, gitignored)
WORKTREES_DIR="$PROJECT_ROOT/worktrees"

# Get worktree path for a task
get_worktree_path() {
    local task_num="$1"
    echo "$WORKTREES_DIR/ralph-worktree-${task_num}"
}

# Ensure worktrees directory exists
ensure_worktrees_dir() {
    if [ ! -d "$WORKTREES_DIR" ]; then
        mkdir -p "$WORKTREES_DIR"
        log_info "Created worktrees directory at $WORKTREES_DIR"
    fi
}

# Check if worktree already exists
worktree_exists() {
    local worktree_path="$1"
    git -C "$PROJECT_ROOT" worktree list | grep -q "$worktree_path"
}

# Create worktree for task
create_worktree() {
    local task_dir="$1"
    local task_num=$(echo "$task_dir" | cut -d'_' -f1)
    local branch_name="ralph/${task_dir}"
    local worktree_path=$(get_worktree_path "$task_num")

    # Ensure worktrees directory exists
    ensure_worktrees_dir >&2

    # Check if worktree already exists
    if worktree_exists "$worktree_path"; then
        log_info "Worktree already exists at $worktree_path" >&2
        echo "$worktree_path"
        return 0
    fi

    # Check if branch exists
    if git -C "$PROJECT_ROOT" show-ref --verify --quiet "refs/heads/$branch_name"; then
        log_info "Branch $branch_name exists, creating worktree..." >&2
        git -C "$PROJECT_ROOT" worktree add "$worktree_path" "$branch_name" >&2
    else
        log_info "Creating new branch $branch_name with worktree..." >&2
        git -C "$PROJECT_ROOT" worktree add -b "$branch_name" "$worktree_path" >&2
    fi

    echo "$worktree_path"
}

# Copy environment and secret files to worktree (including .example for structure reference)
copy_env_files() {
    local worktree_path="$1"
    local copied=0

    # Copy ALL .env* files (including .example for structure reference)
    for env_file in "$PROJECT_ROOT"/.env*; do
        if [ -f "$env_file" ]; then
            local filename=$(basename "$env_file")
            cp "$env_file" "$worktree_path/$filename"
            log_info "Copied $filename to worktree"
            ((copied++))
        fi
    done

    # Copy ALL .secret* files (including .example for structure reference)
    for secret_file in "$PROJECT_ROOT"/.secret*; do
        if [ -f "$secret_file" ]; then
            local filename=$(basename "$secret_file")
            cp "$secret_file" "$worktree_path/$filename"
            log_info "Copied $filename to worktree"
            ((copied++))
        fi
    done

    if [ $copied -eq 0 ]; then
        log_info "No .env or .secret files found to copy"
    fi
}

# Build the agent prompt
build_prompt() {
    local worktree_path="$1"
    local task_dir="$2"
    local session_id="$3"

    # Read the prompt template
    local prompt_template=""
    if [ -f "$PROMPTS_DIR/AGENT_PROMPT.md" ]; then
        prompt_template=$(cat "$PROMPTS_DIR/AGENT_PROMPT.md")
    else
        log_error "Prompt template not found at $PROMPTS_DIR/AGENT_PROMPT.md"
        exit 1
    fi

    # Build file references
    local task_path="dev_docs/active/${task_dir}"
    local progress_file="${task_path}/ralph_progress.txt"

    # Create prompt with context files
    cat <<PROMPT
@CLAUDE.md
@${task_path}/

Session ID: ${session_id}
Task: ${task_dir}
Worktree Path: ${worktree_path}
Progress File: ${progress_file}

${prompt_template}
PROMPT
}

# Append progress to task's ralph_progress.txt
log_progress() {
    local worktree_path="$1"
    local task_dir="$2"
    local session_id="$3"
    local status="$4"
    local details="$5"

    local progress_file="${worktree_path}/dev_docs/active/${task_dir}/ralph_progress.txt"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local branch_name="ralph/${task_dir}"

    # Ensure directory exists
    mkdir -p "$(dirname "$progress_file")"

    # Append JSONL entry
    echo "{\"timestamp\": \"$timestamp\", \"session\": \"$session_id\", \"branch\": \"$branch_name\", \"status\": \"$status\", \"details\": \"$details\"}" >> "$progress_file"
}

# Show status
show_status() {
    log_info "Ralph Status"
    echo "============================================"

    # Find active task
    local task_dir=$(find_active_task)
    if [ -z "$task_dir" ]; then
        log_warn "No active tasks found in dev_docs/active/"
        return 0
    fi

    echo "Active task: $task_dir"

    local task_num=$(echo "$task_dir" | cut -d'_' -f1)
    local worktree_path=$(get_worktree_path "$task_num")
    local branch_name="ralph/${task_dir}"

    # Check worktree
    if worktree_exists "$worktree_path"; then
        echo "Worktree: $worktree_path (exists)"
    else
        echo "Worktree: $worktree_path (not created)"
    fi

    # Check branch
    if git -C "$PROJECT_ROOT" show-ref --verify --quiet "refs/heads/$branch_name"; then
        echo "Branch: $branch_name (exists)"
        local commits=$(git -C "$PROJECT_ROOT" rev-list --count main..$branch_name 2>/dev/null || echo "0")
        echo "Commits ahead of main: $commits"
    else
        echo "Branch: $branch_name (not created)"
    fi

    # Check progress file
    local progress_file="$PROJECT_ROOT/dev_docs/active/${task_dir}/ralph_progress.txt"
    if [ -f "$progress_file" ]; then
        echo ""
        echo "Recent progress (last 5 entries):"
        tail -5 "$progress_file" 2>/dev/null || echo "  (empty)"
    fi

    echo "============================================"
}

# Cleanup worktree and optionally branch
cleanup() {
    local task_dir=$(find_active_task)
    if [ -z "$task_dir" ]; then
        log_warn "No active task to clean up"
        return 0
    fi

    local task_num=$(echo "$task_dir" | cut -d'_' -f1)
    local worktree_path=$(get_worktree_path "$task_num")
    local branch_name="ralph/${task_dir}"

    log_info "Cleaning up Ralph artifacts for $task_dir"

    # Remove worktree
    if worktree_exists "$worktree_path"; then
        log_info "Removing worktree at $worktree_path"
        git -C "$PROJECT_ROOT" worktree remove --force "$worktree_path" 2>/dev/null || rm -rf "$worktree_path"
    fi

    # Ask about branch
    if git -C "$PROJECT_ROOT" show-ref --verify --quiet "refs/heads/$branch_name"; then
        read -p "Delete branch $branch_name? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git -C "$PROJECT_ROOT" branch -D "$branch_name"
            log_success "Branch deleted"
        else
            log_info "Branch kept"
        fi
    fi

    log_success "Cleanup complete"
}

# Dry run - show what would happen
dry_run() {
    log_info "DRY RUN MODE"
    echo "============================================"

    local task_dir=$(find_active_task)
    if [ -z "$task_dir" ]; then
        log_warn "No active tasks found in dev_docs/active/"
        log_info "Create a task with /dev-docs first"
        return 0
    fi

    local task_num=$(echo "$task_dir" | cut -d'_' -f1)
    local branch_name="ralph/${task_dir}"
    local worktree_path=$(get_worktree_path "$task_num")
    local worktree_abs=$(cd "$PROJECT_ROOT" && cd "$(dirname "$worktree_path")" && pwd)/$(basename "$worktree_path")

    echo "Would work on: $task_dir"
    echo "Branch name: $branch_name"
    echo "Worktree path: $worktree_path"
    echo ""
    echo "Allowed tools would be:"
    echo "  Write(${worktree_abs}/**)"
    echo "  Edit(${worktree_abs}/**)"
    echo "  Read(*)"
    echo "  Glob(*)"
    echo "  Grep(*)"
    echo "  Bash(pytest:*)"
    echo "  Bash(ruff:*)"
    echo "  Bash(git status:*)"
    echo "  Bash(git add:*)"
    echo "  Bash(git commit:*)"
    echo ""
    echo "Task files:"
    ls -la "$PROJECT_ROOT/dev_docs/active/${task_dir}/" 2>/dev/null || echo "  (directory empty)"
    echo ""
    echo "Prompt preview (first 50 lines):"
    echo "----------------------------------------"
    build_prompt "$worktree_path" "$task_dir" "dry-run" | head -50
    echo "..."
    echo "============================================"
}

# Main loop
main() {
    local max_iterations="${1:-20}"

    # Generate session ID
    local session_id="$(date +%Y%m%d-%H%M%S)-$$"

    echo "============================================"
    echo "     Ralph Self-Continuing Agent"
    echo "============================================"
    log_info "Session: $session_id"
    log_info "Max iterations: $max_iterations"
    echo ""

    # Find active task
    local task_dir=$(find_active_task)
    if [ -z "$task_dir" ]; then
        log_error "No active tasks found in dev_docs/active/"
        log_info "Create a task with /dev-docs first"
        exit 1
    fi

    log_info "Working on task: $task_dir"

    # Create worktree
    local worktree_path=$(create_worktree "$task_dir")
    local worktree_abs=$(cd "$(dirname "$worktree_path")" && pwd)/$(basename "$worktree_path")

    log_success "Worktree ready at: $worktree_path"

    # Copy environment files to worktree
    copy_env_files "$worktree_path"

    # Log session start
    log_progress "$worktree_path" "$task_dir" "$session_id" "session_start" "Starting Ralph session with max $max_iterations iterations"

    # Build allowed tools with absolute path
    local allowed_tools="Write(${worktree_abs}/**),Edit(${worktree_abs}/**),Read(*),Glob(*),Grep(*),Bash(pytest:*),Bash(python -m pytest:*),Bash(ruff check:*),Bash(ruff format:*),Bash(git status:*),Bash(git diff:*),Bash(git add:*),Bash(git commit:*),Bash(ls:*),Bash(cat:*),Bash(head:*),Bash(tail:*)"

    # Main iteration loop
    for ((i=1; i<=$max_iterations; i++)); do
        echo ""
        log_info "========== Iteration $i of $max_iterations =========="

        log_progress "$worktree_path" "$task_dir" "$session_id" "iteration_start" "Starting iteration $i"

        # Build prompt
        local prompt=$(build_prompt "$worktree_path" "$task_dir" "$session_id")

        # Run Claude from within the worktree
        log_info "Running Claude in worktree..."

        local result=""
        local exit_code=0

        # Change to worktree and run Claude
        pushd "$worktree_path" > /dev/null
        result=$(claude --dangerously-skip-permissions \
            --allowedTools "$allowed_tools" \
            -p "$prompt" 2>&1) || exit_code=$?
        popd > /dev/null

        # Check for Claude errors
        if [ $exit_code -ne 0 ]; then
            log_error "Claude exited with code $exit_code"
            log_progress "$worktree_path" "$task_dir" "$session_id" "claude_error" "Claude exited with code $exit_code"
            echo "$result"
            exit 1
        fi

        # Check for completion markers in output
        if [[ "$result" == *"$ALL_TASKS_DONE"* ]]; then
            echo ""
            log_success "============================================"
            log_success "ALL TASKS COMPLETE!"
            log_success "============================================"
            log_progress "$worktree_path" "$task_dir" "$session_id" "all_complete" "All tasks completed"

            local branch_name="ralph/${task_dir}"
            echo ""
            echo "Branch $branch_name is ready for review."
            echo ""
            echo "To merge:"
            echo "  cd $PROJECT_ROOT"
            echo "  git merge $branch_name"
            echo ""
            echo "To create PR:"
            echo "  gh pr create --base main --head $branch_name"
            echo ""
            echo "To discard:"
            echo "  git branch -D $branch_name"
            echo "  git worktree remove $worktree_path"
            exit 0
        fi

        if [[ "$result" == *"$ERROR_STOP"* ]]; then
            echo ""
            log_error "============================================"
            log_error "ERROR - Agent requested stop"
            log_error "============================================"
            log_progress "$worktree_path" "$task_dir" "$session_id" "error_stop" "Agent encountered error and stopped"
            echo ""
            echo "Check the progress file for details:"
            echo "  cat $worktree_path/dev_docs/active/${task_dir}/ralph_progress.txt"
            exit 1
        fi

        if [[ "$result" == *"$TASK_ITEM_DONE"* ]]; then
            log_success "Task item completed. Continuing to next..."
            log_progress "$worktree_path" "$task_dir" "$session_id" "item_complete" "Task item completed in iteration $i"
        else
            log_warn "No completion marker found in output"
            log_progress "$worktree_path" "$task_dir" "$session_id" "no_marker" "Iteration $i completed without marker"
        fi

        # Small delay between iterations
        sleep 2
    done

    echo ""
    log_warn "============================================"
    log_warn "Max iterations ($max_iterations) reached"
    log_warn "============================================"
    log_progress "$worktree_path" "$task_dir" "$session_id" "max_iterations" "Reached maximum iterations limit"

    local branch_name="ralph/${task_dir}"
    echo ""
    echo "Work in progress on branch: $branch_name"
    echo "Run again to continue: .claude/scripts/ralph/ralph.sh"
}

# Parse arguments
case "${1:-}" in
    --dry-run)
        dry_run
        ;;
    --status)
        show_status
        ;;
    --cleanup)
        cleanup
        ;;
    --help|-h)
        echo "Ralph - Self-Continuing Agent for dev_docs Tasks"
        echo ""
        echo "Usage:"
        echo "  .claude/scripts/ralph/ralph.sh [iterations]    Run for N iterations (default: 20)"
        echo "  .claude/scripts/ralph/ralph.sh --dry-run       Show what would happen"
        echo "  .claude/scripts/ralph/ralph.sh --status        Show current status"
        echo "  .claude/scripts/ralph/ralph.sh --cleanup       Remove worktree and branch"
        echo "  .claude/scripts/ralph/ralph.sh --help          Show this help"
        ;;
    *)
        main "${1:-20}"
        ;;
esac
