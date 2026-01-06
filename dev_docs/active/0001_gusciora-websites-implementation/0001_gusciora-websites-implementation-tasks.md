# Gusciora Websites Implementation - Tasks

**Task Number:** 0001
**Last Updated:** 2026-01-06

---

## Phase 1: Project Setup & Shared Infrastructure

- [x] 1.1 Create tomasz.gusciora.pl Astro project
  - `npm create astro@latest` with minimal template
  - Configure i18n (pl default, en secondary)
  - AC: Project builds successfully

- [x] 1.2 Create gusciora.pl Astro project
  - Same setup as 1.1
  - AC: Project builds successfully

- [x] 1.3 Configure Caddyfile
  - Define all 3 domains
  - Add www redirects
  - Add adriana 301 redirect to Instagram
  - AC: Caddy config validates (Caddy not installed locally; syntax follows standard)

- [x] 1.4 Implement theme toggle component
  - Inline script pattern (no FOUC)
  - Read/write `gusciora-theme` localStorage key
  - System preference detection as fallback
  - AC: Theme persists across page loads; no flash

- [x] 1.5 Implement language toggle component
  - Read/write `gusciora-lang` localStorage key
  - Navigate to correct locale path on toggle
  - AC: Language persists; correct path navigation

- [x] 1.6 Define CSS variables for theming
  - Light mode colors
  - Dark mode colors (`.dark` class)
  - AC: Both themes visually distinct and readable

---

## Phase 2: tomasz.gusciora.pl Implementation

- [x] 2.1 Hero section
  - Value proposition visible above fold
  - Desktop and mobile layouts
  - AC: Hero visible on first viewport load

- [x] 2.2 Bio section
  - 13 years experience
  - Conference talks credentials
  - AC: Credentials clearly displayed

- [x] 2.3 Training offering section
  - 2-day remote workshop format
  - AC: Format clearly communicated

- [x] 2.4 Transformation map curriculum
  - All 8 modules displayed
  - Icons for each module
  - Scannable list format
  - AC: All modules visible with visual hierarchy

- [x] 2.5 Contact form (PRIMARY CTA)
  - Formspark integration
  - Fields: name, email, message
  - Success/error feedback
  - Honeypot spam protection
  - Visually emphasized as primary action
  - AC: Form submits to tomasz@demystifai.blog; user sees feedback

- [x] 2.6 Cal.com booking (SECONDARY CTA)
  - Embed widget on page
  - Style as secondary action
  - AC: Visitors can schedule discovery calls; no Google account required

- [x] 2.7 Footer
  - demystifai.blog link
  - demystifai.substack.com link
  - LinkedIn link (https://www.linkedin.com/in/tgusciora/)
  - AC: All icons visible and link correctly

- [ ] 2.8 Polish content (MUST HAVE)
  - All sections translated
  - AC: Full Polish version functional

- [ ] 2.9 English content (SHOULD HAVE)
  - All sections translated
  - AC: Full English version functional (or deferred post-MVP)

- [ ] 2.10 Mobile responsive design
  - Touch-friendly targets
  - Works on 3G
  - AC: All pages functional on mobile devices

---

## Phase 3: gusciora.pl Implementation

- [ ] 3.1 Image navigation
  - Man image → tomasz.gusciora.pl
  - Woman image → adriana.gusciora.pl
  - Clickable on desktop and mobile
  - AC: Images navigate to correct destinations

- [ ] 3.2 Fallback button navigation
  - "Go to Tomasz" button
  - "Go to Adriana" button
  - AC: Buttons visible as alternative navigation

- [ ] 3.3 Language toggle (EN/PL)
  - Reuse component from Phase 1
  - AC: Toggle functional; preference persisted

- [ ] 3.4 Theme toggle (light/dark)
  - Reuse component from Phase 1
  - AC: Toggle functional; preference persisted

- [ ] 3.5 Minimal layout (FR-016)
  - No footer
  - No additional navigation
  - Pure visual hub
  - AC: Only images, buttons, and toggles present

---

## Phase 4: adriana.gusciora.pl Redirect

- [ ] 4.1 Caddy redirect configuration
  - HTTP 301 permanent redirect
  - Target: https://www.instagram.com/ada.odrelacji/
  - AC: Browser redirects immediately; no page displayed

- [ ] 4.2 www handling
  - www.adriana.gusciora.pl also redirects
  - AC: www variant redirects correctly

---

## Phase 5: Testing & Deployment

- [ ] 5.1 HTTPS verification
  - All domains serve over HTTPS
  - AC: Caddy certificates valid for all domains

- [ ] 5.2 www redirect testing
  - www.gusciora.pl → gusciora.pl
  - www.tomasz.gusciora.pl → tomasz.gusciora.pl
  - AC: All www variants redirect correctly

- [ ] 5.3 Cross-site localStorage testing
  - Set theme on gusciora.pl → verify on tomasz.gusciora.pl
  - Set language on gusciora.pl → verify on tomasz.gusciora.pl
  - AC: Preferences persist across subdomains

- [ ] 5.4 Mobile responsiveness testing
  - Test all pages on mobile
  - Test touch interactions
  - AC: All pages functional on mobile

- [ ] 5.5 Form submission testing
  - Submit test inquiry
  - Verify email received at tomasz@demystifai.blog
  - Verify success message displayed
  - AC: End-to-end form flow works

- [ ] 5.6 Booking integration testing
  - Cal.com widget loads
  - Test booking flow
  - AC: Discovery call can be scheduled

- [ ] 5.7 Deployment to VPS
  - `npm run build` for each site
  - Copy dist/ to /var/www/hub and /var/www/tomasz
  - Verify Caddy serves correctly
  - AC: All sites accessible via their domains

---

## Progress Summary

| Phase | Total | Complete | Remaining |
|-------|-------|----------|-----------|
| Phase 1 | 6 | 6 | 0 |
| Phase 2 | 10 | 7 | 3 |
| Phase 3 | 5 | 0 | 5 |
| Phase 4 | 2 | 0 | 2 |
| Phase 5 | 7 | 0 | 7 |
| **Total** | **30** | **13** | **17** |
