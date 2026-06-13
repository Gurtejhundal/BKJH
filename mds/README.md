# Bibi Kaulan Ji Hospital Website — MD Pack

This folder contains the planning documents for a production-ready hospital website built with the **Modern Monolith** approach:

- Python
- Django
- PostgreSQL
- Django Templates
- HTMX
- Alpine.js
- Optional Redis later
- Hostinger VPS deployment

The goal is not to build a generic AI-looking hospital template. The goal is to build a clean, mobile-first, trustworthy local hospital website that feels like it was planned and executed by a senior developer.

## Core Decision

This project is a **hospital website with admin control**, not a full hospital management system.

Included:

- Public website pages
- Doctors, departments, OPD timings
- Appointment request form
- Emergency and ambulance visibility
- Gallery
- Admin management for main content
- Mobile-first UX
- Basic SEO and security hygiene

Not included in v1:

- Patient medical records
- Lab report portal
- Payment gateway
- SMS/WhatsApp API automation
- Doctor slot engine
- Pharmacy/inventory system
- Full HMS/ERP

## Recommended Build Order

1. Read `01-project-overview.md`
2. Read `02-design-system.md`
3. Read `03-global-hospital-reference-analysis.md`
4. Build public pages from `04-pages-and-sections.md`
5. Collect real content using `05-content-requirements.md`
6. Build admin scope from `06-admin-panel-requirements.md`
7. Build database from `07-database-models.md`
8. Follow architecture in `08-technical-architecture.md`
9. Execute phases in `09-development-phases.md`
10. Deploy using `10-deployment-hostinger-vps.md`
11. Protect scope using `11-scope-payment-boundaries.md`
12. Use `12-senior-developer-quality-bar.md` before showing client
13. Use `13-testing-security-launch-checklist.md` before going live

## Design Summary

- Style: clean premium local hospital website
- Colors: white, deep blue, soft teal, light grey
- Language: English with selective Punjabi support lines
- UX: mobile-first
- Animation: light, smooth, premium, never distracting
- Admin: Django Admin plus custom appointment dashboard
- Departments: cards first, clickable detail pages
- Doctors: clean cards, no separate doctor pages in v1
- Gallery: category-based grid

## Important Warning

Do not start adding random advanced modules to impress the client. The site must be polished, stable, and easy for the hospital staff to manage. Over-engineering will kill the project.


## Added SEO File

- `14-seo-local-search-optimization.md` — dedicated SEO, local search, metadata, structured data, sitemap, robots.txt, Search Console, and launch checklist for the hospital website.
