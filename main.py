from fastapi import FastAPI, Request, BackgroundTasks
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from birth_report import generate_birth_report
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import logging
from datetime import datetime
import re

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Environment variables
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_NAME = os.getenv("SENDER_NAME", "Athyna Luna | SacredSpace")
MANUAL_REVIEW = os.getenv("MANUAL_REVIEW", "false").lower() == "true"

class WebhookData(BaseModel):
    data: dict

def validate_birthdate(date_str: str) -> bool:
    """Validate birthdate format and reasonableness"""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        # Check if date is between 1900 and today
        if date_obj.year < 1900 or date_obj > datetime.now():
            return False
        return True
    except ValueError:
        return False

@app.post("/webhook")
async def tally_webhook(request: Request, background_tasks: BackgroundTasks):
    try:
        body = await request.json()
        logger.info(f"Received webhook at {datetime.now()}")
        
        answers = body.get("data", {}).get("fields", [])
        logger.info(f"🔍 Raw webhook body: {body}")
        logger.info(f"🔍 Answers array: {answers}")
        # Field reference mapping (update with your actual Tally field refs)
        ref_map = {
    "question_BxOPLR": "full_name",
    "question_eRqGBl": "birthdate",
    "question_kNDV0o": "email",
    "question_pDjl08": "spiritual_focus"
}                 
        def by_ref(ref_key):
    ref = ref_map.get(ref_key)
    for a in answers:
        if a.get("key") == ref:
            return a.get("value", "")
    return ""
    
        
        # Extract and validate data
        name = by_ref("full_name").strip()
        birthdate = by_ref("birthdate").strip()
        birthtime = by_ref("birthtime").strip() if by_ref("birthtime") else "12:00"
        birthplace = by_ref("birthplace").strip() if by_ref("birthplace") else "San Francisco, CA"
        email = by_ref("email").strip().lower()
        focus = by_ref("spiritual_focus").strip() if by_ref("spiritual_focus") else "personal growth"
        report_type = by_ref("report_type").strip() if by_ref("report_type") else "Deep Dive Birth Chart"

        
        # Validation
        if not all([name, birthdate, email]):
            logger.error(f"Missing required fields: name={name}, birthdate={birthdate}, email={email}")
            return {
                "ok": False, 
                "msg": "Missing required fields", 
                "got": {"name": name, "birthdate": birthdate, "email": email}
            }
        
        if not validate_birthdate(birthdate):
            logger.error(f"Invalid birthdate: {birthdate}")
            return {"ok": False, "msg": "Invalid birthdate format or value"}
        
        # Email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            logger.error(f"Invalid email: {email}")
            return {"ok": False, "msg": "Invalid email format"}
        
        # Step 1: Send instant confirmation email
        send_confirmation_email(email, name, report_type, focus)
        logger.info(f"Confirmation email sent to {email}")
        
        # Step 2: Schedule welcome email (12 hours - use background task or scheduler)
        # For immediate implementation, send welcome email now
        # In production, use Celery, APScheduler, or Zapier for delayed sending
        send_welcome_email(email, name, focus)
        logger.info(f"Welcome email sent to {email}")
        
        # Step 3: Generate report
        if MANUAL_REVIEW:
            logger.info(f"Manual review enabled - report queued for {name}")
            # Store order details for manual processing
            return {
                "ok": True, 
                "msg": "Order received - manual review required",
                "client": name
            }
        
        # Generate report
        try:
            pdf_path = generate_birth_report(name, birthdate, birthtime, birthplace, focus, report_type)
            logger.info(f"Report generated: {pdf_path}")
        except Exception as e:
            logger.error(f"Report generation failed: {str(e)}")
            send_error_notification(email, name)
            return {"ok": False, "msg": f"Report generation failed: {str(e)}"}
        
        # Step 4: Send delivery email with report
        send_delivery_email(email, name, focus, report_type, pdf_path)
        logger.info(f"Delivery email sent to {email}")
        
        # Step 5: Schedule follow-up email (5-7 days)
        # Use background task or external scheduler
        # background_tasks.add_task(schedule_followup, email, name, report_type)
        
        return {
            "ok": True, 
            "sent_to": email,
            "report_type": report_type,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Webhook processing error: {str(e)}")
        return {"ok": False, "msg": f"Server error: {str(e)}"}


def send_confirmation_email(recipient, name, report_type, focus):
    """Instant confirmation email - mystical and reassuring"""
    subject = "✨ Your Cosmic Journey Begins Now"
    
    body = f"""Dear {name},

🌙 Your {report_type} order has been received!

The cosmos has aligned, and your sacred report is now being prepared with care and intention. 

**What happens next:**
• Within 12 hours: You'll receive a personal welcome email with insights into what your report will reveal
• Within 24-72 hours: Your complete {report_type} will arrive in your inbox
• Your focus: {focus}

Your birth chart holds profound wisdom about your soul's journey. I'm honored to be your guide through the cosmic lens.

If you have any questions, simply reply to this email. I'm here for you.

With cosmic love and light,
Athyna Luna 🌙
SacredSpace: Through The Cosmic Lens

P.S. Check your spam folder if you don't see my emails - the universe works in mysterious ways! 😊"""

    send_email(recipient, subject, body)


def send_welcome_email(recipient, name, focus):
    """Welcome email - builds anticipation and connection"""
    subject = "🔮 Your Chart is Being Crafted With Sacred Intention"
    
    body = f"""Dear {name},

I wanted to reach out personally to let you know that your cosmic reading is underway.

As I prepare your chart, I'm already sensing the powerful energy around your journey with {focus}. The stars have so much to reveal to you.

**What makes your reading special:**
✨ Personalized shadow work prompts aligned with your chart
🌙 Trauma-informed guidance honoring your spiritual awakening
⚡ Practical rituals you can use immediately
💫 Insights into your soul's deepest purpose

Your report isn't just data - it's a sacred tool for transformation.

I'll have your complete reading to you within 24-72 hours. In the meantime, take a moment to set an intention: What do you most want to understand about yourself?

The cosmos is listening.

Blessed be,
Athyna Luna 🌙
SacredSpace: Through The Cosmic Lens"""

    send_email(recipient, subject, body)


def send_delivery_email(recipient, name, focus, report_type, pdf_path):
    """Delivery email - mystical reveal with gentle upsell"""
    subject = f"🌟 Your {report_type} Has Arrived"
    
    body = f"""Dear {name},

The moment has arrived. Your {report_type} is ready.

This reading was crafted specifically for you, with deep attention to your journey with {focus}. Inside, you'll find:

✨ Your unique cosmic blueprint
🌙 Shadow work prompts tailored to your placements
⚡ Personalized rituals for alignment
💫 Guidance for your soul's evolution

**How to use your report:**
1. Find a quiet, sacred space
2. Light a candle or play soft music
3. Read slowly, allowing insights to land
4. Journal about what resonates most
5. Revisit it during major life transitions

Your chart is a living document - it will reveal new layers as you grow.

**What's next?**
If this reading sparks questions or you want to go deeper, I offer follow-up consultations and specialized reports (Career Code, Love Blueprint, 30-Day Outlook). Simply reply to this email.

May this reading illuminate your path and empower your journey.

With cosmic blessings,
Athyna Luna 🌙
SacredSpace: Through The Cosmic Lens

P.S. I'd love to hear what resonates most with you. Hit reply and share your biggest "aha!" moment. 💫"""

    send_email(recipient, subject, body, pdf_path)


def send_followup_email(recipient, name, report_type):
    """Follow-up email 5-7 days after delivery - feedback and upsell"""
    subject = "🌙 How is Your Cosmic Journey Unfolding?"
    
    body = f"""Dear {name},

It's been about a week since your {report_type} arrived, and I've been wondering how it's landing for you.

Have you had any breakthrough moments? Any questions arising? I'd genuinely love to hear.

**Quick question:** What was the most powerful insight from your reading?

Many clients find that after sitting with their birth chart for a few days, they're ready to explore specific areas more deeply:

💼 **Career Code** - Discover your professional purpose and ideal path
💕 **Love Blueprint** - Understand your relationship patterns and soul mate indicators  
🔮 **30-Day Outlook** - Navigate upcoming transits with confidence

**Special offer for you:** As a valued client, you receive 15% off your next report. Use code COSMIC15 at checkout.

I'm here to support your continued awakening.

Blessed be,
Athyna Luna 🌙
SacredSpace: Through The Cosmic Lens"""

    send_email(recipient, subject, body)


def send_error_notification(recipient, name):
    """Error notification - compassionate and solution-oriented"""
    subject = "⚠️ A Cosmic Hiccup (We're On It!)"
    
    body = f"""Dear {name},

I'm reaching out because there was a technical issue generating your report. Mercury retrograde strikes again! 😅

**Here's what's happening:**
I'm personally reviewing your order and will have your report to you within 24 hours. Sometimes the cosmos asks us to slow down and do things with extra care.

You'll receive an email from me as soon as your reading is ready.

Thank you for your patience and trust.

With cosmic apologies,
Athyna Luna 🌙
SacredSpace: Through The Cosmic Lens"""

    send_email(recipient, subject, body)


def send_email(recipient, subject, body, attachment_path=None):
    """Core email sending function with error handling"""
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
        msg["To"] = recipient
        msg.set_content(body)
        
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, "rb") as f:
                msg.add_attachment(
                    f.read(), 
                    maintype="application", 
                    subtype="pdf", 
                    filename=os.path.basename(attachment_path)
                )
        
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.login(SMTP_USER, SMTP_PASS)
            smtp.send_message(msg)
            
        logger.info(f"Email sent successfully to {recipient}: {subject}")
        
    except Exception as e:
        logger.error(f"Email sending failed to {recipient}: {str(e)}")
        raise


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}