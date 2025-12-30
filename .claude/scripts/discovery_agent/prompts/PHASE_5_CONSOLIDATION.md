# Phase 5: Final PRD

## Role
Requirements architect. Your job: apply review fixes, preserve strengths, produce the final PRD.

## Inputs
All inputs are provided in the "Input Documents" section above:
- `03-prd-draft.md` - Draft PRD from synthesis phase
- `04-prd-review.md` - Critical review with issues and strengths

## Output
**Save to the "Output File" path specified at the top of this prompt** (`05-prd-final.md`)

## Process

### Step 1: Extract Review Findings

From the review document, identify:
1. **Issues by severity** — Critical and High must be resolved
2. **Strengths to preserve** — These must NOT be degraded by fixes
3. **Lens scores** — Any ⚠️ or ❌ must improve
4. **Devil's Advocate questions** — Must have explicit answers in final PRD

### Step 2: Triage Issues

For each issue, decide:
- **Accept**: Apply recommendation as-is
- **Modify**: Apply variation with rationale
- **Reject**: Don't apply (Medium/Low only, requires justification)

Rules:
- Critical → Must Accept or Modify
- High → Should Accept or Modify
- Medium/Low → May Reject with documented reason

### Step 3: Verify Strength Preservation

Before finalizing any fix:
- Check if it impacts an identified strength
- If yes, find alternative approach that preserves the strength

### Step 4: Produce Final PRD

Integrate all changes. Ensure Devil's Advocate questions are answered within relevant PRD sections (not as separate appendix).

---

## Output Format

```markdown
# [Project Name] - Product Requirements Document

**Version**: 1.0
**Date**: {date}
**Status**: Approved | Needs Revision
**Confidence**: High | Medium | Low

---

## Review Integration

**Confidence Rationale**: [1 sentence]

| Severity | Accepted | Modified | Rejected |
|----------|----------|----------|----------|
| Critical | X | X | 0 |
| High | X | X | X |
| Medium | X | X | X |

| Lens | Before → After |
|------|----------------|
| Feasibility | ⚠️ → ✅ |
| Completeness | ❌ → ⚠️ |
| ... | ... |

**Key Changes from Draft:**
- [Change 1]
- [Change 2]
- [Change 3]

**Rejected Recommendations** (if any):
- [Issue]: [Why rejected]

---

## Executive Summary

[3-5 sentences: What, why, success definition]

---

## Problem Statement

[Pain points with evidence]
[Quantified impact]

---

## Users

### Primary Persona
**[Name]** — [Role]
- Goals: ...
- Pain points: ...
- Context: ...

### Secondary Personas
[Brief list]

### Anti-Personas
[Who this is NOT for]

---

## Goals & Metrics

| Outcome | Metric | Target | Measurement |
|---------|--------|--------|-------------|
| ... | ... | ... | ... |

---

## Requirements

### MUST HAVE

| ID | Requirement | Acceptance Criteria |
|----|-------------|---------------------|
| FR-001 | ... | ... |

### SHOULD HAVE

| ID | Requirement | Acceptance Criteria |
|----|-------------|---------------------|
| ... | ... | ... |

### COULD HAVE

| ID | Requirement | Acceptance Criteria |
|----|-------------|---------------------|
| ... | ... | ... |

### Non-Functional

| Category | Requirement | Target |
|----------|-------------|--------|
| Performance | ... | ... |
| Security | ... | ... |
| Scalability | ... | ... |

---

## Technical Approach

[Architecture overview]
[Key tech choices + rationale]
[Integration points]

---

## Constraints

| Constraint | Type | Impact |
|------------|------|--------|
| ... | Tech/Business/Time | ... |

---

## Risks & Mitigations

| Risk | L/I | Mitigation |
|------|-----|------------|
| ... | H/M, H/M | ... |

---

## Out of Scope

| Item | Reason | Revisit |
|------|--------|---------|
| ... | ... | [When/Never] |

---

## Open Questions

| Question | Blocking? | Owner |
|----------|-----------|-------|
| ... | Yes/No | ... |
```

---

## Confidence Ratings

- **High**: All critical/high resolved, all lenses ✅, strengths preserved
- **Medium**: No critical, high mostly resolved, no ❌ lenses
- **Low**: Any critical unresolved OR multiple ❌ lenses

## Quality Gate

Before marking "Approved":
- [ ] Zero critical issues unresolved
- [ ] Zero high issues unresolved without justification  
- [ ] No lens at ❌
- [ ] All identified strengths preserved
- [ ] Devil's Advocate questions answered in PRD body (not appendix)