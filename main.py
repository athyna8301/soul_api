from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ---------------- App + CORS ----------------
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev: open; tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------- Models --------------------
class BirthData(BaseModel):
    full_name: str
    birthdate: str  # YYYY-MM-DD


# --------------- Numerology helpers (simple & safe) ---------------
def _digitsum(n: int) -> int:
    return sum(int(c) for c in str(abs(n)) if c.isdigit())


def _reduce(n: int) -> int:
    # reduce to 1..9, except keep master 11/22/33 as-is
    while n > 9 and n not in (11, 22, 33):
        n = _digitsum(n)
    return n


def _letters_only(s: str) -> str:
    return "".join(ch for ch in s.lower() if "a" <= ch <= "z")


def _name_number(name: str) -> int:
    # A1..Z26 Pythagorean
    total = 0
    for ch in _letters_only(name):
        total += (ord(ch) - 96)
    return _reduce(total)


def calculate_life_path(birthdate: str) -> int:
    # yyyy-mm-dd or yyyy/mm/dd etc -> strip non-digits
    nums = "".join(c for c in birthdate if c.isdigit())
    if not nums:
        return 0
    return _reduce(_digitsum(int(nums)))


def calculate_expression(name: str) -> int:
    return _name_number(name)


def calculate_soul_urge(name: str) -> int:
    vowels = set("aeiouy")
    total = 0
    for ch in _letters_only(name):
        if ch in vowels:
            total += (ord(ch) - 96)
    return _reduce(total)


def calculate_personality(name: str) -> int:
    vowels = set("aeiouy")
    total = 0
    for ch in _letters_only(name):
        if ch not in vowels:
            total += (ord(ch) - 96)
    return _reduce(total)


def generate_numerology_text(data: BirthData) -> str:
    name = data.full_name.strip()
    life_path = calculate_life_path(data.birthdate)
    expression = calculate_expression(name)
    soul_urge = calculate_soul_urge(name)
    personality = calculate_personality(name)

    # Build with joins (no triple quotes!)
    parts: list[str] = []
    parts.append(f"🌙 Sacred Numerology Report for {name}")
    parts.append(f"Date of Birth: {data.birthdate}")
    parts.append("Prepared with reverence by Athyna Luna | SacredSpace: Through The Cosmic Lens")
    parts.append("")
    parts.append("— — —")
    parts.append("")
    parts.append("✨ Introduction")
    parts.append("This isn’t prophecy; it’s remembrance. Trust what resonates, release what doesn’t.")
    parts.append("")
    parts.append(f"🔢 Life Path {life_path}")
    parts.append("Your primary lesson and path in this lifetime.")
    parts.append("")
    parts.append(f"🔠 Expression {expression}")
    parts.append("How your gifts naturally want to express.")
    parts.append("")
    parts.append(f"💓 Soul Urge {soul_urge}")
    parts.append("What your heart quietly longs for.")
    parts.append("")
    parts.append(f"🌀 Personality {personality}")
    parts.append("What the world first perceives about you.")
    parts.append("")
    parts.append("🌕 Closing Affirmation")
    parts.append("I trust my cosmic blueprint. I am both human and holy.")
    return "\n".join(parts)


# --------------- Email (no triple quotes) ---------------
def render_email_html(name: str, birthdate: str, spiritual_focus: str, report_text: str) -> str:
    br = "<br>"
    # escape minimal; if your report_text contains '<', it will render literally.
    # For now we keep it simple; you can html.escape() later if needed.
    lines = []
    lines.append('<div style="background:#faf6ff;padding:24px;border-radius:12px;'
                 'font-family:Georgia,serif;color:#2d2056;line-height:1.7;">')
    lines.append('<h2 style="text-align:center;margin:0 0 12px;">🌙 Your Sacred Numerology Report 🌙</h2>')
    lines.append('<div style="background:#fff;padding:20px;border-radius:12px;margin-top:8px;">')
    lines.append(f'<p style="margin:0 0 8px;"><strong>Name:</strong> {name}</p>')
    lines.append(f'<p style="margin:0 0 16px;"><strong>Birthdate:</strong> {birthdate}</p>')
    if spiritual_focus:
        lines.append(f'<p style="margin:0 0 16px;"><strong>Focus:</strong> {spiritual_focus}</p>')
    # report body as <br> lines
    safe = report_text.replace("\n", br)
    lines.append(f'<div style="white-space:normal;font-family:\'Courier New\',monospace;color:#3b2363;">{safe}</div>')
    lines.append('</div>')
    lines.append('<p style="margin-top:24px;">With infinite reverence,'
                 '<br><strong>Athyna Luna</strong>'
                 '<br><em>SacredSpace: Through The Cosmic Lens ✨</em></p>')
    lines.append('</div>')
    return "".join(lines)


def send_email_html(to_email: str, subject: str, html: str) -> None:
    import os
    import smtplib
    from email.message import EmailMessage

    smtp_host = os.getenv("SMTP_HOST", "smtp.ionos.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")  # e.g. you@yourdomain.com
    smtp_pass = os.getenv("SMTP_PASS")
    sender_email = os.getenv("SENDER_EMAIL", smtp_user)
    sender_name = os.getenv("SENDER_NAME", "Athyna Luna ✨")

    if not (smtp_user and smtp_pass and sender_email):
        # Fail loudly so you can see it in logs if env vars are missing
        raise RuntimeError("SMTP credentials/SENDER_EMAIL not configured in env")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"{sender_name} <{sender_email}>"
    msg["To"] = to_email

    # 1) Plain-text part (fallback for clients that don't render HTML)
    msg.set_content("Your sacred numerology report is attached as HTML.")

    # 2) HTML part (exactly ONE add_alternative)
    msg.add_alternative(html, subtype="html")

    # Send via SMTP with STARTTLS (no explicit SSL context needed)
    with smtplib.SMTP(smtp_host, smtp_port) as srv:
        srv.starttls()              # <-- if you had srv.starttls(context=context), change to this
        srv.login(smtp_user, smtp_pass)
        srv.send_message(msg)


# ---------------- Routes (NO TRIPLE QUOTES BELOW) ----------------
@app.get("/")
def root():
    return {"ok": True, "msg": "Soul API is alive 🌙"}


@app.post("/numerology/")
def numerology_report(data: BirthData):
    return {"report": generate_numerology_text(data)}


@app.post("/tally-webhook")
async def tally_webhook(req: Request):
    body = await req.json()
    answers = body.get("data", {}).get("answers", [])

    def by_ref(ref: str) -> Optional[str]:
        for a in answers:
            if a.get("field", {}).get("ref") == ref:
                return a.get("email") or a.get("text") or a.get("date")
        return None

    name = (by_ref("full_name") or "").strip()
    birthdate = (by_ref("birthdate") or "").strip()
    email = (by_ref("email") or "").strip()
    spiritual_focus = (by_ref("spiritual_focus") or "").strip()

    if not (name and birthdate and email):
        return {
            "ok": False,
            "msg": "Missing required fields from Tally",
            "got": {"name": name, "birthdate": birthdate, "email": email},
        }

    report_text = generate_numerology_text(BirthData(full_name=name, birthdate=birthdate))
    html = render_email_html(name, birthdate, spiritual_focus, report_text)
    send_email_html(email, "Your Sacred Numerology Report 🌙", html)
    return {"ok": True, "sent_to": email}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
