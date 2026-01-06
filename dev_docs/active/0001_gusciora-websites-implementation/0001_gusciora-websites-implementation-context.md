# Gusciora Websites Implementation - Context

**Task Number:** 0001
**Last Updated:** 2026-01-06

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
All sites share parent domain `gusciora.pl`, so localStorage keys are naturally shared:
- `gusciora-theme`: stores `"light"` or `"dark"`
- `gusciora-lang`: stores `"en"` or `"pl"`

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
