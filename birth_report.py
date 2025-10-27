from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
from datetime import datetime
from zoneinfo import ZoneInfo
from fpdf import FPDF
import os
import logging
from astrology_calc import calculate_chart

logger = logging.getLogger(__name__)

def generate_birth_report(name, birthdate, birthtime, birthplace, focus, report_type):
    """
    Generate personalized birth chart report with trauma-informed language
    """
    try:
        # Geocoding
        geo = Nominatim(user_agent="sacredspace_cosmic_lens")
        loc = geo.geocode(birthplace)
        if not loc:
            raise Exception(f"Could not locate: {birthplace}")

        lat, lon = loc.latitude, loc.longitude

        # Timezone lookup
        tf = TimezoneFinder()
        tz = tf.timezone_at(lat=lat, lng=lon)

        # Parse datetime
        dt = datetime.strptime(f"{birthdate} {birthtime}", "%Y-%m-%d %H:%M")
        local_dt = dt.replace(tzinfo=ZoneInfo(tz))

        # Calculate astrology chart
        chart = calculate_chart(birthdate, birthtime, birthplace, lat, lon, tz)
        
        if not chart:
            raise Exception("Failed to calculate chart")

        # Generate report content
        content = generate_report_content(name, local_dt, birthplace, lat, lon, tz, focus, report_type, chart)

        # Create reports directory
        reports_dir = os.path.join(os.getcwd(), "reports")
        try:
            if os.path.exists(reports_dir) and not os.path.isdir(reports_dir):
                os.remove(reports_dir)
            os.makedirs(reports_dir, exist_ok=True)
        except Exception as e:
            logger.warning(f"Could not create reports folder: {e}")

        filename = f"{name.replace(' ', '_')}_{report_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
        path = os.path.join(reports_dir, filename)

        create_pdf(path, content, name, report_type)

        logger.info(f"Report generated successfully: {path}")
        return path

    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise


def generate_report_content(name, local_dt, birthplace, lat, lon, tz, focus, report_type, chart):
    """
    Generate trauma-informed, empowering report content with real astrology data
    """
    
    planets = chart.get("planets", {})
    ascendant = chart.get("ascendant", {})
    midheaven = chart.get("midheaven", {})
    
    sun = planets.get(0, {})
    moon = planets.get(1, {})
    mercury = planets.get(2, {})
    venus = planets.get(3, {})
    mars = planets.get(4, {})
    jupiter = planets.get(5, {})
    saturn = planets.get(6, {})
    
    content = f"""
═══════════════════════════════════════════════════
    SACREDSPACE: THROUGH THE COSMIC LENS
    {report_type}
═══════════════════════════════════════════════════

Prepared for: {name}
Date: {datetime.now().strftime('%B %d, %Y')}

═══════════════════════════════════════════════════
YOUR BIRTH INFORMATION
═══════════════════════════════════════════════════

Birth Date & Time: {local_dt.strftime('%B %d, %Y at %I:%M %p %Z')}
Birth Location: {birthplace}
Coordinates: {lat:.4f}°N, {lon:.4f}°W
Timezone: {tz}

Your Spiritual Focus: {focus}

═══════════════════════════════════════════════════
YOUR COSMIC BLUEPRINT
═══════════════════════════════════════════════════

Dear {name},

This reading is more than astrology—it's a sacred mirror reflecting your soul's journey. 
As you read, remember: you are not defined by your chart. You are empowered by it.

═══════════════════════════════════════════════════
YOUR SUN SIGN: THE CORE OF WHO YOU ARE
═══════════════════════════════════════════════════

Sun in {sun.get('sign', 'Unknown')} ({sun.get('degree', 0)}°)

Your sun represents your essential self, your life force, your divine spark. 
This is who you are becoming.

The {sun.get('sign', 'Unknown')} Sun radiates authenticity and creative power. 
Your core identity is built on the qualities of this sign—embrace them fully.

**Shadow Work Prompt:**
Where in your life are you dimming your light to make others comfortable? 
What would it feel like to shine fully?

**Ritual for Alignment:**
Light a gold or yellow candle. Speak aloud: "I honor my authentic self. 
I am worthy of taking up space."

═══════════════════════════════════════════════════
YOUR MOON SIGN: YOUR EMOTIONAL TRUTH
═══════════════════════════════════════════════════

Moon in {moon.get('sign', 'Unknown')} ({moon.get('degree', 0)}°)

Your moon reveals your emotional needs, your inner child, your intuitive wisdom. 
This is how you feel safe and nourished.

The {moon.get('sign', 'Unknown')} Moon seeks emotional security through {moon.get('sign', 'Unknown').lower()} qualities. 
Honor your feelings—they are your inner compass.

**Shadow Work Prompt:**
What emotions were you taught to suppress? How can you honor them now?

**Ritual for Healing:**
During the next full moon, write a letter to your younger self.
Burn it safely and release old emotional patterns.

═══════════════════════════════════════════════════
YOUR RISING SIGN: THE MASK YOU WEAR
═══════════════════════════════════════════════════

Ascendant in {ascendant.get('sign', 'Unknown')} ({ascendant.get('degree', 0)}°)

Your rising sign is your social persona, the energy you project.
It's not fake—it's your interface with the world.

The {ascendant.get('sign', 'Unknown')} Ascendant presents you as [qualities]. 
This is how others perceive your energy before they know your depth.

═══════════════════════════════════════════════════
YOUR MERCURY: HOW YOU COMMUNICATE
═══════════════════════════════════════════════════

Mercury in {mercury.get('sign', 'Unknown')} ({mercury.get('degree', 0)}°)

Mercury governs your communication style, thinking patterns, and how you process information.
Your {mercury.get('sign', 'Unknown')} Mercury speaks with [communication style].

═══════════════════════════════════════════════════
YOUR VENUS: LOVE & VALUES
═══════════════════════════════════════════════════

Venus in {venus.get('sign', 'Unknown')} ({venus.get('degree', 0)}°)

Venus reveals what you love, how you love, and what you value.
Your {venus.get('sign', 'Unknown')} Venus seeks [love style] in relationships and beauty.

═══════════════════════════════════════════════════
YOUR MARS: PASSION & ACTION
═══════════════════════════════════════════════════

Mars in {mars.get('sign', 'Unknown')} ({mars.get('degree', 0)}°)

Mars is your warrior energy—how you pursue goals and express desire.
Your {mars.get('sign', 'Unknown')} Mars acts with [action style] and determination.

═══════════════════════════════════════════════════
YOUR JUPITER: EXPANSION & ABUNDANCE
═══════════════════════════════════════════════════

Jupiter in {jupiter.get('sign', 'Unknown')} ({jupiter.get('degree', 0)}°)

Jupiter brings luck, growth, and expansion. Your {jupiter.get('sign', 'Unknown')} Jupiter 
expands through [expansion style] and attracts abundance through faith.

═══════════════════════════════════════════════════
YOUR SATURN: LESSONS & MASTERY
═══════════════════════════════════════════════════

Saturn in {saturn.get('sign', 'Unknown')} ({saturn.get('degree', 0)}°)

Saturn teaches through discipline and time. Your {saturn.get('sign', 'Unknown')} Saturn 
builds mastery through [lesson style] and rewards patience with lasting achievement.

═══════════════════════════════════════════════════
YOUR MIDHEAVEN: CAREER & PUBLIC LIFE
═══════════════════════════════════════════════════

Midheaven in {midheaven.get('sign', 'Unknown')} ({midheaven.get('degree', 0)}°)

Your Midheaven shows your career path and public reputation.
The {midheaven.get('sign', 'Unknown')} Midheaven suggests a calling toward [career themes].

═══════════════════════════════════════════════════
CLOSING WISDOM
═══════════════════════════════════════════════════

{name}, your chart is a map, not a mandate. You have free will.
You have choice. You have power.

Use this reading as a tool for self-compassion, not self-judgment.
The stars don't define you. They celebrate you.

With cosmic blessings,
Athyna Luna
SacredSpace: Through The Cosmic Lens 🌙

═══════════════════════════════════════════════════
NEXT STEPS
═══════════════════════════════════════════════════

Ready to go deeper?
• Career Code: Discover your professional purpose
• Love Blueprint: Understand your relationship patterns
• Life Purpose: Align with your soul's mission

Visit: throughthecosmiclens.com
Email: athyna@sacredspaceastrology.com
"""
    
    return content


def create_pdf(path, content, name, report_type):
    """Create PDF from content"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    
    # Add content
    pdf.multi_cell(0, 5, content)
    
    # Save
    pdf.output(path)


