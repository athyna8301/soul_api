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
    
    sun_sign = planets.get('Sun', {}).get('sign', 'Unknown')
    sun_deg = planets.get('Sun', {}).get('degree', 0)
    moon_sign = planets.get('Moon', {}).get('sign', 'Unknown')
    moon_deg = planets.get('Moon', {}).get('degree', 0)
    mercury_sign = planets.get('Mercury', {}).get('sign', 'Unknown')
    mercury_deg = planets.get('Mercury', {}).get('degree', 0)
    venus_sign = planets.get('Venus', {}).get('sign', 'Unknown')
    venus_deg = planets.get('Venus', {}).get('degree', 0)
    mars_sign = planets.get('Mars', {}).get('sign', 'Unknown')
    mars_deg = planets.get('Mars', {}).get('degree', 0)
    jupiter_sign = planets.get('Jupiter', {}).get('sign', 'Unknown')
    jupiter_deg = planets.get('Jupiter', {}).get('degree', 0)
    saturn_sign = planets.get('Saturn', {}).get('sign', 'Unknown')
    saturn_deg = planets.get('Saturn', {}).get('degree', 0)
    north_node_sign = planets.get('North Node', {}).get('sign', 'Unknown')
    north_node_deg = planets.get('North Node', {}).get('degree', 0)
    chiron_sign = planets.get('Chiron', {}).get('sign', 'Unknown')
    chiron_deg = planets.get('Chiron', {}).get('degree', 0)
    
    houses = chart_data.get('houses', {})
    ascendant_deg = houses.get('ascendant', 0)
    mc_deg = houses.get('mc', 0)
    
    rising_sign = get_sign_from_degree(ascendant_deg)
    mc_sign = get_sign_from_degree(mc_deg)
    
    logger.info(f"Extracted: Sun {sun_sign} {sun_deg:.1f}°, Moon {moon_sign} {moon_deg:.1f}°, Rising {rising_sign}")
    
    if report_type == "Deep Dive Birth Chart":
        prompt = f"""Create a comprehensive 20-25 page DEEP DIVE BIRTH CHART for {name}.

BIRTH DATA:
- Born: {birthdate} at {birthtime} in {birthplace}
- Spiritual Focus: {spiritual_focus}

ACTUAL PLANETARY PLACEMENTS (DO NOT IGNORE - USE THESE EXACT PLACEMENTS):
- Sun in {sun_sign} at {sun_deg:.1f}°
- Moon in {moon_sign} at {moon_deg:.1f}°
- Rising (Ascendant) in {rising_sign} at {ascendant_deg:.1f}°
- Mercury in {mercury_sign} at {mercury_deg:.1f}°
- Venus in {venus_sign} at {venus_deg:.1f}°
- Mars in {mars_sign} at {mars_deg:.1f}°
- Jupiter in {jupiter_sign} at {jupiter_deg:.1f}°
- Saturn in {saturn_sign} at {saturn_deg:.1f}°
- North Node in {north_node_sign} at {north_node_deg:.1f}°
- Chiron in {chiron_sign} at {chiron_deg:.1f}°
- Midheaven in {mc_sign} at {mc_deg:.1f}°

REQUIRED SECTIONS (BE SPECIFIC TO THESE EXACT PLACEMENTS):
1. COSMIC BLUEPRINT OVERVIEW (2-3 pages): Core identity, life theme, spiritual mission based on Sun {sun_sign}, Moon {moon_sign}, Rising {rising_sign}
2. SUN SIGN DEEP DIVE (2-3 pages): {sun_sign} at {sun_deg:.1f}° - identity, ego expression, life purpose, creative power
3. MOON SIGN (2-3 pages): {moon_sign} at {moon_deg:.1f}° - emotional nature, inner world, security patterns
4. RISING SIGN (2 pages): {rising_sign} at {ascendant_deg:.1f}° - appearance, mask, first impressions, life direction
5. PLANETARY PLACEMENTS (4-5 pages): Mercury {mercury_sign}, Venus {venus_sign}, Mars {mars_sign}, Jupiter {jupiter_sign}, Saturn {saturn_sign} - career, relationships, finances, home, creativity
6. MAJOR ASPECTS (3-4 pages): Analyze conjunctions, trines, squares, oppositions between these planets
7. KARMIC LESSONS (2-3 pages): North Node {north_node_sign}, Chiron {chiron_sign} - soul lessons, past patterns, healing
8. COSMIC GIFTS & CHALLENGES (2-3 pages): Strengths, talents, challenges, growth edges
9. LOVE PATTERNS (2-3 pages): Venus {venus_sign}, Mars {mars_sign} - love language, attraction, relationship style
10. CAREER & LIFE DIRECTION (2-3 pages): Sun {sun_sign}, Mercury {mercury_sign}, Saturn {saturn_sign}, Midheaven {mc_sign} - career calling, talents, ideal work
11. SHADOW WORK & INTEGRATION (2-3 pages): 5-7 journal prompts, rituals, practices specific to these placements

CRITICAL: Do NOT say you need more information. You have all the data. Use these exact placements to create a personalized, detailed, specific analysis."""
    
    elif report_type == "Love Blueprint":
        prompt = f"""Create a 10-12 page LOVE BLUEPRINT for {name}.

ACTUAL CHART DATA:
- Venus in {venus_sign} at {venus_deg:.1f}°
- Mars in {mars_sign} at {mars_deg:.1f}°
- Moon in {moon_sign} at {moon_deg:.1f}°
- Spiritual Focus: {spiritual_focus}

SECTIONS:
1. VENUS SIGN (2 pages): {venus_sign} at {venus_deg:.1f}° - love language, attraction, values, what you need in relationships
2. MARS PLACEMENT (1.5 pages): {mars_sign} at {mars_deg:.1f}° - desire, passion, sexuality, how you pursue
3. PARTNERSHIP PATTERNS (2 pages): Moon {moon_sign}, Venus {venus_sign}, Mars {mars_sign} - your relationship style
4. RELATIONSHIP BLOCKS & HEALING (1.5 pages): Fears, blocks, growth edges
5. SACRED UNION BLUEPRINT (1 page): Vision of ideal partnership
6. LOVE ACTIVATION RITUALS (1 page): 3-4 specific rituals for magnetizing love
7. INTEGRATION (1.5 pages): Journal prompts and practices

Use ONLY these exact placements. Do NOT ask for more data."""
    
    elif report_type == "Career Code":
        prompt = f"""Create 10-12 page CAREER CODE for {name}.

ACTUAL CHART DATA:
- Sun in {sun_sign} at {sun_deg:.1f}°
- Mercury in {mercury_sign} at {mercury_deg:.1f}°
- Saturn in {saturn_sign} at {saturn_deg:.1f}°
- Jupiter in {jupiter_sign} at {jupiter_deg:.1f}°
- Midheaven in {mc_sign} at {mc_deg:.1f}°
- Spiritual Focus: {spiritual_focus}

SECTIONS:
1. CAREER CALLING (3 pages): Based on Sun {sun_sign}, Midheaven {mc_sign}
2. NATURAL TALENTS (2 pages): Mercury {mercury_sign}, Jupiter {jupiter_sign}
3. DISCIPLINE & STRUCTURE (2 pages): Saturn {saturn_sign} - how you build
4. IDEAL WORK ENVIRONMENT (1.5 pages): What brings fulfillment
5. CHALLENGES & GROWTH (1.5 pages): Saturn {saturn_sign} lessons
6. ABUNDANCE ACTIVATION (1 page): Rituals and practices
7. 5-YEAR VISION (1.5 pages): Your career evolution

Use these exact placements. Be specific."""
    
    elif report_type == "Life Purpose":
        prompt = f"""Create 10-12 page LIFE PURPOSE for {name}.

ACTUAL CHART DATA:
- Sun in {sun_sign} at {sun_deg:.1f}°
- North Node in {north_node_sign} at {north_node_deg:.1f}°
- Chiron in {chiron_sign} at {chiron_deg:.1f}°
- Spiritual Focus: {spiritual_focus}

SECTIONS:
1. SOUL'S CALLING (3 pages): North Node {north_node_sign} - your destiny
2. LIFE MISSION (2 pages): Sun {sun_sign} - your core purpose
3. CHIRON HEALING (2 pages): {chiron_sign} at {chiron_deg:.1f}° - your wounded healer gift
4. PAST LIFE PATTERNS (2 pages): What you're here to transcend
5. PURPOSE ACTIVATION RITUALS (1.5 pages): Practices to embody your mission
6. SHADOW WORK (1.5 pages): Journal prompts and integration
7. YOUR COSMIC ROLE (1 page): How you serve the world

Use these exact placements. Do NOT ask for more data."""
    
    else:
        prompt = f"""Create personalized {report_type} for {name} born {birthdate} at {birthtime} in {birthplace}.

CHART DATA: Sun {sun_sign} {sun_deg:.1f}°, Moon {moon_sign} {moon_deg:.1f}°, Rising {rising_sign}, Mercury {mercury_sign}, Venus {venus_sign}, Mars {mars_sign}, Jupiter {jupiter_sign}, Saturn {saturn_sign}, North Node {north_node_sign}, Chiron {chiron_sign}.

Spiritual focus: {spiritual_focus}

Write warm, mystical, empowering report using THESE EXACT PLACEMENTS."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error generating {report_type}: {e}")
        return f"Unable to generate report. Error: {str(e)}"

def get_sign_from_degree(degree):
    """Convert zodiac degree to sign."""
    signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    sign_index = int(degree / 30)
    return signs[sign_index % 12]

def generate_pdf(name, birthdate, birthtime, birthplace, report_type, spiritual_focus, content):
    pdf = FPDF()
    pdf.add_page()
    
    logo_paths = ["logos/NEW_LOGO.png", "logos/NEW LOGO.png", "/opt/render/project/src/logos/NEW_LOGO.png"]
    
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
