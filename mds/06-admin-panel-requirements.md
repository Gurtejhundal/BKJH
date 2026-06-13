# Admin Panel Requirements

## Admin Strategy

Use a hybrid admin approach:

1. Django Admin for content management
2. Custom appointment dashboard for hospital staff workflow

This gives fast development while keeping the client-facing admin experience clean enough.

## Admin User Roles

### Super Admin

Developer/owner role.

Can manage:

- Everything
- Users
- Site settings
- Content
- Appointments

### Hospital Admin

Hospital staff role.

Can manage:

- Doctors
- Departments
- OPD timings
- Gallery
- Appointment requests
- Notices
- Emergency/ambulance details

### Optional Staff Role

Can only view/update appointments.

Do not add complex role system unless needed.

## Manageable Content

Admin must be able to manage:

- Site settings
- Hospital information
- Doctors
- Departments
- Department details
- OPD timings
- Appointment requests
- Emergency details
- Ambulance details
- Gallery categories
- Gallery images
- Services
- Facilities
- Homepage notices
- Health camp updates

## Appointment Dashboard

Appointment fields:

- Patient name
- Phone number
- Department
- Preferred doctor
- Preferred date
- Preferred time/session
- Message
- Status
- Admin notes
- Created date
- Updated date

Statuses:

- Pending
- Contacted
- Confirmed
- Completed
- Cancelled

Admin actions:

- View appointment list
- Filter by status
- Filter by date
- Search by name/phone
- Update status
- Add internal note
- Export CSV optional later

## Django Admin Models

Register these models:

- SiteSetting
- Department
- Doctor
- OPDTiming
- AppointmentRequest
- GalleryCategory
- GalleryImage
- Service
- Facility
- Notice
- HealthCampUpdate
- EmergencyInfo
- AmbulanceInfo

## Admin UX Rules

- Use readable model names.
- Add list display fields.
- Add search fields.
- Add list filters.
- Add ordering.
- Use image preview where useful.
- Hide unpublished content from public site.
- Use `is_active` or `is_published` flags.

## Content Publishing Rules

Every public content model should have:

- title/name
- slug where needed
- short description
- detailed content where needed
- image optional
- display order
- active/published boolean
- created_at
- updated_at

## Appointment Notification

V1:

- Store appointment request in database.
- Show success message to patient.
- Admin manually handles follow-up.

Optional later:

- Email notification
- WhatsApp click-to-chat
- SMS/WhatsApp API

Do not promise automated SMS/WhatsApp in v1.

## Security Requirements

- Admin login protected.
- CSRF enabled.
- Strong password required.
- Admin URL can be customized.
- Forms validate server-side.
- File uploads restricted to images only.
- No public access to admin/dashboard.

## Admin Dashboard Sections

Recommended custom dashboard:

- Today’s appointment requests
- Pending requests
- Recent appointments
- Quick status update
- Contact numbers preview

Do not build large analytics charts in v1.

## Admin Simplicity Rule

Hospital staff should not need training longer than 15 minutes to update normal content.
