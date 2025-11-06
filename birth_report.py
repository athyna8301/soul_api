import os
from fpdf import FPDF
from datetime import datetime
from openai import OpenAI
import logging
from astrology_calc import calculate_chart

logger = logging.getLogger(__name__)
def generate_ai_interpretation(name, birthdate, birthtime, birthplace, chart_data, focus):
    """Generate AI-powered astrological interpretation"""
    try:
        # Initialize OpenAI client
        import os
        # Initialize OpenAI client
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            logger.error("OPENAI_API_KEY environment variable not set!")
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        logger.info(f"API key found: {api_key[:10]}...")  # Log first 10 chars for debugging
        client = OpenAI(api_key=api_key)

        
        # Extract key chart data
        sun = chart_data['planets']['Sun']
        moon = chart_data['planets']['Moon']
        mercury = chart_data['planets']['Mercury']
        venus = chart_data['planets']['Venus']
        mars = chart_data['planets']['Mars']
        jupiter = chart_data['planets']['Jupiter']
        saturn = chart_data['planets']['Saturn']
        
        # Get rising sign
        # Get rising sign (calculate it directly)
asc_degree = chart_data['houses']['ascendant']
signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
rising_sign = signs[int(asc_degree / 30) % 12]
        
        # Create detailed prompt
        prompt = f"""You are a professional astrologer with expertise in trauma-informed spiritual guidance, shadow work, and empowerment. Write as a Sacred Warrior-Healer.

Generate a comprehensive Deep Dive Birth Chart interpretation for {name}.

BIRTH DATA:
- Born: {birthdate} at {birthtime} in {birthplace}
- Coordinates: {chart_data['latitude']:.4f}°, {chart_data['longitude']:.4f}°
- Timezone: {chart_data['timezone']}

CHART PLACEMENTS:
- Sun: {sun['sign']} at {sun['degree']:.1f}° {'(Retrograde)' if sun['retrograde'] else ''}
- Moon: {moon['sign']} at {moon['degree']:.1f}° {'(Retrograde)' if moon['retrograde'] else ''}
- Rising (Ascendant): {rising_sign} at {asc_degree:.1f}°
- Mercury: {mercury['sign']} at {mercury['degree']:.1f}° {'(Retrograde)' if mercury['retrograde'] else ''}
- Venus: {venus['sign']} at {venus['degree']:.1f}° {'(Retrograde)' if venus['retrograde'] else ''}
- Mars: {mars['sign']} at {mars['degree']:.1f}° {'(Retrograde)' if mars['retrograde'] else ''}
- Jupiter: {jupiter['sign']} at {jupiter['degree']:.1f}° {'(Retrograde)' if jupiter['retrograde'] else ''}
- Saturn: {saturn['sign']} at {saturn['degree']:.1f}° {'(Retrograde)' if saturn['retrograde'] else ''}

SPIRITUAL FOCUS: {focus}

Write a deeply personalized, mystical, and empowering interpretation (2500-3000 words) that includes:

1. CORE ESSENCE (Sun Sign)
   - Soul identity and life purpose
   - Natural gifts and authentic self-expression
   - How to embody this energy fully

2. EMOTIONAL LANDSCAPE (Moon Sign)
   - Emotional needs and inner world
   - How you process feelings and find comfort
   - Shadow work prompts for emotional healing

3. OUTER PERSONA (Rising Sign)
   - How you show up in the world
   - First impressions and life approach
   - Your cosmic mask and authentic presence

4. MIND & COMMUNICATION (Mercury)
   - How you think and communicate
   - Learning style and mental gifts
   - Ways to honor your unique voice

5. LOVE & VALUES (Venus)
   - How you love and what you value
   - Relationship patterns and desires
   - Self-love practices

6. DRIVE & ACTION (Mars)
   - How you take action and assert yourself
   - Passion, anger, and healthy boundaries
   - Sacred rage and empowered action

7. EXPANSION & WISDOM (Jupiter)
   - Where you find meaning and growth
   - Natural abundance and optimism
   - Spiritual gifts

8. DISCIPLINE & MASTERY (Saturn)
   - Life lessons and karmic themes
   - Where you build lasting foundations
   - Shadow work for Saturn healing

9. SACRED GUIDANCE
   - Personalized guidance for their spiritual focus: "{focus}"
   - Ritual recommendations aligned with their chart
   - Empowering affirmations
   - Next steps on their cosmic journey

Use mystical, poetic language. Be trauma-informed, compassionate, and empowering. Avoid jargon. Make it feel like a sacred conversation between souls.

End with a powerful closing that honors their cosmic blueprint and encourages their transformation."""

        # Call OpenAI API
        logger.info("Generating AI interpretation...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Cost-effective and great quality
            messages=[
                {"role": "system", "content": "You are a professional astrologer specializing in trauma-informed spiritual guidance, shadow work, and empowerment. You write as a Sacred Warrior-Healer with mystical, compassionate, and empowering language."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,  # Creative but coherent
            max_tokens=4000   # Enough for 2500-3000 words
        )
        
        interpretation = response.choices[0].message.content
        logger.info(f"AI interpretation generated: {len(interpretation)} characters")
        
        return interpretation
        
    except Exception as e:
        logger.error(f"Error generating AI interpretation: {e}")
        # Return fallback content if AI fails
        return f"""
# Your Cosmic Blueprint

Dear {name},

Your birth chart reveals a unique cosmic signature that holds the keys to your soul's journey.

**Sun in {sun['sign']}**: Your core essence radiates the energy of {sun['sign']}, guiding your life purpose and authentic self-expression.

**Moon in {moon['sign']}**: Your emotional world is colored by {moon['sign']}, showing how you nurture yourself and process feelings.

**Rising in {rising_sign}**: You meet the world through the lens of {rising_sign}, shaping how others perceive you and how you approach life.

This is just the beginning of understanding your cosmic blueprint. Each planetary placement holds deeper wisdom waiting to be discovered.

Your spiritual focus on "{focus}" is woven throughout your chart, offering guidance for your journey ahead.

With cosmic blessings,
SacredSpace: Through The Cosmic Lens 🌙
"""

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
        
        # Remove 'reports' if it exists as a file
        if os.path.exists("reports") and not os.path.isdir("reports"):
            os.remove("reports")
        
        # Create directory if it doesn't exist
        if not os.path.exists("reports"):
            os.makedirs("reports")
        
        create_pdf(pdf_path, content, name, "Deep Dive Birth Chart")
        
        logger.info(f"Birth chart report generated: {pdf_path}")
        return pdf_path
        
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        raise

def generate_report_content(name, birthdate, birthtime, birthplace, chart_data, focus):
    """Generate report content from chart data using AI"""
    
    # Generate AI interpretation
    ai_content = generate_ai_interpretation(name, birthdate, birthtime, birthplace, chart_data, focus)
    
    # Build complete report
    content = f"""# Deep Dive Birth Chart Report
## For {name}

**Birth Details:**
- Date: {birthdate}
- Time: {birthtime}
- Place: {birthplace}
- Location: {chart_data['full_address']}
- Coordinates: {chart_data['latitude']:.4f}°, {chart_data['longitude']:.4f}°
- Timezone: {chart_data['timezone']}

---

{ai_content}

---

## Technical Chart Data

**Planetary Positions:**
"""
    
    # Add planetary data
    for planet, data in chart_data['planets'].items():
        retro = " ℞" if data['retrograde'] else ""
        content += f"\n- **{planet}**: {data['sign']} {data['degree']:.2f}°{retro}"
    
    # Add house data
    content += "\n\n**House Cusps:**\n"
    for i, cusp in enumerate(chart_data['houses']['cusps'], 1):
        sign = get_zodiac_sign(cusp)
        content += f"\n- House {i}: {sign} {cusp:.2f}°"
    
    content += f"\n\n**Ascendant**: {get_zodiac_sign(chart_data['houses']['ascendant'])} {chart_data['houses']['ascendant']:.2f}°"
    content += f"\n**Midheaven (MC)**: {get_zodiac_sign(chart_data['houses']['mc'])} {chart_data['houses']['mc']:.2f}°"
    
    content += "\n\n---\n\n*Report generated with love by SacredSpace: Through The Cosmic Lens* 🌙"
    
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
