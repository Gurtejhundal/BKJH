# Development Phases

## Phase 0 — Project Setup

Tasks:

- Create GitHub repository
- Create Django project
- Add apps: core, hospital, appointments, gallery, dashboard
- Configure environment variables
- Add PostgreSQL support
- Add static/media settings
- Add base template structure
- Add Tailwind/CSS setup or structured CSS
- Add README setup instructions

Deliverable:

- Running Django project locally

## Phase 1 — Database and Admin Foundation

Tasks:

- Create models
- Create migrations
- Register models in Django admin
- Add admin list displays, filters, search
- Add image fields and upload paths
- Add active/published flags
- Add ordering

Deliverable:

- Admin can create departments, doctors, OPD timings, gallery, services, facilities, notices

## Phase 2 — Design System and Base Layout

Tasks:

- Build base layout
- Build header
- Build footer
- Build emergency strip
- Build mobile sticky action bar
- Define typography
- Define color tokens
- Build reusable buttons/cards
- Build responsive grid system

Deliverable:

- Design shell ready for all pages

## Phase 3 — Homepage

Tasks:

- Build mobile-first hero
- Add emergency and appointment CTA
- Add quick action cards
- Add about preview
- Add department preview
- Add doctors preview
- Add OPD preview
- Add emergency/ambulance block
- Add gallery preview
- Add contact/location preview

Deliverable:

- Homepage ready with real or placeholder content

## Phase 4 — Public Pages

Tasks:

- About page
- Departments listing
- Department detail page
- Doctors page
- OPD timing page
- Services page
- Facilities page
- Gallery page
- Emergency page
- Ambulance page
- Contact/location page

Deliverable:

- All public pages functional and responsive

## Phase 5 — Appointment System

Tasks:

- Create appointment form
- Validate form server-side
- Save appointment request
- Show success message
- Add admin view in Django admin
- Build custom appointment dashboard
- Add status update flow
- Add filters/search

Deliverable:

- Patient can submit request; admin can track and update status

## Phase 6 — Content Integration

Tasks:

- Add hospital name
- Add address/map
- Add contact numbers
- Add departments
- Add doctors
- Add OPD timings
- Add gallery photos
- Add services/facilities
- Add notices if any

Deliverable:

- Website has client-approved content

## Phase 7 — Polish and Senior-Level UI Pass

Tasks:

- Fix spacing
- Fix typography hierarchy
- Fix mobile layouts
- Remove generic text
- Add subtle animations
- Improve empty states
- Improve card consistency
- Optimize images
- Check real content layout

Deliverable:

- Website looks intentional, not AI-generated

## Phase 8 — Security and Testing

Tasks:

- Test forms
- Test admin permissions
- Test appointment status changes
- Test image uploads
- Test broken/empty data states
- Test mobile navigation
- Test emergency/call links
- Test map links
- Set DEBUG=False for production
- Check CSRF and allowed hosts

Deliverable:

- Site ready for deployment

## Phase 9 — Deployment

Tasks:

- Prepare VPS
- Install dependencies
- Configure PostgreSQL
- Configure Gunicorn
- Configure Nginx
- Configure domain
- Configure SSL
- Collect static files
- Run migrations
- Create superuser
- Test production

Deliverable:

- Live website on domain

## Phase 10 — Client Handover

Tasks:

- Give admin login
- Show how to add doctor
- Show how to update OPD timing
- Show how to check appointments
- Show how to add gallery photo
- Collect final payment before full handover
- Share basic maintenance notes

Deliverable:

- Client can operate basic admin features

## Timeline Estimate

For one developer:

- Basic working version: 7–10 days
- Polished version with admin: 14–21 days
- Depends heavily on client content speed

## Brutal Scope Warning

Do not start Phase 5 advanced booking/slots unless payment and scope are revised. Appointment request form is not the same as full booking engine.
