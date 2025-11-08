import logging
from openai import OpenAI
from fpdf import FPDF
from astrology_calc import calculate_chart
import os

logger = logging.getLogger(__name__)

def generate_report_content(name, birthdate, birthtime, birthplace, report_type, spiritual_focus):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY not set")
        raise ValueError("OPENAI_API_KEY not set")
    
    client = OpenAI(api_key=api_key)
    
    try:
        chart_data = calculate_chart(birthdate, birthtime, birthplace)
        logger.info(f"Chart calculated: {chart_data}")
    except Exception as e:
        logger.error(f"Error calculating chart: {e}")
        chart_data = {}
    
    planets = chart_data.get('planets', {})
    sun_sign = planets.get('sun', {}).get('sign', 'Unknown')
    sun_deg = planets.get('sun', {}).get('degree', 0)
    moon_sign = planets.get('moon', {}).get('sign', 'Unknown')
    moon_deg = planets.get('moon', {}).get('degree', 0)
    rising_sign = planets.get('rising', {}).get('sign', 'Unknown')
    rising_deg = planets.get('rising', {}).get('degree', 0)
    mercury_sign = planets.get('mercury', {}).get('sign', 'Unknown')
    venus_sign = planets.get('venus', {}).get('sign', 'Unknown')
    mars_sign = planets.get('mars', {}).get('sign', 'Unknown')
    jupiter_sign = planets.get('jupiter', {}).get('sign', 'Unknown')
    saturn_sign = planets.get('saturn', {}).get('sign', 'Unknown')
    north_node = planets.get('north_node', {}).get('sign', 'Unknown')
    south_node = planets.get('south_node', {}).get('sign', 'Unknown')
    chiron_sign = planets.get('chiron', {}).get('sign', 'Unknown')
    
    chart_summary = f"Sun {sun_sign} {sun_deg:.0f}°, Moon {moon_sign} {moon_deg:.0f}°, Rising {rising_sign} {rising_deg:.0f}°, Mercury {mercury_sign}, Venus {venus_sign}, Mars {mars_sign}, Jupiter {jupiter_sign}, Saturn {saturn_sign}, North Node {north_node}, South Node {south_node}, Chiron {chiron_sign}"
    
    if report_type == "Deep Dive Birth Chart":
        prompt = f"Create comprehensive 20-25 page DEEP DIVE BIRTH CHART for {name} born {birthdate} at {birthtime} in {birthplace}. ACTUAL CHART DATA: {chart_summary}. Include: Cosmic blueprint overview, Sun sign deep dive (identity, ego, purpose), Moon sign (emotions, needs, security), Rising sign (appearance, life path), planetary placements in houses (career, relationships, finances, home, creativity), major aspects and patterns, karmic lessons (North/South Node, Chiron), cosmic gifts and challenges, love patterns, career direction, shadow work with 5-7 journal prompts and rituals. Spiritual focus: {spiritual_focus}. BE SPECIFIC TO THESE ACTUAL PLACEMENTS."
    elif report_type == "Love Blueprint":
        prompt = f"Create 10-12 page LOVE BLUEPRINT for {name}. ACTUAL CHART: {chart_summary}. Include: Venus sign deep dive (love language, attraction, values), Mars placement (desire, passion, sexuality), 7th house partnership patterns, relationship patterns, love blocks and healing, sacred union blueprint, 3-4 love activation rituals. Spiritual focus: {spiritual_focus}. BE SPECIFIC TO VENUS IN {venus_sign} AND MARS IN {mars_sign}."
    elif report_type == "Career Code":
        prompt = f"Create 10-12 page CAREER CODE for {name}. ACTUAL CHART: {chart_summary}. Include: 10th house/Midheaven analysis, Sun in {sun_sign} career context, Mercury in {mercury_sign} skills, Saturn in {saturn_sign} discipline, Jupiter in {jupiter_sign} expansion, natural talents, challenges, ideal work environment, abundance activation, 5-year vision. Spiritual focus: {spiritual_focus}."
    elif report_type == "Life Purpose":
        prompt = f"Create 10-12 page LIFE PURPOSE for {name}. ACTUAL CHART: {chart_summary}. Include: Soul's calling (North Node in {north_node}), life mission blueprint, karmic contracts (South Node in {south_node}), spiritual gifts (Sun in {sun_sign}), shadow work, past life themes, Chiron in {chiron_sign} healing, purpose activation rituals, integration steps. Spiritual focus: {spiritual_focus}."
    elif report_type == "30 Day Outlook":
        prompt = f"Create 10-12 page 30 DAY OUTLOOK for {name} born {birthdate}. CHART: {chart_summary}. Include: Current transits overview, week-by-week forecast (4 weeks), key themes, challenges/opportunities, ritual recommendations, daily affirmations. Spiritual focus: {spiritual_focus}."
    elif report_type == "Cosmic Calendar":
        prompt = f"Create 8-10 page COSMIC CALENDAR for {name}. CHART: {chart_summary}. Include: Monthly overview, New Moon intentions, Full Moon release, weekly cosmic weather, daily alerts/rituals, affirmations, recommended practices. Spiritual focus: {spiritual_focus}."
    elif report_type == "Human Design":
        prompt = f"Create 50+ page HUMAN DESIGN for {name} born {birthdate} at {birthtime} in {birthplace}. Include: HD basics, Type & Strategy (5 pages), Authority (5 pages), Profile (5 pages), Channels (8 pages), Gates (10 pages), Lines (8 pages), career/relationship guidance, shadow work, 90-day experiment plan. Spiritual focus: {spiritual_focus}."
    elif report_type == "Starseed Lineage":
        prompt = f"Create 12-15 page STARSEED LINEAGE for {name}. CHART: {chart_summary}. Include: Starseed origins, galactic heritage/mission, planetary influences, starseed gifts, Earth integration challenges, cosmic contracts, activation rituals, connecting with star family. Spiritual focus: {spiritual_focus}."
    elif report_type == "Astrocartography":
        prompt = f"Create 20-40 page ASTROCARTOGRAPHY for {name} born {birthdate} at {birthtime} in {birthplace}. CHART: {chart_summary}. Include: Basics, personal power lines (Sun/Moon/Venus/Mars/Jupiter/Saturn), top 5 recommended locations with coordinates, locations to avoid, relocation impact, timing, integration rituals, 30-day relocation plan. Spiritual focus: {spiritual_focus}."
    elif report_type == "Shadow Work Workbook":
        prompt = f"Create 80+ page SHADOW WORK WORKBOOK for {name}. CHART: {chart_summary}. Include: Trauma-informed intro, shadow archetypes, 12 weeks of work (awareness, root causes, integration, transmutation, embodiment, mastery) with 15 journal prompts per 2-week block, weekly rituals, affirmations, resources. Spiritual focus: {spiritual_focus}."
    else:
        prompt = f"Create personalized {report_type} for {name} born {birthdate} at {birthtime} in {birthplace}. CHART: {chart_summary}. Spiritual focus: {spiritual_focus}. Write warm, mystical, empowering report."
    
    try:
        response = client.chat.completions.create(model="gpt-4", messages=[{"role": "user", "content": prompt}], max_tokens=4000)
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error generating {report_type}: {e}")
        return f"Unable to generate report. Error: {str(e)}"

def generate_pdf(name, birthdate, birthtime, birthplace, report_type, spiritual_focus, content):
    pdf = FPDF()
    pdf.add_page()
    
    logo_paths = ["logos/NEW_LOGO.png", "logos/NEW LOGO.png", "/opt/render/project/src/logos/NEW_LOGO.png", "/opt/render/project/src/logos/NEW LOGO.png"]
    
    for logo_path in logo_paths:
        if os.path.exists(logo_path):
            try:
                pdf.image(logo_path, x=150, y=10, w=50)
                logger.info(f"Logo added from: {logo_path}")
                break
            except Exception as e:
                logger.warning(f"Failed to add logo from {logo_path}: {e}")
    
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
