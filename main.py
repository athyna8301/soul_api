from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from reports.birth_report import generate_birth_report

load_dotenv()

# Email config
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_NAME = os.getenv("SENDER_NAME")

app = FastAPI()

class BirthData(BaseModel):
    full_name: str
    birthdate: str

# Generate email HTML
def render_email_html(name, birthdate, spiritual_focus, report_path):
    return f"""
    <html>
        <body>
            <h2>Your Sacred Numerology Report</h2>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Birthdate:</strong> {birthdate}</p>
            <p><strong>Spiritual Focus:</strong> {spiritual_focus}</p>
            <hr>
            <p>Your PDF report is attached.</p>
        </body>
    </html>
    """

# Send email with attachment
def send_email_html(to_email, subject, html, attachment_path):
    msg = MIMEMultipart("mixed")
    msg["Subject"] = subject
    msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    msg["To"] = to_email

    msg.attach(MIMEText(html, "html"))

    with open(attachment_path, "rb") as f:
        msg.attach(MIMEText(f.read(), "base64", "utf-8"))
        msg.get_payload()[-1].add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment_path)}")

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

@app.post("/tally-webhook")
async def tally_webhook(req: Request):
    body = await req.json()
    print("\n🚀 Tally Payload:", body)

    answers = body.get("data", {}).get("answers", [])

    # These must match Tally question `ref`s
    ref_map = {
        "full_name": "full_name_abc123",
        "birthdate": "birthdate_def456",
        "email": "email_ghi789",
        "spiritual_focus": "spiritual_focus_xyz321"
    }

    def get_answer(ref_key: str) -> Optional[str]:
        ref = ref_map[ref_key]
        for answer in answers:
            if answer.get("field", {}).get("ref") == ref:
                return answer.get("text") or answer.get("email") or answer.get("date")
        return None

    name = (get_answer("full_name") or "").strip()
    birthdate = (get_answer("birthdate") or "").strip()
    email = (get_answer("email") or "").strip()
    spiritual_focus = (get_answer("spiritual_focus") or "").strip()
    birthtime = "03:59"
    birthplace = "Chicago, IL"  # Optional: collect via form

    if not (name and birthdate and email):
        return {
            "ok": False,
            "msg": "Missing required fields",
            "got": {"name": name, "birthdate": birthdate, "email": email}
        }

    report_path = generate_birth_report(name, birthdate, birthtime, birthplace)
    html = render_email_html(name, birthdate, spiritual_focus, report_path)
    send_email_html(email, "Your Sacred Numerology Report ✨", html, report_path)

    return {"ok": True, "sent_to": email}

# Local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
