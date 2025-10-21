from fastapi import FastAPI, Request, BackgroundTasks
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from birth_report import generate_birth_report
import os
import resend
from dotenv import load_dotenv
import logging
from datetime import datetime
import re
import asyncio
import random

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Environment variables
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "onboarding@resend.dev")
SENDER_NAME = os.getenv("SENDER_NAME", "Athyna Luna | SacredSpace")
MANUAL_REVIEW = os.getenv("MANUAL_REVIEW", "false").lower() == "true"
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"

# Initialize Resend
resend.api_key = RESEND_API_KEY

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

async def delayed_email_sequence(email, name, report_type, focus, birthdate, birthtime, birthplace):
    """Send emails with realistic delays (or skip delays in TEST_MODE)"""
    try:
        # Step 1: Confirmation email (5-10 minutes delay, or instant in TEST_MODE)
        if TEST_MODE:
            logger.info(f"🧪 TEST_MODE: Sending confirmation email immediately")
            delay_seconds = 0
        else:
            delay_minutes = random.randint(5, 10)
            delay_seconds = delay_minutes * 60
            logger.info(f"⏰ Scheduling confirmation email in {delay_minutes} minutes")
        
        await asyncio.sleep(delay_seconds)
        send_confirmation_email(email, name, report_type, focus)
        logger.info(f"✅ Confirmation email sent to {email}")
        
        # Step 2: Welcome email (6 hours after confirmation, or 10 seconds in TEST_MODE)
        if TEST_MODE:
            logger.info(f"🧪 TEST_MODE: Sending welcome email in 10 seconds")
            await asyncio.sleep(10)
        else:
            logger.info(f"⏰ Scheduling welcome email in 6 hours")
            await asyncio.sleep(6 * 60 * 60)
        
        send_welcome_email(email, name, focus, report_type)
        logger.info(f"✅ Welcome email sent to {email}")
        
        # Step 3: Generate report (happens after welcome email, or 10 seconds in TEST_MODE)
        if TEST_MODE:
            logger.info(f"🧪 TEST_MODE: Generating report in 10 seconds")
            await asyncio.sleep(10)
        
        if MANUAL_REVIEW:
            logger.info(f"Manual review enabled - report queued for {name}")
            return
        
        # Generate report
        try:
            pdf_path = generate_birth_report(name, birthdate, birthtime, birthplace, focus, report_type)
            logger.info(f"Report generated: {pdf_path}")
            
            # Step 4: Send delivery email with report
            send_delivery_email(email, name, focus, report_type, pdf_path)
            logger.info(f"✅ Delivery email sent to {email}")
            
        except Exception as e:
            logger.error(f"Report generation failed: {str(e)}")
            send_error_notification(email, name)
            
    except Exception as e:
        logger.error(f"Email sequence error: {str(e)}")

@app.post("/webhook")
async def tally_webhook(request: Request, background_tasks: BackgroundTasks):
    try:
        body = await request.json()
        logger.info(f"Received webhook at {datetime.now()}")
        
        answers = body.get("data", {}).get("fields", [])
        logger.info(f"🔍 Raw webhook body: {body}")
        logger.info(f"🔍 Answers array: {answers}")
        
        # Field reference mapping
        ref_map = {
            "full_name": "question_BxOPLR",
            "birthdate": "question_eRqGBl",
            "email": "question_kNDV0o",
            "spiritual_focus": "question_pDjl08"
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
        report_type = by_ref("report_type").strip() if by_ref("report_type") else "Numerology Nexus"

        logger.info(f"✅ Extracted fields: name={name}, email={email}, birthdate={birthdate}")
        
        # Validation
        if not all([name, birthdate, email]):
            logger.error(f"Missing required fields: name={name}, birthdate={birthdate}, email={email}")
            return {
                "ok": False, 
                "msg": "Missing required fields", 
                "got": {"name": name, "birthdate": birthdate, "email": email}
            }
        
        logger.info("✅ Validation passed")
        
        if not validate_birthdate(birthdate):
            logger.error(f"Invalid birthdate: {birthdate}")
            return {"ok": False, "msg": "Invalid birthdate format or value"}
        
        # Email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            logger.error(f"Invalid email: {email}")
            return {"ok": False, "msg": "Invalid email format"}
        
        if TEST_MODE:
            logger.info("🧪 TEST_MODE enabled - emails will send immediately")
        
        logger.info("✅ Starting delayed email sequence")
        
        # Schedule the delayed email sequence in the background
        background_tasks.add_task(
            delayed_email_sequence, 
            email, name, report_type, focus, birthdate, birthtime, birthplace
        )
        
        return {
            "ok": True, 
            "msg": "Order received - emails scheduled",
            "sent_to": email,
            "report_type": report_type,
            "test_mode": TEST_MODE,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Webhook processing error: {str(e)}")
        # Send immediate error notification
        try:
            send_error_notification(email, name)
        except:
            pass
        return {"ok": False, "msg": f"Server error: {str(e)}"}


def send_confirmation_email(recipient, name, report_type, focus):
    """Confirmation email - Penn's enhanced copy"""
    subject = f"✨ Your {report_type} Is Being Woven by the Stars"
    
    body = f"""Dear {name},

🌙 **Your {report_type} order has been received—and the timing of this moment is no accident.**

I felt the energy shift the moment your order came through. The cosmos has been calling you here, and you answered. That takes courage.

Right now, I'm preparing your sacred reading with deep intention. This isn't a generic report—it's a personalized map of your soul's journey, crafted specifically for where you are *right now* in your spiritual awakening.

**Here's what happens next:**

⏰ **Within 6 hours:** You'll receive a personal message from me with a sneak peek into what your chart is already revealing (trust me, you'll want to read this one)

📬 **Within 24-72 hours:** Your complete {report_type} arrives—a sacred tool you'll return to again and again

🎯 **Your focus:** {focus}  
*The universe heard this intention. Your reading will speak directly to it.*

---

**A quick note from my heart to yours:**

I know what it's like to walk away from restrictive beliefs and step into your own spiritual power. It's terrifying and exhilarating all at once. This reading will meet you exactly where you are—no judgment, only clarity and compassion.

If questions come up before your report arrives, hit reply. I'm here.

**With cosmic love and fierce support,**  
Athyna Luna 🌙  
*Your guide through the cosmic lens*

P.S. Add {SENDER_EMAIL} to your contacts so my emails land in your inbox, not the void. The universe works in mysterious ways, but your spam filter doesn't have to. 😉"""

    send_email(recipient, subject, body)


def send_welcome_email(recipient, name, focus, report_type):
    """Welcome email - Penn's enhanced copy"""
    subject = f"🔮 I'm Seeing Something Powerful in Your Chart, {name}"
    
    body = f"""Dear {name},

I'm deep into your chart right now, and I had to pause to reach out.

**There's something here I need you to know.**

Your journey with {focus} isn't just a question you're asking the universe—it's a *calling* your soul has been whispering for lifetimes. And the cosmic blueprint I'm uncovering? It's breathtaking.

Here's what I'm weaving into your {report_type}:

✨ **Shadow work prompts** designed specifically for *your* placements—not generic advice, but the exact inner work your soul is ready for right now

🌙 **Trauma-informed guidance** that honors where you've been and illuminates where you're going (because spiritual growth shouldn't retraumatize you)

⚡ **Rituals you can start TODAY**—practical, powerful, and aligned with your unique energy

💫 **The truth about your soul's purpose**—the one you've always sensed but couldn't quite name

---

**Here's what I'm sensing as I prepare your reading:**

Your chart is showing me that {focus} is only the *beginning* of what you're meant to discover. There are layers here—gifts you haven't fully claimed yet, patterns ready to be released, and a version of yourself that's waiting to emerge.

*(I'll reveal more when your full report arrives in the next 24-72 hours.)*

---

**While you wait, I have a question for you:**

*What would change in your life if you had absolute clarity about your soul's path?*

Sit with that. Journal it. Light a candle and let the answer come through. Because that clarity? It's about to land in your inbox.

**And here's something most people don't know:**

Your {report_type} is just one lens through which to view your cosmic truth. Many of my clients discover that pairing it with another reading—like the **Love Blueprint** (if relationships are calling you) or the **Career Code** (if you're ready to align your work with your purpose)—creates a complete picture that's absolutely life-changing.

*But we'll talk about that later. For now, just know: you're exactly where you need to be.*

**Blessed be,**  
Athyna Luna 🌙  
*SacredSpace: Through The Cosmic Lens*

P.S. Your report will arrive within 24-72 hours, but if you're feeling impatient (I get it—cosmic downloads don't wait for anyone), hit reply and tell me what you're most excited to discover. I love hearing from you."""

    send_email(recipient, subject, body)


def send_delivery_email(recipient, name, focus, report_type, pdf_path):
    """Delivery email - Penn's enhanced copy"""
    subject = f"🌟 Your {report_type} Has Arrived—Open When You're Ready"
    
    body = f"""Dear {name},

**Take a breath. Light a candle. Find your sacred space.**

Because what I'm about to send you isn't just a report—it's a mirror reflecting the truth of who you really are.

🌟 **Your {report_type} is ready.**

I poured intention, intuition, and deep cosmic wisdom into every word. This reading was crafted specifically for *you*—for your journey with {focus}, for the version of yourself you're becoming, and for the soul-level transformation you're ready to claim.

**Inside your report, you'll discover:**

✨ **Your unique cosmic blueprint**—the energetic signature you were born with and how to work *with* it instead of against it

🌙 **Shadow work prompts tailored to YOUR placements**—not surface-level questions, but the deep inner work that creates lasting change

⚡ **Personalized rituals for alignment**—simple, powerful practices you can start today

💫 **Guidance for your soul's evolution**—the path forward, illuminated

---

**How to use your report (this matters):**

1. **Create sacred space.** Turn off distractions. Light a candle. Play soft music. This isn't something to skim on your lunch break.

2. **Read slowly.** Let the insights land. Some will resonate immediately. Others will reveal themselves over time.

3. **Journal as you go.** Write down what stirs something in you—the "aha!" moments, the uncomfortable truths, the sudden clarity.

4. **Return to it often.** Your chart is a *living document*. It will speak to you differently during every season of your life.

5. **Trust what resonates.** If something doesn't feel true yet, bookmark it. Your soul knows the timing.

---

**Now, here's what I need you to know:**

This reading is a beginning, not an ending.

Many clients tell me their {report_type} cracked something open—and suddenly, they had *more* questions. Deeper ones. Like:

- *"Now that I understand my purpose, how do I align my career with it?"* → **Career Code**
- *"I see my patterns in love—how do I break them and attract my soul mate?"* → **Love Blueprint**  
- *"What's coming for me in the next 30 days, and how do I navigate it?"* → **30-Day Outlook**
- *"I need to go even deeper into my soul's mission."* → **Life Purpose Reading**
- *"I want the full picture—all of it."* → **Deep Dive Birth Chart**

If you're feeling that pull to go deeper, **I'm offering you 15% off your next reading** as a thank-you for trusting me with your journey. Just reply to this email with the word **"DEEPER"** and tell me what you're being called to explore next.

*(This offer is just for you, and it's available for the next 7 days.)*

---

**But for now?**

Read your report. Sit with it. Let it work its magic.

And when you're ready, hit reply and tell me: **What was your biggest "aha!" moment?**

I genuinely want to know. Your breakthroughs fuel my soul.

**May this reading illuminate your path, validate your journey, and empower every step forward.**

**With cosmic blessings and fierce love,**  
Athyna Luna 🌙  
*SacredSpace: Through The Cosmic Lens*

P.S. If this reading resonated deeply, I'd be honored if you'd share your experience. Your story might be exactly what another woman needs to hear to take the first step on her own cosmic journey. 💫"""

    send_email(recipient, subject, body, pdf_path)


def send_followup_email(
