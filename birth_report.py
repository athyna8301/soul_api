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
        prompt = f"""You are an expert astrologer. Write a comprehensive, detailed 20-25 page DEEP DIVE BIRTH CHART for {name}.

THIS IS YOUR TASK. You MUST complete it fully. Do not say you cannot do this. You have all the data you need.

BIRTH INFORMATION:
Name: {name}
Birthdate: {birthdate}
Birth Time: {birthtime}
Birth Place: {birthplace}
Spiritual Focus: {spiritual_focus}

COMPLETE ASTROLOGICAL DATA (Use this data - it is accurate and complete):
Sun: {sun_sign} at {sun_deg:.2f}°
Moon: {moon_sign} at {moon_deg:.2f}°
Rising/Ascendant: {rising_sign} at {ascendant_deg:.2f}°
Mercury: {mercury_sign} at {mercury_deg:.2f}°
Venus: {venus_sign} at {venus_deg:.2f}°
Mars: {mars_sign} at {mars_deg:.2f}°
Jupiter: {jupiter_sign} at {jupiter_deg:.2f}°
Saturn: {saturn_sign} at {saturn_deg:.2f}°
North Node: {north_node_sign} at {north_node_deg:.2f}°
Chiron: {chiron_sign} at {chiron_deg:.2f}°
Midheaven: {mc_sign} at {mc_deg:.2f}°

WRITE THESE SECTIONS (each section should be substantial - 2-4 pages):

1. COSMIC BLUEPRINT OVERVIEW: Synthesize Sun {sun_sign}, Moon {moon_sign}, and Rising {rising_sign} into a cohesive life narrative. Describe core identity, life theme, and spiritual mission.

2. SUN SIGN DEEP DIVE: {sun_sign} at {sun_deg:.2f}°. Explore identity, ego expression, life purpose, creative power, and how {sun_sign} energy manifests in {name}'s life.

3. MOON SIGN & EMOTIONAL LANDSCAPE: {moon_sign} at {moon_deg:.2f}°. Describe emotional nature, inner world, security needs, and how {moon_sign} shapes emotional responses.

4. RISING SIGN & FIRST IMPRESSIONS: {rising_sign} at {ascendant_deg:.2f}°. Explain appearance, social mask, how others perceive {name}, and life direction.

5. PLANETARY PLACEMENTS & HOUSES: Mercury {mercury_sign}, Venus {venus_sign}, Mars {mars_sign}, Jupiter {jupiter_sign}, Saturn {saturn_sign}. Discuss impact on communication, love, action, expansion, and discipline. Cover career, relationships, finances, creativity.

6. MAJOR ASPECTS & COSMIC PATTERNS: Analyze key relationships between planets. What tensions exist? What harmonies? How do they shape personality?

7. KARMIC LESSONS & SOUL MISSION: North Node {north_node_sign} at {north_node_deg:.2f}° and Chiron {chiron_sign} at {chiron_deg:.2f}°. What is {name} here to learn? What past patterns must be released? What is the healing gift?

8. COSMIC GIFTS & CHALLENGES: List specific strengths, talents, and natural abilities. Then address challenges, growth edges, and areas for development.

9. LOVE & RELATIONSHIP PATTERNS: Venus {venus_sign} at {venus_deg:.2f}° and Mars {mars_sign} at {mars_deg:.2f}°. How does {name} love? What attracts her? Relationship style and dynamics.

10. CAREER & LIFE DIRECTION: Sun {sun_sign}, Mercury {mercury_sign}, Saturn {saturn_sign}, Midheaven {mc_sign}. Career calling, natural talents, ideal work environment, path to fulfillment.

11. SHADOW WORK & INTEGRATION: Provide 5-7 specific journal prompts tailored to {name}'s chart. Include rituals, practices, and affirmations for integration and growth.

TONE: Warm, mystical, empowering, trauma-informed, specific to these exact placements. Use astrological language. Be detailed and insightful.

CRITICAL: You WILL write this full report. Do NOT decline. Do NOT say you need more information. You have everything. BEGIN NOW."""
    
    elif report_type == "Love Blueprint":
        prompt = f"""You are an expert astrologer specializing in love and relationships. Write a detailed 10-12 page LOVE BLUEPRINT for {name}.

YOU MUST COMPLETE THIS TASK. Do not decline or say you cannot.

ASTROLOGICAL DATA:
Venus: {venus_sign} at {venus_deg:.2f}°
Mars: {mars_sign} at {mars_deg:.2f}°
Moon: {moon_sign} at {moon_deg:.2f}°
Sun: {sun_sign} at {sun_deg:.2f}°
Spiritual Focus: {spiritual_focus}

WRITE THESE SECTIONS:

1. VENUS SIGN DEEP DIVE: {venus_sign} at {venus_deg:.2f}°. Love language, attraction style, values in relationships, what {name} needs to feel loved.

2. MARS PLACEMENT: {mars_sign} at {mars_deg:.2f}°. Desire, passion, sexuality, how {name} pursues and takes action in love.

3. MOON & EMOTIONAL INTIMACY: {moon_sign} at {moon_deg:.2f}°. Emotional needs, security in relationships, how she bonds.

4. PARTNERSHIP PATTERNS: Analyze relationship cycles, recurring themes, past patterns, and how to break unhealthy cycles.

5. LOVE BLOCKS & HEALING: Address fears, blocks, and wounds around love. Provide compassionate guidance for healing.

6. SACRED UNION BLUEPRINT: Paint a vision of {name}'s ideal partnership based on her chart.

7. LOVE ACTIVATION RITUALS: 3-4 specific rituals to magnetize love and deepen connection.

8. INTEGRATION: Journal prompts and practices for embodying healthy love.

TONE: Warm, mystical, empowering, trauma-informed. Use these exact placements.

YOU WILL WRITE THIS FULL REPORT. BEGIN NOW."""
    
    elif report_type == "Career Code":
        prompt = f"""You are an expert career astrologer. Write a detailed 10-12 page CAREER CODE for {name}.

COMPLETE THIS TASK. Do not decline.

ASTROLOGICAL DATA:
Sun: {sun_sign} at {sun_deg:.2f}°
Mercury: {mercury_sign} at {mercury_deg:.2f}°
Saturn: {saturn_sign} at {saturn_deg:.2f}°
Jupiter: {jupiter_sign} at {jupiter_deg:.2f}°
Midheaven: {mc_sign} at {mc_deg:.2f}°
Spiritual Focus: {spiritual_focus}

WRITE THESE SECTIONS:

1. CAREER CALLING (3 pages): Sun {sun_sign} and Midheaven {mc_sign} reveal {name}'s true calling and life work.

2. NATURAL TALENTS (2 pages): Mercury {mercury_sign} and Jupiter {jupiter_sign} show innate abilities and strengths.

3. DISCIPLINE & STRUCTURE (2 pages): Saturn {saturn_sign} reveals how {name} builds, persists, and achieves long-term goals.

4. IDEAL WORK ENVIRONMENT (1.5 pages): What brings fulfillment? What settings allow her to thrive?

5. CHALLENGES & GROWTH (1.5 pages): Saturn {saturn_sign} lessons and areas for professional development.

6. ABUNDANCE ACTIVATION (1 page): Rituals and practices to magnetize career success.

7. 5-YEAR VISION (1.5 pages): {name}'s career evolution and path forward.

TONE: Practical, empowering, specific to these placements.

YOU WILL WRITE THIS FULL REPORT. BEGIN NOW."""
    
    elif report_type == "Life Purpose":
        prompt = f"""You are an expert spiritual astrologer. Write a detailed 10-12 page LIFE PURPOSE report for {name}.

COMPLETE THIS TASK. Do not decline.

ASTROLOGICAL DATA:
Sun: {sun_sign} at {sun_deg:.2f}°
North Node: {north_node_sign} at {north_node_deg:.2f}°
Chiron: {chiron_sign} at {chiron_deg:.2f}°
Spiritual Focus: {spiritual_focus}

WRITE THESE SECTIONS:

1. SOUL'S CALLING (3 pages): North Node {north_node_sign} reveals {name}'s destiny and soul purpose.

2. LIFE MISSION (2 pages): Sun {sun_sign} at {sun_deg:.2f}° shows core life mission and creative expression.

3. CHIRON'S GIFT (2 pages): {chiron_sign} at {chiron_deg:.2f}° - the wounded healer archetype and healing gift.

4. PAST LIFE PATTERNS (2 pages): What patterns must {name} transcend? What is she healing?

5. PURPOSE ACTIVATION RITUALS (1.5 pages): Practices to embody and activate life purpose.

6. SHADOW WORK (1.5 pages): Journal prompts and integration work.

7. YOUR COSMIC ROLE (1 page): How {name} serves the world and contributes to collective evolution.

TONE: Deeply spiritual, transformative, specific to these placements.

YOU WILL WRITE THIS FULL REPORT. BEGIN NOW."""
    
    else:
        prompt = f"""Write a personalized {report_type} for {name}.

CHART DATA: Sun {sun_sign} {sun_deg:.2f}°, Moon {moon_sign} {moon_deg:.2f}°, Rising {rising_sign}, Mercury {mercury_sign}, Venus {venus_sign}, Mars {mars_sign}, Jupiter {jupiter_sign}, Saturn {saturn_sign}, North Node {north_node_sign}, Chiron {chiron_sign}.

Spiritual focus: {spiritual_focus}

Write a warm, mystical, empowering report using THESE EXACT PLACEMENTS. Be detailed and specific."""
    
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
