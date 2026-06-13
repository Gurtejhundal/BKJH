# Codex Master Prompt — Hospital Website Build

You are building a production-quality hospital website for **Bibi Kaulan Ji Hospital** using Django, PostgreSQL, Django Templates, HTMX, Alpine.js, and mobile-first responsive design.

This is not a generic template project. Do not produce an AI-looking website with repetitive cards, fake medical stock-photo energy, random gradients, or overused landing page patterns.

## Product Type

Build a **hospital website with admin control**, not a hospital management system.

The website must help real local patients quickly do these things:

- Know what the hospital offers
- Check departments
- Check doctors
- Check OPD timings
- Request an appointment
- Call emergency service
- Call ambulance
- View gallery/facilities
- Find the location on Google Maps

The admin must be able to manage the important public-facing content without touching code.

## Required Stack

- Python
- Django
- PostgreSQL
- Django Templates
- HTMX for partial updates where useful
- Alpine.js for small UI interactions
- Tailwind CSS or carefully structured CSS utility system
- Django Admin for content management
- Custom admin/dashboard screen for appointment requests
- Hostinger VPS deployment path

Redis is optional and should not be added in v1 unless there is a real need.

## Design Direction

Use a clean premium local hospital design:

- White base
- Deep blue primary color
- Soft teal accent
- Light grey surfaces
- Strong readability
- Calm spacing
- Trustworthy tone
- Smooth light animation
- Mobile-first layout

Do not use:

- Heavy cinematic hero animation
- Fake-looking doctors/photos
- Bright random gradients
- Overloaded glassmorphism
- Dark UI for main website
- Excessive hover effects
- Tiny text
- Generic AI-written medical claims

## Hero Reference Direction

Take structural inspiration from global hospital websites:

- Mayo Clinic: clear request appointment, find doctor, locations, departments/patient guidance style
- Cleveland Clinic: prominent find doctor, locations, appointment/access actions
- Apollo Hospitals: book appointment, find doctors, specialties, emergency/contact visibility
- Fortis Healthcare: doctor discovery, appointment flow, hospital/location trust points

Do not copy their design. Use the same UX principle: immediate patient actions first.

## Homepage Priority

Mobile and desktop homepage must prioritize:

1. Hospital name and trust line
2. Emergency call
3. Appointment request
4. OPD timing
5. Location/map
6. Doctors and departments
7. Ambulance service
8. Gallery/facilities

## Mobile Bottom Action Bar

On mobile, implement a sticky bottom action bar:

- Call
- Appointment
- Location
- Emergency

This must be visible, simple, and fast.

## Pages

Build:

- Home
- About Hospital
- Departments listing
- Department detail page
- Doctors
- OPD Timing
- Appointment
- Emergency Service
- Ambulance
- Gallery
- Services
- Facilities
- Contact / Location
- Privacy / Terms basic pages if needed

## Admin Capabilities

Admin should manage:

- Doctors
- Departments
- Department detail content
- OPD timings
- Appointment requests and statuses
- Gallery categories and photos
- Emergency numbers
- Ambulance details
- Homepage notices
- Services
- Facilities
- About page content

Appointment statuses:

- Pending
- Contacted
- Confirmed
- Completed
- Cancelled

## Quality Rules

Every page must satisfy:

- Looks professional without requiring final photos
- Works well on mobile first
- Clear CTA above the fold
- No Lorem Ipsum in final visible UI
- No fake claims like “world-class” unless client provides proof
- No broken admin flows
- All images have fallbacks
- Forms validate properly
- Admin actions are protected
- Site remains usable if client provides incomplete content

## Tone

Use human, professional medical wording:

- Clear
- Local
- Trustworthy
- Direct

Example tone:

> Trusted hospital care for families, OPD consultation, emergency support, and essential medical services.

Selective Punjabi support lines are allowed for key patient-facing actions:

> Emergency Care Available  
> ਐਮਰਜੈਂਸੀ ਸੇਵਾ ਉਪਲਬਧ

Do not make the entire site multilingual in v1.

## Final Output Expected

Build a clean, working Django project with:

- Structured apps
- Database models
- Admin registration
- Public routes
- Responsive templates
- Form handling
- Appointment dashboard
- Deployment readiness
- Seed/demo content for development only
- Clean README for setup

## Non-Negotiable

This website must look like it was designed intentionally, not assembled from generic AI sections.


## SEO Execution Requirement
Read `14-seo-local-search-optimization.md` before implementing public templates. The site must include page-level metadata, clean URLs, sitemap.xml, robots.txt, canonical URLs, Hospital/LocalBusiness JSON-LD, mobile-first performance rules, and Google Search Console readiness. Do not treat SEO as an afterthought.
