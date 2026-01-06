# Gusciora Websites Implementation - Context

**Task Number:** 0001
**Last Updated:** 2026-01-06

---

## SESSION PROGRESS - 2026-01-06

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

**Next Iteration Should:**
- Begin Phase 2: tomasz.gusciora.pl sections (Hero, Bio, Training, etc.)
- Consider invoking /frontend-design for visual polish

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
