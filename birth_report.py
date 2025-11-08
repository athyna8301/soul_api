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
        "overview": f"Write 2-3 paragraphs COSMIC BLUEPRINT for {name}. Sun {sun_sign} {sun_degree:.0f}°, Moon {moon_sign} {moon_degree:.0f}°, Ascendant {rising_sign} {rising_degree:.0f}°. Core identity, life theme, spiritual mission.",
        "sun": f"Write 2-3 pages SUN SIGN for {name}. Sun in {sun_sign} at {sun_degree:.0f}°. Identity, ego, life purpose, creative power SPECIFIC to {sun_sign}.",
        "moon": f"Write 2-3 pages MOON SIGN for {name}. Moon in {moon_sign} at {moon_degree:.0f}°. Emotional nature, inner world, needs, security SPECIFIC to {moon_sign}.",
        "rising": f"Write 2-3 pages RISING SIGN for {name}. Ascendant in {rising_sign} at {rising_degree:.0f}°. Appearance, mask, first impressions, life direction.",
        "houses": f"Write 4-5 pages PLANETARY PLACEMENTS for {name}. Mercury {mercury_sign}, Venus {venus_sign}, Mars {mars_sign}, Jupiter {jupiter_sign}, Saturn {saturn_sign}. Career, relationships, finances, home, creativity.",
        "aspects": f"Write 3-4 pages MAJOR ASPECTS for {name}. Sun {sun_sign}, Moon {moon_sign}, Mercury {mercury_sign}, Venus {venus_sign}, Mars {mars_sign}. Inner tensions or harmonies.",
        "nodes": f"Write 2-3 pages KARMIC LESSONS for {name}. North Node {north_node_sign}, South Node {south_node_sign}, Chiron {chiron_sign}. Soul lessons, past patterns, healing.",
        "strengths": f"Write 2-3 pages COSMIC GIFTS for {name}. Sun {sun_sign}, Moon {moon_sign}, Rising {rising_sign}. Strengths, talents, challenges, growth edges.",
        "relationships": f"Write 2-3 pages LOVE PATTERNS for {name}. Venus {venus_sign}, Mars {mars_sign}. Love language, attraction, relationship style.",
        "career": f"Write 2-3 pages CAREER for {name}. Sun {sun_sign}, Mercury {mercury_sign}, Saturn {saturn_sign}. Career calling, talents, ideal work.",
        "integration": f"Write 2-3 pages SHADOW WORK for {name}. Sun {sun_sign}, Moon {moon_sign}. 5-7 journal prompts, rituals, practices. Focus: {spiritual_focus}.",
    }
    
    for section_name, prompt in prompts.items():
        try:
            response = client.chat.completions.create(model="gpt-4", messages=[{"role": "user", "content": prompt}], max_tokens=3000)
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
    mars_sign = planets.get('mars', {}).get('sign', 'Unknown')
    moon_sign = planets.get('moon', {}).get('sign', 'Unknown')
    
    prompts = {
        "venus": f"Write 2 pages VENUS for {name}. Venus in {venus_sign}. Love language, attraction, values.",
        "mars": f"Write 1.5 pages MARS for {name}. Mars in {mars_sign}. Desire, passion, sexuality.",
        "7th_house": f"Write 2 pages PARTNERSHIP for {name}. Venus {venus_sign}, Mars {mars_sign}. Partnership patterns, ideal partner.",
        "patterns": f"Write 1.5 pages RELATIONSHIP PATTERNS for {name}. Moon {moon_sign}, Venus {venus_sign}. Recurring themes, cycles.",
        "blocks": f"Write 1.5 pages LOVE BLOCKS for {name}. Venus {venus_sign}, Mars {mars_sign}. Fears, blocks, growth edges.",
        "sacred_union": f"Write 1 page IDEAL PARTNERSHIP for {name}. Venus {venus_sign}, Mars {mars_sign}, Moon {moon_sign}. Vision.",
        "rituals": f"Write 1 page LOVE RITUALS for {name}. 3-4 rituals to magnetize love. Venus {venus_sign}. Focus: {spiritual_focus}.",
    }
    
    for section_name, prompt in prompts.items():
        try:
            response = client.chat.completions.create(model="gpt-4", messages=[{"role": "user", "content": prompt}], max_tokens=2500)
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
    
    prompt = f"Create 10-12 page CAREER CODE for {name}. Sun {sun_sign}, Mercury {mercury_sign}, Saturn {saturn_sign}, Jupiter {jupiter_sign}. Career path, talents, challenges, ideal work, abundance. Focus: {spiritual_focus}"
    
    try:
        response = client.chat.completions.create(model="gpt-4", messages=[{"role": "user", "content": prompt}], max_tokens=3500)
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
    
    prompt = f"Create 10-12 page LIFE PURPOSE for {name}. Sun {sun_sign}, North Node {north_node}, South Node {south_node}, Chiron {chiron_sign}. Soul calling, mission, karmic contracts, gifts, shadow work, past lives, rituals. Focus: {spiritual_focus}"
    
    try:
        response = client.chat.completions.create(model="gpt-4", messages=[{"role": "user", "content": prompt}], max_tokens=3500)
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error generating life purpose: {e}")
        return f"Unable to generate report. Error: {str(e)}"

def generate_30day_outlook(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client):
    """Generate 10-12 page 30 Day Outlook."""
    prompt = f"Create 10-12 page 30 DAY OUTLOOK for {name} born {birthdate}. Transits, week-by-week forecast, key themes, challenges, opportunities, rituals, affirmations. Focus: {spiritual_focus}"
    
    try:
        response = client.chat.completions.create(model="gpt-4", messages=[{"role": "user", "content": prompt}], max_tokens=3500)
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error generating 30 day outlook: {e}")
        return f"Unable to generate report. Error: {str(e)}"

def generate_cosmic_calendar(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client):
    """Generate 8-10 page Cosmic Calendar."""
    prompt = f"Create 8-10 page COSMIC CALENDAR for {name}. Monthly overview, New Moon intentions, Full Moon release, weekly cosmic weather, daily rituals, affirmations. Focus: {spiritual_focus}"
    
    try:
        response = client.chat.completions.create(model="gpt-4", messages=[{"role": "user", "content": prompt}], max_tokens=3500)
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error generating cosmic calendar: {e}")
        return f"Unable to generate calendar. Error: {str(e)}"

def generate_human_design(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client):
    """Generate 50+ page Human Design Reading."""
    prompt = f"Create 50+ page HUMAN DESIGN for {name} born {birthdate}. Type, Strategy, Authority, Profile, Channels, Gates, Lines, career, relationships, shadow work, 90-day plan. Focus: {spiritual_focus}"
    
    try:
        response = client.chat.completions.create(model="gpt-4", messages=[{"role": "user", "content": prompt}], max_tokens=4000)
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error generating human design: {e}")
        return f"Unable to generate report. Error: {str(e)}"

def generate_starseed_lineage(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client):
    """Generate 12-15 page Starseed Lineage."""
    prompt = f"Create 12-15 page STARSEED LINEAGE for {name}. Origins, galactic heritage, mission, planetary influences, gifts, Earth integration, cosmic contracts, rituals, star family connection. Focus: {spiritual_focus}"
    
    try:
        response = client.chat.completions.create(model="gpt-4", messages=[{"role": "user", "content": prompt}], max_tokens=3500)
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error generating starseed lineage: {e}")
        return f"Unable to generate report. Error: {str(e)}"

def generate_astrocartography(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client):
    """Generate 
