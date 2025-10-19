from fastapi import FastAPI, Request
from typing import Optional
from pydantic import BaseModel
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Email configuration from .env
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_NAME = os.getenv("SENDER_NAME")

# Initialize FastAPI app
app = FastAPI()

# Model for birth data
class BirthData(BaseModel):
    full_name: str
    birthdate: str

# Placeholder: Generate numerology report
def generate_numerology_text(data: BirthData) -> str:
    return f"Hello {data.full_name}, based on your birthdate {data.birthdate}, your Life Path Number is... (coming soon)."

# HTML email content
def render_email_html(name: str, birthdate: str, spiritual_focus: str, report_text: str) -> str:
    return f"""
    <html>
        <body>
            <h2>Your Sacred Numerology Report</h2>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Birthdate:</strong> {birthdate}</p>
            <p><strong>Spiritual Focus:</strong> {spiritual_focus}</p>
            <hr>
            <p>{report_text}</p>
        </body>
    </html>
    """

# Send email
def send_email_html(to_email: str, subject: str, html: str) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    msg["To"] = to_email
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as srv:
        srv.starttls()
        srv.login(SMTP_USER, SMTP_PASS)
        srv.send_message(msg)

# Tally Webhook
@app.post("/tally-webhook")
async def tally_webhook(req: Request):
    try:
        body = await req.json()
        print("\n🚀 Raw Tally Payload:", body)
    except Exception as e:
        print("❌ Could not parse JSON:", e)
        return {"ok": False, "error": str(e)}

    answers = body.get("data", {}).get("answers", [])
    print("✅ Extracted Answers:", answers)

    ref_map = {
        "full_name": "full_name_abc123",  # Replace with real field ref later
        "birthdate": "birthdate_def456",
        "email": "email_ghi789",
        "spiritual_focus": "spiritual_focus_xyz321"
    }

    def by_ref(ref_key: str) -> Optional[str]:
        target_ref = ref_map.get(ref_key)
        for a in answers:
            if a.get("field", {}).get("ref") == target_ref:
                return a.get("email") or a.get("text") or a.get("date")
        return None

    name = (by_ref("full_name") or "").strip()
    birthdate = (by_ref("birthdate") or "").strip()
    email = (by_ref("email") or "").strip()
    spiritual_focus = (by_ref("spiritual_focus") or "").strip()

    print("🧾 Parsed Data →", {"name": name, "birthdate": birthdate, "email": email, "focus": spiritual_focus})

    if not (name and birthdate and email):
        return {
            "ok": False,
            "msg": "Missing required fields from Tally",
            "got": {"name": name, "birthdate": birthdate, "email": email},
        }

    report_text = generate_numerology_text(BirthData(full_name=name, birthdate=birthdate))
    html = render_email_html(name, birthdate, spiritual_focus, report_text)
    send_email_html(email, "Your Sacred Numerology Report ✨", html)

    return {"ok": True, "sent_to": email}


# Local testing only
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
