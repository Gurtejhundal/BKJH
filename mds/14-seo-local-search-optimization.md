# 14 - SEO & Local Search Optimization

## Purpose
This file defines the search engine optimization plan for the hospital website. The goal is not fake ranking tricks. The goal is to make the hospital easy to discover when local patients search for the hospital name, departments, doctors, OPD timing, emergency care, ambulance support, and location.

This website is for a local hospital, so the SEO strategy must prioritize:

- Local search visibility
- Mobile search experience
- Clear hospital identity
- Accurate contact and location data
- Fast pages
- Proper metadata
- Structured data
- Search Console indexing
- Google Business Profile consistency

## Hard Rule
Do not write exaggerated medical claims.

Avoid:

- "Best hospital in Punjab" unless legally/officially proven
- "100% cure"
- "Guaranteed treatment"
- Fake reviews
- Fake doctor credentials
- Keyword stuffing
- Stock-photo-driven trust manipulation

Use factual, clean wording only.

---

## Primary Local SEO Targets

### Branded Searches
The website must rank clearly for:

- Bibi Kaulan Ji Hospital
- Bibi Kaulan Hospital
- Bibi Kaulan Ji Hospital Amritsar
- Bibi Kaulan Ji Hospital location
- Bibi Kaulan Ji Hospital OPD timing
- Bibi Kaulan Ji Hospital doctors
- Bibi Kaulan Ji Hospital appointment

### Service Searches
Target pages should naturally support:

- Hospital near me
- Hospital in Amritsar
- Emergency hospital in Amritsar
- Ambulance service in Amritsar
- OPD hospital in Amritsar
- Doctor consultation in Amritsar
- Medical departments in Amritsar

Do not overuse these phrases. Use them naturally in page headings, body copy, title tags, and meta descriptions.

---

## Page URL Structure

Use clean, stable, readable URLs.

| Page | URL |
|---|---|
| Home | `/` |
| About | `/about/` |
| Departments | `/departments/` |
| Department Detail | `/departments/<slug>/` |
| Doctors | `/doctors/` |
| OPD Timing | `/opd-timing/` |
| Appointment | `/appointment/` |
| Emergency | `/emergency/` |
| Ambulance | `/ambulance/` |
| Gallery | `/gallery/` |
| Contact | `/contact/` |
| Health Updates | `/updates/` |
| Health Update Detail | `/updates/<slug>/` |

Rules:

- Use lowercase slugs.
- Use hyphens, not underscores.
- Never expose database IDs in public URLs.
- Keep old URLs redirected if changed later.

---

## Page Metadata Requirements

Every public page must define:

- `<title>`
- `<meta name="description">`
- canonical URL
- Open Graph title
- Open Graph description
- Open Graph image where relevant
- Twitter card metadata
- index/follow robots directive unless intentionally hidden

### Recommended Title Pattern

Use this structure:

```text
Primary Page Topic | Bibi Kaulan Ji Hospital
```

Examples:

```text
Departments | Bibi Kaulan Ji Hospital
OPD Timing | Bibi Kaulan Ji Hospital
Emergency Service | Bibi Kaulan Ji Hospital
```

For homepage:

```text
Bibi Kaulan Ji Hospital | Healthcare, OPD & Emergency Services
```

### Recommended Meta Description Style

Keep descriptions human and specific.

Example homepage description:

```text
Bibi Kaulan Ji Hospital provides OPD consultation, emergency care, ambulance support, doctor information, departments, and appointment assistance for patients and families.
```

Example OPD page description:

```text
Check OPD timings, doctor availability, departments, and appointment information for Bibi Kaulan Ji Hospital.
```

---

## Homepage SEO Structure

The homepage must have only one H1.

Recommended H1:

```text
Bibi Kaulan Ji Hospital
```

Recommended section hierarchy:

```text
H1: Bibi Kaulan Ji Hospital
H2: Emergency Care and Ambulance Support
H2: OPD Timing and Doctor Consultation
H2: Departments
H2: Doctors
H2: Hospital Facilities
H2: Location and Contact
```

Do not use headings only for styling. Use headings for real content hierarchy.

---

## Department Page SEO

### Departments Listing Page

Purpose: show all departments in card layout.

Each department card should include:

- Department name
- Short description
- Relevant icon or image
- Link to detail page

### Department Detail Page

Each department detail page should include:

- Department name as H1
- Clear description
- Services/treatments provided
- Available doctors if mapped
- OPD timing if available
- Appointment CTA
- Emergency note if relevant

Example title:

```text
General Medicine Department | Bibi Kaulan Ji Hospital
```

Example meta description:

```text
Learn about the General Medicine department, available doctors, OPD timing, and appointment support at Bibi Kaulan Ji Hospital.
```

---

## Doctors SEO

Doctor cards should be crawlable HTML, not only JavaScript-rendered content.

Each doctor card should include:

- Doctor name
- Qualification
- Specialization
- OPD days
- OPD timing
- Appointment CTA

Do not create separate doctor pages unless the client provides enough real information. Thin doctor pages are worse than strong doctor cards.

If doctor detail pages are added later, they must include:

- Real qualification
- Registration number if available
- Specialization
- OPD availability
- Department connection
- Appointment CTA
- No fake achievements

---

## Local Business / Hospital Structured Data

Add JSON-LD structured data on the homepage. Use `Hospital` where appropriate, with local business fields.

Template:

```json
{
  "@context": "https://schema.org",
  "@type": "Hospital",
  "name": "Bibi Kaulan Ji Hospital",
  "url": "https://example.com/",
  "telephone": "+91-XXXXXXXXXX",
  "image": "https://example.com/static/images/hospital-og.jpg",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Add full street address here",
    "addressLocality": "Amritsar",
    "addressRegion": "Punjab",
    "postalCode": "Add PIN code here",
    "addressCountry": "IN"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 31.8592837,
    "longitude": 74.9525495
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
      "opens": "09:00",
      "closes": "17:00"
    }
  ],
  "sameAs": [
    "Add Google Maps / Business Profile link here",
    "Add Facebook page if official",
    "Add Instagram page if official"
  ]
}
```

Rules:

- Replace placeholder URL, phone, address, and timings.
- Do not add fake social links.
- Keep schema data identical to visible page content.
- If 24/7 emergency is true, mention emergency hours separately and visibly.

---

## Google Business Profile Consistency

The hospital website must match the Google Business Profile exactly for:

- Hospital name
- Address
- Main phone number
- Emergency phone number
- Opening hours
- Website URL
- Map location

This is NAP consistency:

```text
Name
Address
Phone
```

Do not write the hospital name differently across pages.

Bad:

```text
Bibi Kaulan Hospital
Bibi Kaulan Ji Hosp.
Bibi Kaulan Ji Charitable Hospital
```

Good:

```text
Bibi Kaulan Ji Hospital
```

Use one official name everywhere unless the client confirms otherwise.

---

## Technical SEO Requirements

### Sitemap

Generate `/sitemap.xml`.

It must include:

- Homepage
- About
- Departments
- Department detail pages
- Doctors
- OPD Timing
- Appointment
- Emergency
- Ambulance
- Gallery
- Contact
- Updates if enabled

In Django, use `django.contrib.sitemaps`.

### Robots File

Create `/robots.txt`.

Recommended:

```txt
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /dashboard/
Disallow: /accounts/

Sitemap: https://example.com/sitemap.xml
```

Do not block static files.

### Canonical URLs

Every page should include canonical URL:

```html
<link rel="canonical" href="https://example.com/current-page/">
```

Use HTTPS canonical URLs only after final domain is live.

### Redirects

- Force HTTPS.
- Redirect non-www to www or www to non-www. Choose one and keep it consistent.
- Redirect trailing slash consistently.

Recommended:

```text
https://domain.com/
```

without `www`, unless the client specifically wants `www`.

---

## Performance SEO

Mobile users are the priority.

Targets:

- Largest Contentful Paint under 2.5s where possible
- Avoid layout shift
- Compress images
- Use modern image formats where possible
- Lazy-load gallery images
- Keep CSS lean
- Keep JavaScript minimal
- Do not add animation libraries unless needed

Image handling:

- Use responsive image sizes.
- Compress uploaded gallery images.
- Generate thumbnails.
- Do not load full-size images in cards.
- Use descriptive alt text.

Bad alt text:

```text
image1
photo
hospital
```

Good alt text:

```text
Main entrance of Bibi Kaulan Ji Hospital
OPD waiting area at Bibi Kaulan Ji Hospital
Ambulance service at Bibi Kaulan Ji Hospital
```

---

## Content SEO Rules

Each page needs real content. Empty pages damage quality.

Minimum content expectations:

| Page | Minimum Content |
|---|---|
| Home | 300-500 words distributed across sections |
| About | 400-700 words |
| Departments | 100-150 words intro + department cards |
| Department Detail | 250-500 words per department |
| Doctors | Real doctor details, not fake filler |
| OPD Timing | Clear table + contact CTA |
| Emergency | Emergency number, process, location, ambulance support |
| Ambulance | Availability, contact number, service area if known |
| Contact | Address, phone, map, WhatsApp, route CTA |

Avoid generic filler like:

```text
We provide world-class healthcare with advanced technology and compassionate doctors.
```

Use specific local wording:

```text
Bibi Kaulan Ji Hospital provides OPD consultation, emergency support, ambulance assistance, and department-wise doctor information for patients and families visiting the hospital.
```

---

## Search-Friendly UI Rules

Do:

- Use real HTML links.
- Use server-rendered Django templates.
- Keep important content visible without requiring JavaScript.
- Use descriptive button text.

Avoid:

- Hiding important content inside animation-only components.
- Loading doctor/department data only after frontend JavaScript.
- Using vague CTA text everywhere.

Bad CTA:

```text
Click Here
Read More
Submit
```

Good CTA:

```text
Book Appointment
View OPD Timing
Call Emergency Number
View Department Details
Get Directions
```

---

## Google Search Console Setup

After deployment:

1. Add domain property to Google Search Console.
2. Verify domain using DNS TXT record.
3. Submit sitemap URL.
4. Request indexing for homepage.
5. Check indexing coverage.
6. Monitor mobile usability.
7. Check page experience issues.
8. Check manual actions/security issues.

Do not skip this. A website without Search Console is blind.

---

## Analytics Setup

Install one analytics tool:

Recommended:

- Google Analytics 4
- Or Plausible / Umami if privacy-focused analytics is preferred

Track:

- Appointment form submissions
- Click-to-call clicks
- WhatsApp clicks
- Google Maps direction clicks
- Emergency number clicks
- Department page views

Do not collect patient medical details in analytics.

---

## Appointment Form SEO + Privacy Boundary

Appointment forms should not ask for sensitive medical history in v1.

Allowed fields:

- Name
- Phone
- Department
- Preferred doctor if available
- Preferred date
- Message / reason for visit

Avoid:

- Aadhaar number
- Diagnosis
- Detailed medical history
- Prescription upload
- Report upload

If medical records are collected later, the project becomes more serious from privacy/security perspective.

---

## Local Landing Pages

Do not create fake city/location pages.

Bad:

```text
Hospital in Delhi
Hospital in Mumbai
Hospital in Ludhiana
```

Only create local pages if the hospital actually serves/has presence there.

Acceptable:

```text
Hospital in Amritsar
Emergency Hospital in Amritsar
Ambulance Service in Amritsar
```

Even these should be integrated naturally, not spam pages.

---

## Social Sharing Preview

Every main page should have Open Graph metadata.

Example:

```html
<meta property="og:title" content="Bibi Kaulan Ji Hospital | Healthcare, OPD & Emergency Services">
<meta property="og:description" content="Find doctors, departments, OPD timing, emergency support, ambulance contact, and appointment information.">
<meta property="og:image" content="https://example.com/static/images/og/hospital-home.jpg">
<meta property="og:url" content="https://example.com/">
<meta property="og:type" content="website">
```

Use real hospital images once available.

---

## SEO Checklist Before Launch

- [ ] Final domain connected
- [ ] HTTPS working
- [ ] Sitemap generated
- [ ] Robots.txt added
- [ ] Google Search Console verified
- [ ] Sitemap submitted
- [ ] Homepage has one H1
- [ ] All pages have unique titles
- [ ] All pages have unique meta descriptions
- [ ] LocalBusiness/Hospital schema added
- [ ] Contact details visible on every page footer
- [ ] Google Map embedded on contact page
- [ ] Mobile bottom action bar added
- [ ] Images compressed
- [ ] Gallery images lazy-loaded
- [ ] Broken links checked
- [ ] 404 page created
- [ ] Admin/private pages noindexed or blocked properly
- [ ] Appointment form tested
- [ ] Emergency number click tested on mobile
- [ ] WhatsApp link tested
- [ ] Map direction link tested

---

## SEO Implementation Notes For Django

Create reusable SEO context fields.

Recommended pattern:

```python
seo = {
    "title": "Departments | Bibi Kaulan Ji Hospital",
    "description": "Explore departments, doctors, OPD timing, and appointment support at Bibi Kaulan Ji Hospital.",
    "canonical_path": request.path,
    "og_image": "images/og/default-hospital.jpg",
}
```

In `base.html`:

```html
<title>{{ seo.title }}</title>
<meta name="description" content="{{ seo.description }}">
<link rel="canonical" href="{{ request.scheme }}://{{ request.get_host }}{{ seo.canonical_path }}">
```

For department detail pages, use model fields:

```python
class Department(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    short_description = models.TextField()
    full_description = models.TextField(blank=True)
    seo_title = models.CharField(max_length=160, blank=True)
    seo_description = models.CharField(max_length=300, blank=True)
```

If `seo_title` is blank, generate default title from department name.

---

## Senior Developer Rule

SEO must be part of the codebase, not a last-minute plugin.

Build SEO into:

- URL design
- Django models
- template blocks
- metadata system
- sitemap
- robots.txt
- image upload handling
- admin content fields
- performance budget
- launch checklist

If SEO is added only at the end, it will look patched and weak.
