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
        prompt = f"""Write a comprehensive 15-20 page spiritual and archetypal birth chart profile for {name}.

BIRTH DATA:
Name: {name}
Born: {birthdate} at {birthtime} in {birthplace}
Spiritual Focus: {spiritual_focus}

COSMIC DATA:
Sun: {sun_sign} at {sun_deg:.2f}°
Moon: {moon_sign} at {moon_deg:.2f}°
Rising: {rising_sign} at {ascendant_deg:.2f}°
Mercury: {mercury_sign} at {mercury_deg:.2f}°
Venus: {venus_sign} at {venus_deg:.2f}°
Mars: {mars_sign} at {mars_deg:.2f}°
Jupiter: {jupiter_sign} at {jupiter_deg:.2f}°
Saturn: {saturn_sign} at {saturn_deg:.2f}°
North Node: {north_node_sign} at {north_node_deg:.2f}°
Chiron: {chiron_sign} at {chiron_deg:.2f}°
Midheaven: {mc_sign} at {mc_deg:.2f}°

Write 12 detailed sections (15-20 pages total): Cosmic Blueprint Overview, Primary Archetype Deep Dive, Emotional Landscape, Persona & First Impressions, Communication & Intellect, Love & Relationships, Expansion & Growth, Discipline & Structure, Soul's Direction, Wounded Healer, Life Purpose & Vocation, Integration & Shadow Work. Be comprehensive, specific, and deeply insightful."""
    
    elif report_type == "Love Blueprint":
        prompt = f"""Write a detailed 12-15 page love and relationship profile for {name}.

COSMIC DATA:
Venus: {venus_sign} at {venus_deg:.2f}°
Mars: {mars_sign} at {mars_deg:.2f}°
Moon: {moon_sign} at {moon_deg:.2f}°
Sun: {sun_sign} at {sun_deg:.2f}°
Spiritual Focus: {spiritual_focus}

Write 9 detailed sections (12-15 pages total): Love Archetype, Desire & Passion, Emotional Intimacy, Core Identity in Love, Partnership Patterns, Love Blocks & Healing, Sacred Union Vision, Love Activation Rituals, Integration & Practices. Be warm, empowering, and specific."""
    
    elif report_type == "Career Code":
        prompt = f"""Write a detailed 12-15 page career and vocation profile for {name}.

COSMIC DATA:
Sun: {sun_sign} at {sun_deg:.2f}°
Mercury: {mercury_sign} at {mercury_deg:.2f}°
Saturn: {saturn_sign} at {saturn_deg:.2f}°
Jupiter: {jupiter_sign} at {jupiter_deg:.2f}°
Midheaven: {mc_sign} at {mc_deg:.2f}°
Spiritual Focus: {spiritual_focus}

Write 9 detailed sections (12-15 pages total): Career Calling, Natural Talents & Gifts, Discipline & Building Mastery, Expansion & Abundance, Ideal Work Environment, Challenges & Professional Growth, Life Purpose Through Work, Abundance Activation, 5-Year Vision & Evolution. Be practical, empowering, and inspirational."""
    
    elif report_type == "Life Purpose":
        prompt = f"""Write a detailed 12-15 page life purpose and soul mission profile for {name}.

COSMIC DATA:
Sun: {sun_sign} at {sun_deg:.2f}°
North Node: {north_node_sign} at {north_node_deg:.2f}°
Chiron: {chiron_sign} at {chiron_deg:.2f}°
Midheaven: {mc_sign} at {mc_deg:.2f}°
Spiritual Focus: {spiritual_focus}

Write 8 detailed sections (12-15 pages total): Soul's Calling, Life Mission, Wounded Healer Gift, Past Patterns & Transcendence, Spiritual Gifts & Talents, Purpose Activation Rituals, Shadow Work & Integration, Your Cosmic Role. Be deeply spiritual, transformative, and empowering."""
    
    elif report_type == "Starseed Lineage":
        prompt = f"""Write a detailed 10-15 page Starseed Lineage and galactic soul origin profile for {name}.

BIRTH DATA:
Name: {name}
Born: {birthdate} at {birthtime} in {birthplace}
Spiritual Focus: {spiritual_focus}

COSMIC DATA:
Sun: {sun_sign} at {sun_deg:.2f}°
Moon: {moon_sign} at {moon_deg:.2f}°
Rising: {rising_sign} at {ascendant_deg:.2f}°
Mercury: {mercury_sign} at {mercury_deg:.2f}°
Venus: {venus_sign} at {venus_deg:.2f}°
Mars: {mars_sign} at {mars_deg:.2f}°
Jupiter: {jupiter_sign} at {jupiter_deg:.2f}°
Saturn: {saturn_sign} at {saturn_deg:.2f}°
North Node: {north_node_sign} at {north_node_deg:.2f}°
Chiron: {chiron_sign} at {chiron_deg:.2f}°

Write 9 detailed sections (10-15 pages total): Cosmic Blueprint & Divine Origin, Starseed Lineage Identification, Galactic Soul Mission, Starseed Gifts & Abilities, Earth Mission & Service, Starseed Challenges & Integration, Connection to Star Family, Activation Codes & Practices, Embodying Your Cosmic Power. Be mystical, empowering, specific, and deeply spiritual."""
    
    elif report_type == "Human Design":
        prompt = f"""Write a detailed 10-15 page Human Design profile for {name}.

BIRTH DATA:
Name: {name}
Born: {birthdate} at {birthtime} in {birthplace}
Spiritual Focus: {spiritual_focus}

COSMIC DATA:
Sun: {sun_sign} at {sun_deg:.2f}°
Moon: {moon_sign} at {moon_deg:.2f}°
Rising: {rising_sign} at {ascendant_deg:.2f}°
Mercury: {mercury_sign} at {mercury_deg:.2f}°
Venus: {venus_sign} at {venus_deg:.2f}°
Mars: {mars_sign} at {mars_deg:.2f}°

Write 8 detailed sections (10-15 pages total): Human Design Overview, Type & Strategy, Authority & Decision Making, Profile & Life Theme, Centers & Channels, Defined vs Undefined Centers, Conditioning & Shadow Work, Living Your Design. Use the chart data to inform the Human Design analysis. Be practical, empowering, and specific."""
    
    elif report_type == "Astrocartography":
        prompt = f"""Write a detailed 10-15 page Astrocartography and relocation profile for {name}.

BIRTH DATA:
Name: {name}
Born: {birthdate} at {birthtime} in {birthplace}
Spiritual Focus: {spiritual_focus}

COSMIC DATA:
Sun: {sun_sign} at {sun_deg:.2f}°
Moon: {moon_sign} at {moon_deg:.2f}°
Rising: {rising_sign} at {ascendant_deg:.2f}°
Mercury: {mercury_sign} at {mercury_deg:.2f}°
Venus: {venus_sign} at {venus_deg:.2f}°
Mars: {mars_sign} at {mars_deg:.2f}°

Write 8 detailed sections (10-15 pages total): Astrocartography Overview, Sun Lines, Moon Lines, Mercury Lines, Venus Lines, Mars Lines, Optimal Locations & Relocation Guidance, Activation Practices. Be practical, specific, and empowering."""
    
    elif report_type == "Shadow Work Workbook":
        prompt = f"""Write a detailed 12-15 page Shadow Work Workbook and integration guide for {name}.

BIRTH DATA:
Name: {name}
Born: {birthdate} at {birthtime} in {birthplace}
Spiritual Focus: {spiritual_focus}

COSMIC DATA:
Sun: {sun_sign} at {sun_deg:.2f}°
Moon: {moon_sign} at {moon_deg:.2f}°
Saturn: {saturn_sign} at {saturn_deg:.2f}°
Chiron: {chiron_sign} at {chiron_deg:.2f}°
North Node: {north_node_sign} at {north_node_deg:.2f}°

Write 10 detailed sections (12-15 pages total): Shadow Work Introduction, Identifying Your Shadows, Core Wounds & Patterns, Saturn's Lessons, Chiron's Healing, North Node Integration, 21-Day Shadow Work Challenge (with daily prompts), Journaling Exercises, Rituals & Ceremonies, Integration & Wholeness. Include 15-20 specific journal prompts and practices. Be compassionate, trauma-informed, and transformative."""
    
    elif report_type == "Future Outlook":
        prompt = f"""Write an extensive 20-30 page future forecast for {name} covering the next 12-24 months.

COSMIC DATA:
Sun: {sun_sign} at {sun_deg:.2f}°
Moon: {moon_sign} at {moon_deg:.2f}°
North Node: {north_node_sign} at {north_node_deg:.2f}°
Birth Date: {birthdate}
Spiritual Focus: {spiritual_focus}

Write 12 comprehensive sections (20-30 pages total): Overview & Major Themes, Current Transits & Impact, Love & Relationships Forecast, Career & Abundance Forecast, Personal Growth & Transformation, Health & Wellness Cycles, Financial Forecast, Family & Home Themes, Creative & Spiritual Expansion, Challenges & Growth Edges, Monthly Breakdown (12 months), Rituals & Activation Practices. Be extensive, detailed, and specific."""
    
    elif report_type == "Cosmic Calendar (One Time Purchase)" or report_type == "Cosmic Calendar (Monthly Subscription)":
        prompt = f"""Write a detailed 30-day cosmic calendar and daily guidance for {name}.

COSMIC DATA:
Sun: {sun_sign} at {sun_deg:.2f}°
Moon: {moon_sign} at {moon_deg:.2f}°
Spiritual Focus: {spiritual_focus}

Provide daily guidance for 30 days including:
- Daily cosmic weather and planetary influences
- Recommended actions and focus areas
- Rituals and practices for each day
- Affirmations and intentions
- Warnings or things to avoid

Make it practical, actionable, and spiritually empowering. Format as: Day 1, Day 2, etc."""
    
    elif report_type == "Numerology Nexus":
        prompt = f"""Write a detailed 10-15 page Numerology profile for {name}.

BIRTH DATA:
Name: {name}
Born: {birthdate}
Spiritual Focus: {spiritual_focus}

COSMIC DATA:
Sun: {sun_sign} at {sun_deg:.2f}°
Moon: {moon_sign} at {moon_deg:.2f}°

Write 8 detailed sections (10-15 pages total): Numerology Overview, Life Path Number, Expression Number, Soul Urge Number, Personality Number, Birth Day Number, Personal Year Cycles, Numerology Practices & Activation. Use the birth date to calculate all numerology numbers. Be detailed, specific, and empowering."""
    
    else:
        prompt = f"""Write a personalized {report_type} for {name}.

COSMIC DATA: Sun {sun_sign}, Moon {moon_sign}, Rising {rising_sign}, Mercury {mercury_sign}, Venus {venus_sign}, Mars {mars_sign}, Jupiter {jupiter_sign}, Saturn {saturn_sign}, North Node {north_node_sign}, Chiron {chiron_sign}.

Spiritual focus: {spiritual_focus}

Write a warm, mystical, empowering report using these placements. Be detailed and specific."""
    
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
        if os.