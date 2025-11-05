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
        logger.info(f"🔍 DEBUG: chart_data keys: {chart_data.keys()}")
        logger.info(f"🔍 DEBUG: chart_data content: {chart_data}")
        
        # Generate content
        content = generate_report_content(name, birthdate, birthtime, birthplace, chart_data, focus)
        
        # Create PDF
        pdf_path = f"reports/{email.replace('@', '_at_')}_birth_chart.pdf"
if not os.path.exists("reports"):
    os.makedirs("reports")
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
    
    # Extract planets and houses
    planets = chart_data['planets']
    houses = chart_data['houses']
    
    # Build content piece by piece
    lines = []
    lines.append("DEEP DIVE BIRTH CHART REPORT")
    lines.append(f"For {name}")
    lines.append("")
    lines.append("Birth Information:")
    lines.append(f"Date: {birthdate}")
    lines.append(f"Time: {birthtime}")
    lines.append(f"Place: {birthplace}")
    lines.append(f"Coordinates: {lat:.4f} N, {lon:.4f} W")
    lines.append(f"Timezone: {tz}")
    lines.append("")
    lines.append(f"Your Spiritual Focus: {focus}")
    lines.append("")
    lines.append("===================================")
    lines.append("YOUR COSMIC BLUEPRINT")
    lines.append("===================================")
    lines.append("")
    lines.append("THE BIG THREE")
    lines.append("")
    lines.append(f"Sun Sign: {planets['Sun']['sign']} at {planets['Sun']['degree']:.2f} degrees")
    lines.append("Your core essence, life force, and authentic self.")
    lines.append("")
    lines.append(f"Moon Sign: {planets['Moon']['sign']} at {planets['Moon']['degree']:.2f} degrees")
    lines.append("Your emotional nature, inner world, and subconscious patterns.")
    lines.append("")
    asc_sign = get_sign_from_longitude(houses['ascendant'])
    asc_deg = houses['ascendant'] % 30
    lines.append(f"Rising Sign (Ascendant): {asc_sign} at {asc_deg:.2f} degrees")
    lines.append("Your outer personality, how others see you, and your life path.")
    lines.append("")
    lines.append("===================================")
    lines.append("PLANETARY POSITIONS")
    lines.append("===================================")
    lines.append("")
    lines.append(f"Mercury in {planets['Mercury']['sign']} at {planets['Mercury']['degree']:.2f} degrees")
    lines.append("Communication, thinking, and mental processes.")
    lines.append("")
    lines.append(f"Venus in {planets['Venus']['sign']} at {planets['Venus']['degree']:.2f} degrees")
    lines.append("Love, relationships, values, and what brings you pleasure.")
    lines.append("")
    lines.append(f"Mars in {planets['Mars']['sign']} at {planets['Mars']['degree']:.2f} degrees")
    lines.append("Drive, passion, anger, and how you take action.")
    lines.append("")
    lines.append(f"Jupiter in {planets['Jupiter']['sign']} at {planets['Jupiter']['degree']:.2f} degrees")
    lines.append("Growth, expansion, luck, and abundance.")
    lines.append("")
    lines.append(f"Saturn in {planets['Saturn']['sign']} at {planets['Saturn']['degree']:.2f} degrees")
    lines.append("Discipline, responsibility, lessons, and karmic patterns.")
    lines.append("")
    lines.append(f"Uranus in {planets['Uranus']['sign']} at {planets['Uranus']['degree']:.2f} degrees")
    lines.append("Innovation, rebellion, sudden changes, and awakening.")
    lines.append("")
    lines.append(f"Neptune in {planets['Neptune']['sign']} at {planets['Neptune']['degree']:.2f} degrees")
    lines.append("Dreams, intuition, spirituality, and illusions.")
    lines.append("")
    lines.append(f"Pluto in {planets['Pluto']['sign']} at {planets['Pluto']['degree']:.2f} degrees")
    lines.append("Transformation, power, death/rebirth, and deep healing.")
    lines.append("")
    lines.append("===================================")
    lines.append("LUNAR NODES & CHIRON")
    lines.append("===================================")
    lines.append("")
    lines.append(f"North Node in {planets['North Node']['sign']} at {planets['North Node']['degree']:.2f} degrees")
    lines.append("Your soul's purpose and destiny in this lifetime.")
    lines.append("")
    south_sign = get_opposite_sign(planets['North Node']['sign'])
    south_deg = (planets['North Node']['longitude'] + 180) % 30
    lines.append(f"South Node in {south_sign} at {south_deg:.2f} degrees")
    lines.append("Past life gifts and patterns to release.")
    lines.append("")
    lines.append(f"Chiron in {planets['Chiron']['sign']} at {planets['Chiron']['degree']:.2f} degrees")
    lines.append("Your deepest wound and greatest healing gift.")
    lines.append("")
    lines.append("===================================")
    lines.append("HOUSE SYSTEM")
    lines.append("===================================")
    
    for i, cusp in enumerate(houses['cusps'], 1):
        sign = get_sign_from_longitude(cusp)
        degree = cusp % 30
        lines.append(f"House {i}: {sign} at {degree:.2f} degrees")
    
    lines.append("")
    lines.append("===================================")
    lines.append("INTERPRETATION & GUIDANCE")
    lines.append("===================================")
    lines.append("")
    lines.append("This chart reveals your unique cosmic blueprint. Each planetary placement,")
    lines.append("house position, and aspect weaves together to tell the story of your soul's")
    lines.append("journey in this lifetime.")
    lines.append("")
    lines.append(f"Your spiritual focus on '{focus}' is deeply connected to your chart patterns.")
    lines.append("Look to your North Node for your soul's calling, your Chiron for healing")
    lines.append("opportunities, and your planetary placements for how to express your gifts.")
    lines.append("")
    lines.append("Remember: You are not defined by your chart - you are empowered by it.")
    lines.append("The stars show possibilities, but you create your destiny.")
    lines.append("")
    lines.append("Blessed be on your cosmic journey.")
    lines.append("")
    lines.append("---")
    lines.append("Report generated by SacredSpace: Through The Cosmic Lens")
    
    return "\n".join(lines)


def get_sign_from_longitude(longitude):
    """Convert longitude to zodiac sign"""
    signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
             'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    return signs[int(longitude / 30) % 12]


def get_opposite_sign(sign):
    """Get opposite zodiac sign"""
    signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
             'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    idx = signs.index(sign)
    return signs[(idx + 6) % 12]


def create_pdf(path, content, name, report_type):
    """Create PDF from content"""
    
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 16)
            self.cell(0, 10, report_type, 0, 1, 'C')
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
    
    # Add content
    pdf.multi_cell(0, 5, content)
    
    # Save
    pdf.output(path)
