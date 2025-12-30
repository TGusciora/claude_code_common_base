# Phase 2: Research

## Context
You are conducting web research to validate and expand interview findings from Phase 1.

**Input**: `01-interview.md` (provided in Input Documents above)
**Output**: See "Output File" path above (save your research there)

## Instructions

### 1. Extract Research Questions
Read the interview findings and extract concrete questions that need external validation. Prioritize:
- **Must validate**: Core assumptions the product depends on (technical feasibility, market existence)
- **Should validate**: Competitive landscape, user expectations
- **Nice to have**: Best practices, edge cases

### 2. Execute Research
Use `WebSearch` for discovery, `WebFetch` to read promising sources in depth.

**Search patterns:**
- Direct: "[topic] best practices 2024", "[technology] architecture"
- Problem-focused: "[problem] solutions", "how companies solve [problem]"
- Competitive: "[competitor] vs alternatives", "best [product category] tools"

**Source prioritization:**
1. Official docs, academic papers → high trust
2. Industry reports, established tech blogs → medium-high trust
3. Community discussions (HN, Reddit, Stack Overflow) → good for sentiment/gotchas
4. Vendor content → useful but flag bias

### 3. Synthesize Findings
For each research question:
- State finding clearly
- Note confidence level (strong/moderate/weak) based on source quality and agreement
- Flag contradictions or gaps
- Link to sources

### 4. Stopping Conditions
Stop researching a topic when:
- You have 2+ quality sources agreeing
- You've found authoritative documentation
- 3 different search queries yield no new useful info

Move on from research phase when all "must validate" questions are answered.

## Output Structure

Write findings in a format appropriate to what you discovered. Include:

1. **Executive Summary** (3-5 sentences max)
2. **Validated Assumptions** - table mapping interview claims → research findings
3. **Competitive Landscape** - only if relevant competitors exist
4. **Technical Findings** - architecture patterns, technology recommendations with tradeoffs
5. **Risks & Gaps** - what couldn't be validated, conflicting information
6. **Source Index** - URLs with 1-line summaries, grouped by credibility

Omit sections that aren't relevant. Depth matters more than coverage.

## Quality Gates
Before completing, verify:
- [ ] All "must validate" items addressed
- [ ] High-impact claims have quality sources
- [ ] Contradictions are flagged, not hidden
- [ ] Technical recommendations include tradeoffs