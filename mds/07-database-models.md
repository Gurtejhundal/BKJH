# Database Models

Database: PostgreSQL

Framework: Django ORM

## Model Design Principles

- Keep models simple.
- Use slugs for public detail pages.
- Add `is_active`/`is_published` flags.
- Add `display_order` for manual ordering.
- Add timestamps.
- Avoid over-normalization in v1.
- Do not model full hospital operations.

## Core Models

### SiteSetting

Stores global hospital information.

Fields:

- hospital_name
- short_tagline
- about_short
- address
- google_maps_url
- google_maps_embed_url
- main_phone
- emergency_phone
- ambulance_phone
- whatsapp_number
- email
- logo
- created_at
- updated_at

Use singleton pattern or limit to one active row.

### Department

Fields:

- name
- slug
- icon
- short_description
- detailed_description
- image
- services_list
- is_featured
- is_active
- display_order
- created_at
- updated_at

Relationships:

- Department has many Doctors
- Department has many OPDTimings

### Doctor

Fields:

- full_name
- slug optional but no public detail page in v1
- photo
- qualification
- specialization
- experience_years
- department ForeignKey
- short_bio optional
- opd_days_text
- opd_time_text
- appointment_enabled
- is_featured
- is_active
- display_order
- created_at
- updated_at

No separate doctor detail page in v1 unless explicitly added later.

### OPDTiming

Fields:

- department ForeignKey nullable
- doctor ForeignKey nullable
- days
- start_time
- end_time
- room_or_location
- notes
- is_active
- display_order
- created_at
- updated_at

### AppointmentRequest

Fields:

- patient_name
- phone
- department ForeignKey nullable
- preferred_doctor ForeignKey nullable
- preferred_date
- preferred_time_text
- message
- status
- admin_note
- created_at
- updated_at

Status choices:

- pending
- contacted
- confirmed
- completed
- cancelled

### GalleryCategory

Fields:

- name
- slug
- description
- is_active
- display_order
- created_at
- updated_at

### GalleryImage

Fields:

- category ForeignKey
- title
- image
- alt_text
- caption
- is_featured
- is_active
- display_order
- created_at
- updated_at

### Service

Fields:

- title
- slug
- short_description
- detailed_description
- icon
- image optional
- is_featured
- is_active
- display_order
- created_at
- updated_at

### Facility

Fields:

- title
- slug
- short_description
- detailed_description
- image
- is_featured
- is_active
- display_order
- created_at
- updated_at

### Notice

Fields:

- title
- message
- link_text optional
- link_url optional
- start_date optional
- end_date optional
- priority
- is_active
- created_at
- updated_at

Use notices for homepage alerts like camps, timing updates, or temporary announcements.

### HealthCampUpdate

Fields:

- title
- slug
- short_description
- detailed_description
- date
- image
- is_active
- display_order
- created_at
- updated_at

### EmergencyInfo

Fields:

- title
- emergency_phone
- availability_text
- description
- instructions
- is_active
- updated_at

### AmbulanceInfo

Fields:

- title
- ambulance_phone
- availability_text
- service_area
- description
- is_active
- updated_at

## Suggested Django App Structure

```text
apps/
  core/
    models.py        # SiteSetting, Notice
    views.py
  hospital/
    models.py        # Department, Doctor, OPDTiming, Service, Facility
    views.py
  appointments/
    models.py        # AppointmentRequest
    views.py
    forms.py
  gallery/
    models.py        # GalleryCategory, GalleryImage
    views.py
  dashboard/
    views.py         # Custom admin appointment dashboard
```

## Slug Rules

- Departments, services, facilities, and updates need slugs.
- Generate slug from title/name.
- Ensure unique slugs.

## Image Upload Rules

Upload paths:

```python
doctors/%Y/%m/
departments/%Y/%m/
gallery/%Y/%m/
facilities/%Y/%m/
services/%Y/%m/
```

Validation:

- Allow only image file types.
- Compress/resize images where practical.
- Add alt text field.

## Query Optimization

Use:

- `select_related` for doctor.department
- `prefetch_related` where needed
- Limit homepage queries to featured/active items

## Initial Seed Data

Use seed data only in development.

Do not publish fake doctors or fake emergency info.
