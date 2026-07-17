# BKGH Hospitals Public Design System

## Product And Users

BKGH Hospitals is a parent healthcare gateway for two hospital websites. Patients must first understand whether they are on the network page, Bibi Kaulan Ji Hospital, or Miri Piri Mission Hospital, then reach the correct phone, location, OPD, doctor, or service information with minimal scanning.

## Design Objective

Create three distinct but related experiences without changing the established routes or Django content model:

- BKGH parent: calm institutional hospital selector.
- Bibi Kaulan Ji Hospital: practical community hospital with strong emergency and OPD access.
- Miri Piri Mission Hospital: separate mission-hospital identity focused on Amritsar, OPD, critical care, and gynecology support.

## Style Direction

Primary style: restrained Flat Design 2.0.

Secondary influence: minimalist institutional editorial layout. Depth comes from borders, spacing, and limited shadows rather than gradients, glass effects, decorative shapes, or nested cards.

## Identity Themes

### BKGH Parent

- Primary: `#183247` deep navy.
- Primary dark: `#102534`.
- Accent: `#39715f` muted emerald.
- Background: `#fbfaf6` ivory.
- Surface: `#f2f4ef`.
- Emergency: `#d9272e` only for urgent contact.
- Motif: two connected hospital identities and location guidance.

### Bibi Kaulan Ji Hospital

- Primary: `#006b54` hospital green.
- Primary dark: `#004233`.
- Accent: `#168f7b`.
- Background: `#ffffff`.
- Surface: `#f2faf7`.
- Emergency: `#e11d24`.
- Motif: direct patient actions, OPD utility, community access.

### Miri Piri Mission Hospital

- Primary: `#0d5961` deep teal.
- Primary dark: `#173747` navy teal.
- Accent: `#b66442` warm clay.
- Accent soft: `#f6e8de`.
- Background: `#fffdf8` ivory.
- Surface: `#f3f7f5`.
- Emergency: `#d9272e`.
- Motif: logo-led mission identity, warm section dividers, Amritsar location.

## Shared Foundations

- Typeface: Inter for English and Noto Sans Gurmukhi for Punjabi.
- Body: 16px minimum on desktop and mobile, 1.55-1.65 line height.
- Display headings: responsive `clamp()` sizes, no viewport-width-only scaling.
- Content width: maximum 1440px with fluid side padding.
- Spacing: 4, 8, 12, 16, 24, 32, 48, 64.
- Radius: 6px controls, 8px cards, 12px only for flagship hospital selectors.
- Borders: one-pixel neutral or theme-tinted borders.
- Shadows: limited to navigation and flagship selectors; no floating section cards.
- Icons: existing single-stroke icon partial only.
- Buttons: minimum 44px touch height, primary/secondary/emergency hierarchy.

## Components

### Header

- Parent uses the approved Bibi Kaulan Ji logo with the text `BKGH Hospitals`.
- Parent navigation contains only Hospitals, About, and Contact.
- Hospital headers use their own names, logos, navigation, and theme colors.
- Mobile navigation remains a menu sheet with 44px links and visible focus.

### Parent Hero

- Editorial two-column layout, not a hospital marketing hero.
- Left: network statement and three actions.
- Right: compact two-campus network visual using both real logos.
- No doctors, OPD table, department grid, or fabricated photography.

### Flagship Hospital Selectors

- Two equal-height cards with distinct accent rails.
- Clear location, verified highlights, and three actions.
- BKJH card uses green; Miri card uses teal with clay detail.
- Cards remain one column on mobile with full-width primary actions.

### Hospital Detail Pages

- BKJH preserves green/mint and prioritizes emergency, appointments, doctors, and timings.
- Miri uses a logo-led hero, teal/navy surfaces, clay labels, and different section composition.
- Empty homepage sections are hidden. Detail pages use patient-facing empty guidance only.

### CMS

- Hospital ownership is always visible.
- New clinical content defaults to BKJH, never shared.
- Shared content must be selected intentionally.
- Cross-hospital doctor, department, OPD, gallery, and appointment relationships are validated.
- Appointments expose hospital source and status.

## Interaction And Motion

- 160-240ms transitions for color, border, and small vertical movement.
- Reveal motion uses opacity and transform only.
- No scroll-jacking, parallax, or decorative continuous animation.
- `prefers-reduced-motion` removes reveals and movement.

## Accessibility

- WCAG 2.2 AA contrast target.
- Visible `:focus-visible` treatment using the active theme color.
- Logical heading order and semantic sections.
- Meaningful image alt text is mandatory in CMS-managed galleries.
- Emergency links remain text-labelled, not icon-only.
- Mobile targets are at least 44 by 44 CSS pixels.

## Responsive Rules

- 360-767px: single-column heroes and cards, full-width primary actions, compact top strip.
- 768-1023px: two-column utility grids only where content remains readable.
- 1024px and above: parent and Miri heroes use two columns; flagship selectors are equal-height pairs.
- No page-level horizontal overflow.
- Sticky headers must not cover section anchors.

## Forbidden Patterns

- Parent page styled as a copy of BKJH.
- Admin, approval, pending-entry, or content-policy wording on public pages.
- Empty review or gallery announcements on hospital homepages.
- Fake statistics, awards, claims, reviews, or department imagery.
- Shared hospital content by default.
- Large gradients, decorative blobs, excessive pill labels, or cards inside cards.

## QA Checklist

- Verify `/`, `/bibi-kaulan-ji-hospital/`, and `/miri-piri-mission-hospital/` at 360, 390, 768, 1024, and 1440 widths.
- Confirm theme and header/footer identity differ on all three routes.
- Confirm all hospital phone and map actions use the correct profile.
- Confirm inactive and wrong-scope content is absent.
- Confirm appointments save the selected hospital source.
- Confirm no internal CMS wording appears publicly.
- Run Django tests, checks, migration checks, keyboard navigation, console review, and overflow checks.
