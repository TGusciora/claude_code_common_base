# Gusciora Websites Implementation Plan

**Task Number:** 0001
**Last Updated:** 2026-01-06
**Status:** Planning
**Source:** docs/discovery/gusciora-websites/05-prd-final.md

---

## Executive Summary

Implement three websites for the Gusciora family:
1. **tomasz.gusciora.pl** - B2B landing page for Claude Code training services (primary business value)
2. **gusciora.pl** - Visual hub routing to family member sites
3. **adriana.gusciora.pl** - HTTP 301 redirect to Instagram

All sites use Astro framework, deployed to existing VPS with Caddy, with shared localStorage for theme/language preferences across subdomains.

---

## Current State Analysis

### Existing Infrastructure
- VPS with Caddy server (automatic HTTPS)
- Domains owned: gusciora.pl, tomasz.gusciora.pl, adriana.gusciora.pl
- DNS already configured
- Google Workspace (Starter tier) for tomasz@demystifai.blog

### What Needs to Be Built
| Site | Complexity | Key Features |
|------|------------|--------------|
| tomasz.gusciora.pl | High | Hero, bio, curriculum, contact form, Cal.com booking, footer |
| gusciora.pl | Low | Two clickable images, fallback buttons, toggles |
| adriana.gusciora.pl | Minimal | Caddy redirect only (no Astro site) |

---

## Proposed Future State

### Architecture
```
Internet → Caddy Server (VPS)
           ├── gusciora.pl → /var/www/hub (Astro static)
           ├── tomasz.gusciora.pl → /var/www/tomasz (Astro static)
           └── adriana.gusciora.pl → 301 → Instagram
```

### Shared Features
- localStorage keys: `gusciora-theme`, `gusciora-lang`
- Theme: light/dark with OS preference detection
- Language: EN/PL toggle (PL required, EN optional for MVP)

---

## Implementation Phases

### Phase 1: Project Setup & Shared Infrastructure
**Goal:** Create repository structure and shared utilities

1.1 Create tomasz.gusciora.pl Astro project
1.2 Create gusciora.pl Astro project
1.3 Configure Caddyfile for all three domains
1.4 Implement shared theme toggle component
1.5 Implement shared language toggle component
1.6 Define shared CSS variables for theming

### Phase 2: tomasz.gusciora.pl Implementation
**Goal:** Build the primary B2B landing page

2.1 Hero section with value proposition
2.2 Bio section (13 years experience, credentials)
2.3 Training offering section (2-day remote workshop)
2.4 Transformation map curriculum (8 modules with icons)
2.5 Contact form (PRIMARY CTA) with Formspark
2.6 Cal.com booking integration (SECONDARY CTA)
2.7 Footer with social links
2.8 Polish content (MUST HAVE)
2.9 English content (SHOULD HAVE)
2.10 Mobile-responsive design

### Phase 3: gusciora.pl Implementation
**Goal:** Build minimal visual hub

3.1 Two clickable images (man → tomasz, woman → adriana)
3.2 Fallback button navigation
3.3 EN/PL language toggle
3.4 Light/dark theme toggle
3.5 No footer, minimal design (FR-016)

### Phase 4: adriana.gusciora.pl Redirect
**Goal:** Configure Instagram redirect

4.1 Add Caddy redirect rule (301 → Instagram)
4.2 Handle www variant

### Phase 5: Testing & Deployment
**Goal:** Verify all requirements and deploy

5.1 Verify HTTPS on all domains
5.2 Test www redirects
5.3 Test cross-site localStorage sharing
5.4 Test mobile responsiveness
5.5 Verify form submission
5.6 Verify Cal.com booking
5.7 Deploy to VPS

---

## Detailed Tasks

### Phase 1: Project Setup

| # | Task | Effort | Acceptance Criteria |
|---|------|--------|---------------------|
| 1.1 | Create tomasz.gusciora.pl Astro project | S | `npm create astro@latest` with minimal template; i18n configured |
| 1.2 | Create gusciora.pl Astro project | S | Same setup as 1.1 |
| 1.3 | Configure Caddyfile | S | All 3 domains defined; www redirects; adriana 301 |
| 1.4 | Theme toggle component | M | Inline script; reads/writes `gusciora-theme`; no FOUC |
| 1.5 | Language toggle component | M | Reads/writes `gusciora-lang`; redirects to locale path |
| 1.6 | CSS variables for theming | S | Light/dark color schemes defined |

### Phase 2: tomasz.gusciora.pl

| # | Task | Effort | Acceptance Criteria |
|---|------|--------|---------------------|
| 2.1 | Hero section | M | Value prop visible above fold; desktop + mobile |
| 2.2 | Bio section | S | 13 years experience, conference talks displayed |
| 2.3 | Training offering | S | 2-day remote workshop format clear |
| 2.4 | Curriculum visualization | L | 8 modules with icons; scannable list format |
| 2.5 | Contact form | M | Formspark integration; name/email/message; success/error feedback |
| 2.6 | Cal.com embed | M | Discovery calls bookable; no Google account required |
| 2.7 | Footer | S | Icons linking to demystifai.blog, Substack, LinkedIn |
| 2.8 | Polish content | M | All sections translated to Polish |
| 2.9 | English content | M | All sections in English (SHOULD HAVE) |
| 2.10 | Mobile responsive | M | Touch-friendly; works on 3G |

### Phase 3: gusciora.pl

| # | Task | Effort | Acceptance Criteria |
|---|------|--------|---------------------|
| 3.1 | Image navigation | M | Man/woman images clickable; link to correct subdomains |
| 3.2 | Fallback buttons | S | "Go to Tomasz" / "Go to Adriana" buttons visible |
| 3.3 | Language toggle | S | Reuse component from Phase 1 |
| 3.4 | Theme toggle | S | Reuse component from Phase 1 |
| 3.5 | Minimal layout | S | No footer; pure visual hub |

### Phase 4: Redirect

| # | Task | Effort | Acceptance Criteria |
|---|------|--------|---------------------|
| 4.1 | Caddy redirect | S | HTTP 301 to https://www.instagram.com/ada.odrelacji/ |
| 4.2 | www handling | S | www.adriana.gusciora.pl also redirects |

### Phase 5: Testing & Deployment

| # | Task | Effort | Acceptance Criteria |
|---|------|--------|---------------------|
| 5.1 | HTTPS verification | S | All domains serve over HTTPS |
| 5.2 | www redirect test | S | www variants redirect to non-www |
| 5.3 | localStorage test | M | Theme/lang persist when navigating between sites |
| 5.4 | Mobile test | M | All pages functional on mobile |
| 5.5 | Form test | S | Submission reaches tomasz@demystifai.blog |
| 5.6 | Booking test | S | Cal.com widget loads; booking works |
| 5.7 | Deploy to VPS | M | `npm run build` + copy dist to /var/www/ |

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Images need optimization | Medium | Medium | Test/compress before launch; use WebP |
| EN translation unavailable | Medium | Low | PL-only MVP acceptable |
| FOUC with theme toggle | Low | Low | Use Astro `is:inline` directive |
| Form spam | Low | Low | Enable Formspark spam filtering |
| Repo divergence over time | Medium | Medium | Document shared conventions |

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Training inquiries | 1+/month | Formspark dashboard |
| Booking requests | 1+/month | Cal.com dashboard |
| HTTPS uptime | 100% | Caddy auto-certificates |
| Redirect success | 100% | HTTP 301 verification |

---

## Dependencies

### External Services
- **Formspark** - Contact form backend (250/month free)
- **Cal.com** - Booking integration (free tier)
- **Caddy** - Already on VPS

### Content Required
- [ ] Hero copy for tomasz.gusciora.pl
- [ ] Professional photo (placeholder acceptable initially)
- [ ] Images for gusciora.pl hub (man/woman photos)

---

## Out of Scope

- Site analytics (measure via service dashboards)
- Blog functionality
- E-commerce/payments
- User accounts
- CMS
- Full Adriana landing page
- Testimonials/client logos (no content available)
