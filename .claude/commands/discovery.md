---
description: Start or resume the Discovery-to-PRD pipeline
argument-hint: [--description "<text>"] [--resume <phase>] [--project <name>]
---

Run the Discovery Pipeline to transform ideas into Product Requirements Documents.

## What This Does

Executes a 5-phase discovery pipeline:

1. **Interview** (Interactive): Socratic questioning to understand requirements
2. **Research** (Autonomous): Web search to validate and expand findings
3. **Synthesis** (Autonomous): Combine into structured PRD draft
4. **Review** (Autonomous): Adversarial critical review with lens scoring
5. **Consolidation** (Autonomous): Synthesize review into final PRD

Each phase runs in isolation with fresh context.

## Usage

**Start new discovery:**
```bash
/discovery
```
You will be prompted for a description of what you want to build. The project name is auto-derived from your description.

**Start with inline description:**
```bash
/discovery -d "A mobile app for tracking personal expenses"
```
Skips the interactive prompt and derives project name from description.

**Resume from specific phase:**
```bash
/discovery --resume research
/discovery --resume synthesis
/discovery --resume review
/discovery --resume consolidation
```

**Start with project name:**
```bash
/discovery --project mobile-checkout
```

**List phases:**
```bash
/discovery --list
```

## Output Location

All artifacts saved to: `docs/discovery/<project-name>/`
- `01-interview.md` - Interview notes
- `02-research.md` - Research findings
- `03-prd-draft.md` - PRD draft
- `04-prd-review.md` - Critical review with lens scores
- `05-prd-final.md` - Final PRD (consolidated)

## Execution

**IMPORTANT:** Check `$ARGUMENTS` BEFORE running any commands.

### If `--list` is present:
Display the phase list from "What This Does" section above. Do NOT run any scripts.

### If `--resume <phase>` is present:
Run the Python orchestrator to continue from that phase:
```bash
python .claude/scripts/discovery_agent/discovery_agent.py $ARGUMENTS
```

### Otherwise (new discovery - NO --resume flag):
**Do NOT run the Python script.** Handle Phase 1 directly:

1. **Get project description:**
   - If `--description` or `-d` provided in $ARGUMENTS, use that value
   - Otherwise, ask user: "What do you want to build?"

2. **Derive project name:**
   - Create a kebab-case name from the description (2-4 words, lowercase)
   - If `--project` provided, use that instead

3. **Create output directory:**
   ```bash
   mkdir -p docs/discovery/<project-name>
   ```

4. **Run Phase 1 Interview:**
   Read and follow the Socratic interview prompt from:
   `.claude/scripts/discovery_agent/prompts/PHASE_1_INTERVIEW.md`

5. **Save interview output:**
   Write the completed discovery document to: `docs/discovery/<project-name>/01-interview.md`

6. **AUTO-CONTINUE to Phase 2:**
   After Phase 1 is complete, run phases 2-5 autonomously:
   ```bash
   python .claude/scripts/discovery_agent/discovery_agent.py --resume research --project <project-name>
   ```
