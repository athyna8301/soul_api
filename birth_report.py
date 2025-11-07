import logging
from openai import OpenAI
from fpdf import FPDF
from astrology_calc import calculate_chart
import os

# Logo configuration
LOGO_PATH = os.path.join(os.path.dirname(__file__), 'logos', 'NEW_LOGO.png')

logger = logging.getLogger(__name__)

def generate_report_content(name, birthdate, birthtime, birthplace, report_type, spiritual_focus):
    """Generate report content using OpenAI and astrology data."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY not set")
        raise ValueError("OPENAI_API_KEY not set")
    
    try:
        client = OpenAI(api_key=api_key)
    except Exception as e:
        logger.error(f"Error initializing OpenAI client: {e}")
        raise

    # Calculate astrology chart
    try:
        chart_data = calculate_chart(birthdate, birthtime, birthplace)
    except Exception as e:
        logger.error(f"Error calculating chart: {e}")
        raise

    # Extract key chart data
    sun = chart_data['planets']['Sun']
    moon = chart_data['planets']['Moon']
    mercury = chart_data['planets']['Mercury']
    venus = chart_data['planets']['Venus']
    mars = chart_data['planets']['Mars']
    jupiter = chart_data['planets']['Jupiter']
    saturn = chart_data['planets']['Saturn']

    # Get rising sign (calculate it directly)
    asc_degree = chart_data['houses']['ascendant']
    signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
             'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    rising_sign = signs[int(asc_degree / 30) % 12]

    # Create detailed prompt
    prompt = f"""You are a professional astrologer with expertise in trauma-informed spiritual guidance, shadow work, and empowerment coaching.

Generate a comprehensive Deep Dive Birth Chart interpretation for {name}.

BIRTH DATA:
- Born: {birthdate} at {birthtime} in {birthplace}

ASTROLOGICAL PLACEMENTS:
- Sun: {sun['sign']} ({sun['degree']:.2f}°)
- Moon: {moon['sign']} ({moon['degree']:.2f}°)
- Rising Sign: {rising_sign}
- Mercury: {mercury['sign']} ({mercury['degree']:.2f}°)
- Venus: {venus['sign']} ({venus['degree']:.2f}°)
- Mars: {mars['sign']} ({mars['degree']:.2f}°)
- Jupiter: {jupiter['sign']} ({jupiter['degree']:.2f}°)
- Saturn: {saturn['sign']} ({saturn['degree']:.2f}°)

SPIRITUAL FOCUS: {spiritual_focus}

Please provide:
1. A warm, welcoming introduction
2. Sun Sign Interpretation (core identity, ego, life purpose)
3. Moon Sign Interpretation (emotional nature, inner world, needs)
4. Rising Sign Interpretation (how others perceive you, first impression)
5. Mercury Interpretation (communication style, thinking patterns)
6. Venus Interpretation (love, values, relationships)
7. Mars Interpretation (drive, passion, action)
8. Jupiter Interpretation (growth, luck, expansion)
9. Saturn Interpretation (lessons, boundaries, maturity)
10. Integration & Shadow Work Prompts (practical exercises for self-discovery)
11. Closing affirmation and encouragement

Use a warm, mystical, trauma-informed tone. Balance cosmic wisdom with practical, actionable advice. Include journal prompts and reflection questions."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=3000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error calling OpenAI: {e}")
        raise

    return content

def generate_pdf(name, birthdate, birthtime, birthplace, report_type, spiritual_focus, content):
    """Generate PDF report with logo watermark."""
    pdf = FPDF()
    pdf.add_page()
    
    # Add logo as watermark (top right corner)
    try:
        logo_path = "logos/NEW_LOGO.png"  # Change to your logo filename
        pdf.image(logo_path, x=150, y=10, w=50)  # x, y position, width
    except Exception as e:
        logger.warning(f"Could not add logo: {e}")
    
    # Title and info
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, f"Deep Dive Birth Chart", ln=True, align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 5, f"For: {name}", ln=True)
    pdf.cell(0, 5, f"Born: {birthdate} at {birthtime} in {birthplace}", ln=True)
    pdf.ln(5)
    
    # Content
    pdf.set_font("Helvetica", "", 9)
    content_clean = content.encode('latin-1', errors='replace').decode('latin-1')
    pdf.multi_cell(0, 5, content_clean)
    
    filename = f"/tmp/{name.replace(' ', '_')}_chart.pdf"
    pdf.output(filename)
    return filename



