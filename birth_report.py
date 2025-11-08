import logging
from openai import OpenAI
from fpdf import FPDF
from astrology_calc import calculate_chart
import os

logger = logging.getLogger(__name__)

def generate_report_content(name, birthdate, birthtime, birthplace, report_type, spiritual_focus):
    """Generate comprehensive report content using OpenAI and astrology data."""
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
    
    if report_type == "Deep Dive Birth Chart":
        return generate_deep_dive(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client)
    else:
        return generate_standard_report(name, birthdate, birthtime, birthplace, report_type, spiritual_focus, chart_data, client)

def generate_deep_dive(name, birthdate, birthtime, birthplace, spiritual_focus, chart_data, client):
    """Generate a comprehensive 20-25 page Deep Dive Birth Chart."""
    sections = []
    
    prompts = {
        "overview": f"""Create a compelling 2-3 paragraph COSMIC BLUEPRINT OVERVIEW for {name} born {birthdate} at {birthtime} in {birthplace}.
Include their core cosmic identity, life theme, and spiritual mission. Make it mystical, empowering, and deeply personal.
Chart data: {chart_data}
Spiritual focus: {spiritual_focus}""",
        
        "sun": f"""Write a detailed 2-3 page SUN SIGN DEEP DIVE for {name}.
Explain their core identity, ego expression, life purpose, creative power, and how they shine in the world.
Include childhood patterns, adult expression, and shadow aspects.
Chart data: {chart_data}""",
        
        "moon": f"""Write a detailed 2-3 page MOON SIGN & EMOTIONAL LANDSCAPE section.
Explore {name}'s emotional nature, inner world, needs, security patterns, and subconscious drives.
Include family patterns, emotional triggers, and path to emotional mastery.
Chart data: {chart_data}""",
        
        "rising": f"""Write a detailed 2-3 page RISING SIGN & LIFE PATH section.
Describe how {name} appears to others, their mask, first impressions, and life direction.
Include physical presence, personality projection, and life lessons through relationships.
Chart data: {chart_data}""",
        
        "houses": f"""Write a comprehensive 4-5 page PLANETARY PLACEMENTS IN HOUSES section.
For {name}, describe each planet's house placement with deep interpretation of life areas affected.
Include: career, relationships, finances, home, creativity, spirituality, and personal growth.
Chart data: {chart_data}""",
        
        "aspects": f"""Write a detailed 3-4 page MAJOR ASPECTS & COSMIC PATTERNS section.
Analyze {name}'s significant aspects (conjunctions, trines, squares, oppositions, sextiles).
Explain how these aspects create their personality, challenges, gifts, and life themes.
Chart data: {chart_data}""",
        
        "nodes": f"""Write a detailed 2-3 page KARMIC LESSONS & SOUL MISSION section.
Explore {name}'s North Node (soul growth), South Node (past patterns), and Chiron (healing journey).
Include past life themes, current life lessons, and spiritual evolution path.
Chart data: {chart_data}""",
        
        "strengths": f"""Write a 2-3 page COSMIC GIFTS & CHALLENGES section.
Detail {name}'s natural strengths, talents, and gifts from their chart.
Also explore their challenges, growth edges, and areas requiring conscious work.
Chart data: {chart_data}""",
        
        "relationships": f"""Write a 2-3 page LOVE & RELATIONSHIPS PATTERNS section.
Analyze {name}'s Venus placement, Mars placement, and 7th house for relationship patterns.
Include attraction style, love language, partnership needs, and relationship evolution.
Chart data: {chart_data}""",
        
        "career": f"""Write a 2-3 page CAREER & LIFE DIRECTION section.
Explore {name}'s 10th house, Midheaven, and planetary placements for career calling.
Include natural talents for work, ideal work environment, and life purpose alignment.
Chart data: {chart_data}""",
        
        "integration": f"""Write a 2-3 page INTEGRATION & SHADOW WORK section.
Provide 5-7 specific shadow work prompts and integration rituals for {name}.
Include journal questions, meditation practices, and rituals aligned to their chart.
Make it trauma-informed and empowering.
Spiritual focus: {spiritual_focus}"""
    }
    
    for section_name, prompt in prompts.items():
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=3000
            )
            content = response.choices[0].message.content
            sections.append(content)
            logger.info(f"Generated {section_name} section for {name}")
        except Exception as e:
            logger.error(f"Error generating {section_name}: {e}")
            sections.append(f"[Section unavailable: {str(e)}]")
    
    return "\n\n".join(sections)

def generate_standard_report(name, birthdate, birthtime, birthplace, report_type, spiritual_focus, chart_data, client):
    """Generate standard report for other report types."""
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
        logger.info(f"Generated {report_type} for {name}")
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
