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
    venus_sign = planets.get('Venus', {}).get('sign', 'Unknown')
    mars_sign = planets.get('Mars', {}).get('sign', 'Unknown')
    jupiter_sign = planets.get('Jupiter', {}).get('sign', 'Unknown')
    saturn_sign = planets.get('Saturn', {}).get('sign', 'Unknown')
    north_node_sign = planets.get('North Node', {}).get('sign', 'Unknown')
    chiron_sign = planets.get('Chiron', {}).get('sign', 'Unknown')
    
    houses = chart_data.get('houses', {})
    ascendant_deg = houses.get('ascendant', 0)
    mc_deg = houses.get('mc', 0)
    
    rising_sign = get_sign_from_degree(ascendant_deg)
    mc_sign = get_sign_from_degree(mc_deg)
    
    logger.info(f"Extracted: Sun {sun_sign}, Moon {moon_sign}, Rising {rising_sign}")
    
    if report_type == "Deep Dive Birth Chart":
        prompt = f"Write a comprehensive 15-20 page spiritual birth chart for {name}. Sun: {sun_sign}, Moon: {moon_sign}, Rising: {rising_sign}. Include 12 sections: Overview, Archetype, Emotions, Persona, Communication, Love, Expansion, Discipline, Soul Direction, Healer, Purpose, Integration."
    else:
        prompt = f"Write a personalized {report_type} for {name}. Sun {sun_sign}, Moon {moon_sign}, Rising {rising_sign}."
    
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