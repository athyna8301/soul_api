import os
from fpdf import FPDF
from datetime import datetime
import logging
from astrology_calc import calculate_chart

logger = logging.getLogger(__name__)

def generate_birth_chart_report(name, birthdate, birthtime, birthplace, focus, email):
    """Generate birth chart report"""
    try:
        logger.info(f"Generating birth chart for {name}")
        
        # Calculate chart
        chart_data = calculate_chart(birthdate, birthtime, birthplace)
        
        # Generate content
        content = generate_report_content(name, birthdate, birthtime, birthplace, chart_data, focus)
        
        # Create PDF
        pdf_path = f"reports/{email.replace('@', '_at_')}_birth_chart.pdf"
        os.makedirs("reports", exist_ok=True)
        create_pdf(pdf_path, content, name, "Deep Dive Birth Chart")
        
        logger.info(f"Birth chart report generated: {pdf_path}")
        return pdf_path
        
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        raise

def generate_report_content(name, birthdate, birthtime, birthplace, chart_data, focus):
    """Generate report content from chart data"""
    
    # Format coordinates and timezone
    lat = chart_data['latitude']
    lon = chart_data['longitude']
    tz = chart_data['timezone']
    
    content = f"""
DEEP DIVE BIRTH CHART REPORT
For {name}

Birth Information:
Date: {birthdate}
Time: {birthtime}
Place: {birthplace}
Coordinates: {lat:.4f} N, {lon:.4f} W
Timezone: {tz}

Your Spiritual Focus: {focus}

===================================
YOUR COSMIC BLUEPRINT
===================================

THE BIG THREE

Sun Sign: {chart_data['sun']['sign']} at {chart_data['sun']['degree']:.2f} degrees
Your core essence, life force, and authentic self.

Moon Sign: {chart_data['moon']['sign']} at {chart_data['moon']['degree']:.2f} degrees
Your emotional nature, inner world, and subconscious patterns.

Rising Sign (Ascendant): {chart_data['ascendant']['sign']} at {chart_data['ascendant']['degree']:.2f} degrees
Your outer personality, how others see you, and your life path.

===================================
PLANETARY POSITIONS
===================================

Mercury in {chart_data['mercury']['sign']} at {chart_data['mercury']['degree']:.2f} degrees
Communication, thinking, and mental processes.

Venus in {chart_data['venus']['sign']} at {chart_data['venus']['degree']:.2f} degrees
Love, relationships, values, and what brings you pleasure.

Mars in {chart_data['mars']['sign']} at {chart_data['mars']['degree']:.2f} degrees
Drive, passion, anger, and how you take action.

Jupiter in {chart_data['jupiter']['sign']} at {chart_data['jupiter']['degree']:.2f} degrees
Growth, expansion, luck, and abundance.

Saturn in {chart_data['saturn']['sign']} at {chart_data['saturn']['degree']:.2f} degrees
Discipline, responsibility, lessons, and karmic patterns.

Uranus in {chart_data['uranus']['sign']} at {chart_data['uranus']['degree']:.2f} degrees
Innovation, rebellion, sudden changes, and awakening.

Neptune in {chart_data['neptune']['sign']} at {chart_data['neptune']['degree']:.2f} degrees
Dreams, intuition, spirituality, and illusions.

Pluto in {chart_data['pluto']['sign']} at {chart_data['pluto']['degree']:.2f} degrees
Transformation, power, death/rebirth, and deep healing.

===================================
LUNAR NODES & CHIRON
===================================

North Node in {chart_data['north_node']['sign']} at {chart_data['north_node']['degree']:.2f} degrees
Your soul's purpose and destiny in this lifetime.

South Node in {chart_data['south_node']['sign']} at {chart_data['south_node']['degree']:.2f} degrees
Past life gifts and patterns to release.

Chiron in {chart_data['chiron']['sign']} at {chart_data['chiron']['degree']:.2f} degrees
Your deepest wound and greatest healing gift.

===================================
HOUSE SYSTEM
===================================
"""

    # Add houses
    for i, house in enumerate(chart_data['houses'], 1):
        content += f"\nHouse {i}: {house['sign']} at {house['degree']:.2f} degrees"
    
    content += """

===================================
MAJOR ASPECTS
===================================
"""

    # Add aspects
    if chart_data['aspects']:
        for aspect in chart_data['aspects']:
            content += f"\n{aspect['planet1']} {aspect['aspect']} {aspect['planet2']} (orb: {aspect['orb']:.2f} degrees)"
    else:
        content += "\nNo major aspects within orb."

    content += """

===================================
INTERPRETATION & GUIDANCE
===================================

This chart reveals your unique cosmic blueprint. Each planetary placement, 
house position, and aspect weaves together to tell the story of your soul's 
journey in this lifetime.

Your spiritual focus on "{focus}" is deeply connected to your chart patterns.
Look to your North Node for your soul's calling, your Chiron for healing 
opportunities, and your planetary placements for how to express your gifts.

Remember: You are not defined by your chart - you are empowered by it.
The stars show possibilities, but you create your destiny.

Blessed be on your cosmic journey.

---
Report generated by SacredSpace: Through The Cosmic Lens
""".replace("{focus}", focus)

    return content


def create_pdf(path, content, name, report_type):
    """Create PDF from content"""
    
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 16)
            self.cell(0, 10, f'{report_type}', 0, 1, 'C')
            self.set_font('Arial', 'I', 10)
            self.cell(0, 5, 'SacredSpace: Through The Cosmic Lens', 0, 1, 'C')
            self.ln(5)
        
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=10)
    
    # Replace any remaining special characters
    content = content.replace('°', ' degrees')
    content = content.replace('♈', 'Aries')
    content = content.replace('♉', 'Taurus')
    content = content.replace('♊', 'Gemini')
    content = content.replace('♋', 'Cancer')
    content = content.replace('♌', 'Leo')
    content = content.replace('♍', 'Virgo')
    content = content.replace('♎', 'Libra')
    content = content.replace('♏', 'Scorpio')
    content = content.replace('♐', 'Sagittarius')
    content = content.replace('♑', 'Capricorn')
    content = content.replace('♒', 'Aquarius')
    content = content.replace('♓', 'Pisces')
    content = content.replace('"', '"')
    content = content.replace('"', '"')
    content = content.replace(''', "'")
    content = content.replace(''', "'")
    content = content.replace('—', '-')
    content = content.replace('–', '-')
    
    # Add content
    pdf.multi_cell(0, 5, content)
    
    # Save
    pdf.output(path)
