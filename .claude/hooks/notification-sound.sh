#!/bin/bash
# Cross-platform notification sound
# Plays a notification sound on macOS, Linux, and Windows

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOUND_FILE="$SCRIPT_DIR/PeonBuildingComplete1.wav"

play_sound() {
    case "$OSTYPE" in
        darwin*)
            afplay "$SOUND_FILE" 2>/dev/null
            ;;
        linux*)
            if command -v paplay &>/dev/null; then
                paplay "$SOUND_FILE" 2>/dev/null
            elif command -v aplay &>/dev/null; then
                aplay "$SOUND_FILE" 2>/dev/null
            fi
            ;;
        msys*|cygwin*|mingw*)
            powershell.exe -c "(New-Object Media.SoundPlayer '$SOUND_FILE').PlaySync()" 2>/dev/null
            ;;
        *)
            printf '\a'
            ;;
    esac
}

play_sound
exit 0
