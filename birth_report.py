import logging
from openai import OpenAI
from fpdf import FPDF
from astrology_calc import calculate_chart
import os

logger = logging.getLogger(name)

def generate_report_content(name, birthdate, birthtime, birthplace, report_type, spiritual_focus):
    """Route to appropriate report generator based on type."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY not set")
        raise ValueError("OPENAI_API_KEY not set")

client = OpenAI(api_key=api_key)

try:
    chart_data = calculate_chart(birthdate, birthtime, birthplace)
except Exception as e:
    logger.error(f"Error calculating chart: {e}")
    chart_data = {}

# Route to appropriate generator
if report_type == "Deep Dive Birth Chart":
    return generate_deep_dive(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client)
elif report_type == "Love Blueprint":
    return generate_love_blueprint(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client)
elif report_type == "Career Code":
    return generate_career_code(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client)
elif report_type == "Life Purpose":
    return generate_life_purpose(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client)
elif report_type == "30 Day Outlook":
    return generate_30day_outlook(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client)
elif report_type == "Cosmic Calendar":
    return generate_cosmic_calendar(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client)
elif report_type == "Human Design":
    return generate_human_design(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client)
elif report_type == "Starseed Lineage":
    return generate_starseed_lineage(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client)
elif report_type == "Astrocartography":
    return generate_astrocartography(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client)
elif report_type == "Shadow Work Workbook":
    return generate_shadow_work_workbook(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client)
else:
    return generate_standard_report(name, birthdate, birthtime, birthplace, report_type, spiritual_focus, chart_data, client)

def generate_deep_dive(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client):
    """Generate 20-25 page Deep Dive Birth Chart."""
    sections = []
    prompts = {
        "overview": f"Create a compelling 2-3 paragraph COSMIC BLUEPRINT OVERVIEW for {name}. Include core cosmic identity, life theme, and spiritual mission. Chart: {chart_data}",
        "sun": f"Write 2-3 pages on SUN SIGN DEEP DIVE for {name}. Cover identity, ego expression, life purpose, creative power. Chart: {chart_data}",
        "moon": f"Write 2-3 pages on MOON SIGN & EMOTIONAL LANDSCAPE for {name}. Explore emotional nature, inner world, needs, security patterns. Chart: {chart_data}",
        "rising": f"Write 2-3 pages on RISING SIGN & LIFE PATH for {name}. Describe appearance, mask, first impressions, life direction. Chart: {chart_data}",
        "houses": f"Write 4-5 pages on PLANETARY PLACEMENTS IN HOUSES for {name}. Cover career, relationships, finances, home, creativity. Chart: {chart_data}",
        "aspects": f"Write 3-4 pages on MAJOR ASPECTS & COSMIC PATTERNS for {name}. Analyze conjunctions, trines, squares, oppositions. Chart: {chart_data}",
        "nodes": f"Write 2-3 pages on KARMIC LESSONS & SOUL MISSION for {name}. Explore North Node, South Node, Chiron. Chart: {chart_data}",
        "strengths": f"Write 2-3 pages on COSMIC GIFTS & CHALLENGES for {name}. Detail strengths, talents, challenges, growth edges. Chart: {chart_data}",
        "relationships": f"Write 2-3 pages on LOVE & RELATIONSHIPS PATTERNS for {name}. Analyze Venus, Mars, 7th house. Chart: {chart_data}",
        "career": f"Write 2-3 pages on CAREER & LIFE DIRECTION for {name}. Explore 10th house, Midheaven, career calling. Chart: {chart_data}",
        "integration": f"Write 2-3 pages on INTEGRATION & SHADOW WORK for {name}. Provide 5-7 prompts, rituals, practices. Focus: {spiritual_focus}",
    }

for section_name, prompt in prompts.items():
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000
        )
        sections.append(response.choices[0].message.content)
        logger.info(f"Generated {section_name} for {name}")
    except Exception as e:
        logger.error(f"Error generating {section_name}: {e}")
        sections.append(f"[Section unavailable]")

return "\n\n".join(sections)

def generate_love_blueprint(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client):
    """Generate 10-12 page Love Blueprint."""
    sections = []
    prompts = {
        "venus": f"Write 2 pages on VENUS SIGN DEEP DIVE for {name}. Explore love language, attraction style, values. Chart: {chart_data}",
        "mars": f"Write 1.5 pages on MARS PLACEMENT for {name}. Analyze desire, passion, sexuality, pursuit style. Chart: {chart_data}",
        "7th_house": f"Write 2 pages on 7TH HOUSE ANALYSIS for {name}. Describe partnership patterns, ideal partner blueprint. Chart: {chart_data}",
        "patterns": f"Write 1.5 pages on RELATIONSHIP PATTERNS for {name}. Identify recurring themes, past cycles, healing. Chart: {chart_data}",
        "blocks": f"Write 1.5 pages on LOVE BLOCKS & HEALING for {name}. Explore fears, blocks, growth edges compassionately. Chart: {chart_data}",
        "sacred_union": f"Write 1 page on SACRED UNION BLUEPRINT for {name}. Paint vision of ideal partnership. Chart: {chart_data}",
        "rituals": f"Write 1 page on LOVE ACTIVATION RITUALS for {name}. Provide 3-4 rituals to magnetize love. Focus: {spiritual_focus}",
    }

for section_name, prompt in prompts.items():
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2500
        )
        sections.append(response.choices[0].message.content)
        logger.info(f"Generated {section_name} for {name}")
    except Exception as e:
        logger.error(f"Error generating {section_name}: {e}")
        sections.append(f"[Section unavailable]")

return "\n\n".join(sections)

def generate_career_code(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client):
    """Generate 10-12 page Career Code."""
    sections = []
    prompts = {
        "midheaven": f"Write 2 pages on 10TH HOUSE & MIDHEAVEN for {name}. Describe public image, career calling, life direction. Chart: {chart_data}",
        "sun_career": f"Write 1.5 pages on SUN SIGN IN CAREER for {name}. Explain gifts, leadership style, professional shine. Chart: {chart_data}",
        "planets_work": f"Write 2 pages on PLANETARY PLACEMENTS FOR WORK for {name}. Analyze Mercury, Mars, Jupiter. Chart: {chart_data}",
        "talents": f"Write 1.5 pages on NATURAL TALENTS & SUPERPOWERS for {name}. Detail unique gifts, competitive advantages. Chart: {chart_data}",
        "challenges": f"Write 1.5 pages on CAREER CHALLENGES for {name}. Explore obstacles, growth edges, development areas. Chart: {chart_data}",
        "environment": f"Write 1 page on IDEAL WORK ENVIRONMENT for {name}. Describe culture, team dynamics, thriving settings. Chart: {chart_data}",
        "abundance": f"Write 1 page on ABUNDANCE & PROSPERITY ACTIVATION for {name}. Provide rituals and practices. Focus: {spiritual_focus}",
        "vision": f"Write 0.5 pages on 5-YEAR CAREER VISION for {name}. Outline trajectory and action steps. Chart: {chart_data}",
    }

for section_name, prompt in prompts.items():
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2500
        )
        sections.append(response.choices[0].message.content)
        logger.info(f"Generated {section_name} for {name}")
    except Exception as e:
        logger.error(f"Error generating {section_name}: {e}")
        sections.append(f"[Section unavailable]")

return "\n\n".join(sections)

def generate_life_purpose(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client):
    """Generate 10-12 page Life Purpose."""
    sections = []
    prompts = {
        "calling": f"Write 2 pages on SOUL'S CALLING for {name}. Explore North Node, chart ruler, life mission. Chart: {chart_data}",
        "mission": f"Write 2 pages on LIFE MISSION BLUEPRINT for {name}. Describe unique purpose and why they're here. Chart: {chart_data}",
        "karma": f"Write 1.5 pages on KARMIC CONTRACTS & LESSONS for {name}. Identify soul agreements and lessons. Chart: {chart_data}",
        "gifts": f"Write 1.5 pages on SPIRITUAL GIFTS & SUPERPOWERS for {name}. Detail unique spiritual abilities. Chart: {chart_data}",
        "shadow": f"Write 1.5 pages on SHADOW WORK FOR SOUL EVOLUTION for {name}. Explore shadow aspects and integration. Chart: {chart_data}",
        "past_life": f"Write 1 page on PAST LIFE THEMES for {name}. Describe South Node patterns and releases. Chart: {chart_data}",
        "rituals": f"Write 1 page on PURPOSE ACTIVATION RITUALS for {name}. Provide ceremonies and practices. Focus: {spiritual_focus}",
        "steps": f"Write 0.5 pages on INTEGRATION & NEXT STEPS for {name}. Clear action steps for living purpose. Chart: {chart_data}",
    }

for section_name, prompt in prompts.items():
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2500
        )
        sections.append(response.choices[0].message.content)
        logger.info(f"Generated {section_name} for {name}")
    except Exception as e:
        logger.error(f"Error generating {section_name}: {e}")
        sections.append(f"[Section unavailable]")

return "\n\n".join(sections)

def generate_30day_outlook(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client):
    """Generate 10-12 page 30 Day Outlook."""
    sections = []
    prompts = {
        "overview": f"Write 1 page on CURRENT PLANETARY TRANSITS OVERVIEW for {name}. Explain major transits this month. Chart: {chart_data}",
        "weekly": f"Write 6 pages on WEEK-BY-WEEK FORECAST for {name}. Cover 4 weeks with themes, challenges, opportunities, affirmations. Chart: {chart_data}",
        "themes": f"Write 1 page on KEY THEMES & COSMIC WEATHER for {name}. Summarize month's overall energy. Chart: {chart_data}",
        "opportunities": f"Write 1 page on CHALLENGES & OPPORTUNITIES for {name}. Identify obstacles and growth opportunities. Chart: {chart_data}",
        "rituals": f"Write 1 page on RITUAL RECOMMENDATIONS for {name}. Suggest 3-4 rituals aligned to energy. Focus: {spiritual_focus}",
        "affirmations": f"Write 1 page on DAILY AFFIRMATIONS & MANTRAS for {name}. Provide affirmations for each week. Chart: {chart_data}",
    }

for section_name, prompt in prompts.items():
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2500
        )
        sections.append(response.choices[0].message.content)
        logger.info(f"Generated {section_name} for {name}")
    except Exception as e:
        logger.error(f"Error generating {section_name}: {e}")
        sections.append(f"[Section unavailable]")

return "\n\n".join(sections)

def generate_cosmic_calendar(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client):
    """Generate 8-10 page Cosmic Calendar."""
    prompt = f"""Create a personalized 8-10 page COSMIC CALENDAR for {name}.

SECTIONS:





Monthly Overview & Theme (1 page)



New Moon Intentions (1 page)



Full Moon Release Work (1 page)



Weekly Cosmic Weather (2 pages)



Daily Cosmic Alerts & Rituals (2 pages)



Affirmations & Mantras (1 page)



Recommended Practices (1 page)

Make it practical, mystical, actionable, and themed.
Chart: {chart_data}
Focus: {spiritual_focus}"""

try:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=3500
    )
    return response.choices[0].message.content
except Exception as e:
    logger.error(f"Error generating cosmic calendar: {e}")
    return f"Unable to generate calendar. Error: {str(e)}"

def generate_human_design(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client):
    """Generate 50-180 page Human Design Reading."""
    sections = []
    prompts = {
        "basics": f"Write 3 pages on HD BASICS EXPLAINED for {name}. Cover Type, Strategy, Authority. Chart: {chart_data}",
        "type": f"Write 5 pages on YOUR TYPE & STRATEGY for {name}. Explain decision-making process. Chart: {chart_data}",
        "authority": f"Write 5 pages on YOUR AUTHORITY for {name}. Describe emotional, sacral, intuitive, etc. Chart: {chart_data}",
        "profile": f"Write 5 pages on YOUR PROFILE for {name}. Explain life theme and role in relationships. Chart: {chart_data}",
        "channels": f"Write 8 pages on YOUR CHANNELS for {name}. Describe how energy flows through them. Chart: {chart_data}",
        "gates": f"Write 10 pages on YOUR GATES for {name}. Detail specific gifts and challenges. Chart: {chart_data}",
        "lines": f"Write 8 pages on YOUR LINES for {name}. Explain how they operate in each gate. Chart: {chart_data}",
        "career": f"Write 5 pages on CAREER & RELATIONSHIP GUIDANCE via HD for {name}. Chart: {chart_data}",
        "shadow": f"Write 5 pages on SHADOW WORK & INTEGRATION for {name}. Focus: {spiritual_focus}",
        "experiment": f"Write 5 pages on 90-DAY EXPERIMENT PLAN for {name}. Provide actionable steps. Chart: {chart_data}",
    }

for section_name, prompt in prompts.items():
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3500
        )
        sections.append(response.choices[0].message.content)
        logger.info(f"Generated {section_name} for {name}")
    except Exception as e:
        logger.error(f"Error generating {section_name}: {e}")
        sections.append(f"[Section unavailable]")

return "\n\n".join(sections)

def generate_starseed_lineage(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client):
    """Generate 12-15 page Starseed Lineage."""
    sections = []
    prompts = {
        "origins": f"Write 2 pages on STARSEED ORIGINS & LINEAGE for {name}. Identify star origins and heritage. Chart: {chart_data}",
        "mission": f"Write 2 pages on GALACTIC HERITAGE & MISSION for {name}. Describe cosmic purpose. Chart: {chart_data}",
        "planets": f"Write 1.5 pages on PLANETARY INFLUENCES for {name}. Analyze Pluto, Chiron, outer planets. Chart: {chart_data}",
        "gifts": f"Write 1.5 pages on STARSEED GIFTS & SUPERPOWERS for {name}. Detail cosmic abilities. Chart: {chart_data}",
        "challenges": f"Write 1.5 pages on EARTH INTEGRATION CHALLENGES for {name}. Explore being starseed on Earth. Chart: {chart_data}",
        "contracts": f"Write 1.5 pages on COSMIC CONTRACTS & SOUL AGREEMENTS for {name}. Describe missions. Chart: {chart_data}",
        "rituals": f"Write 1 page on ACTIVATION RITUALS & PRACTICES for {name}. Provide ceremonies. Focus: {spiritual_focus}",
        "connection": f"Write 1 page on CONNECTING WITH YOUR STAR FAMILY for {name}. Guidance for cosmic connection. Chart: {chart_data}",
    }

for section_name, prompt in prompts.items():
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2500
        )
        sections.append(response.choices[0].message.content)
        logger.info(f"Generated {section_name} for {name}")
    except Exception as e:
        logger.error(f"Error generating {section_name}: {e}")
        sections.append(f"[Section unavailable]")

return "\n\n".join(sections)

def generate_astrocartography(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client):
    """Generate 20-40 page Astrocartography Report."""
    sections = []
    prompts = {
        "basics": f"Write 2 pages on ASTROCARTOGRAPHY BASICS for {name}. Explain power lines. Chart: {chart_data}",
        "lines": f"Write 5 pages on PERSONAL POWER LINES for {name}. Analyze Sun, Moon, Venus, Mars, Jupiter, Saturn. Chart: {chart_data}",
        "locations": f"Write 10 pages on TOP 5 RECOMMENDED LOCATIONS for {name}. Include coordinates, alignment, experiences. Chart: {chart_data}",
        "avoid": f"Write 3 pages on LOCATIONS TO AVOID for {name}. Explain compassionately. Chart: {chart_data}",
        "impact": f"Write 3 pages on RELOCATION IMPACT ANALYSIS for {name}. Describe life changes. Chart: {chart_data}",
        "timing": f"Write 2 pages on TIMING FOR RELOCATION for {name}. Provide optimal timing. Chart: {chart_data}",
        "integration": f"Write 2 pages on INTEGRATION & ACTIVATION for {name}. Provide rituals. Focus: {spiritual_focus}",
        "ritual_plan": f"Write 3 pages on 30-DAY RELOCATION RITUAL PLAN for {name}. Day-by-day practices. Chart: {chart_data}",
    }

for section_name, prompt in prompts.items():
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000
        )
        sections.append(response.choices[0].message.content)
        logger.info(f"Generated {section_name} for {name}")
    except Exception as e:
        logger.error(f"Error generating {section_name}: {e}")
        sections.append(f"[Section unavailable]")

return "\n\n".join(sections)

def generate_shadow_work_workbook(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client):
    """Generate 80-260 page Shadow Work Workbook."""
    sections = []
    prompts = {
        "intro": f"Write 3 pages on INTRODUCTION TO SHADOW WORK for {name}. Make it trauma-informed. Chart: {chart_data}",
        "archetypes": f"Write 5 pages on SHADOW ARCHETYPES for {name}. Based on their chart. Chart: {chart_data}",
        "week1": f"Write 8 pages on WEEK 1-2: AWARENESS & RECOGNITION for {name}. Include 15 journal prompts. Chart: {chart_data}",
        "week3": f"Write 8 pages on WEEK 3-4: ROOT CAUSES & ORIGINS for {name}. Include 15 journal prompts. Chart: {chart_data}",
        "week5": f"Write 8 pages on WEEK 5-6: INTEGRATION & ACCEPTANCE for {name}. Include 15 journal prompts. Chart: {chart_data}",
        "week7": f"Write 8 pages on WEEK 7-8: TRANSMUTATION & HEALING for {name}. Include 15 journal prompts. Chart: {chart_data}",
        "week9": f"Write 8 pages on WEEK 9-10: EMBODIMENT & EXPRESSION for {name}. Include 15 journal prompts. Chart: {chart_data}",
        "week11": f"Write 8 pages on WEEK 11-12: MASTERY & EMPOWERMENT for {name}. Include 15 journal prompts. Chart: {chart_data}",
        "rituals": f"Write 5 pages on WEEKLY RITUALS & CEREMONIES for {name}. Provide 12 rituals. Focus: {spiritual_focus}",
        "affirmations": f"Write 3 pages on AFFIRMATIONS & MANTRAS for {name}. By shadow theme. Chart: {chart_data}",
        "resources": f"Write 2 pages on RESOURCES & SUPPORT for {name}. Provide guidance. Chart: {chart_data}",
    }

for section_name, prompt in prompts.items():
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000
        )
        sections.append(response.choices[0].message.content)
        logger.info(f"Generated {section_name} for {name}")
    except Exception as e:
        logger.error(f"Error generating {section_name}: {e}")
        sections.append(f"[Section unavailable]")

return "\n\n".join(sections)

def generate_standard_report(name, birthdate, birthtime, birthplace, report_type, spiritual_focus, chart_data, client):
    """Fallback for any other report types."""
    prompt = f"""Create a personalized {report_type} report for {name} born {birthdate} at {birthtime} in {birthplace}.
Spiritual focus: {spiritual_focus}
Chart data: {chart_data}
Write a warm, mystical, and empowering report addressing their spiritual question."""

try:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000
    )
    return response.choices[0].message.content
except Exception as e:
    logger.error(f"Error generating {report_type}: {e}")
    return f"Unable to generate report. Error: {str(e)}"

def generate_pdf(name, birthdate, birthtime, birthplace, report_type, spiritual_focus, content):
    """Generate PDF report with logo and content."""
    pdf = FPDF()
    pdf.add_page()

logo_paths = [
    "logos/NEW_LOGO.png",
    "logos/NEW LOGO.png",
    "/opt/render/project/src/logos/NEW_LOGO.png",
    "/opt/render/project/src/logos/NEW LOGO.png"
]

logo_added = False
for logo_path in logo_paths:
    if os.path.exists(logo_path):
        try:
            pdf.image(logo_path, x=150, y=10, w=50)
            logger.info(f"Logo added from: {logo_path}")
            logo_added = True
            break
        except Exception as e:
            logger.warning(f"Failed to add logo from {logo_path}: {e}")

if not logo_added:
    logger.warning(f"Logo not found in paths: {logo_paths}")

pdf.set_font("Helvetica", "B", 16)
pdf.cell(0, 10, f"{report_type}", ln=True, align="C")
pdf.set_font("Helvetica", "", 10)
pdf.cell(0, 5, f"For: {name}", ln=True, align="C")
pdf.cell(0, 5, f"Born: {birthdate} at {birthtime} in {birthplace}", ln=True, align="C")
pdf.ln(5)

pdf.set_font("Helvetica", "", 9)
content_clean = content.encode('latin-1', errors='replace').decode('latin-1')
pdf.multi_cell(0, 5, content_clean)

filename = f"/tmp/{name.replace(' ', '_')}_chart.pdf"
pdf.output(filename)
logger.info(f"PDF generated: {filename}")
return filename