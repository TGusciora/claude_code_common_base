# Phase 4: Critical Review

## Role
Skeptical senior engineer. Your job: find problems AND identify strengths. Do not fix anything — that's the consolidation phase's job.

## Inputs
All inputs are provided in the "Input Documents" section above:
- `03-prd-draft.md` - Draft PRD from synthesis phase
- `01-interview.md` - Original user requirements
- `02-research.md` - Technical research findings

## Output
**Save to the "Output File" path specified at the top of this prompt** (`04-prd-review.md`)

This is a **review document only** — do NOT include a revised PRD. The consolidation phase will produce the final PRD based on your review.

---

## Process

### Step 1: First Read
Read the draft PRD completely without judging. Form overall impression before being critical.

### Step 2: Cross-Reference Validation
Verify draft against interview and research:
- Calculate interview coverage (% of interview points addressed)
- Calculate research integration (% of research findings incorporated)
- List any dropped items (things from interview/research not in PRD)

### Step 3: Apply Review Lenses

For each lens, score it and document both issues AND strengths.

**Scoring Criteria:**
- ✅ **Pass**: No critical/high issues, minor issues only
- ⚠️ **Warning**: Some high issues or multiple medium issues
- ❌ **Fail**: Critical issues or many high issues

**Feasibility Lens**
- Can this be built with specified tech stack?
- Is timeline realistic for complexity?
- Are there skill gaps or missing dependencies?

**Completeness Lens**
- All user journeys covered?
- Edge cases and error states defined?
- Migration/maintenance considered?

**Consistency Lens**
- Any contradictory requirements?
- Do success metrics actually measure stated goals?
- Does scope match constraints?

**Risk Lens**
- Technical risks identified with mitigations?
- What's the worst-case scenario?
- What if scale is 10x expected?

### Step 4: Identify Strengths to Preserve
Document what the PRD does WELL. These must be preserved in consolidation.

### Step 5: Devil's Advocate Questions
Pose 3-5 hard questions that the consolidation phase MUST explicitly answer.

---

## Output Format

Use the project name from the "Project" field at the top of this prompt.

```markdown
# PRD Review Report: [Project Name]

**Date**: [today's date]
**Reviewer**: Phase 4 - Critical Review
**PRD Reviewed**: 03-prd-draft.md

---

## Review Summary

**Overall Assessment**: Ready / Needs Work / Significant Issues
**Issue Count**: X Critical, X High, X Medium, X Low
**Key Concerns**:
1. [Top concern]
2. [Second concern]
3. [Third concern]

---

## Lens Scorecard

| Lens | Score | Summary |
|------|-------|---------|
| Feasibility | ✅/⚠️/❌ | [1-line summary] |
| Completeness | ✅/⚠️/❌ | [1-line summary] |
| Consistency | ✅/⚠️/❌ | [1-line summary] |
| Risk | ✅/⚠️/❌ | [1-line summary] |

---

## Review Findings by Lens

### Feasibility Review (Score: ✅/⚠️/❌)

**Issues Found:**

| Section | Issue | Severity | Recommendation |
|---------|-------|----------|----------------|
| ... | ... | Critical/High/Medium/Low | ... |

**Strengths:**
- [What works well for feasibility]
- [Another strength]

---

### Completeness Review (Score: ✅/⚠️/❌)

**Issues Found:**

| Section | Issue | Severity | Recommendation |
|---------|-------|----------|----------------|
| ... | ... | Critical/High/Medium/Low | ... |

**Strengths:**
- [What works well for completeness]
- [Another strength]

---

### Consistency Review (Score: ✅/⚠️/❌)

**Issues Found:**

| Section | Issue | Severity | Recommendation |
|---------|-------|----------|----------------|
| ... | ... | Critical/High/Medium/Low | ... |

**Strengths:**
- [What works well for consistency]
- [Another strength]

---

### Risk Review (Score: ✅/⚠️/❌)

**Issues Found:**

| Section | Issue | Severity | Recommendation |
|---------|-------|----------|----------------|
| ... | ... | Critical/High/Medium/Low | ... |

**Strengths:**
- [What works well for risk management]
- [Another strength]

---

## Cross-Reference Validation

**Interview Coverage**: X% of interview points addressed
**Research Integration**: X% of research findings incorporated

**Dropped Items** (from interview/research not in PRD):
| Source | Item | Why Concerning |
|--------|------|----------------|
| Interview | ... | ... |
| Research | ... | ... |

---

## Prioritized Issues List

| Rank | Issue | Section | Severity | Fix Complexity | Recommendation |
|------|-------|---------|----------|----------------|----------------|
| 1 | ... | ... | Critical | Easy/Medium/Hard | ... |
| 2 | ... | ... | High | Easy/Medium/Hard | ... |
| ... | ... | ... | ... | ... | ... |

---

## Strengths to Preserve

> **Critical**: The consolidation phase MUST maintain these strengths. Do not let issue fixes degrade these.

1. **[Strength Title]**: [Specific examples from PRD]
2. **[Strength Title]**: [Specific examples from PRD]
3. **[Strength Title]**: [Specific examples from PRD]

---

## Devil's Advocate Questions

> The consolidation phase MUST explicitly answer each of these in the final PRD.

1. **[Hard Question 1]**
   - Context: [Why this matters]

2. **[Hard Question 2]**
   - Context: [Why this matters]

3. **[Hard Question 3]**
   - Context: [Why this matters]

---

## Review Completion Checklist

- [ ] All four lenses scored
- [ ] Strengths identified for each lens
- [ ] Cross-reference validation completed
- [ ] Issues prioritized with recommendations
- [ ] Strengths to preserve documented
- [ ] Devil's advocate questions posed
```

---

## Important Reminders

1. **Do NOT fix issues** — only identify and recommend
2. **Do NOT produce a revised PRD** — that's Phase 5's job
3. **Be specific** — vague criticism is useless
4. **Balance criticism with recognition** — identify what works well
5. **Prioritize** — not all issues are equal
6. **Pose hard questions** — challenge assumptions the consolidation must address
