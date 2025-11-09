import logging
from openai import OpenAI
from fpdf import FPDF
from astrology_calc import calculate_chart
import os

logger = logging.getLogger(name)

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
    prompt = f"Write a comprehensive 15-20 page spiritual birth chart for {name}. Sun: {sun_sign} {sun_deg:.1f}°, Moon: {moon_sign} {moon_deg:.1f}°, Rising: {rising_sign}. Include 12 sections: Overview, Archetype, Emotions, Persona, Communication, Love, Expansion, Discipline, Soul Direction, Healer, Purpose, Integration. Be detailed and spiritual."
elif report_type == "Love Blueprint":
    prompt = f"Write a 12-15 page love profile for {name}. Venus: {venus_sign} {venus_deg:.1f}°, Mars: {mars_sign} {mars_deg:.1f}°, Moon: {moon_sign}. Cover: Love Archetype, Desire, Intimacy, Identity, Patterns, Blocks, Vision, Rituals, Integration. Be warm and empowering."
elif report_type == "Career Code":
    prompt = f"Write a 12-15 page career profile for {name}. Sun: {sun_sign}, Mercury: {mercury_sign}, Saturn: {saturn_sign}, Jupiter: {jupiter_sign}, MC: {mc_sign}. Cover: Calling, Talents, Mastery, Abundance, Environment, Challenges, Purpose, Activation, 5-Year Vision."
elif report_type == "Life Purpose":
    prompt = f"Write a 12-15 page life purpose profile for {name}. Sun: {sun_sign}, North Node: {north_node_sign}, Chiron: {chiron_sign}, MC: {mc_sign}. Cover: Calling, Mission, Wounded Healer, Patterns, Gifts, Rituals, Shadow Work, Cosmic Role."
elif report_type == "Starseed Lineage":
    prompt = f"Write a 10-15 page starseed lineage profile for {name}. Sun: {sun_sign}, Moon: {moon_sign}, Rising: {rising_sign}. Cover: Blueprint, Lineage ID, Mission, Gifts, Earth Service, Challenges, Star Family, Activation, Cosmic Power. Be mystical and empowering."
elif report_type == "Human Design":
    prompt = f"Write a 10-15 page Human Design profile for {name}. Sun: {sun_sign}, Moon: {moon_sign}, Rising: {rising_sign}. Cover: Overview, Type, Authority, Profile, Centers, Defined/Undefined, Conditioning, Living Design."
elif report_type == "Astrocartography":
    prompt = f"Write a 10-15 page astrocartography profile for {name}. Sun: {sun_sign}, Moon: {moon_sign}, Mercury: {mercury_sign}, Venus: {venus_sign}, Mars: {mars_sign}. Cover: Overview, Sun Lines, Moon Lines, Mercury Lines, Venus Lines, Mars Lines, Optimal Locations, Practices."
elif report_type == "Shadow Work Workbook":
    prompt = f"Write a 12-15 page shadow work guide for {name}. Saturn: {saturn_sign}, Chiron: {chiron_sign}, North Node: {north_node_sign}. Include 10 sections with 15-20 journal prompts. Cover: Intro, Shadows, Wounds, Saturn, Chiron, North Node, 21-Day Challenge, Journaling, Rituals, Integration."
elif report_type == "Future Outlook":
    prompt = f"Write a 20-30 page future forecast for {name} for next 12-24 months. Sun: {sun_sign}, Moon: {moon_sign}, North Node: {north_node_sign}. Cover 12 sections: Overview, Transits, Love, Career, Growth, Health, Finances, Family, Creativity, Challenges, Monthly Breakdown, Rituals."
elif report_type == "Cosmic Calendar (One Time Purchase)" or report_type == "Cosmic Calendar (Monthly Subscription)":
    prompt = f"Write a 30-day cosmic calendar for {name}. Sun: {sun_sign}, Moon: {moon_sign}. Format as Day 1-30 with daily cosmic weather, actions, rituals, affirmations, warnings. Be practical and empowering."
elif report_type == "Numerology Nexus":
    prompt = f"Write a 10-15 page numerology profile for {name}. Born: {birthdate}. Cover 8 sections: Overview, Life Path, Expression, Soul Urge, Personality, Birth Day, Personal Year, Practices. Calculate all numbers and be specific."
else:
    prompt = f"Write a personalized {report_type} for {name}. Sun {sun_sign}, Moon {moon_sign}, Rising {rising_sign}. Be warm, mystical, and empowering."

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