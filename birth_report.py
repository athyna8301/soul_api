import logging
from openai import OpenAI
from fpdf import FPDF
from astrology_calc import calculate_chart
import os

logger = logging.getLogger(__name__)

def generate_report_content(name, birthdate, birthtime, birthplace, report_type, spiritual_focus):
    """Generate report content using OpenAI and astrology data."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY not set")
        raise ValueError("OPENAI_API_KEY not set")
    
    client = OpenAI(api_key=api_key)
    
    try:
        chart_data = calculate_chart(birthdate, birthtime, birthplace)
    except Exception as e:
        logger.error(f"Error calculating chart: {e}")
        chart_data = {}
    
    prompt = f"""Create a personalized {report_type} report for {name} born on {birthdate} at {birthtime} in {birthplace}.
Spiritual focus: {spiritual_focus}

Chart data available: {chart_data}

Write a warm, mystical, and empowering report that addresses their spiritual question.
Include practical insights and actionable guidance."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )
        content = response.choices[0].message.content
        logger.info(f"Generated content for {name}")
        return content
    except Exception as e:
        logger.error(f"Error generating content: {e}")
        return f"Unable to generate report at this time. Error: {str(e)}"

def generate_pdf(name, birthdate, birthtime, birthplace, report_type, spiritual_focus, content):
    """Generate PDF report with logo and content."""
    pdf = FPDF()
    pdf.add_page()
    
    try:
        if os.path.exists("logos/NEW_LOGO.png"):
            pdf.image("logos/NEW_LOGO.png", x=150, y=10, w=50)
    except Exception as e:
        logger.warning(f"Logo not added: {e}")
    
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


