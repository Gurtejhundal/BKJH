from datetime import time
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from apps.core.models import SiteSetting
from apps.gallery.models import GalleryCategory, GalleryImage
from apps.gallery.hospital.models import (
    AmbulanceInfo,
    Department,
    Doctor,
    EmergencyInfo,
    Facility,
    OPDTiming,
    Service,
)


BASE_DIR = Path(__file__).resolve().parents[4]


def upsert(model, lookup, defaults):
    obj, _ = model.objects.get_or_create(**lookup, defaults=defaults)
    changed = False
    for field, value in defaults.items():
        if getattr(obj, field) != value:
            setattr(obj, field, value)
            changed = True
    if changed:
        obj.save()
    return obj


def lines(*items):
    return "\n".join(items)


class Command(BaseCommand):
    help = "Seed verified Bibi Kaulan Ji Hospital and Miri Piri Mission Hospital public website content."

    def handle(self, *args, **options):
        site = SiteSetting.objects.first() or SiteSetting()
        site.hospital_name = "Bibi Kaulan Ji Hospital"
        site.short_tagline = "Compassionate care, advanced treatments, and affordable support for families in Fatehgarh Churian."
        site.about_short = (
            "Bibi Kaulan Ji Hospital runs under Bibi Kaulan Ji Hospitals Charitable Society and serves "
            "patients around Fatehgarh Churian with emergency care, OPD consultation, dialysis support, "
            "specialist procedures, and cashless treatment support where applicable."
        )
        site.address = "Ajnala Road, Opp. Axis Bank, Fatehgarh Churian, Distt. Gurdaspur, Punjab"
        site.google_maps_url = "https://www.google.com/maps/search/?api=1&query=Bibi+Kaulan+Ji+Hospital+Ajnala+Road+Fatehgarh+Churian"
        site.google_maps_embed_url = "https://www.google.com/maps?q=Bibi%20Kaulan%20Ji%20Hospital%20Ajnala%20Road%20Fatehgarh%20Churian&output=embed"
        site.main_phone = "+91 79738 14987"
        site.emergency_phone = "+91 78886 96623"
        site.ambulance_phone = "+91 98782 11131"
        site.whatsapp_number = "+91 97805 15050"
        site.meta_title = "Bibi Kaulan Ji Hospital | 24x7 Emergency & Specialist Care in Fatehgarh Churian"
        site.meta_description = (
            "Bibi Kaulan Ji Hospital on Ajnala Road, Fatehgarh Churian provides emergency support, "
            "dialysis, OPD consultation, specialist procedures, doctors, and appointment requests."
        )
        site.save()

        Department.objects.filter(name__in=["Emergency Support", "OPD Consultation"]).update(is_active=False)
        Service.objects.filter(title="Free Dialysis Centre").update(title="Dialysis", slug="dialysis")
        Facility.objects.filter(title="Free Dialysis Centre").update(title="Dialysis", slug="dialysis")

        departments = [
            {
                "name": "Emergency Medicine",
                "short": "24x7 emergency response for urgent medical, trauma, poisoning, bite, cardiac, and respiratory cases.",
                "details": "Emergency Medicine handles urgent assessment, stabilization, and hospital emergency coordination.",
                "services": lines("Poisoning", "Accident and trauma cases", "Snake bite", "Cardiac emergencies", "Respiratory diseases", "CHF (Congestive Heart Failure)", "CVA (Stroke)", "24x7 emergency support"),
                "icon": "emergency",
                "scope": "both",
                "featured": True,
            },
            {
                "name": "Pulmonary Medicine",
                "short": "Chest, TB, bronchoscopy, sleep study, allergy, and respiratory intervention support.",
                "details": "Pulmonary Medicine supports chest and respiratory care, bronchoscopy, TB-related consultation, and selected interventions.",
                "services": lines("Splanchnic block", "Thoracoscopy", "Pediatric chest procedures", "Chest intervention", "CT-guided intervention", "Sleep study", "Smoking cessation", "Allergy clinic"),
                "icon": "lungs",
                "scope": "both",
                "featured": True,
            },
            {
                "name": "Pediatrics",
                "short": "Child health OPD, neonatal care, vaccination, growth, jaundice, and pediatric emergency support.",
                "details": "Pediatrics supports newborns, children, pediatric emergencies, and child development concerns.",
                "services": lines("NICU - Neonatal Intensive Care Unit", "PICU - Pediatric Intensive Care Unit", "Vaccinations", "Baby growth and development issues", "Phototherapy for newborn jaundice", "Bubble CPAP support", "24x7 pediatric emergency", "Neonatal care"),
                "icon": "child",
                "scope": "both",
                "featured": True,
            },
            {
                "name": "Orthopedics",
                "short": "Bone, joint, spine, trauma, ligament, arthroscopy, epidural, and tendon repair support.",
                "details": "Orthopedics covers fracture care, joint problems, spine issues, trauma, replacement surgeries, and follow-up rehabilitation planning.",
                "services": lines("Hip replacement", "Joint replacement", "Spine problems", "Trauma", "Ligament surgery", "Revision total hip replacement (THR)", "Arthroscopy", "Epidurals", "Tendon repairs"),
                "icon": "bone",
                "scope": "both",
                "featured": True,
            },
            {
                "name": "General Medicine",
                "short": "Adult OPD care for BP, thyroid, diabetes, liver, kidney, heart, and non-invasive cardiology concerns.",
                "details": "General Medicine handles common adult medical problems and long-term disease follow-up.",
                "services": lines("Hypertension", "Thyroid disorders", "Diabetes", "Liver cirrhosis", "AKI (Acute Kidney Injury)", "CAD (Coronary Artery Disease)", "CHF (Congestive Heart Failure)", "Non-invasive cardiology"),
                "icon": "medicine",
                "scope": "both",
                "featured": True,
            },
            {
                "name": "Urology",
                "short": "Urology OPD and procedure support including stones, prostate, bladder, and kidney-related procedures.",
                "details": "Urology supports consultation and procedures for urinary tract, bladder, prostate, kidney stones, and related concerns.",
                "services": lines("PCNL (Percutaneous Nephrolithotomy)", "URS (Ureteroscopy)", "Prostate surgery (TURP)", "Bladder incontinence", "Frequent urination issues", "Nephrectomy", "UVF / urethral-related procedure - confirm exact wording", "RIRS (Retrograde Intrarenal Surgery)"),
                "icon": "urology",
                "scope": "both",
                "featured": True,
            },
            {
                "name": "General Surgery",
                "short": "General operations including hernia, appendix, gallbladder, piles, thyroid, and similar surgical care.",
                "details": "General Surgery covers common planned and urgent surgical consultation and procedures.",
                "services": lines("Hernia surgery", "Appendix surgery", "Gallbladder surgery", "Piles treatment", "Thyroid surgery", "General surgical consultation"),
                "icon": "surgery",
                "scope": "both",
                "featured": True,
            },
            {
                "name": "Hip & Joint Replacement",
                "short": "Knee replacement, hip replacement, joint reconstruction, and arthritis surgery support.",
                "details": "Hip and joint replacement care supports patients with arthritis, severe joint pain, and replacement surgery planning.",
                "services": lines("Knee replacement", "Hip replacement", "Joint reconstruction", "Arthritis surgery", "Revision replacement consultation"),
                "icon": "bone",
                "scope": "both",
                "featured": True,
            },
            {
                "name": "Trauma & Accident Care",
                "short": "Emergency treatment for road accidents, fractures, and serious injuries.",
                "details": "Trauma and accident care supports emergency assessment and stabilization for injuries and fractures.",
                "services": lines("Road accident care", "Fracture care", "Serious injury stabilization", "Trauma emergency support"),
                "icon": "emergency",
                "scope": "both",
                "featured": True,
            },
            {
                "name": "Critical Care",
                "short": "ICU, ventilator support, and care for critically ill patients.",
                "details": "Critical Care supports patients requiring ICU-level monitoring, ventilator support, and urgent medical attention.",
                "services": lines("ICU care", "Ventilator support", "Critical patient monitoring", "Emergency critical care support"),
                "icon": "emergency",
                "scope": "both",
                "featured": True,
            },
            {
                "name": "Dermatology",
                "short": "Skin, hair, nail, allergy, STD, pigmentation, PRP, and laser procedure support.",
                "details": "Dermatology covers skin, hair, nail, allergy, cosmetic skin, and related OPD concerns.",
                "services": lines("Skin allergy", "STD (Sexually Transmitted Diseases)", "Pigmentation", "PRP (Platelet-Rich Plasma)", "Laser procedures"),
                "icon": "skin",
                "scope": "bkjh",
                "featured": False,
            },
            {
                "name": "Plastic Surgery",
                "short": "Tumor removal, VAC therapy, grafting, skin flaps, and reconstruction support.",
                "details": "Plastic Surgery supports reconstructive and wound-related procedures after hospital consultation.",
                "services": lines("Tumor removal", "Vacuum therapy / VAC", "Grafting", "Skin flaps", "Reconstruction"),
                "icon": "surgery",
                "scope": "both",
                "featured": True,
            },
            {
                "name": "Physiotherapy & Rehabilitation Services",
                "short": "Recovery after surgery, injury rehabilitation, pain relief, and mobility improvement.",
                "details": "Physiotherapy and rehabilitation services support recovery, movement, and pain-management plans.",
                "services": lines("Post-surgery recovery", "Injury rehabilitation", "Pain relief", "Mobility improvement"),
                "icon": "rehab",
                "scope": "bkjh",
                "featured": False,
            },
            {
                "name": "Dental & Implants",
                "short": "Dental treatments, root canal, braces, dental implants, and cosmetic dentistry.",
                "details": "Dental and implant services support oral health, dental restoration, and cosmetic dental treatment.",
                "services": lines("Dental treatment", "Root canal", "Braces", "Dental implants", "Cosmetic dentistry"),
                "icon": "dental",
                "scope": "bkjh",
                "featured": False,
            },
            {
                "name": "ENT",
                "short": "Ear, nose, and throat specialist consultation and treatment support.",
                "details": "ENT services cover specialist consultation for ear, nose, throat, and related concerns.",
                "services": lines("Ear consultation", "Nose consultation", "Throat consultation", "ENT specialist services"),
                "icon": "ent",
                "scope": "both",
                "featured": False,
            },
            {
                "name": "Gynecology",
                "short": "Women care and gynecology consultation support at Miri Piri Mission Hospital.",
                "details": "Gynecology supports women's health consultation and related OPD care at Miri Piri Mission Hospital.",
                "services": lines("Women health consultation", "Gynecology OPD", "Maternity-related consultation", "Follow-up care"),
                "icon": "gynecology",
                "scope": "miri",
                "featured": True,
            },
        ]

        department_map = {}
        for index, item in enumerate(departments, start=1):
            department_map[item["name"]] = upsert(
                Department,
                {"name": item["name"]},
                {
                    "short_description": item["short"],
                    "detailed_description": item["details"],
                    "services_list": item["services"],
                    "icon": item["icon"],
                    "hospital_scope": item["scope"],
                    "is_featured": item["featured"],
                    "is_active": True,
                    "display_order": index,
                    "seo_title": f"{item['name']} | Bibi Kaulan Ji Hospital",
                    "seo_description": f"{item['name']} services, doctors, OPD timing, and appointment support.",
                },
            )

        services = [
            ("24x7 Emergency", "Emergency support is available round the clock through the confirmed hospital emergency numbers.", "emergency", "both", 1),
            ("Dialysis", "Dialysis support is available as a key patient service.", "dialysis", "both", 2),
            ("Bronchoscopy", "Bronchoscopy support for chest and respiratory care.", "lungs", "both", 3),
            ("Pediatric Bronchoscopy", "Pediatric bronchoscopy support linked with child and respiratory care.", "child", "both", 4),
            ("Cystoscopy and Urology Procedures", "Cystoscopy and other urology procedure support.", "urology", "both", 5),
            ("Plastic Surgery", "Plastic surgery consultation and procedure support.", "surgery", "both", 6),
            ("Critical Care", "ICU, ventilator, and critical patient support.", "emergency", "both", 7),
            ("Cashless Treatment Support", "Empanelled with Ayushman Bharat, private and government insurance TPA for eligible cashless treatment.", "insurance", "bkjh", 8),
            ("Gynecology Care", "Women care and gynecology consultation support.", "gynecology", "miri", 9),
        ]
        for title, short, icon, scope, order in services:
            upsert(
                Service,
                {"title": title},
                {
                    "short_description": short,
                    "detailed_description": short,
                    "icon": icon,
                    "hospital_scope": scope,
                    "is_featured": True,
                    "is_active": True,
                    "display_order": order,
                    "seo_title": f"{title} | Hospital Service",
                    "seo_description": short,
                },
            )

        facilities = [
            ("Dialysis", "Dialysis support highlighted by the hospital.", "both", 1),
            ("Emergency Department", "Emergency access through the confirmed emergency numbers.", "both", 2),
            ("OPD Consultation Rooms", "Patient consultation rooms for visiting doctors and OPD care.", "both", 3),
            ("ICU and Critical Care", "Critical care and ICU support for seriously ill patients.", "both", 4),
            ("Reception and Waiting Area", "Patient reception and waiting support areas.", "both", 5),
            ("Ambulance Assistance", "24x7 assistance contact support for patients and attendants.", "both", 6),
        ]
        for title, short, scope, order in facilities:
            upsert(
                Facility,
                {"title": title},
                {
                    "short_description": short,
                    "detailed_description": short,
                    "hospital_scope": scope,
                    "is_featured": True,
                    "is_active": True,
                    "display_order": order,
                    "seo_title": f"{title} | Hospital Facility",
                    "seo_description": short,
                },
            )

        Doctor.objects.filter(full_name__in=["Dr. Manbir Verka", "Dr. Mandir Singh"]).update(is_active=False, is_featured=False)
        doctor_rows = [
            ("Dr. Kashish Gupta", "Facility Director", "", None, "", "", "bkjh", True, 1, "dr-kashish-gupta.jpg"),
            ("Dr. Gagandeep Kaur", "MBBS, MD, DNB (Pulmonary Medicine)", "Chest & TB", "Pulmonary Medicine", "Mon, Wed, Fri", "10:00 AM - 2:00 PM", "both", True, 2, "dr-gagandeep-kaur.jpg"),
            ("Dr. Mandeep", "", "Orthopedic", "Orthopedics", "Mon, Thu", "11:00 AM - 3:00 PM", "both", False, 3, ""),
            ("Dr. SS Kaler", "", "Dermatology", "Dermatology", "Thu", "3:00 PM - 5:00 PM", "bkjh", False, 4, ""),
            ("Dr. Shahzad", "", "General Medicine", "General Medicine", "Mon to Sat", "9:00 AM - 3:00 PM", "both", False, 5, ""),
            ("Dr. Manpreet", "", "General Medicine", "General Medicine", "Mon to Sat", "3:00 PM - 8:00 PM", "both", True, 6, ""),
            ("Dr. Navneet Kaur", "", "Dental", "Dental & Implants", "Mon to Sat", "10:00 AM - 4:00 PM", "bkjh", False, 7, ""),
            ("Dr. Amit Srivastava", "", "ENT / Eye", "ENT", "Mon to Sat", "10:00 AM - 4:00 PM", "both", False, 8, ""),
            ("Dr. Parneet", "", "Physiotherapy", "Physiotherapy & Rehabilitation Services", "Mon to Sat", "9:00 AM - 5:00 PM", "bkjh", False, 9, ""),
            ("Dr. Manbir Singh", "MBBS, MD (Paediatrics)", "Pediatrics", "Pediatrics", "Wed, Fri", "12:00 PM - 3:00 PM", "both", True, 10, "dr-manbir-singh.jpg"),
            ("Dr. Himanchu Lata", "", "Gynecology", "Gynecology", "Call to confirm", "Contact hospital", "miri", True, 11, ""),
        ]

        for full_name, qualification, specialization, department_name, days, timing, scope, featured, order, photo_name in doctor_rows:
            doctor = upsert(
                Doctor,
                {"full_name": full_name},
                {
                    "qualification": qualification,
                    "specialization": specialization,
                    "department": department_map.get(department_name) if department_name else None,
                    "opd_days_text": days,
                    "opd_time_text": timing,
                    "hospital_scope": scope,
                    "appointment_enabled": True,
                    "is_featured": featured,
                    "is_active": True,
                    "display_order": order,
                },
            )
            if photo_name and not doctor.photo:
                photo_path = BASE_DIR / "static" / "images" / "doctors" / photo_name
                if photo_path.exists():
                    with photo_path.open("rb") as handle:
                        doctor.photo.save(photo_name, File(handle), save=True)

        timings = [
            ("Dr. Gagandeep Kaur", "Pulmonary Medicine", "Mon, Wed, Fri", time(10, 0), time(14, 0), "both", 1),
            ("Dr. Mandeep", "Orthopedics", "Mon, Thu", time(11, 0), time(15, 0), "both", 2),
            ("Dr. SS Kaler", "Dermatology", "Thu", time(15, 0), time(17, 0), "bkjh", 3),
            ("Dr. Shahzad", "General Medicine", "Mon to Sat", time(9, 0), time(15, 0), "both", 4),
            ("Dr. Manpreet", "General Medicine", "Mon to Sat", time(15, 0), time(20, 0), "both", 5),
            ("Dr. Navneet Kaur", "Dental & Implants", "Mon to Sat", time(10, 0), time(16, 0), "bkjh", 6),
            ("Dr. Amit Srivastava", "ENT", "Mon to Sat", time(10, 0), time(16, 0), "both", 7),
            ("Dr. Parneet", "Physiotherapy & Rehabilitation Services", "Mon to Sat", time(9, 0), time(17, 0), "bkjh", 8),
            ("Dr. Manbir Singh", "Pediatrics", "Wed, Fri", time(12, 0), time(15, 0), "both", 9),
        ]
        doctor_map = {doctor.full_name: doctor for doctor in Doctor.objects.filter(full_name__in=[row[0] for row in timings])}
        for doctor_name, department_name, days, start, end, scope, order in timings:
            upsert(
                OPDTiming,
                {"doctor": doctor_map[doctor_name], "days": days},
                {
                    "department": department_map[department_name],
                    "start_time": start,
                    "end_time": end,
                    "room_or_location": "OPD",
                    "notes": "Timing from supplied hospital team schedule reference.",
                    "hospital_scope": scope,
                    "is_active": True,
                    "display_order": order,
                },
            )

        upsert(
            EmergencyInfo,
            {"title": "24x7 Emergency"},
            {
                "emergency_phone": "+91 78886 96623",
                "availability_text": "24x7 emergency assistance",
                "description": "Emergency contacts: +91 78886 96623 and +91 97805 15050. Main hospital number: +91 79738 14987.",
                "instructions": "For urgent symptoms, call emergency support immediately. 24x7 assistance: +91 98782 11131.",
                "is_active": True,
            },
        )
        upsert(
            AmbulanceInfo,
            {"title": "24x7 Assistance"},
            {
                "ambulance_phone": "+91 98782 11131",
                "availability_text": "24x7 assistance",
                "service_area": "Fatehgarh Churian and nearby areas",
                "description": "24x7 assistance contact support for patients and attendants.",
                "is_active": True,
            },
        )

        self.seed_gallery()
        self.stdout.write(self.style.SUCCESS("Hospital website content seeded."))

    def seed_gallery(self):
        category = upsert(
            GalleryCategory,
            {"name": "Hospital Photos"},
            {"description": "Approved real hospital interior and facility photos.", "is_active": True, "display_order": 1},
        )
        photos = [
            ("Reception", "bkjh-gallery-reception.jpg", "Reception and patient support desk", 1),
            ("Waiting Area", "bkjh-gallery-waiting-area.jpg", "Patient waiting area", 2),
            ("Patient Care Beds", "bkjh-gallery-patient-care-beds.jpg", "Patient care bed area", 3),
            ("Dialysis Support", "bkjh-gallery-dialysis-support.jpg", "Dialysis and patient care equipment", 4),
        ]
        for title, filename, alt, order in photos:
            image = upsert(
                GalleryImage,
                {"title": title},
                {
                    "category": category,
                    "alt_text": alt,
                    "caption": alt,
                    "is_featured": True,
                    "is_active": True,
                    "display_order": order,
                },
            )
            if not image.image:
                photo_path = BASE_DIR / "static" / "images" / "hospital" / filename
                if photo_path.exists():
                    with photo_path.open("rb") as handle:
                        image.image.save(filename, File(handle), save=True)
