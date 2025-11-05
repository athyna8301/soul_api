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
    
    # Extract planets and houses
    planets = chart_data['planets']
    houses = chart_data['houses']
    
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

Sun Sign: {planets['Sun']['sign']} at {planets['Sun']['degree']:.2f} degrees
Your core essence, life force, and authentic self.

Moon Sign: {planets['Moon']['sign']} at {planets['Moon']['degree']:.2f} degrees
Your emotional nature, inner world, and subconscious patterns.

Rising Sign (Ascendant): {get_sign_from_longitude(houses['ascendant'])} at {houses['ascendant'] % 30:.2f} degrees
Your outer personality, how others see you, and your life path.

===================================
PLANETARY POSITIONS
===================================

Mercury in {planets['Mercury']['sign']} at {planets['Mercury']['degree']:.2f} degrees
Communication, thinking, and mental processes.

Venus in {planets['Venus']['sign']} at {planets['Venus']['degree']:.2f} degrees
Love, relationships, values, and what brings you pleasure.

Mars in {planets['Mars']['sign']} at {planets['Mars']['degree']:.2f} degrees
Drive, passion, anger, and how you take action.

Jupiter in {planets['Jupiter']['sign']} at {planets['Jupiter']['degree']:.2f} degrees
Growth, expansion, luck, and abundance.

Saturn in {planets['Saturn']['sign']} at {planets['Saturn']['degree']:.2f} degrees
Discipline, responsibility, lessons, and karmic patterns.

Uranus in {planets['Uranus']['sign']} at {planets['Uranus']['degree']:.2f} degrees
Innovation, rebellion, sudden changes, and awakening.

Neptune in {planets['Neptune']['sign']} at {planets['Neptune']['degree']:.2f} degrees
Dreams, intuition, spirituality, and illusions.

Pluto in {planets['Pluto']['sign']} at {planets['Pluto']['degree']:.2f} degrees
Transformation, power, death/rebirth, and deep healing.

===================================
LUNAR NODES & CHIRON
===================================

North Node in {planets['North Node']['sign']} at {planets['North Node']['degree']:.2f} degrees
Your soul's purpose and destiny in this lifetime.

South Node in {get_opposite_sign(planets['North Node']['sign'])} at {(planets['North Node']['longitude'] + 180) % 30:.2f} degrees
Past life gifts and patterns to release.

Chiron in {planets['Chiron']['sign']} at {planets['Chiron']['degree']:.2f} degrees
Your deepest wound and greatest healing gift.

===================================
HOUSE SYSTEM
===================================
"""

    # Add houses
    for i, cusp in enumerate(houses['cusps'], 1):
        sign = get_sign_from_longitude(cusp)
        degree = cusp % 30
        content += f"\nHouse {i}: {sign} at {degree:.2f} degrees"
    
    content += """

===================================
INTERPRETATION & GUIDANCE
===================================

This chart reveals your unique cosmic blueprint. Each planetary placement, 
house position, and aspect weaves together to tell the story of your soul's 
journey in this lifetime.

Your spiritual focus on \"""" + focus + """\" is deeply connected to your chart patterns.
Look to your North Node for your soul's calling, your Chiron for healing 
opportunities, and your planetary placements for how to express your gifts.

Remember: You are not defined by your chart - you are empowered by it.
The stars show possibilities, but you create your destiny.

Blessed be on your cosmic journey.

---
Report generated by SacredSpace: Through The Cosmic Lens
"""

    return content


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
    content = content.replace('°
