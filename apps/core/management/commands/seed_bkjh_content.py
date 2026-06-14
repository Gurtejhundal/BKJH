from datetime import time
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from apps.core.models import SiteSetting
from apps.hospital.models import (
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


class Command(BaseCommand):
    help = "Seed verified Bibi Kaulan Ji Hospital public website content from supplied hospital references."

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
        site.main_phone = "+91 97805 15050"
        site.emergency_phone = "+91 97805 15050"
        site.ambulance_phone = "+91 97815 15050"
        site.whatsapp_number = "+91 97805 15050"
        site.meta_title = "Bibi Kaulan Ji Hospital | 24x7 Emergency & Specialist Care in Fatehgarh Churian"
        site.meta_description = (
            "Bibi Kaulan Ji Hospital on Ajnala Road, Fatehgarh Churian provides 24x7 emergency support, "
            "free dialysis centre, OPD consultation, specialist procedures, doctors, and appointment requests."
        )
        site.save()

        departments = [
            ("Emergency Medicine", "24x7 emergency response and urgent hospital contact support.", "Emergency care\nUrgent assessment\nStabilization support", "+", True, 1),
            ("Pulmonary Medicine", "Chest, TB, bronchoscopy, and respiratory consultation support.", "Chest and TB OPD\nBronchoscopy\nPaediatric bronchoscopy support", "+", True, 2),
            ("Pediatrics", "Child health OPD and paediatric consultation support.", "Child OPD\nPaediatric care\nPaediatric bronchoscopy support", "+", True, 3),
            ("Orthopedics", "Bone, joint, injury, and orthopedic consultation support.", "Bone and joint care\nInjury consultation\nOrthopedic OPD", "+", True, 4),
            ("General Medicine", "General medicine OPD for common adult health concerns.", "General OPD\nBP and sugar care\nFollow-up consultation", "+", True, 5),
            ("Urology", "Cystoscopy and urology procedure support.", "Cystoscopy\nUrology procedures\nUrinary health consultation", "+", True, 6),
            ("Dentistry", "Dental OPD and oral health consultation.", "Dental consultation\nTooth care\nOral health support", "+", False, 7),
            ("Ophthalmology", "Eye OPD and ophthalmology consultation.", "Eye check-up\nOphthalmology OPD\nVision support", "+", False, 8),
            ("Dermatology", "Skin care OPD and dermatology consultation.", "Skin consultation\nDermatology OPD\nFollow-up care", "+", False, 9),
            ("Physiotherapy", "Physiotherapy and rehabilitation support.", "Physiotherapy\nMobility support\nRehabilitation exercises", "+", False, 10),
            ("Plastic Surgery", "Plastic surgery consultation and procedure support.", "Plastic surgery consultation\nProcedure support\nFollow-up care", "+", True, 11),
            ("Vascular Surgery", "Vascular surgery consultation and procedure support.", "Vascular consultation\nVascular surgeries\nFollow-up care", "+", True, 12),
        ]
        department_map = {}
        for name, short, services, icon, featured, order in departments:
            department_map[name] = upsert(
                Department,
                {"name": name},
                {
                    "short_description": short,
                    "detailed_description": short,
                    "services_list": services,
                    "icon": icon,
                    "is_featured": featured,
                    "is_active": True,
                    "display_order": order,
                    "seo_title": f"{name} | Bibi Kaulan Ji Hospital",
                    "seo_description": f"{name} services and OPD support at Bibi Kaulan Ji Hospital, Fatehgarh Churian.",
                },
            )

        services = [
            ("24x7 Emergency", "Emergency support is available round the clock through the confirmed hospital emergency number.", "+", 1),
            ("Free Dialysis Centre", "Dialysis support is highlighted by the hospital as a key patient service.", "+", 2),
            ("Bronchoscopy", "Bronchoscopy support for chest and respiratory care.", "+", 3),
            ("Paediatric Bronchoscopy", "Paediatric bronchoscopy support linked with child and respiratory care.", "+", 4),
            ("Cystoscopy and Urology Procedures", "Cystoscopy and other urology procedure support.", "+", 5),
            ("Plastic Surgery", "Plastic surgery consultation and procedure support.", "+", 6),
            ("Vascular Surgeries", "Vascular surgery consultation and procedure support.", "+", 7),
            ("Cashless Treatment Support", "Empanelled with Ayushman Bharat, private and government insurance TPA for eligible cashless treatment.", "+", 8),
        ]
        for title, short, icon, order in services:
            upsert(
                Service,
                {"title": title},
                {
                    "short_description": short,
                    "detailed_description": short,
                    "icon": icon,
                    "is_featured": True,
                    "is_active": True,
                    "display_order": order,
                    "seo_title": f"{title} | Bibi Kaulan Ji Hospital",
                    "seo_description": f"{title} at Bibi Kaulan Ji Hospital, Fatehgarh Churian.",
                },
            )

        facilities = [
            ("Free Dialysis Centre", "Dialysis centre support highlighted by the hospital.", 1),
            ("Emergency Department", "24x7 emergency access through the confirmed emergency number.", 2),
            ("OPD Consultation Rooms", "Patient consultation rooms for visiting doctors and OPD care.", 3),
            ("Reception and Waiting Area", "Patient reception and waiting support areas.", 4),
        ]
        for title, short, order in facilities:
            upsert(
                Facility,
                {"title": title},
                {
                    "short_description": short,
                    "detailed_description": short,
                    "is_featured": True,
                    "is_active": True,
                    "display_order": order,
                    "seo_title": f"{title} | Bibi Kaulan Ji Hospital",
                    "seo_description": f"{title} at Bibi Kaulan Ji Hospital, Fatehgarh Churian.",
                },
            )

        doctor_rows = [
            ("Dr. Kashish Gupta", "Facility Director", "", None, "", "", True, 1, "dr-kashish-gupta.jpg"),
            ("Dr. Gagandeep Kaur", "MBBS, MD, DNB (Pulmonary Medicine)", "Chest & TB", "Pulmonary Medicine", "Mon, Wed, Fri", "10:00 AM - 2:00 PM", True, 2, "dr-gagandeep-kaur.jpg"),
            ("Dr. Mandeep", "", "Orthopedic", "Orthopedics", "Mon, Thu", "11:00 AM - 3:00 PM", False, 3, ""),
            ("Dr. SS Kaler", "", "Derma", "Dermatology", "Thu", "3:00 PM - 5:00 PM", False, 4, ""),
            ("Dr. Shahzad", "", "General Medicine", "General Medicine", "Mon to Sat", "9:00 AM - 3:00 PM", False, 5, ""),
            ("Dr. Manpreet", "", "General Medicine", "General Medicine", "Mon to Sat", "3:00 PM - 8:00 PM", False, 6, ""),
            ("Dr. Navneet Kaur", "", "Dentist", "Dentistry", "Mon to Sat", "10:00 AM - 4:00 PM", False, 7, ""),
            ("Dr. Amit Srivastava", "", "Eyes", "Ophthalmology", "Mon to Sat", "10:00 AM - 4:00 PM", False, 8, ""),
            ("Dr. Parneet", "", "Physiotherapy", "Physiotherapy", "Mon to Sat", "9:00 AM - 5:00 PM", False, 9, ""),
            ("Dr. Manbir Singh", "MBBS, MD (Paediatrics)", "Paediatric", "Pediatrics", "", "", True, 10, "dr-manbir-singh.jpg"),
            ("Dr. Manbir Verka", "", "Paediatric", "Pediatrics", "Wed, Fri", "12:00 PM - 3:00 PM", False, 11, ""),
        ]

        for full_name, qualification, specialization, department_name, days, timing, featured, order, photo_name in doctor_rows:
            doctor = upsert(
                Doctor,
                {"full_name": full_name},
                {
                    "qualification": qualification,
                    "specialization": specialization,
                    "department": department_map.get(department_name) if department_name else None,
                    "opd_days_text": days,
                    "opd_time_text": timing,
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
            ("Dr. Gagandeep Kaur", "Pulmonary Medicine", "Mon, Wed, Fri", time(10, 0), time(14, 0), 1),
            ("Dr. Mandeep", "Orthopedics", "Mon, Thu", time(11, 0), time(15, 0), 2),
            ("Dr. SS Kaler", "Dermatology", "Thu", time(15, 0), time(17, 0), 3),
            ("Dr. Shahzad", "General Medicine", "Mon to Sat", time(9, 0), time(15, 0), 4),
            ("Dr. Manpreet", "General Medicine", "Mon to Sat", time(15, 0), time(20, 0), 5),
            ("Dr. Navneet Kaur", "Dentistry", "Mon to Sat", time(10, 0), time(16, 0), 6),
            ("Dr. Amit Srivastava", "Ophthalmology", "Mon to Sat", time(10, 0), time(16, 0), 7),
            ("Dr. Parneet", "Physiotherapy", "Mon to Sat", time(9, 0), time(17, 0), 8),
            ("Dr. Manbir Verka", "Pediatrics", "Wed, Fri", time(12, 0), time(15, 0), 9),
        ]
        OPDTiming.objects.filter(doctor__full_name="Dr. Manbir Singh", days="Wed, Fri").update(is_active=False)
        doctor_map = {doctor.full_name: doctor for doctor in Doctor.objects.filter(full_name__in=[row[0] for row in timings])}
        for doctor_name, department_name, days, start, end, order in timings:
            upsert(
                OPDTiming,
                {"doctor": doctor_map[doctor_name], "days": days},
                {
                    "department": department_map[department_name],
                    "start_time": start,
                    "end_time": end,
                    "room_or_location": "OPD",
                    "notes": "Timing from supplied hospital team schedule reference.",
                    "is_active": True,
                    "display_order": order,
                },
            )

        upsert(
            EmergencyInfo,
            {"title": "24x7 Emergency"},
            {
                "emergency_phone": "+91 97805 15050",
                "availability_text": "24x7 emergency",
                "description": "Call the hospital emergency number for urgent guidance before visiting.",
                "instructions": "For serious symptoms, call the emergency number immediately or visit the hospital directly.",
                "is_active": True,
            },
        )
        upsert(
            AmbulanceInfo,
            {"title": "Ambulance Service"},
            {
                "ambulance_phone": "+91 97815 15050",
                "availability_text": "Call hospital to confirm ambulance availability.",
                "service_area": "Fatehgarh Churian and nearby areas",
                "description": "Ambulance contact support for patients around Fatehgarh Churian.",
                "is_active": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("Bibi Kaulan Ji Hospital verified content seeded."))
