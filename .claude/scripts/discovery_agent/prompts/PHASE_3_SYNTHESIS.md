# Phase 3: PRD Synthesis

## Context

You are synthesizing a Product Requirements Document from:
- **Interview notes**: `01-interview.md` (provided in "Input Documents" above) — User's stated needs, goals, constraints
- **Research findings**: `02-research.md` (provided in "Input Documents" above) — Technical feasibility, architecture options, implementation approaches

**Output**: Save to the "Output File" path specified at the top of this prompt.

## Pre-flight Check

Before synthesizing, verify source materials exist and contain:

**Interview (minimum required):**
- [ ] Clear problem statement
- [ ] At least one user persona or use case
- [ ] Success criteria or goals
- [ ] Constraints (time, budget, technical)

**Research (minimum required):**
- [ ] Architecture recommendation with rationale
- [ ] Technology stack decisions
- [ ] Risk assessment
- [ ] Implementation complexity estimate

If critical information is missing, note it in "Open Questions" and flag uncertainty level on affected requirements.

## Synthesis Logic

### 1. Establish Ground Truth

Interview findings = "what users say they need"
Research findings = "what's technically feasible and advisable"

When they align → high confidence requirement
When they conflict → document the tension, recommend resolution, mark as needing validation

### 2. Derive Requirements (not just copy)

Bad: "User said they want fast performance" → FR: "Fast performance"
Good: "User said reports take too long (>30s)" + Research shows "pagination + caching achieves <2s" → FR: "Report generation <2s via paginated queries with Redis cache"

Every requirement should show your work:
- What was asked for (interview)
- What's achievable (research)  
- What you're recommending (synthesis)

### 3. Prioritize Ruthlessly

**MUST**: Without this, the product fails its core purpose
**SHOULD**: Users will complain loudly, but can work around
**COULD**: Nice-to-have, implement if time permits
**WON'T (this version)**: Explicitly deferred — prevents scope creep

Default to fewer MUSTs. If everything is critical, nothing is.

### 4. Be Honest About Unknowns

Use these markers:
- `[ASSUMPTION]` — We're guessing; needs validation
- `[RISK]` — Could go wrong; needs mitigation plan
- `[OPEN]` — Blocks progress; needs answer before implementation
- `[CONFLICT]` — Interview vs research disagree; needs resolution

## Output Structure

Use the project name from the "Project" field at the top of this prompt.

```markdown
# [Project Name] — Product Requirements Document

**Version**: 0.1 (Draft from synthesis)
**Date**: [today's date]
**Status**: Pending Review Phase
**Confidence**: High/Medium/Low (based on input completeness)

---

## Executive Summary
[3-5 sentences: What are we building, why, what does success look like]

## Problem & Opportunity
[Current state pain points with evidence from interview]
[Business/user impact — quantified where possible]

## Users
[Primary persona with goals, pain points, context]
[Anti-personas — who this is NOT for]

## Success Metrics
| Outcome | Metric | Target | How Measured |
|---------|--------|--------|--------------|
| ... | ... | ... | ... |

## Requirements

### Functional — MUST HAVE
| ID | Requirement | Acceptance Criteria | Source | Confidence |
|----|-------------|---------------------|--------|------------|
| FR-001 | ... | ... | Interview: "...", Research: "..." | High/Med/Low |

### Functional — SHOULD/COULD HAVE
[Same format, briefer]

### Non-Functional
| Category | Requirement | Target | Rationale |
|----------|-------------|--------|-----------|
| Performance | ... | ... | ... |
| Security | ... | ... | ... |
| Scalability | ... | ... | ... |

### Constraints
[Technical, business, timeline constraints from interview + research]

## Technical Direction
[High-level architecture from research]
[Key technology choices with rationale]
[Integration points]

## Out of Scope
| Item | Why Excluded | Revisit When |
|------|--------------|--------------|
| ... | ... | ... |

## Risks & Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| ... | ... | ... | ... |

## Open Questions
| Question | Blocks | Suggested Owner |
|----------|--------|-----------------|
| ... | ... | ... |

## Appendix: Source Traceability
[Key interview quotes that drove decisions]
[Key research findings that shaped architecture]
```

## Quality Gates

Before marking complete, verify:
- [ ] No requirement without acceptance criteria
- [ ] No requirement without source reference
- [ ] MUST requirements ≤ 40% of total (avoid everything-is-critical)
- [ ] Every `[OPEN]` question has clear impact stated
- [ ] Metrics are measurable, not aspirational fluff
- [ ] Out of scope section exists (prevents scope creep later)