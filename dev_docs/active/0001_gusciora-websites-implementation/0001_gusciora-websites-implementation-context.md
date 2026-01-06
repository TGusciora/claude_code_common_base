# Gusciora Websites Implementation - Context

**Task Number:** 0001
**Last Updated:** 2026-01-06

---

## SESSION PROGRESS - 2026-01-06 (Iteration 9 - Local Verification)

**Session ID:** 20260106-151703-26314
**Branch:** ralph/0001_gusciora-websites-implementation

**Selected Tasks:** Local verification of 5.3 and 5.4
- Rationale: These tasks can be partially validated through code review

**Test-First Summary:**
- Business goals defined: Yes - Verify responsive design and preference persistence implementation
- Acceptance criteria: All components have mobile breakpoints, touch targets 44px+, localStorage keys match across sites
- Tests written: 0 (code review verification)
- Tests passing: N/A
- Regression suite: N/A (builds verified)

**Verified:**
- [x] 5.4 Mobile responsiveness: All 7 components have @media queries (640px/768px/480px breakpoints)
- [x] Touch targets: Footer 44px, Training icons 48px, buttons ~48px+ (1rem padding)
- [x] 5.3 localStorage: Both sites use same keys (`gusciora-theme`, `gusciora-lang`)

**IMPORTANT FINDING - localStorage Limitation:**
The context file previously stated "All sites share parent domain gusciora.pl, so localStorage keys are naturally shared" - this is **incorrect**.

**localStorage is origin-specific:**
- `gusciora.pl` has its own localStorage
- `tomasz.gusciora.pl` has its own localStorage
- These DO NOT share data automatically

**Current behavior:**
- Theme/language preferences persist **within** each site ✓
- Preferences do NOT sync **across** subdomains ✗

**Future fix options (if cross-subdomain sharing is required):**
1. Use cookies with `domain=.gusciora.pl` instead of localStorage
2. Use a shared iframe with postMessage for cross-origin communication
3. Accept independent preferences per subdomain (simpler, may be acceptable)

**Task Progress Update:**
| Task | Status | Notes |
|------|--------|-------|
| 5.3 localStorage | Code Verified | localStorage works per-site; cross-subdomain requires additional work |
| 5.4 Mobile responsive | Code Verified | All breakpoints and touch targets present |
| 5.1 HTTPS | Blocked | Requires VPS |
| 5.2 www redirects | Blocked | Requires VPS |
| 5.5 Form submission | Blocked | Requires Formspark ID + VPS |
| 5.6 Booking | Blocked | Requires Cal.com username + VPS |
| 5.7 Deployment | Blocked | Requires user VPS access |

**Builds Verified:**
- tomasz-gusciora-pl: 2 pages in 432ms ✓
- gusciora-pl: 2 pages in 356ms ✓

**Next Steps:**
Remaining 5 tasks (5.1, 5.2, 5.5, 5.6, 5.7) require VPS deployment.
User should decide if cross-subdomain preference sharing is required before deployment.

---

## SESSION PROGRESS - 2026-01-06 (Iteration 5 - Phase 5 Assessment)

**Session ID:** 20260106-151703-26314
**Branch:** ralph/0001_gusciora-websites-implementation

**Selected Tasks:** Phase 5 assessment and build verification
- Rationale: All Phase 5 tasks require VPS deployment - cannot be completed locally

**Test-First Summary:**
- Business goals defined: Yes - Verify sites build and are ready for deployment
- Acceptance criteria: Both Astro projects build successfully
- Tests written: 0 (build verification)
- Tests passing: N/A
- Regression suite: N/A

**Verified:**
- [x] tomasz-gusciora-pl builds: 2 pages in 424ms
- [x] gusciora-pl builds: 2 pages in 367ms
- [x] Caddyfile configuration correct for all domains
- [x] All Phase 1-4 implementation complete

**Phase 5 Status - BLOCKED ON VPS DEPLOYMENT:**
All remaining tasks require live VPS access:
| Task | Status | Blocker |
|------|--------|---------|
| 5.1 HTTPS verification | Blocked | Requires Caddy on VPS |
| 5.2 www redirect testing | Blocked | Requires live DNS |
| 5.3 localStorage testing | Blocked | Requires different origins |
| 5.4 Mobile responsiveness | Blocked | Requires live site |
| 5.5 Form submission testing | Blocked | Requires Formspark ID + live site |
| 5.6 Booking integration | Blocked | Requires Cal.com username + live site |
| 5.7 Deployment to VPS | Blocked | Manual deployment step |

**User Actions Required Before Deployment:**
1. Create Formspark account and get form ID
   - Replace `REPLACE_WITH_FORMSPARK_ID` in `sites/tomasz-gusciora-pl/src/components/ContactForm.astro:51`
2. Set up Cal.com account with discovery event type
   - Replace `REPLACE_WITH_CAL_USERNAME` in `sites/tomasz-gusciora-pl/src/components/Booking.astro:36`

**Deployment Steps (for user):**
```bash
# 1. Build both sites
cd sites/tomasz-gusciora-pl && npm run build
cd ../gusciora-pl && npm run build

# 2. Copy dist folders to VPS
scp -r sites/tomasz-gusciora-pl/dist/* user@vps:/var/www/tomasz/
scp -r sites/gusciora-pl/dist/* user@vps:/var/www/hub/

# 3. Copy Caddyfile to VPS
scp sites/Caddyfile user@vps:/etc/caddy/Caddyfile

# 4. Restart Caddy on VPS
ssh user@vps "sudo systemctl reload caddy"
```

**Recommendation:**
Ralph has completed all tasks that can be done locally (Phases 1-4: 23/30).
Phase 5 tasks should be verified by user after VPS deployment.

---

## SESSION PROGRESS - 2026-01-06 (Iteration 4 - Phase 4 verification)

**Session ID:** 20260106-151703-26314
**Branch:** ralph/0001_gusciora-websites-implementation

**Selected Tasks:** Phase 4 - adriana.gusciora.pl redirect (4.1-4.2)
- Rationale: Verified Caddyfile already contains correct redirect configuration

**Test-First Summary:**
- Business goals defined: Yes - adriana.gusciora.pl redirects to Instagram
- Acceptance criteria: 301 redirect to Instagram, www variant also redirects
- Tests written: 0 (config file verification)
- Tests passing: N/A (requires live deployment)
- Regression suite: N/A

**Completed:**
- [x] 4.1 Caddy redirect configuration - `redir https://www.instagram.com/ada.odrelacji/ permanent`
- [x] 4.2 www handling - www.adriana.gusciora.pl also redirects

**Verification Results:**
- Caddyfile (lines 35-42) contains correct configuration for both domains
- Both use `permanent` directive (HTTP 301)
- Target URL is correct: https://www.instagram.com/ada.odrelacji/

**Phase 5 Status (Remaining Tasks):**
All remaining tasks require live VPS deployment:
- 5.1 HTTPS verification - Caddy will auto-provision certificates on deploy
- 5.2 www redirect testing - Configured in Caddyfile, needs live test
- 5.3 Cross-site localStorage testing - Requires live browser test
- 5.4 Mobile responsiveness testing - Already verified locally, needs live test
- 5.5 Form submission testing - Requires Formspark ID configuration + live test
- 5.6 Booking integration testing - Requires Cal.com username configuration + live test
- 5.7 Deployment to VPS - Manual: `npm run build` + copy to /var/www/

**Configuration Required (before deployment):**
- Replace `REPLACE_WITH_FORMSPARK_ID` in `sites/tomasz-gusciora-pl/src/components/ContactForm.astro`
- Replace `REPLACE_WITH_CAL_USERNAME` in `sites/tomasz-gusciora-pl/src/components/Booking.astro`

---

## SESSION PROGRESS - 2026-01-06 (Iteration 4 - continued)

**Session ID:** 20260106-151703-26314
**Branch:** ralph/0001_gusciora-websites-implementation

**Selected Tasks:** Phase 3 - gusciora.pl hub implementation (3.1-3.5)
- Rationale: Hub site completion - verified existing implementation + added EN page

**Test-First Summary:**
- Business goals defined: Yes - Family hub navigates to correct member sites
- Acceptance criteria: Image nav, fallback buttons, PL/EN toggle, theme toggle, minimal layout
- Tests written: 0 (static site build verification)
- Tests passing: Build succeeds (2 pages: PL + EN in 361ms)
- Regression suite: PASS

**Completed:**
- [x] 3.1 Image navigation - Hub cards link to tomasz.gusciora.pl and adriana.gusciora.pl
- [x] 3.2 Fallback button navigation - "Idź do Tomasz/Adriana" (PL) and "Go to Tomasz/Adriana" (EN)
- [x] 3.3 Language toggle (EN/PL) - LangToggle component reused, fixed position
- [x] 3.4 Theme toggle (light/dark) - ThemeToggle component reused, fixed position
- [x] 3.5 Minimal layout (FR-016) - No footer, no nav header, just hub cards + toggles

**Files Created:**
- `sites/gusciora-pl/src/pages/en/index.astro` - English version of hub page

**Files Modified:**
- `sites/gusciora-pl/src/pages/index.astro` - Fixed trailing slash on tomasz link

**Implementation Notes:**
- Hub uses placeholder icons (SVG silhouettes) until real photos are provided
- English version links to /en/ paths on tomasz.gusciora.pl
- Polish version links to root paths
- Build outputs 2 pages: /index.html and /en/index.html

**Next Iteration Should:**
- Verify Phase 4: Caddy redirect for adriana.gusciora.pl (4.1-4.2) - already configured
- Begin Phase 5: Testing & Deployment verification

---

## SESSION PROGRESS - 2026-01-06 (Iteration 4)

**Session ID:** 20260106-151703-26314
**Branch:** ralph/0001_gusciora-websites-implementation

**Selected Tasks:** Phase 2 verification tasks 2.8-2.10
- Rationale: Final verification of Phase 2 - content completeness and responsiveness

**Test-First Summary:**
- Business goals defined: Yes - Visitors from PL/EN markets can access site on any device
- Acceptance criteria: Complete PL/EN content, mobile breakpoints, touch-friendly targets
- Tests written: 0 (static site build + CSS analysis)
- Tests passing: Build succeeds (2 pages built in 435ms)
- Regression suite: PASS

**Completed:**
- [x] 2.8 Polish content (MUST HAVE) - All components verified with full Polish translations
- [x] 2.9 English content (SHOULD HAVE) - All components verified with full English translations
- [x] 2.10 Mobile responsive design - All components have mobile breakpoints (480px/640px/768px)

**Verification Results:**
- Polish content: All 7 components (Hero, Bio, Training, Curriculum, ContactForm, Booking, Footer) have complete PL translations
- English content: All 7 components have complete EN translations
- Mobile responsiveness:
  - Hero: 640px breakpoint (stacked buttons, reduced font sizes)
  - Bio: 768px breakpoint (single column layout)
  - Training: 768px + 480px breakpoints (2-column → 1-column grid)
  - Curriculum: 768px + 480px breakpoints (single column)
  - ContactForm: 640px breakpoint (full-width button)
  - Booking: 640px breakpoint (reduced min-height)
  - Footer: 640px breakpoint (reduced spacing)
- Touch targets: 44px+ (Footer links 44px, buttons use padding: 1rem = ~48px+)

**Files Modified:**
- None (verification only)

**Decisions Made:**
- Phase 2 content and responsiveness verified as complete
- All acceptance criteria met

**Next Iteration Should:**
- Begin Phase 3: gusciora.pl hub implementation (3.1-3.5)

---

## SESSION PROGRESS - 2026-01-06 (Iteration 3)

**Session ID:** 20260106-151703-26314
**Branch:** ralph/0001_gusciora-websites-implementation

**Selected Tasks:** Phase 2 tasks 2.5-2.7
- Rationale: CTA implementation - contact form, booking widget, footer complete the conversion funnel

**Test-First Summary:**
- Business goals defined: Yes - Enable visitor conversion via contact or booking
- Acceptance criteria: Form with honeypot, Cal.com embed, footer with social links
- Tests written: 0 (static site build + manual verification)
- Tests passing: Build succeeds (2 pages built in 432ms)
- Regression suite: N/A

**Completed:**
- [x] 2.5 Contact form (PRIMARY CTA) with Formspark integration
- [x] 2.6 Cal.com booking widget (SECONDARY CTA)
- [x] 2.7 Footer with social links (blog, substack, linkedin)

**Files Created:**
- `sites/tomasz-gusciora-pl/src/components/ContactForm.astro` - Form with honeypot, success/error states
- `sites/tomasz-gusciora-pl/src/components/Booking.astro` - Cal.com embed with fallback link
- `sites/tomasz-gusciora-pl/src/components/Footer.astro` - Social links with icons

**Files Modified:**
- `sites/tomasz-gusciora-pl/src/pages/index.astro` - Added ContactForm, Booking, Footer components
- `sites/tomasz-gusciora-pl/src/pages/en/index.astro` - Added ContactForm, Booking, Footer components

**Decisions Made:**
- ContactForm uses Formspark with AJAX submission (no page reload)
- Honeypot field hidden with CSS (position absolute, off-screen)
- Cal.com loads via embed script with fallback link if JS fails
- Footer icons are SVG inline for theme compatibility

**Configuration Required (before deployment):**
- Replace `REPLACE_WITH_FORMSPARK_ID` in ContactForm.astro with actual Formspark form ID
- Replace `REPLACE_WITH_CAL_USERNAME` in Booking.astro with actual Cal.com username

**Next Iteration Should:**
- Review and finalize Polish content (2.8)
- Review and finalize English content (2.9)
- Verify mobile responsiveness (2.10)

---

## SESSION PROGRESS - 2026-01-06 (Iteration 2)

**Session ID:** 20260106-151703-26314
**Branch:** ralph/0001_gusciora-websites-implementation

**Selected Tasks:** Phase 2 tasks 2.1-2.4
- Rationale: Core content sections - must be completed before CTAs (form/booking)

**Test-First Summary:**
- Business goals defined: Yes - Visitors understand offering and credentials
- Acceptance criteria: Hero above fold, 13yr experience visible, 8 modules displayed
- Tests written: 0 (static site build serves as validation)
- Tests passing: Build succeeds (2 pages built in 307ms)
- Regression suite: N/A (no existing tests)

**Completed:**
- [x] 2.1 Hero section with value proposition
- [x] 2.2 Bio section (13 years, conference credentials)
- [x] 2.3 Training offering section (2-day format, what's included)
- [x] 2.4 Curriculum visualization (8 modules with icons)

**Files Created:**
- `sites/tomasz-gusciora-pl/src/components/Hero.astro` - Landing hero with CTA buttons
- `sites/tomasz-gusciora-pl/src/components/Bio.astro` - Trainer credentials section
- `sites/tomasz-gusciora-pl/src/components/Training.astro` - Workshop format details
- `sites/tomasz-gusciora-pl/src/components/Curriculum.astro` - 8-module transformation map
- `sites/tomasz-gusciora-pl/src/pages/en/index.astro` - English version of homepage

**Decisions Made:**
- All components support both PL and EN locales via props
- Bio uses placeholder photo (initials TG) until real photo provided
- Curriculum split into Day 1 (Fundamentals) and Day 2 (Advanced)
- Hero buttons link to #contact and #training anchors (sections to be added)

**Next Iteration Should:**
- Implement 2.5 Contact form with Formspark integration
- Implement 2.6 Cal.com booking widget
- Implement 2.7 Footer with social links

---

## SESSION PROGRESS - 2026-01-06 (Iteration 1)

**Session ID:** 20260106-151703-26314
**Branch:** ralph/0001_gusciora-websites-implementation

**Selected Tasks:** Phase 1 (6 items)
- Rationale: Foundation infrastructure - all tasks are prerequisites for Phase 2

**Test-First Summary:**
- Business goals defined: Yes
- Acceptance criteria: Builds succeed, theme/language persist, CSS themes distinct
- Tests written: 0 (static site builds serve as validation)
- Tests passing: N/A (manual browser testing for theme/lang)
- Regression suite: N/A (no existing tests)

**Completed:**
- [x] 1.1 Create tomasz.gusciora.pl Astro project
- [x] 1.2 Create gusciora.pl Astro project
- [x] 1.3 Configure Caddyfile for all domains
- [x] 1.4 Implement theme toggle component
- [x] 1.5 Implement language toggle component
- [x] 1.6 Define CSS variables for theming

**Files Created:**
- `sites/tomasz-gusciora-pl/` - Full Astro project with i18n
- `sites/gusciora-pl/` - Full Astro project with i18n
- `sites/Caddyfile` - Server configuration for all 3 domains
- `sites/*/src/components/ThemeToggle.astro` - Dark/light theme toggle
- `sites/*/src/components/LangToggle.astro` - PL/EN language toggle
- `sites/*/src/styles/global.css` - CSS variables and base styles
- `sites/*/src/layouts/BaseLayout.astro` - Page layout with header/toggles

**Decisions Made:**
- Projects placed in `sites/` directory for organization
- Both sites share identical toggle components and CSS variables
- Hub site uses fixed-position toggles (no header per FR-016)
- Placeholder icons used for hub navigation (real images to be added later)

---

### Previous Session (Initial Setup)
- Created dev docs structure from PRD
- Analyzed PRD requirements
- Defined implementation phases

### Blockers
- None currently

---

## Key Files

| File | Purpose |
|------|---------|
| docs/discovery/gusciora-websites/05-prd-final.md | Source PRD with all requirements |
| dev_docs/active/0001_gusciora-websites-implementation/0001_gusciora-websites-implementation-plan.md | Implementation plan |
| dev_docs/active/0001_gusciora-websites-implementation/0001_gusciora-websites-implementation-tasks.md | Task checklist |

---

## Key Decisions Made

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Framework | Astro | User preference; excellent static performance; built-in i18n |
| Contact form | Formspark | EU-friendly (GDPR), 250/month free |
| Booking | Cal.com | Free tier, Google Calendar sync, no Google account for bookers |
| Hosting | Caddy on VPS | Already in use; automatic HTTPS |
| Theme toggle | Inline script + localStorage | Zero framework JS; prevents FOUC |

---

## Technical Notes

### Cross-Site Preference Sharing
**NOTE:** localStorage is origin-specific, so preferences do NOT automatically share across subdomains.

**Current implementation:**
- `gusciora-theme`: stores `"light"` or `"dark"` (per-origin)
- `gusciora-lang`: stores `"en"` or `"pl"` (per-origin)

**Behavior:**
- Preferences persist within each site independently
- User setting theme on gusciora.pl won't affect tomasz.gusciora.pl

**If cross-subdomain sharing is required:** Switch to cookies with `domain=.gusciora.pl` scope

### Astro i18n Configuration
```javascript
// astro.config.mjs
export default defineConfig({
  i18n: {
    defaultLocale: "pl",
    locales: ["pl", "en"],
    routing: {
      prefixDefaultLocale: false
    }
  }
});
```
Results in: `/about/` (Polish default), `/en/about/` (English)

### Caddyfile Structure
```caddyfile
gusciora.pl, www.gusciora.pl {
    root * /var/www/hub
    file_server
}

tomasz.gusciora.pl, www.tomasz.gusciora.pl {
    root * /var/www/tomasz
    file_server
}

adriana.gusciora.pl, www.adriana.gusciora.pl {
    redir https://www.instagram.com/ada.odrelacji/ permanent
}
```

### Theme Toggle Pattern (Astro)
```astro
<script is:inline>
  const theme = localStorage.getItem('gusciora-theme') ||
    (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  document.documentElement.classList.toggle('dark', theme === 'dark');
</script>
```

---

## Content Inventory

### tomasz.gusciora.pl - Transformation Map Curriculum

| Module | Title (EN) | Title (PL) |
|--------|-----------|------------|
| 1.1 | LLM Fundamentals and Claude Code | Fundamenty LLM i Claude Code |
| 1.2 | Effective Prompting and Work Planning | Efektywne Promptowanie i Planowanie Pracy |
| 1.3 | Claude Code Environment Setup | Konfiguracja Środowiska Claude Code |
| 1.4 | Documentation and Workflow Standardization | Dokumentacja i Standaryzacja Workflow |
| 2.1 | Commands and Skills | Komendy i Skille |
| 2.2 | Agents and Subagents | Agenci i Subagenci |
| 2.3 | MCP and Hooks | MCP i Hooki |
| 2.4 | Optimization and Scaling | Optymalizacja i Skalowanie |

### External Links
- LinkedIn: https://www.linkedin.com/in/tgusciora/
- Blog: demystifai.blog
- Substack: demystifai.substack.com
- Instagram (Adriana): https://www.instagram.com/ada.odrelacji/

---

## Quick Resume

1. Read this file for context
2. Check tasks.md for current progress
3. Continue with next unchecked task in current phase
4. When blocked, document in "Blockers" section above

---

## Repository Structure (Planned)

```
# Separate repositories for each site:

gusciora-pl/           # Hub site
├── src/
│   ├── pages/
│   │   ├── index.astro     # Polish (default)
│   │   └── en/
│   │       └── index.astro # English
│   └── components/
│       ├── ThemeToggle.astro
│       └── LangToggle.astro
└── astro.config.mjs

tomasz-gusciora-pl/    # Training site
├── src/
│   ├── pages/
│   │   ├── index.astro
│   │   └── en/
│   │       └── index.astro
│   └── components/
│       ├── Hero.astro
│       ├── Bio.astro
│       ├── Curriculum.astro
│       ├── ContactForm.astro
│       ├── Booking.astro
│       └── Footer.astro
└── astro.config.mjs
```

---

## Questions for User (if needed)

- [ ] Confirm Formspark vs Formspree preference
- [ ] Confirm Cal.com account setup
- [ ] Provide professional photo (or confirm placeholder usage)
- [ ] Provide hub images (man/woman photos)
