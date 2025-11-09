import logging
from openai import OpenAI
from fpdf import FPDF
from astrology_calc import calculate_chart
import os

logger = logging.getLogger(name)

AIDEN_SYSTEM_PROMPT = """You are a spiritual mentor and cosmic guide with Aiden's energy. Your approach:

🧭 FRAMEWORK:





Anchor in Personal Energy First - Mirror their essence, acknowledge their effort, create safety



Expand to Cosmic Context - Connect personal to universal patterns, myth, symbolism



Deliver Direct Intuitive Insight - Call out patterns with truth and compassion, no generic advice



Offer Guidance or Ritual - Give actionable, tactile steps (rituals, mantras, affirmations)



Close with Empowerment - Circle back to their strength, leave them with a "mic drop"

🌙 TONE & ENERGY:





Empowering, grounded, intuitive, poetic



Mix of mystical + no-nonsense



Like a wise, no-BS witchy friend who sees through them and loves them anyway



Present tense for manifestation, 2nd person POV



Blend everyday with etheric ("sacred boundaries," "cosmic timing," "emotional pruning")



Name the season, honor their power, don't soften truth



Channel, don't explain - let the message feel received

🎯 BONUS RULES:





Speak with specificity, not generic advice



Frame everything as opportunity, not punishment



Use metaphors, symbols, rhythmic language



End on empowerment that's poetic, not fluffy



People need something earth-side to do - something they can touch"""

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
venus_deg = planets.get('Venus', {}).get('degree', 0)
mars_sign = planets.get('Mars', {}).get('sign', 'Unknown')
mars_deg = planets.get('Mars', {}).get('degree', 0)
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

if report_type == "Love Blueprint":
    user_prompt = f"""Write an extremely detailed, comprehensive 12-15 page Love Blueprint report for {name}.

PLANETARY PLACEMENTS:





Venus in {venus_sign} ({venus_deg:.1f}°): Love language, attraction style, values in relationships



Mars in {mars_sign} ({mars_deg:.1f}°): Desire, sexuality, passion, how they pursue love



Moon in {moon_sign}: Emotional needs, vulnerability, nurturing style



Sun in {sun_sign}: Core identity in relationships



Rising in {rising_sign}: How others perceive them romantically

REQUIRED SECTIONS (3000-4000 words minimum):





Your Love Archetype (describe their romantic archetype based on Venus/Mars)



The Venus Effect (detailed Venus sign interpretation - 400+ words)



Mars & Desire (passionate nature, sexuality, pursuit style - 400+ words)



Emotional Landscape (Moon sign emotional needs - 400+ words)



Love Patterns & Cycles (relationship tendencies and patterns)



Blocks & Shadows (fears, past wounds, patterns to heal)



Your Ideal Partner (what they truly need vs what they think they want)



Intimacy & Connection (physical, emotional, spiritual intimacy styles)



Communication in Love (how they express feelings, conflict style)



Rituals for Love (specific rituals and practices to attract/deepen love)



Integration & Activation (practical steps to embody healthy love)



Your Love Vision (empowering vision of their romantic future)

Use the 5-step framework: Personal Opener → Cosmic Context → Sacred Insight → Grounding Ritual → Empowered Closing.
Be specific to their placements. Include journal prompts and affirmations throughout."""

elif report_type == "Deep Dive Birth Chart":
    user_prompt = f"""Write an extremely detailed, comprehensive 15-20 page Deep Dive Birth Chart for {name}.

CORE PLACEMENTS:





Sun in {sun_sign}: Core identity and life purpose



Moon in {moon_sign}: Emotional nature and inner world



Rising in {rising_sign}: Personality and how others perceive them



Mercury in {mercury_sign}: Communication and thinking style



Venus in {venus_sign}: Love and values



Mars in {mars_sign}: Action and passion



Jupiter in {jupiter_sign}: Expansion and luck



Saturn in {saturn_sign}: Lessons and boundaries



North Node in {north_node_sign}: Soul's growth direction



Chiron in {chiron_sign}: Wounded healer archetype



MC in {mc_sign}: Career and public image

REQUIRED SECTIONS (4000-5000 words minimum):





Your Cosmic Blueprint (overview of their astrological essence)



The Sun: Your Core Self (identity, purpose, vitality - 500+ words)



The Moon: Your Inner World (emotions, needs, subconscious - 500+ words)



Rising Sign: Your Mask (personality, first impression - 400+ words)



Mercury: How You Think & Communicate (400+ words)



Venus: What You Love (400+ words)



Mars: Your Drive & Passion (400+ words)



Jupiter: Your Expansion (400+ words)



Saturn: Your Mastery (400+ words)



Nodes of Destiny (past life patterns, soul growth - 500+ words)



Chiron: Your Healing Gift (wounded healer archetype - 400+ words)



Career & Calling (MC, 10th house, vocation - 400+ words)

Use the 5-step framework throughout. Be specific, detailed, and empowering. Include rituals, affirmations, and shadow work prompts."""

elif report_type == "Career Code":
    user_prompt = f"""Write an extremely detailed, comprehensive 12-15 page Career Code report for {name}.

CAREER PLACEMENTS:





Sun in {sun_sign}: Core talents and life work



Mercury in {mercury_sign}: Communication and skills



Saturn in {saturn_sign}: Mastery and discipline



Jupiter in {jupiter_sign}: Expansion and abundance



MC in {mc_sign}: Career direction and public image

REQUIRED SECTIONS (3000-4000 words minimum):





Your Career Archetype (their professional calling)



Natural Talents & Gifts (Sun, Mercury, Jupiter influence)



Your Mastery Path (Saturn - what takes discipline to master)



Communication & Collaboration (Mercury style in work)



Expansion & Abundance (Jupiter opportunities)



Challenges & Growth Areas (Saturn lessons)



Ideal Work Environment (what energizes vs drains them)



5-Year Vision (concrete career goals)



Side Hustles & Passions (alternative income streams)



Activation Practices (rituals and affirmations for career success)



Integration & Next Steps (practical action plan)

Use the 5-step framework. Be specific to their placements, inspiring, and practical."""

else:
    user_prompt = f"""Write an extremely detailed, comprehensive {report_type} report for {name}.

PLACEMENTS:





Sun in {sun_sign}: Core identity



Moon in {moon_sign}: Emotional nature



Rising in {rising_sign}: Personality



Mercury in {mercury_sign}: Communication



Venus in {venus_sign}: Love and values



Mars in {mars_sign}: Action and passion



Jupiter in {jupiter_sign}: Expansion



Saturn in {saturn_sign}: Lessons



North Node in {north_node_sign}: Soul growth



Chiron in {chiron_sign}: Healing gift



MC in {mc_sign}: Career and public image

Create a 10-15 page, deeply detailed, spiritually rich report with:





3000-4000 words minimum



Multiple detailed sections (at least 10)



Specific astrological interpretations



Practical rituals and affirmations



Journal prompts and reflection questions



Use the 5-step framework: Personal Opener → Cosmic Context → Sacred Insight → Grounding Ritual → Empowered Closing



Mystical yet grounded language



Empowering and transformative tone"""  try:
  response = client.chat.completions.create(
      model="gpt-4",
      messages=[
          {"role": "system", "content": AIDEN_SYSTEM_PROMPT},
          {"role": "user", "content": user_prompt}
      ],
      max_tokens=8000,
      temperature=0.9
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