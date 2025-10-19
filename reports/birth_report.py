from tzfpy import Tzf
from geopy.geocoders import Nominatim
from datetime import datetime
from zoneinfo import ZoneInfo  # Only works in Python 3.9+
from fpdf import FPDF
import smtplib
from email.message import EmailMessage
import os

def generate_birth_report(name, birthdate, birthtime, birthplace):
    # --------- STEP 1: Convert city to lat/lon ---------
    geolocator = Nominatim(user_agent="birth_report_locator")
    location = geolocator.geocode(birthplace)
    if not location:
        raise Exception(f"Could not find coordinates for {birthplace}")

    latitude = location.latitude
    longitude = location.longitude

    # --------- STEP 2: Get timezone using tzfpy ---------
    tz_lookup = Tzf()
    timezone_str = tz_lookup.timezone_at(latitude, longitude)

    # --------- STEP 3: Combine birthdate and time ---------
    birth_dt_str = f"{birthdate} {birthtime}"  # e.g., 1983-03-02 03:59
    birth_dt = datetime.strptime(birth_dt_str, "%Y-%m-%d %H:%M")

    # --------- STEP 4: Convert to local time with timezone ---------
    birth_dt_local = birth_dt.replace(tzinfo=ZoneInfo(timezone_str))

    # --------- STEP 5: Generate Report Content ---------
    report_text = f"""
--- BIRTH REPORT ---
Name: {name}
Location: {birthplace} ({latitude:.4f}, {longitude:.4f})
Timezone: {timezone_str}
Birth Date & Time (local): {birth_dt_local.strftime('%B %d, %Y at %I:%M %p %Z')}

Horoscope Summary:
Today is a day of new beginnings. Trust your instincts and be open to opportunities.
"""

    # --------- STEP 6: Save to PDF ---------
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in report_text.strip().split("\n"):
        pdf.cell(200, 10, txt=line.strip(), ln=True)

    filename = f"{name.replace(' ', '_')}_birth_report.pdf"
    filepath = os.path.join("reports", filename)
    pdf.output(filepath)

    return filepath


# --------- OPTIONAL STEP 7: Send Email with PDF ---------
def send_email(recipient, subject, body, attachment_path):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = "youremail@example.com"  # Replace this
    msg["To"] = recipient
    msg.set_content(body)

    with open(attachment_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename=os.path.basename(attachment_path)
        )

    with smtplib.SMTP_SSL("smtp.example.com", 465) as smtp:  # Replace with your SMTP details
        smtp.login("youremail@example.com", "yourpassword")  # Replace
        smtp.send_message(msg)
