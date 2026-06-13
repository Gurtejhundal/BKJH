# Design System

## Design Style

Use a mix of:

- Premium hospital brand
- Local practical hospital UX

The site should feel clean, trustworthy, calm, and modern. It should not feel like a cheap WordPress template or an AI-generated landing page.

## Visual Keywords

- Clean
- Trustworthy
- Modern
- Practical
- Calm
- Mobile-first
- Senior-built

## Color Direction

### Primary Palette

| Role | Color Direction | Usage |
|---|---|---|
| Base | White | Main background |
| Primary | Deep Blue | Header, CTAs, headings, trust sections |
| Accent | Soft Teal | Secondary CTAs, icons, badges |
| Surface | Light Grey | Cards, section backgrounds, forms |
| Text | Charcoal/Near Black | Main readable text |
| Muted Text | Slate Grey | Supporting copy |
| Alert | Controlled Red | Emergency-only usage |

### Suggested Tokens

```css
--color-primary: #0B3A64;
--color-primary-dark: #082B4A;
--color-accent: #1B9A8A;
--color-accent-soft: #E7F7F5;
--color-bg: #FFFFFF;
--color-surface: #F5F7FA;
--color-border: #E2E8F0;
--color-text: #172033;
--color-muted: #64748B;
--color-emergency: #B42318;
```

Do not overuse red. Red is only for emergency actions and warnings.

## Typography

Use a professional readable sans-serif.

Recommended options:

- Inter
- Manrope
- Source Sans 3
- Noto Sans

If Punjabi text is used, ensure the font supports Gurmukhi properly.

Suggested font stack:

```css
font-family: Inter, "Noto Sans Gurmukhi", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
```

## Layout Principles

### Desktop

- Wide but controlled max-width
- Strong whitespace
- Clear visual hierarchy
- No cluttered mega sections
- Action cards immediately visible

### Mobile

Mobile is the priority.

Rules:

- CTA buttons must be thumb-friendly.
- Emergency/call actions should not be buried.
- Text must not be too small.
- Cards must stack cleanly.
- Sticky bottom action bar should remain accessible.

## Button System

### Primary Button

Use for appointment request and major navigation.

Text examples:

- Book Appointment
- Request Appointment
- View Doctors

### Emergency Button

Use controlled red.

Text examples:

- Emergency Call
- Call Ambulance

### Secondary Button

Use outline or soft teal.

Text examples:

- View OPD Timing
- Get Directions
- Explore Departments

## Card Design

Use clean cards with:

- 16px to 24px padding
- Rounded corners, not excessive
- Subtle border
- Soft shadow only on interactive cards
- No heavy gradients
- Clear heading and short supporting text

Cards should look structured, not decorative.

## Animation Direction

Use light but smooth premium animation.

Allowed:

- Subtle fade-up on section entry
- Smooth hover lift on cards
- Soft counter reveal if needed
- Mobile menu transition
- Accordion transitions
- HTMX loading indicator

Avoid:

- Heavy parallax
- Excessive scroll effects
- Spinning icons
- Bouncy animations
- Cinematic hero effects
- Animations that delay information access

## Imagery Rules

Since real photos will come later:

- Use layout-friendly placeholders during development.
- Prefer icons/illustrations over fake stock doctors.
- Do not use random foreign hospital/doctor photos.
- All uploaded images should be optimized.
- All images need alt text.
- If no image exists, show a clean fallback block.

## Language Direction

Primary language: English.

Selective support: Punjabi microcopy for important patient actions.

Examples:

```text
Emergency Care Available
ਐਮਰਜੈਂਸੀ ਸੇਵਾ ਉਪਲਬਧ
```

```text
Book an Appointment
ਮੁਲਾਕਾਤ ਲਈ ਬੇਨਤੀ ਕਰੋ
```

Do not build full multilingual CMS in v1.

## Header Design

Desktop header:

- Hospital text/logo left
- Nav links center/right
- Emergency/Appointment CTA right

Mobile header:

- Logo/text left
- Menu button right
- Sticky bottom action bar for main actions

## Footer Design

Footer must include:

- Hospital name
- Address
- Phone numbers
- Emergency number
- Ambulance number
- Google Maps link
- Quick links
- OPD timing summary
- Basic copyright

## Senior Developer Design Rule

Every section must have a reason. If a section exists only to fill space, remove it.
