from fastapi import FastAPI, Request, BackgroundTasks
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import logging
from datetime import datetime
import re
import asyncio
import requests
import base64

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_NAME = os.getenv("SENDER_NAME", "Athyna Luna | SacredSpace")
RESEND_API_KEY = os.getenv("RESEND_API_KEY")

app = FastAPI()


class WebhookData(BaseModel):
    data: dict


def delayed_task(delay, func, *args, **kwargs):
    """Execute a task after a delay"""
    import time
    time.sleep(delay)
    func(*args, **kwargs)


def send_email(recipient, subject, body, attachment_path=None):
    """Email sending using Resend API with optional PDF attachment"""
    try:
        url = "https://api.resend.com/emails"
        headers = {
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "from": f"{SENDER_NAME} <{SENDER_EMAIL}>",
            "to": [recipient],
            "subject": subject,
            "html": body.replace("\n", "<br>")
        }
        
        # Add attachment if provided
        if attachment_path:
            try:
                with open(attachment_path, "rb") as f:
                    file_content = base64.b64encode(f.read()).decode("utf-8")
                
                filename = attachment_path.split("/")[-1]
                data["attachments"] = [
                    {
                        "filename": filename,
                        "content": file_content,
                        "content_type": "application/pdf"
                    }
                ]
                logger.info(f"Attachment added: {filename}")
            except Exception as e:
                logger.warning(f"Could not attach PDF: {str(e)}")
        
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        
        logger.info(f"✅ Email sent successfully to {recipient}: {subject} (ID: {response.json().get('id', 'N/A')})")
        
    except Exception as e:
        logger.error(f"Email sending failed to {recipient}: {str(e)}")
        raise

        
    except Exception as e:
        logger.error(f"Email sending failed to {recipient}: {str(e)}")
        raise


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
If this reading sparks questions or you want to go deeper, I offer follow-up consultations and specialized reports (Career Code, Love Blueprint, Future Outlook). Simply reply to this email.

May this reading illuminate your path and empower your journey.

With cosmic blessings,
Athyna Luna 🌙
SacredSpace: Through The Cosmic Lens

P.S. I'd love to hear what resonates most with you. Hit reply and share your biggest "aha!" moment. 💫"""

    send_email(recipient, subject, body, pdf_path)


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


def generate_and_send_report(name, birthdate, birthtime, birthplace, email, focus, report_type):
    """Generate report and send delivery email"""
    try:
        from birth_report import generate_birth_report
        
        # Generate report
        pdf_path = generate_birth_report(name, birthdate, birthtime, birthplace, focus, report_type)
        logger.info(f"Report generated: {pdf_path}")
        
        # Send delivery email with report
        send_delivery_email(email, name, focus, report_type, pdf_path)
        logger.info(f"Delivery email sent to {email}")
        
    except Exception as e:
        logger.error(f"Report generation failed: {str(e)}")
        send_error_notification(email, name)


@app.post("/webhook")
async def tally_webhook(request: Request, background_tasks: BackgroundTasks):
    """Handle Tally form submissions"""
    try:
        body = await request.json()
        answers = body.get("data", {}).get("fields", [])
        
        logger.info(f"Received webhook at {datetime.now()}")
        logger.info(f"🔍 Raw webhook body: {body}")
        logger.info(f"🔍 Answers array: {answers}")
        
        # Field reference mapping
        ref_map = {
            "full_name": "question_BxOPLR",
            "birthdate": "question_eRqGBl",
            "birthtime": "question_X0eADY",
            "birthplace": "question_8xdDKP",
            "email": "question_kNDV0o",
            "report_type": "question_0OE0xj",
            "spiritual_focus": "question_pDjl08"
        }
        
        # Report type ID to text mapping
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
        
        def by_ref(ref_key):
            """Extract field value by reference key"""
            ref = ref_map.get(ref_key)
            for a in answers:
                if a.get("key") == ref:
                    value = a.get("value", "")
                    # Handle dropdown (returns list of IDs)
                    if isinstance(value, list) and len(value) > 0:
                        return value[0]  # Return first selected ID
                    return value if value else ""
            return ""
        
        # Extract and validate data
        name = by_ref("full_name").strip()
        birthdate = by_ref("birthdate").strip()
        birthtime = by_ref("birthtime").strip() or "12:00"
        birthplace = by_ref("birthplace").strip() or "Minneapolis, MN"
        email = by_ref("email").strip()
        report_type_id = by_ref("report_type").strip()
        focus = by_ref("spiritual_focus").strip() or "spiritual growth"
        
        # Convert report type ID to text
        report_type = report_type_map.get(report_type_id, "Deep Dive Birth Chart")
        
        logger.info(f"✅ Extracted fields: name={name}, email={email}, birthdate={birthdate}, birthtime={birthtime}, birthplace={birthplace}, report_type={report_type}")
        
        # Validate required fields
        if not all([name, birthdate, email]):
            logger.error(f"Missing required fields: name={name}, birthdate={birthdate}, email={email}")
            return {"ok": False, "msg": "Missing required fields"}
        
        logger.info(f"✅ Validation passed")
        
        # Step 1: Send confirmation email
        send_confirmation_email(email, name, report_type, focus)
        logger.info(f"✅ Confirmation email sent to {email}")
        
        # Step 2: Send welcome email (delayed 10 seconds)
        background_tasks.add_task(delayed_task, 10, send_welcome_email, email, name, focus)
        
        # Step 3: Generate and send report (delayed 20 seconds)
        background_tasks.add_task(delayed_task, 20, generate_and_send_report, name, birthdate, birthtime, birthplace, email, focus, report_type)
        
        return {
            "ok": True,
            "sent_to": email,
            "report_type": report_type,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Webhook processing error: {str(e)}")
        return {"ok": False, "msg": f"Server error: {str(e)}"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}