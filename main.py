from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import JSONResponse
import resend
import os
from datetime import datetime
import logging
from birth_report import generate_report_content, generate_pdf

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Load Resend API key
resend.api_key = os.getenv("RESEND_API_KEY")

# Field reference mapping
ref_map = {
    "question_BxOPLR": "name",
    "question_eRqGBl": "birthdate",
    "question_X0eADY": "birthtime",
    "question_8xdDKP": "birthplace",
    "question_kNDV0o": "email",
    "question_0OE0xj": "report_type",
    "question_pDjl08": "spiritual_focus"
}

# Report type ID to name mapping
report_type_map = {
    "4c34cb27-c5be-47bb-abd9-a9f4b5993020": "Numerology Nexus",
    "9c4433ce-ebbb-4c28-bfd8-edd06a34bfff": "Deep Dive Birth Chart",
    "92e90bec-9a42-456a-92c3-de1b0e0df9d8": "Love Blueprint",
    "34233ae1-8a64-4983-bad6-fd8266122750": "Career Code",
    "40f8b83b-557e-4778-97ea-aa3003eac86e": "Life Purpose",
    "7f27fc14-bf3b-4887-a40a-08953e6738f8": "Future Outlook",
    "62fb1e90-b505-453b-97c0-7cddc344b951": "Human Design",
    "a8fdc0ac-e34c-4c98-bb4b-5a811dbfdcca": "Starseed Lineage",
    "5bfc4de1-a41a-4356-aed0-5497d9dad4db": "Cosmic Calendar (One Time Purchase)",
    "748712f0-a60f-4bd0-b0fb-cd50b4778aa0": "Cosmic Calendar (Monthly Subscription)",
    "072c71a1-7ee3-45ba-b2eb-8ebdc494a484": "Astrocartography",
    "fda599e2-8f77-48a7-add5-396af4f0e5d9": "ShadowWork Workbook"
}

def by_ref(answers, ref_key):
    """Extract value by reference key, handling dropdowns"""
    for field in answers:
        if field.get("key") == ref_key:
            value = field.get("value")
            # Handle dropdown: value is a list of IDs
            if isinstance(value, list) and len(value) > 0:
                dropdown_id = value[0]
                # Look up the text from options
                options = field.get("options", [])
                for opt in options:
                    if opt.get("id") == dropdown_id:
                        return opt.get("text")
                return dropdown_id  # fallback to ID if text not found
            return value
    return None

def send_email(to_email: str, subject: str, html_content: str, attachment_path: str = None):
    """Send email via Resend with optional attachment"""
    try:
        params = {
            "from": "SacredSpace <onboarding@resend.dev>",
            "to": [to_email],
            "subject": subject,
            "html": html_content
        }
        
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, "rb") as f:
                file_content = f.read()
            
            filename = os.path.basename(attachment_path)
            params["attachments"] = [{
                "filename": filename,
                "content": list(file_content)
            }]
            logger.info(f"Attachment added: {filename}")
        
        email = resend.Emails.send(params)
        logger.info(f"✅ Email sent successfully to {to_email}: {subject} (ID: {email['id']})")
        return email
    except Exception as e:
        logger.error(f"❌ Email send failed: {str(e)}")
        raise

async def process_report(name: str, email: str, birthdate: str, birthtime: str, 
                        birthplace: str, report_type: str, spiritual_focus: str):
    """Background task to generate and send report"""
    try:
        # Send welcome email
        welcome_html = f"""
        <h2>🔮 Your Chart is Being Crafted With Sacred Intention</h2>
        <p>Dear {name.split()[0]},</p>
        <p>Your cosmic blueprint is being woven together with care. Your <strong>{report_type}</strong> will arrive within the next 24-48 hours.</p>
        <p>In the meantime, take a moment to ground yourself and set an intention for what you wish to discover.</p>
        <p>Blessings,<br>Athyna Luna 🌙</p>
        """
        send_email(email, "🔮 Your Chart is Being Crafted With Sacred Intention", welcome_html)
        
        # Generate report
        logger.info(f"Generating {report_type} for {name}...")
        content = generate_report_content(name, birthdate, birthtime, birthplace, report_type, spiritual_focus)
        pdf_path = generate_pdf(name, birthdate, birthtime, birthplace, report_type, spiritual_focus, content)
        logger.info(f"Report generated: {pdf_path}")
        
        # Send delivery email with attachment
        delivery_html = f"""
        <h2>🌟 Your {report_type} Has Arrived</h2>
        <p>Dear {name.split()[0]},</p>
        <p>Your personalized <strong>{report_type}</strong> is attached to this email.</p>
        <p>Take your time exploring the insights within. This is your cosmic roadmap.</p>
        <p>If you have questions or want to go deeper, simply reply to this email.</p>
        <p>With cosmic love,<br>Athyna Luna 🌙</p>
        """
        send_email(email, f"🌟 Your {report_type} Has Arrived", delivery_html, pdf_path)
        logger.info(f"Delivery email sent to {email}")
        
    except Exception as e:
        logger.error(f"Report generation failed: {str(e)}")
        # Send error email
        error_html = f"""
        <h2>⚠️ A Cosmic Hiccup (We're On It!)</h2>
        <p>Dear {name.split()[0]},</p>
        <p>We encountered a small issue generating your report, but we're on it!</p>
        <p>You'll receive your {report_type} shortly. Thank you for your patience.</p>
        <p>Blessings,<br>Athyna Luna 🌙</p>
        """
        send_email(email, "⚠️ A Cosmic Hiccup (We're On It!)", error_html)

@app.post("/webhook")
async def tally_webhook(request: Request, background_tasks: BackgroundTasks):
    """Handle Tally form webhook"""
    try:
        body = await request.json()
        logger.info(f"Received webhook at {datetime.now()}")
        logger.info(f"🔍 Raw webhook body: {body}")
        
        answers = body.get("data", {}).get("fields", [])
        logger.info(f"🔍 Answers array: {answers}")
        
        # Extract fields
        name = by_ref(answers, "question_BxOPLR")
        email = by_ref(answers, "question_kNDV0o")
        birthdate = by_ref(answers, "question_eRqGBl")
        birthtime = by_ref(answers, "question_X0eADY")
        birthplace = by_ref(answers, "question_8xdDKP")
        report_type_raw = by_ref(answers, "question_0OE0xj")
        spiritual_focus = by_ref(answers, "question_pDjl08")
        
        # Map report type ID to name
        report_type = report_type_map.get(report_type_raw, report_type_raw)
        
        logger.info(f"✅ Extracted fields: name={name}, email={email}, birthdate={birthdate}, "
                   f"birthtime={birthtime}, birthplace={birthplace}, report_type={report_type}")
        
        # Validation
        if not all([name, email, birthdate, birthtime, birthplace, report_type]):
            logger.error("❌ Missing required fields")
            return JSONResponse({"status": "error", "message": "Missing required fields"}, status_code=400)
        
        logger.info("✅ Validation passed")
        
        # Send immediate confirmation
        confirmation_html = f"""
        <h2>✨ Your Cosmic Journey Begins Now</h2>
        <p>Dear {name.split()[0]},</p>
        <p>Thank you for trusting me with your birth chart details. I've received your request for a <strong>{report_type}</strong>.</p>
        <p>Your personalized report is being crafted and will arrive in your inbox within 24-48 hours.</p>
        <p>Blessings on your journey,<br>Athyna Luna 🌙</p>
        """
        send_email(email, "✨ Your Cosmic Journey Begins Now", confirmation_html)
        logger.info(f"✅ Confirmation email sent to {email}")
        
        # Schedule report generation
        background_tasks.add_task(process_report, name, email, birthdate, birthtime, 
                                  birthplace, report_type, spiritual_focus)
        
        return JSONResponse({"status": "success", "message": "Webhook received"})
        
    except Exception as e:
        logger.error(f"❌ Webhook processing failed: {str(e)}")
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}