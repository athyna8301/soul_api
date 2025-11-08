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
        logger.info(f"Chart calculated successfully: {chart_data}")
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
    """Generate 20-25 page Deep Dive Birth Chart with REAL astrology data."""
    sections = []
    
    planets = chart_data.get('planets', {})
    houses = chart_data.get('houses', {})
    
    sun_sign = planets.get('sun', {}).get('sign', 'Unknown')
    sun_degree = planets.get('sun', {}).get('degree', 0)
    moon_sign = planets.get('moon', {}).get('sign', 'Unknown')
    moon_degree = planets.get('moon', {}).get('degree', 0)
    rising_sign = planets.get('rising', {}).get('sign', 'Unknown')
    rising_degree = planets.get('rising', {}).get('degree', 0)
    mercury_sign = planets.get('mercury', {}).get('sign', 'Unknown')
    venus_sign = planets.get('venus', {}).get('sign', 'Unknown')
    mars_sign = planets.get('mars', {}).get('sign', 'Unknown')
    jupiter_sign = planets.get('jupiter', {}).get('sign', 'Unknown')
    saturn_sign = planets.get('saturn', {}).get('sign', 'Unknown')
    north_node_sign = planets.get('north_node', {}).get('sign', 'Unknown')
    south_node_sign = planets.get('south_node', {}).get('sign', 'Unknown')
    chiron_sign = planets.get('chiron', {}).get('sign', 'Unknown')
    
    prompts = {
        "overview": f"Write a compelling 2-3 paragraph COSMIC BLUEPRINT OVERVIEW for {name} born {birthdate} at {birthtime} in {birthplace}. Sun in {sun_sign} at {sun_degree:.1f}°, Moon in {moon_sign} at {moon_degree:.1f}°, Ascendant in {rising_sign} at {rising_degree:.1f}°. Focus on core cosmic identity, life theme, and spiritual mission SPECIFIC to these placements.",
        
        "sun": f"Write 2-3 pages on SUN SIGN DEEP DIVE for {name}. Sun in {sun_sign} at {sun_degree:.1f}°. Cover identity, ego expression, life purpose, creative power SPECIFIC to {sun_sign}. Include strengths, challenges, how she shines.",
        
        "moon": f"Write 2-3 pages on MOON SIGN & EMOTIONAL LANDSCAPE for {name}. Moon in {moon_sign} at {moon_degree:.1f}°. Explore emotional nature, inner world, needs, security patterns SPECIFIC to {moon_sign}. How does she process emotions?",
        
        "rising": f"Write 2-3 pages on RISING SIGN & LIFE PATH for {name}. Ascendant in {rising_sign} at {rising_degree:.1f}°. Describe appearance, mask, first impressions, life direction SPECIFIC to {rising_sign}. How does she present to the world?",
        
        "houses": f"Write 4-5 pages on PLANETARY PLACEMENTS for {name}. Mercury in {mercury_sign}, Venus in {venus_sign}, Mars in {mars_sign}, Jupiter in {jupiter_sign}, Saturn in {saturn_sign}. Cover career, relationships, finances, home, creativity. Be specific to these placements.",
        
        "aspects": f"Write 3-4 pages on MAJOR ASPECTS & COSMIC PATTERNS for {name}. Analyze relationships between: Sun in {sun_sign}, Moon in {moon_sign}, Mercury in {mercury_sign}, Venus in {venus_sign}, Mars in {mars_sign}. What inner tensions or harmonies exist?",
        
        "nodes": f"Write 2-3 pages on KARMIC LESSONS & SOUL MISSION for {name}. North Node in {north_node_sign}, South Node in {south_node_sign}, Chiron in {chiron_sign}. What is she here to learn? What past patterns must she release?",
        
        "strengths": f"Write 2-3 pages on COSMIC GIFTS & CHALLENGES for {name}. Based on Sun in {sun_sign}, Moon in {moon_sign}, Rising in {rising_sign}. Detail natural strengths, talents, challenges, growth edges. Be honest and empowering.",
        
        "relationships": f"Write 2-3 pages on LOVE & RELATIONSHIPS for {name}. Venus in {venus_sign}, Mars in {mars_sign}. How does she love? What attracts her? Relationship style SPECIFIC to these placements.",
        
        "career": f"Write 2-3 pages on CAREER & LIFE DIRECTION for {name}. Sun in {sun_sign}, Mercury in {mercury_sign}, Saturn in {saturn_sign}. Career calling, natural talents, ideal work environment. What brings fulfillment?",
        
        "integration": f"Write 2-3 pages on INTEGRATION & SHADOW WORK for {name}. Provide 5-7 journal prompts, rituals, practices specific to Sun in {sun_sign}, Moon in {moon_sign}. Spiritual focus: {spiritual_focus}. Make them actionable.",
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
    
    planets = chart_data.get('planets', {})
    venus_sign = planets.get('venus', {}).get('sign', 'Unknown')
    venus_degree = planets.get('venus', {}).get('degree', 0)
    mars_sign = planets.get('mars', {}).get('sign', 'Unknown')
    mars_degree = planets.get('mars', {}).get('degree', 0)
    moon_sign = planets.get('moon', {}).get('sign', 'Unknown')
    
    prompts = {
        "venus": f"Write 2 pages on VENUS SIGN DEEP DIVE for {name}. Venus in {venus_sign} at {venus_degree:.1f}°. Love language, attraction style, values SPECIFIC to {venus_sign}.",
        "mars": f"Write 1.5 pages on MARS PLACEMENT for {name}. Mars in {mars_sign} at {mars_degree:.1f}°. Desire, passion, sexuality, pursuit style SPECIFIC to {mars_sign}.",
        "7th_house": f"Write 2 pages on 7TH HOUSE & PARTNERSHIP for {name}. Venus in {venus_sign}, Mars in {mars_sign}. Partnership patterns and ideal partner blueprint.",
        "patterns": f"Write 1.5 pages on RELATIONSHIP PATTERNS for {name}. Moon in {moon_sign}, Venus in {venus_sign}. Recurring themes, past cycles, healing opportunities.",
        "blocks": f"Write 1.5 pages on LOVE BLOCKS & HEALING for {name}. Venus in {venus_sign}, Mars in {mars_sign}. Fears, blocks, growth edges. Be compassionate.",
        "sacred_union": f"Write 1 page on SACRED UNION BLUEPRINT for {name}. Vision of ideal partnership based on Venus in {venus_sign}, Mars in {mars_sign}, Moon in {moon_sign}.",
        "rituals": f"Write 1 page on LOVE ACTIVATION RITUALS for {name}. 3-4 rituals to magnetize love, specific to Venus in {venus_sign}. Spiritual focus: {spiritual_focus}.",
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
    planets = chart_data.get('planets', {})
    sun_sign = planets.get('sun', {}).get('sign', 'Unknown')
    mercury_sign = planets.get('mercury', {}).get('sign', 'Unknown')
    saturn_sign = planets.get('saturn', {}).get('sign', 'Unknown')
    jupiter_sign = planets.get('jupiter', {}).get('sign', 'Unknown')
    
    prompt = f"""Create comprehensive 10-12 page CAREER CODE for {name} born {birthdate} at {birthtime} in {birthplace}.

Chart shows: Sun in {sun_sign}, Mercury in {mercury_sign}, Saturn in {saturn_sign}, Jupiter in {jupiter_sign}

Include: 10th House/Midheaven, Sun in {sun_sign} career context, Mercury in {mercury_sign} skills, natural talents, challenges, ideal work environment, abundance activation, 5-year vision.

Spiritual focus: {spiritual_focus}

Be specific and actionable."""
    
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
    planets = chart_data.get('planets', {})
    sun_sign = planets.get('sun', {}).get('sign', 'Unknown')
    north_node = planets.get('north_node', {}).get('sign', 'Unknown')
    south_node = planets.get('south_node', {}).get('sign', 'Unknown')
    chiron_sign = planets.get('chiron', {}).get('sign', 'Unknown')
    
    prompt = f"""Create profound 10-12 page LIFE PURPOSE for {name} born {birthdate} at {birthtime} in {birthplace}.

Chart reveals: Sun in {sun_sign}, North Node in {north_node}, South Node in {south_node}, Chiron in {chiron_sign}

Include: Soul's calling, life mission blueprint, karmic contracts, spiritual gifts, shadow work, past life themes, purpose activation rituals, integration steps.

Spiritual focus: {spiritual_focus}

Be deeply spiritual and transformative."""
    
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
    prompt = f"Create detailed 10-12 page 30 DAY OUTLOOK for {name} born {birthdate}. Include: Current transits, week-by-week forecast (4 weeks), key themes, challenges/opportunities, ritual recommendations, daily affirmations. Spiritual focus: {spiritual_focus}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3500
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error generating 30 day outlook: {e}")
        return
