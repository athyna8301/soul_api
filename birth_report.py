from tzfpy import Tzf
from geopy.geocoders import Nominatim
from datetime import datetime
from zoneinfo import ZoneInfo  # Only works in Python 3.9+
from fpdf import FPDF
import smtplib
from email.message import EmailMessage

# --------- INPUT ---------
name = "Jane Doe"
birthdate = "1990-07-15"
birthtime = "14:30"  # 24-hour format
birthplace = "San Francisco, CA"
email = "client@example.com"

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
birth_dt_str = f"{birthdate} {birthtime}"
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

print(report_text)

# --------- STEP 6: Save to PDF ---------
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
for line in report_text.strip().split("\n"):
    pdf.cell(200, 10, txt=line, ln=True)
pdf_filename = f"{name.replace(' ', '_')}_birth_report.pdf"
pdf.output(pdf_filename)

# --------- STEP 7: Send Email with PDF ---------
def send_email(recipient, subject, body, attachment):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = "youremail@example.com"  # Replace with your email
    msg["To"] = recipient
    msg.set_content(body)

    with open(attachment, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=attachment)

    with smtplib.SMTP_SSL("smtp.example.com", 465) as smtp:  # Replace with your SMTP server & port
        smtp.login("youremail@example.com", "yourpassword")  # Replace with your credentials
        smtp.send_message(msg)

# Uncomment to send email (configure properly first)
# send_email(email, "Your Birth Report", "Attached is your personalized birth report.", pdf_filename)
