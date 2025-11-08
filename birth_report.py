import logging
from openai import OpenAI
from fpdf import FPDF
from astrology_calc import calculate_chart
import os

logger = logging.getLogger(__name__)

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
        "overview": f"Create a compelling 2-3 paragraph COSMIC BLUEPRINT OVERVIEW for {name}. Include core cosmic identity, life theme, and spiritual mission.",
        "sun": f"Write 2-3 pages on SUN SIGN DEEP DIVE for {name}. Cover identity, ego expression, life purpose, creative power.",
        "moon": f"Write 2-3 pages on MOON SIGN & EMOTIONAL LANDSCAPE for {name}. Explore emotional nature, inner world, needs, security patterns.",
        "rising": f"Write 2-3 pages on RISING SIGN & LIFE PATH for {name}. Describe appearance, mask, first impressions, life direction.",
        "houses": f"Write 4-5 pages on PLANETARY PLACEMENTS IN HOUSES for {name}. Cover career, relationships, finances, home, creativity.",
        "aspects": f"Write 3-4 pages on MAJOR ASPECTS & COSMIC PATTERNS for {name}. Analyze conjunctions, trines, squares, oppositions.",
        "nodes": f"Write 2-3 pages on KARMIC LESSONS & SOUL MISSION for {name}. Explore North Node, South Node, Chiron.",
        "strengths": f"Write 2-3 pages on COSMIC GIFTS & CHALLENGES for {name}. Detail strengths, talents, challenges, growth edges.",
        "relationships": f"Write 2-3 pages on LOVE & RELATIONSHIPS PATTERNS for {name}. Analyze Venus, Mars, 7th house.",
        "career": f"Write 2-3 pages on CAREER & LIFE DIRECTION for {name}. Explore 10th house, Midheaven, career calling.",
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
            sections.append("[Section unavailable]")
    
    return "\n\n".join(sections)

def generate_love_blueprint(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client):
    """Generate 10-12 page Love Blueprint."""
    sections = []
    prompts = {
        "venus": f"Write 2 pages on VENUS SIGN DEEP DIVE for {name}. Explore love language, attraction style, values.",
        "mars": f"Write 1.5 pages on MARS PLACEMENT for {name}. Analyze desire, passion, sexuality, pursuit style.",
        "7th_house": f"Write 2 pages on 7TH HOUSE ANALYSIS for {name}. Describe partnership patterns, ideal partner blueprint.",
        "patterns": f"Write 1.5 pages on RELATIONSHIP PATTERNS for {name}. Identify recurring themes, past cycles, healing.",
        "blocks": f"Write 1.5 pages on LOVE BLOCKS & HEALING for {name}. Explore fears, blocks, growth edges compassionately.",
        "sacred_union": f"Write 1 page on SACRED UNION BLUEPRINT for {name}. Paint vision of ideal partnership.",
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
            sections.append("[Section unavailable]")
    
    return "\n\n".join(sections)

def generate_career_code(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client):
    """Generate 10-12 page Career Code."""
    prompt = f"Create a comprehensive 10-12 page CAREER CODE report for {name}. Include: 10th House/Midheaven analysis, Sun in career, Mercury/Mars/Jupiter placements, natural talents, challenges, ideal work environment, abundance activation, and 5-year vision. Focus: {spiritual_focus}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3500
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error generating career code: {e}")
        return f"Unable to generate report. Error: {str(e)}"

def generate_life_purpose(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client):
    """Generate 10-12 page Life Purpose."""
    prompt = f"Create a profound 10-12 page LIFE PURPOSE report for {name}. Include: Soul's calling, life mission blueprint, karmic contracts, spiritual gifts, shadow work, past life themes, purpose activation rituals, and integration steps. Focus: {spiritual_focus}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3500
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error generating life purpose: {e}")
        return f"Unable to generate report. Error: {str(e)}"

def generate_30day_outlook(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client):
    """Generate 10-12 page 30 Day Outlook."""
    prompt = f"Create a detailed 10-12 page 30 DAY OUTLOOK for {name}. Include: Current transits overview, week-by-week forecast (4 weeks), key themes, challenges/opportunities, ritual recommendations, and daily affirmations. Focus: {spiritual_focus}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3500
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error generating 30 day outlook: {e}")
        return f"Unable to generate report. Error: {str(e)}"

def generate_cosmic_calendar(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client):
    """Generate 8-10 page Cosmic Calendar."""
    prompt = f"Create a personalized 8-10 page COSMIC CALENDAR for {name}. Include: Monthly overview, New Moon intentions, Full Moon release, weekly cosmic weather, daily alerts/rituals, affirmations, and recommended practices. Focus: {spiritual_focus}"
    
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
    """Generate 50+ page Human Design Reading."""
    prompt = f"Create a comprehensive 50+ page HUMAN DESIGN READING for {name}. Include: HD basics, Type & Strategy (5 pages), Authority (5 pages), Profile (5 pages), Channels (8 pages), Gates (10 pages), Lines (8 pages), career/relationship guidance, shadow work, and 90-day experiment plan. Focus: {spiritual_focus}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error generating human design: {e}")
        return f"Unable to generate report. Error: {str(e)}"

def generate_starseed_lineage(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client):
    """Generate 12-15 page Starseed Lineage."""
    prompt = f"Create a mystical 12-15 page STARSEED LINEAGE report for {name}. Include: Starseed origins, galactic heritage/mission, planetary influences, starseed gifts, Earth integration challenges, cosmic contracts, activation rituals, and connecting with star family. Focus: {spiritual_focus}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3500
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error generating starseed lineage: {e}")
        return f"Unable to generate report. Error: {str(e)}"

def generate_astrocartography(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client):
    """Generate 20-40 page Astrocartography Report."""
    prompt = f"Create a detailed 20-40 page ASTROCARTOGRAPHY REPORT for {name}. Include: Basics, personal power lines (Sun/Moon/Venus/Mars/Jupiter/Saturn), top 5 recommended locations with coordinates, locations to avoid, relocation impact, timing, integration rituals, and 30-day relocation plan. Focus: {spiritual_focus}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error generating astrocartography: {e}")
        return f"Unable to generate report. Error: {str(e)}"

def generate_shadow_work_workbook(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client):
    """Generate 80+ page Shadow Work Workbook."""
    prompt = f"Create a transformative 80+ page SHADOW WORK WORKBOOK for {name}. Include: Trauma-informed intro, shadow archetypes, 12 weeks of work (awareness, root causes, integration, transmutation, embodiment, mastery) with 15 journal prompts per 2-week block, weekly rituals, affirmations, and resources. Focus: {spiritual_focus}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error generating shadow work workbook: {e}")
        return f"Unable to generate workbook. Error: {str(e)}"

def generate_standard_report(name, birthdate, birthtime, birthplace, report_type, spiritual_focus, chart_data, client):
    """Fallback for any other report types."""
    prompt = f"Create a personalized {report_type} report for {name} born {birthdate} at {birthtime} in {birthplace}. Spiritual focus: {spiritual_focus}. Write a warm, mystical, and empowering report addressing their spiritual question."
    
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
