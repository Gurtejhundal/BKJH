# Testing, Security, and Launch Checklist

## Local Testing

Check:

- Homepage loads
- All nav links work
- All public pages load
- Department detail pages load
- Doctor cards show correctly
- OPD timings display correctly
- Appointment form submits
- Appointment appears in admin/dashboard
- Admin can update appointment status
- Gallery images load
- Contact/map links work
- Emergency/call buttons work

## Mobile Testing

Test on:

- Small Android width
- Large Android width
- iPhone-like width
- Tablet width

Check:

- Header/menu works
- Sticky bottom action bar works
- Buttons are large enough
- No horizontal scrolling
- Forms are usable
- OPD tables do not break layout
- Gallery grid works

## Browser Testing

Test:

- Chrome
- Edge
- Safari if possible
- Android Chrome

## Form Testing

Appointment form:

- Empty submission blocked
- Invalid phone blocked or handled
- Valid submission saved
- Success message shown
- CSRF token present
- Duplicate spam not easy

## Admin Testing

Check:

- Login required
- Normal user cannot access dashboard
- Admin can add doctor
- Admin can add department
- Admin can add OPD timing
- Admin can add gallery photo
- Admin can update appointment status
- Admin cannot accidentally publish incomplete content if `is_active=False`

## Security Checklist

Production settings:

```text
DEBUG=False
SECRET_KEY from environment
ALLOWED_HOSTS configured
CSRF_TRUSTED_ORIGINS configured
Database password strong
Admin password strong
SSL enabled
```

Django checks:

```bash
python manage.py check --deploy
```

## Static and Media Checklist

- Static files collected
- Media upload path works
- Images load in production
- Large images optimized
- Missing images show fallback

## SEO Basics

Each page should have:

- Title tag
- Meta description
- Clean URL
- H1
- Local hospital keywords naturally
- Address and phone visible
- Google Maps link

Suggested local SEO terms:

- Bibi Kaulan Ji Hospital
- hospital near [location]
- OPD consultation
- emergency service
- ambulance service
- doctors and departments

Do not keyword-stuff.

## Accessibility Basics

Check:

- Buttons have clear labels
- Images have alt text
- Color contrast is readable
- Forms have labels
- Keyboard navigation works reasonably
- Emergency buttons are obvious

## Performance Checklist

- Compress images
- Lazy-load gallery images
- Avoid heavy JS
- Avoid large animation libraries
- Use caching headers for static files
- Keep homepage lightweight

## Launch Checklist

Before launch:

- Client approves content
- Client verifies phone numbers
- Client verifies address/map
- Client verifies OPD timings
- Client verifies doctor names/qualifications
- Final payment received or payment terms locked
- Domain points to server
- SSL active
- Admin login created
- Backup plan created

## Post-Launch Checklist

After launch:

- Test contact links live
- Submit test appointment
- Check admin receives it
- Test mobile again
- Check SSL
- Check 404 page
- Check server logs
- Create initial backup

## Maintenance Suggestions

Monthly:

- Update dependencies carefully
- Backup database and media
- Check appointment form
- Check phone numbers/timings
- Review gallery storage

## Emergency Fix Priority

If something breaks, priority is:

1. Phone/emergency links
2. Appointment form
3. Admin access
4. OPD timings
5. Gallery/design polish

A medical website can survive a gallery bug. It cannot survive wrong emergency contact info.
