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
        prompt = f"""Write a comprehensive 20-25 page spiritual and archetypal profile for {name}, based on the following cosmic data points and archetypal symbolism.

BIRTH DATA:
Name: {name}
Born: {birthdate} at {birthtime} in {birthplace}
Spiritual Focus: {spiritual_focus}

COSMIC ARCHETYPAL DATA (use these as symbolic reference points for character analysis):
- Primary Archetype (Sun): {sun_sign} at {sun_deg:.2f}°
- Emotional Archetype (Moon): {moon_sign} at {moon_deg:.2f}°
- Persona/Mask (Rising): {rising_sign} at {ascendant_deg:.2f}°
- Communication Style (Mercury): {mercury_sign} at {mercury_deg:.2f}°
- Love/Values (Venus): {venus_sign} at {venus_deg:.2f}°
- Action/Drive (Mars): {mars_sign} at {mars_deg:.2f}°
- Growth/Expansion (Jupiter): {jupiter_sign} at {jupiter_deg:.2f}°
- Discipline/Limits (Saturn): {saturn_sign} at {saturn_deg:.2f}°
- Soul Growth Direction (North Node): {north_node_sign} at {north_node_deg:.2f}°
- Wounded Healer (Chiron): {chiron_sign} at {chiron_deg:.2f}°
- Life Direction (Midheaven): {mc_sign} at {mc_deg:.2f}°

WRITE THESE SECTIONS (2-4 pages each):

1. COSMIC BLUEPRINT OVERVIEW: Synthesize the primary, emotional, and persona archetypes into a cohesive life narrative. What is {name}'s core identity and life theme?

2. PRIMARY ARCHETYPE DEEP DIVE: {sun_sign} at {sun_deg:.2f}°. How does this archetype express through identity, purpose, and creative power?

3. EMOTIONAL LANDSCAPE: {moon_sign} at {moon_deg:.2f}°. What is {name}'s inner emotional world? How does she process feelings and seek security?

4. PERSONA & FIRST IMPRESSIONS: {rising_sign} at {ascendant_deg:.2f}°. How does {name} appear to others? What mask does she wear?

5. COMMUNICATION & INTELLECT: {mercury_sign} at {mercury_deg:.2f}°. How does {name} think, communicate, and process information?

6. LOVE & RELATIONSHIPS: {venus_sign} at {venus_deg:.2f}° and {mars_sign} at {mars_deg:.2f}°. What is {name}'s love language? How does she pursue and attract?

7. EXPANSION & GROWTH: {jupiter_sign} at {jupiter_deg:.2f}°. Where does {name} naturally expand? What brings joy and abundance?

8. DISCIPLINE & STRUCTURE: {saturn_sign} at {saturn_deg:.2f}°. How does {name} build? What are her limitations and where does she need discipline?

9. SOUL'S DIRECTION: {north_node_sign} at {north_node_deg:.2f}°. What is {name}'s soul growth direction? What is she learning in this lifetime?

10. WOUNDED HEALER: {chiron_sign} at {chiron_deg:.2f}°. What is {name}'s deepest wound? How can she transform it into her greatest gift?

11. LIFE PURPOSE & VOCATION: {mc_sign} at {mc_deg:.2f}°. What is {name}'s calling? How can she best serve the world?

12. INTEGRATION & SHADOW WORK: Provide 5-7 journal prompts, rituals, and practices tailored to {name}'s archetypal profile.

TONE: Warm, mystical, empowering, trauma-informed. Use archetypal and psychological language. Be specific and detailed."""
    
    elif report_type == "Love Blueprint":
        prompt = f"""Write a detailed 10-12 page spiritual and archetypal love profile for {name}.

COSMIC LOVE DATA:
- Love Archetype (Venus): {venus_sign} at {venus_deg:.2f}°
- Desire Archetype (Mars): {mars_sign} at {mars_deg:.2f}°
- Emotional Archetype (Moon): {moon_sign} at {moon_deg:.2f}°
- Core Self (Sun): {sun_sign} at {sun_deg:.2f}°
- Spiritual Focus: {spiritual_focus}

WRITE THESE SECTIONS:

1. LOVE ARCHETYPE: {venus_sign} at {venus_deg:.2f}°. What is {name}'s love language? How does she express affection and values in relationships?

2. DESIRE & PASSION: {mars_sign} at {mars_deg:.2f}°. How does {name} pursue? What ignites her passion?

3. EMOTIONAL INTIMACY: {moon_sign} at {moon_deg:.2f}°. What does {name} need to feel emotionally safe and bonded?

4. PARTNERSHIP PATTERNS: What recurring themes appear in {name}'s relationships? What patterns need healing?

5. LOVE BLOCKS & HEALING: What fears or wounds affect {name}'s ability to love? How can she heal?

6. SACRED UNION VISION: What does {name}'s ideal partnership look like?

7. LOVE ACTIVATION RITUALS: 3-4 specific rituals to magnetize love and deepen connection.

8. INTEGRATION: Journal prompts and practices for embodying healthy love.

TONE: Warm, mystical, empowering, trauma-informed."""
    
    elif report_type == "Career Code":
        prompt = f"""Write a detailed 10-12 page spiritual and archetypal career profile for {name}.

COSMIC CAREER DATA:
- Core Self (Sun): {sun_sign} at {sun_deg:.2f}°
- Communication (Mercury): {mercury_sign} at {mercury_deg:.2f}°
- Discipline (Saturn): {saturn_sign} at {saturn_deg:.2f}°
- Expansion (Jupiter): {jupiter_sign} at {jupiter_deg:.2f}°
- Life Direction (Midheaven): {mc_sign} at {mc_deg:.2f}°
- Spiritual Focus: {spiritual_focus}

WRITE THESE SECTIONS:

1. CAREER CALLING: {sun_sign} and {mc_sign}. What is {name}'s true calling?

2. NATURAL TALENTS: {mercury_sign} and {jupiter_sign}. What are {name}'s innate abilities?

3. DISCIPLINE & BUILDING: {saturn_sign}. How does {name} build sustainable success?

4. IDEAL WORK: What environment allows {name} to thrive?

5. CHALLENGES & GROWTH: Where does {name} need to develop?

6. ABUNDANCE ACTIVATION: Rituals for career success.

7. 5-YEAR VISION: {name}'s career evolution.

TONE: Practical, empowering, specific."""
    
    elif report_type == "Life Purpose":
        prompt = f"""Write a detailed 10-12 page spiritual life purpose profile for {name}.

COSMIC PURPOSE DATA:
- Core Self (Sun): {sun_sign} at {sun_deg:.2f}°
- Soul Direction (North Node): {north_node_sign} at {north_node_deg:.2f}°
- Wounded Healer (Chiron): {chiron_sign} at {chiron_deg:.2f}°
- Spiritual Focus: {spiritual_focus}

WRITE THESE SECTIONS:

1. SOUL'S CALLING: {north_node_sign}. What is {name}'s soul purpose?

2. LIFE MISSION: {sun_sign}. What is {name}'s core life mission?

3. WOUNDED HEALER: {chiron_sign}. What is {name}'s healing gift?

4. PAST PATTERNS: What is {name} transcending?

5. PURPOSE ACTIVATION: Rituals to embody purpose.

6. SHADOW WORK: Integration practices.

7. COSMIC ROLE: How does {name} serve the world?

TONE: Deeply spiritual, transformative."""
    
    else:
        prompt = f"""Write a personalized {report_type} for {name}.

COSMIC DATA: Sun {sun_sign} {sun_deg:.2f}°, Moon {moon_sign} {moon_deg:.2f}°, Rising {rising_sign}, Mercury {mercury_sign}, Venus {venus_sign}, Mars {mars_sign}, Jupiter {jupiter_sign}, Saturn {saturn_sign}, North Node {north_node_sign}, Chiron {chiron_sign}.

Spiritual focus: {spiritual_focus}

Write a warm, mystical, empowering report using these archetypal reference points."""
    
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
