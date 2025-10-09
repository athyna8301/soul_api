from fastapi import Request
def send_email_html(to_email: str, subject: str, html: str):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    sender_email = os.getenv("SENDER_EMAIL")
    sender_name = os.getenv("SENDER_NAME", "Athyna Luna ✨")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"{sender_name} <{sender_email}>"
    msg["To"] = to_email
    msg.set_content("Your sacred numerology report is attached as HTML.")
    msg.add_alternative(html, subtype="html")

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls(context=context)
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)


def render_email_html(name: str, birthdate: str, spiritual_focus: str, report_html: str) -> str:
    # If your generator returns plain text, uncomment the next line to convert newlines → <br>
    # if "<" not in report_html: report_html = report_html.replace("\n", "<br>")
    return f"""
    <div style="background:#faf6ff;padding:24px;border-radius:14px;
                font-family:Georgia,serif;color:#2d2056;line-height:1.6">
      <h2 style="text-align:center;margin:0 0 12px">🌙 Your Sacred Numerology Report 🌙</h2>
      <p><strong>Name:</strong> {name}<br><strong>DOB:</strong> {birthdate}</p>
      {"<p><em>Focus: " + spiritual_focus + "</em></p>" if spiritual_focus else ""}
      <div style="background:#fff;padding:20px;border-radius:12px;border:1px solid #ede7fb">
        {report_html}
      </div>
      <p style="margin-top:24px">With infinite reverence,<br>
         <strong>Athyna Luna</strong><br>
         <em>SacredSpace: Through The Cosmic Lens ✨</em>
      </p>
    </div>
    """

@app.post("/tally-webhook")
async def tally_webhook(req: Request):
    body = await req.json()
    answers = body.get("data", {}).get("answers", [])

    def by_ref(ref: str):
        for a in answers:
            if a.get("field", {}).get("ref") == ref:
                # Tally may put the value in one of these keys depending on field type
                return a.get("email") or a.get("text") or a.get("date")
        return None

    name = by_ref("full_name")
    birthdate = by_ref("birthdate")
    email = by_ref("email")
    spiritual_focus = by_ref("spiritual_focus") or ""

    # basic validation
    if not (name and birthdate and email):
        return {"ok": False, "msg": "Missing required fields from Tally"}

    # Reuse your existing generator + email sender
    report = generate_numerology_text(BirthData(full_name=name, birthdate=birthdate))
html = render_email_html(name, birthdate, spiritual_focus, report)
send_email_html(email, "✨ Your Sacred Numerology Report ✨", html)
return {"ok": True}

