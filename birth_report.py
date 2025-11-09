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
        prompt = f"""Write a comprehensive 15-20 page spiritual and archetypal birth chart profile for {name}, based on the following cosmic data points and archetypal symbolism.

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

WRITE THESE SECTIONS (aim for 15-20 pages total, with detailed exploration):

1. COSMIC BLUEPRINT OVERVIEW (2-3 pages): Synthesize the primary, emotional, and persona archetypes into a cohesive life narrative. What is {name}'s core identity and life theme?

2. PRIMARY ARCHETYPE DEEP DIVE (2-3 pages): {sun_sign} at {sun_deg:.2f}°. How does this archetype express through identity, purpose, and creative power?

3. EMOTIONAL LANDSCAPE (2-3 pages): {moon_sign} at {moon_deg:.2f}°. What is {name}'s inner emotional world? How does she process feelings and seek security?

4. PERSONA & FIRST IMPRESSIONS (1-2 pages): {rising_sign} at {ascendant_deg:.2f}°. How does {name} appear to others? What mask does she wear?

5. COMMUNICATION & INTELLECT (1-2 pages): {mercury_sign} at {mercury_deg:.2f}°. How does {name} think, communicate, and process information?

6. LOVE & RELATIONSHIPS (2-3 pages): {venus_sign} at {venus_deg:.2f}° and {mars_sign} at {mars_deg:.2f}°. What is {name}'s love language? How does she pursue and attract?

7. EXPANSION & GROWTH (1-2 pages): {jupiter_sign} at {jupiter_deg:.2f}°. Where does {name} naturally expand? What brings joy and abundance?

8. DISCIPLINE & STRUCTURE (1-2 pages): {saturn_sign} at {saturn_deg:.2f}°. How does {name} build? What are her limitations and where does she need discipline?

9. SOUL'S DIRECTION (2-3 pages): {north_node_sign} at {north_node_deg:.2f}°. What is {name}'s soul growth direction? What is she learning in this lifetime?

10. WOUNDED HEALER (2-3 pages): {chiron_sign} at {chiron_deg:.2f}°. What is {name}'s deepest wound? How can she transform it into her greatest gift?

11. LIFE PURPOSE & VOCATION (1-2 pages): {mc_sign} at {mc_deg:.2f}°. What is {name}'s calling? How can she best serve the world?

12. INTEGRATION & SHADOW WORK (2-3 pages): Provide 7-10 journal prompts, rituals, and practices tailored to {name}'s archetypal profile. Include specific affirmations and ceremonies.

TONE: Warm, mystical, empowering, trauma-informed. Use archetypal and psychological language. Be specific, detailed, and comprehensive."""
    
    elif report_type == "Love Blueprint":
        prompt = f"""Write a detailed 12-15 page spiritual and archetypal love profile for {name}.

COSMIC LOVE DATA:
- Love Archetype (Venus): {venus_sign} at {venus_deg:.2f}°
- Desire Archetype (Mars): {mars_sign} at {mars_deg:.2f}°
- Emotional Archetype (Moon): {moon_sign} at {moon_deg:.2f}°
- Core Self (Sun): {sun_sign} at {sun_deg:.2f}°
- Spiritual Focus: {spiritual_focus}

WRITE THESE SECTIONS (aim for 12-15 pages total):

1. LOVE ARCHETYPE (2-3 pages): {venus_sign} at {venus_deg:.2f}°. What is {name}'s love language? How does she express affection and values in relationships? What does she seek in a partner?

2. DESIRE & PASSION (2-3 pages): {mars_sign} at {mars_deg:.2f}°. How does {name} pursue? What ignites her passion? Her sexuality and assertiveness in love?

3. EMOTIONAL INTIMACY (2-3 pages): {moon_sign} at {moon_deg:.2f}°. What does {name} need to feel emotionally safe and bonded? Her attachment style and emotional needs?

4. CORE IDENTITY IN LOVE (1-2 pages): {sun_sign} at {sun_deg:.2f}°. How does her core self show up in relationships? Her authentic expression of love?

5. PARTNERSHIP PATTERNS (2-3 pages): What recurring themes appear in {name}'s relationships? What patterns need healing? Cycles and dynamics?

6. LOVE BLOCKS & HEALING (2-3 pages): What fears or wounds affect {name}'s ability to love? How can she heal? Specific blocks and their origins?

7. SACRED UNION VISION (1-2 pages): What does {name}'s ideal partnership look like? Her vision of sacred love?

8. LOVE ACTIVATION RITUALS (1-2 pages): 4-5 specific rituals to magnetize love, deepen connection, and embody healthy partnership.

9. INTEGRATION & PRACTICES (1-2 pages): Journal prompts, affirmations, and daily practices for embodying healthy, sacred love.

TONE: Warm, mystical, empowering, trauma-informed. Detailed and specific to her chart."""
    
    elif report_type == "Career Code":
        prompt = f"""Write a detailed 12-15 page spiritual and archetypal career profile for {name}.

COSMIC CAREER DATA:
- Core Self (Sun): {sun_sign} at {sun_deg:.2f}°
- Communication (Mercury): {mercury_sign} at {mercury_deg:.2f}°
- Discipline (Saturn): {saturn_sign} at {saturn_deg:.2f}°
- Expansion (Jupiter): {jupiter_sign} at {jupiter_deg:.2f}°
- Life Direction (Midheaven): {mc_sign} at {mc_deg:.2f}°
- Spiritual Focus: {spiritual_focus}

WRITE THESE SECTIONS (aim for 12-15 pages total):

1. CAREER CALLING (3-4 pages): {sun_sign} and {mc_sign}. What is {name}'s true calling? Her soul's work and life vocation?

2. NATURAL TALENTS & GIFTS (2-3 pages): {mercury_sign} and {jupiter_sign}. What are {name}'s innate abilities, strengths, and natural talents?

3. DISCIPLINE & BUILDING MASTERY (2-3 pages): {saturn_sign}. How does {name} build sustainable success? Her approach to discipline, persistence, and long-term achievement?

4. EXPANSION & ABUNDANCE (2-3 pages): {jupiter_sign}. Where does {name} naturally expand? What brings professional joy and abundance?

5. IDEAL WORK ENVIRONMENT (1-2 pages): What settings, cultures, and work styles allow {name} to thrive? Her optimal career conditions?

6. CHALLENGES & PROFESSIONAL GROWTH (1-2 pages): Where does {name} need to develop professionally? Her growth edges and learning opportunities?

7. LIFE PURPOSE THROUGH WORK (1-2 pages): How can {name}'s career serve her spiritual purpose and the world?

8. ABUNDANCE ACTIVATION (1-2 pages): 4-5 rituals, affirmations, and practices for magnetizing career success and prosperity.

9. 5-YEAR VISION & EVOLUTION (1-2 pages): {name}'s career trajectory and evolution over the next 5 years. Her potential and path forward.

TONE: Practical, empowering, specific, and inspirational."""
    
    elif report_type == "Life Purpose":
        prompt = f"""Write a detailed 12-15 page spiritual life purpose profile for {name}.

COSMIC PURPOSE DATA:
- Core Self (Sun): {sun_sign} at {sun_deg:.2f}°
- Soul Direction (North Node): {north_node_sign} at {north_node_deg:.2f}°
- Wounded Healer (Chiron): {chiron_sign} at {chiron_deg:.2f}°
- Life Direction (Midheaven): {mc_sign} at {mc_deg:.2f}°
- Spiritual Focus: {spiritual_focus}

WRITE THESE SECTIONS (aim for 12-15 pages total):

1. SOUL'S CALLING (3-4 pages): {north_node_sign}. What is {name}'s soul purpose? Her destiny and evolutionary direction in this lifetime?

2. LIFE MISSION (2-3 pages): {sun_sign}. What is {name}'s core life mission? Her creative expression and authentic purpose?

3. WOUNDED HEALER GIFT (2-3 pages): {chiron_sign}. What is {name}'s deepest wound? How can she transform it into her greatest healing gift to share with the world?

4. PAST PATTERNS & TRANSCENDENCE (2-3 pages): What patterns is {name} transcending? What past-life themes or karmic lessons is she healing?

5. SPIRITUAL GIFTS & TALENTS (1-2 pages): What unique spiritual gifts does {name} possess? How can she develop and share them?

6. PURPOSE ACTIVATION RITUALS (1-2 pages): 4-5 specific rituals and practices to activate, embody, and align with her life purpose.

7. SHADOW WORK & INTEGRATION (1-2 pages): Journal prompts and practices for integrating shadow aspects and stepping fully into her purpose.

8. YOUR COSMIC ROLE (1-2 pages): How does {name} serve the world? Her contribution to collective evolution and healing?

TONE: Deeply spiritual, transformative, empowering, and specific."""
    
    elif report_type == "Future Outlook":
        prompt = f"""Write an extensive 20-30 page spiritual forecast and future outlook for {name}, covering major transits, progressions, and evolutionary themes for the next 12-24 months and beyond.

COSMIC DATA:
- Core Self (Sun): {sun_sign} at {sun_deg:.2f}°
- Emotional Nature (Moon): {moon_sign} at {moon_deg:.2f}°
- Soul Direction (North Node): {north_node_sign} at {north_node_deg:.2f}°
- Spiritual Focus: {spiritual_focus}
- Birth Date: {birthdate}

WRITE THESE SECTIONS (aim for 20-30 pages total - this is comprehensive):

1. OVERVIEW & MAJOR THEMES (2-3 pages): What are the overarching themes for {name}'s next 12-24 months? Major evolutionary shifts and opportunities?

2. CURRENT TRANSITS & THEIR IMPACT (3-4 pages): How are current planetary transits affecting {name}'s life? Key planetary movements and their significance?

3. LOVE & RELATIONSHIPS FORECAST (3-4 pages): What does the future hold for {name}'s romantic life and relationships? Opportunities, challenges, and timing?

4. CAREER & ABUNDANCE FORECAST (3-4 pages): Career developments, professional opportunities, and abundance cycles ahead? When are peak opportunity windows?

5. PERSONAL GROWTH & TRANSFORMATION (3-4 pages): What spiritual and personal growth is {name} being called into? Healing opportunities and evolution?

6. HEALTH & WELLNESS CYCLES (2-3 pages): Physical, emotional, and spiritual wellness themes. Optimal times for healing and renewal?

7. FINANCIAL FORECAST (2-3 pages): Money cycles, abundance patterns, and financial opportunities ahead?

8. FAMILY & HOME THEMES (2-3 pages): Family dynamics, home changes, and domestic themes in the coming period?

9. CREATIVE & SPIRITUAL EXPANSION (2-3 pages): Creative projects, spiritual development, and expansion opportunities?

10. CHALLENGES & GROWTH EDGES (2-3 pages): Potential challenges, obstacles, and how to work with them? Growth opportunities disguised as difficulties?

11. MONTHLY BREAKDOWN (3-4 pages): Key themes, opportunities, and focus areas for each month ahead (next 12 months)?

12. RITUALS & ACTIVATION PRACTICES (2-3 pages): 6-8 powerful rituals, ceremonies, and practices to align with an
