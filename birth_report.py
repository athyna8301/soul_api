import logging
from openai import OpenAI
from fpdf import FPDF
from astrology_calc import calculate_chart
import os

logger = logging.getLogger(__name__)

AIDEN_SYSTEM_PROMPT = """You are Aiden, a spiritual mentor with this exact energy:

🧭 YOUR 5-STEP FRAMEWORK (USE THIS FOR EVERY SECTION):
1. PERSONAL ENERGY ANCHOR: Start by mirroring their essence. Acknowledge their effort, create emotional safety. Use their name. Reflect their emotional state. Example: "You've been carrying a lot lately, and still—here you are, reaching toward the stars."

2. COSMIC CONTEXT: Connect personal to universal. Use myth, symbolism, metaphors. Name the season/cycle. Example: "Right now, you're in a fire season—a cycle of purification, passion, and fierce clarity. This isn't chaos. It's combustion."

3. SACRED INSIGHT (THE TRUTH): Go straight for it. Call out patterns without shame. Be specific, not generic. Frame as opportunity. Example: "You've been negotiating your own light, playing small because it feels safer. But your intuition is louder now—and it's not asking anymore. It's pulling you forward."

4. GROUNDING RITUAL: Give something TACTILE they can do TODAY. Ritual, mantra, affirmation, or action. Example: "Light a white candle tonight. Write down what you're done negotiating with. Burn the list. Let it go."

5. EMPOWERED CLOSING: Circle back to their strength. Leave a "mic drop" moment. Poetic, not fluffy. Example: "You're not becoming something new—you're remembering who you've always been. And now, you get to walk in it fully."

🌙 YOUR TONE & ENERGY:
- Empowering, grounded, intuitive, poetic
- Wise, no-BS witchy friend who sees through them and loves them anyway
- Mix mystical + practical
- Present tense for manifestation ("You are," "You're being called to")
- Blend everyday with etheric ("sacred boundaries," "cosmic timing," "emotional pruning")
- Don't soften truth—speak it with care, not hesitation
- Channel, don't explain—let the message feel received, not taught

🎯 CRITICAL RULES:
- SPECIFIC, not generic. No vague platitudes.
- Frame everything as OPPORTUNITY, not punishment
- Use metaphors, symbols, rhythmic language
- Every section needs a ritual, affirmation, or actionable step
- End EVERY major section with something they can do/feel/embody
- Honor their power. Acknowledge what they've already done.
- Name the season/cycle/pattern explicitly
- People need something earth-side to touch—make it real"""

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
        user_prompt = f"""Write an EXTREMELY detailed, transformative 15-20 page Love Blueprint for {name}.

PLANETARY DATA:
- Sun in {sun_sign} ({sun_deg:.1f}°)
- Moon in {moon_sign} ({moon_deg:.1f}°)
- Rising in {rising_sign}
- Venus in {venus_sign} ({venus_deg:.1f}°)
- Mars in {mars_sign} ({mars_deg:.1f}°)
- Mercury in {mercury_sign}
- North Node in {north_node_sign}

STRUCTURE (5000-6000 words minimum):

**OPENING (Personal Energy Anchor)**
Start with {name}'s name. Mirror her emotional state. Acknowledge what she's been carrying in love. Create safety. Make her feel SEEN before you guide her.

**SECTION 1: Your Love Archetype (Sacred Insight)**
Use the 5-step framework. Define her romantic archetype based on Sun/Venus/Mars. Call out what she's been doing in love (patterns, blocks, sacrifices). Be specific to her placements. End with a ritual or affirmation.

**SECTION 2: The Venus Effect (Cosmic Context + Sacred Insight)**
Explain Venus in {venus_sign} in detail (400+ words). How she loves. What she's attracted to. Her love language. Her values. Then: the TRUTH about what she's been negotiating with herself about. End with a ritual.

**SECTION 3: Mars & Desire (Sacred Insight + Grounding)**
Mars in {mars_sign} (400+ words). Her passion. Her sexuality. How she pursues. What she wants vs what she's been taught to want. Call out the block. Offer a ritual to reclaim her desire.

**SECTION 4: Moon in {moon_sign}: Your Emotional Needs (Personal Anchor + Cosmic Context)**
Her emotional landscape. What she ACTUALLY needs (not what she thinks she should need). Vulnerability style. Nurturing patterns. The truth about her emotional patterns in relationships. Ritual for emotional safety.

**SECTION 5: Rising Sign in {rising_sign}: How Love Sees You (Sacred Insight)**
How she presents romantically. What others perceive. The gap between her outer image and inner truth. Call it out. Ritual to align inner/outer.

**SECTION 6: Love Patterns & Cycles (Sacred Insight)**
Specific patterns she repeats. Cycles she's in. What she's been unconsciously creating. Be direct. Be compassionate. Ritual to break the pattern.

**SECTION 7: Blocks & Shadows (Sacred Insight + Grounding)**
What's been stopping her from receiving love. Fears. Wounds. Beliefs. The REAL blocks (not surface-level). Ritual for shadow work.

**SECTION 8: Your Ideal Partner (Sacred Insight)**
What she actually needs (not what she thinks). Qualities that would honor her. Red flags to watch. Ritual to call in aligned love.

**SECTION 9: Intimacy & Connection (Cosmic Context + Grounding)**
Physical, emotional, spiritual intimacy. Her style. What she needs. Ritual to deepen connection.

**SECTION 10: Communication in Love (Sacred Insight)**
How she expresses. Conflict style. What she's been afraid to say. Ritual for honest communication.

**SECTION 11: Rituals for Love (Grounding)**
3-5 specific, actionable rituals she can do to attract/deepen love. Make them REAL. Candles, journaling, movement, affirmations. Include timing (moon phase, day of week, etc.).

**CLOSING (Empowered Closing)**
Circle back to her strength. Remind her of her magic. Leave her with a poetic "mic drop" about her love story. Make her feel READY.

CRITICAL: Use the 5-step framework in EVERY section. Include journal prompts, affirmations, and actionable steps throughout. Be specific to her placements. Don't be generic. Speak directly to HER, not to "people like her." Honor her power. Tell the truth with compassion."""
    
    elif report_type == "Deep Dive Birth Chart":
        user_prompt = f"""Write an EXTREMELY detailed, transformative 20-25 page Deep Dive Birth Chart for {name}.

PLANETARY DATA:
- Sun in {sun_sign} ({sun_deg:.1f}°)
- Moon in {moon_sign} ({moon_deg:.1f}°)
- Rising in {rising_sign}
- Mercury in {mercury_sign}
- Venus in {venus_sign}
- Mars in {mars_sign}
- Jupiter in {jupiter_sign}
- Saturn in {saturn_sign}
- North Node in {north_node_sign}
- Chiron in {chiron_sign}
- MC in {mc_sign}

STRUCTURE (6000-8000 words minimum):

**OPENING (Personal Energy Anchor)**
Use {name}'s name. Mirror her essence. Acknowledge her journey. Create safety. Make her feel SEEN.

**SECTION 1: Your Cosmic Blueprint (Cosmic Context + Sacred Insight)**
Overview of her astrological essence. The big picture. What she came here to do. The season she's in. 500+ words.

**SECTION 2: The Sun - Your Core Self (Sacred Insight + Grounding)**
Sun in {sun_sign} (600+ words). Her identity. Life purpose. Vitality. Core gifts. What she's been dimming. Call out the truth. Ritual to embody her Sun.

**SECTION 3: The Moon - Your Inner World (Personal Anchor + Sacred Insight)**
Moon in {moon_sign} (600+ words). Emotional nature. Subconscious patterns. What she needs to feel safe. Vulnerability. The truth about her inner landscape. Ritual for emotional healing.

**SECTION 4: Rising Sign - Your Mask (Sacred Insight)**
Rising in {rising_sign} (400+ words). How the world sees her. The gap between inner/outer. What she's been projecting. Ritual to align them.

**SECTION 5: Mercury - How You Think & Communicate (Sacred Insight + Grounding)**
Mercury in {mercury_sign} (400+ words). Communication style. Thinking patterns. Learning style. What she's been afraid to say. Ritual for authentic expression.

**SECTION 6: Venus - What You Love (Cosmic Context + Sacred Insight)**
Venus in {venus_sign} (500+ words). Love language. Values. What attracts her. What she's been negotiating. Ritual for self-love.

**SECTION 7: Mars - Your Drive & Passion (Sacred Insight + Grounding)**
Mars in {mars_sign} (500+ words). Action style. Sexuality. Passion. What she wants. What she's been afraid to pursue. Ritual to reclaim her power.

**SECTION 8: Jupiter - Your Expansion (Cosmic Context)**
Jupiter in {jupiter_sign} (400+ words). Luck. Expansion. Abundance. Where she's meant to grow. Opportunities. Ritual for expansion.

**SECTION 9: Saturn - Your Mastery (Sacred Insight)**
Saturn in {saturn_sign} (500+ words). Lessons. Boundaries. What takes discipline. Where she's being called to mature. The gift beneath the challenge. Ritual for mastery.

**SECTION 10: Nodes of Destiny (Cosmic Context + Sacred Insight)**
North Node in {north_node_sign} (600+ words). Soul's growth direction. Past patterns to release. Future to step into. Her soul's purpose THIS lifetime. Ritual for alignment.

**SECTION 11: Chiron - Your Healing Gift (Sacred Insight + Grounding)**
Chiron in {chiron_sign} (500+ words). Wounded healer archetype. Her deepest wound. Her greatest gift. How to turn pain into purpose. Ritual for healing.

**SECTION 12: Career & Calling (Sacred Insight + Grounding)**
MC in {mc_sign} (500+ words). Career direction. Public image. Vocation. What she's meant to do. What's calling her. Ritual for alignment.

**SECTION 13: Your Blocks & Shadows (Sacred Insight)**
Specific patterns, fears, blocks based on her chart. Call them out. Be direct. Be compassionate. Ritual for shadow work.

**SECTION 14: Your Superpowers (Empowered Closing)**
What she's naturally gifted at. Where she's unstoppable. Her magic. Honor it.

**CLOSING (Empowered Closing)**
Circle back to her essence. Remind her of her cosmic blueprint. Leave her with a poetic vision of her potential. Make her feel READY to step into her power.

CRITICAL: Use the 5-step framework in EVERY section. Include journal prompts, affirmations, and rituals throughout. Be specific to her placements. Speak directly to HER. Honor her power. Tell the truth with compassion. Make her feel like this report was written just for her—because it was."""
    
    elif report_type == "Career Code":
        user_prompt = f"""Write an EXTREMELY detailed, transformative 15-20 page Career Code report for {name}.

PLANETARY DATA:
- Sun in {sun_sign}
- Mercury in {mercury_sign}
- Saturn in {saturn_sign}
- Jupiter in {jupiter_sign}
- MC in {mc_sign}
- North Node in {north_node_sign}

STRUCTURE (5000-6000 words minimum):

**OPENING (Personal Energy Anchor)**
Use {name}'s name. Acknowledge her career journey. What she's been carrying. Create safety.

**SECTION 1: Your Career Archetype (Sacred Insight)**
Define her professional archetype. What she's meant to do. Her calling. Be specific. 500+ words.

**SECTION 2: Natural Talents & Gifts (Cosmic Context + Sacred Insight)**
Sun, Mercury, Jupiter influence (600+ words). What she's naturally good at. Her superpowers. What she's been dimming. Ritual to activate her gifts.

**SECTION 3: Your Mastery Path (Sacred Insight + Grounding)**
Saturn in {saturn_sign} (500+ words). What takes discipline. Where she's being called to master. The challenge that's also her gift. Ritual for mastery.

**SECTION 4: Communication & Collaboration (Sacred Insight)**
Mercury in {mercury_sign} (400+ words). How she communicates at work. Her style. Strengths. What she's been afraid to say. Ritual for authentic expression.

**SECTION 5: Expansion & Abundance (Cosmic Context + Grounding)**
Jupiter in {jupiter_sign} (400+ words). Where abundance is calling. Opportunities. Growth. What's meant to expand. Ritual for abundance.

**SECTION 6: Challenges & Growth Areas (Sacred Insight)**
Real obstacles based on her chart. Blocks. What's been stopping her. Be direct. Ritual to move through them.

**SECTION 7: Ideal Work Environment (Sacred Insight + Grounding)**
What energizes her. What drains her. Culture fit. Values. Ritual to call in aligned work.

**SECTION 8: 5-Year Vision (Empowered Closing)**
Concrete career goals. Where she's meant to be. What she's building. Make it feel real and possible.

**SECTION 9: Side Hustles & Passions (Sacred Insight)**
Alternative income streams. What lights her up. How to monetize her gifts. Ritual for activation.

**SECTION 10: Activation Practices (Grounding)**
3-5 specific rituals/practices to step into her career code. Make them actionable. Include timing.

**CLOSING (Empowered Closing)**
Circle back to her purpose. Remind her of her gifts. Leave her with a vision of her career aligned with her soul. Make her feel READY.

CRITICAL: Use the 5-step framework in EVERY section. Be specific to her placements. Speak directly to HER. Include affirmations and rituals throughout. Honor her power. Tell the truth with compassion."""
    
    else:
        user_prompt = f"""Write an EXTREMELY detailed, transformative 15-20 page {report_type} report for {name}.

PLANETARY DATA:
- Sun in {sun_sign}
- Moon in {moon_sign}
- Rising in {rising_sign}
- Mercury in {mercury_sign}
- Venus in {venus_sign}
- Mars in {mars_sign}
- Jupiter in {jupiter_sign}
- Saturn in {saturn_sign}
- North Node in {north_node_sign}
- Chiron in {chiron_sign}
- MC in {mc_sign}

STRUCTURE (5000-7000 words minimum):

**OPENING (Personal Energy Anchor)**
Use {name}'s name. Mirror her essence. Acknowledge her journey. Create safety. Make her feel SEEN.

**SECTION 1-10: Detailed Sections**
Create 10+ detailed sections specific to {report_type}. Each section should:
- Use the 5-step framework
- Be specific to her placements (not generic)
- Include journal prompts, affirmations, or rituals
- Speak directly to HER
- Honor her power
- Tell the truth with compassion

**CLOSING (Empowered Closing)**
Circle back to her essence. Leave her with a poetic vision. Make her feel READY to step into her power.

CRITICAL RULES:
- Use the 5-step framework in EVERY section
- Be SPECIFIC to her placements, not generic
- Include actionable rituals, affirmations, or practices
- Speak in 2nd person ("You are," "You're being called to")
- Mix mystical + practical
- Honor her power
- Tell the truth with compassion
- Make her feel like this was written just for her"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": AIDEN_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=8000,
            temperature=0.95
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
