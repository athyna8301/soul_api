from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# --- CORS: Let your cosmic portal speak to the world ---
# (Wide open for dev magic—lock it down to your domain when you're ready to launch)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Dev mode = open skies; production = sacred boundaries
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BirthData(BaseModel):
    full_name: str
    birthdate: str  # Format: YYYY-MM-DD (the universe speaks in dates)

# ----------------- Numerology Alchemy -----------------
def _reduce(n: int) -> int:
    """Reduce numbers to their sacred essence—except master numbers 11, 22, 33."""
    while n > 9 and n not in (11, 22, 33):
        n = sum(int(digit) for digit in str(n))
    return n

def calculate_life_path(birthdate: str) -> int:
    """Your soul's blueprint—the path you chose before you arrived."""
    total = sum(int(digit) for digit in birthdate.replace("-", ""))
    return _reduce(total)

def calculate_expression(name: str) -> int:
    """How you show up in the world—your cosmic signature."""
    name = name.upper().replace(" ", "")
    total = sum((ord(char) - 64) for char in name if char.isalpha())
    return _reduce(total)

def calculate_soul_urge(name: str) -> int:
    """What your soul craves when no one's watching—your deepest desires."""
    vowels = "AEIOU"
    name = name.upper()
    total = sum((ord(char) - 64) for char in name if char in vowels)
    return _reduce(total)

def calculate_personality(name: str) -> int:
    """The mask you wear, the energy others feel before you speak."""
    vowels = "AEIOU"
    name = name.upper()
    total = sum((ord(char) - 64) for char in name if char.isalpha() and char not in vowels)
    return _reduce(total)

# ----------------- Sacred Report Generator -----------------
def generate_numerology_text(data: BirthData):
    """Weave the numbers into soul medicine."""
    name = data.full_name
    birthdate = data.birthdate
    life_path = calculate_life_path(birthdate)
    expression = calculate_expression(name)
    soul_urge = calculate_soul_urge(name)
    personality = calculate_personality(name)

    # Life Path Archetypes—each number carries medicine
    life_path_meanings = {
        1: ("The Sacred Pioneer",
            "You came here to lead, to carve paths through unknown landscapes. Your journey is radical independence guided by an inner compass that never lies."),
        2: ("The Peacemaker Priestess",
            "You incarnated to model harmony and emotional intelligence. Gentleness is spiritual mastery, not weakness. Your presence heals."),
        3: ("The Sacred Storyteller",
            "You give language to emotion and color to truth. When you silence your voice, your soul aches. Create fearlessly and share boldly."),
        4: ("The Temple Builder",
            "You create foundations that last lifetimes. Build structures that serve spirit—not cage it. Stability is your superpower."),
        5: ("The Freedom Dancer",
            "Change is your teacher, adventure your classroom. Learn freedom with focus—be both the wind and the wings."),
        6: ("The Hearth Keeper",
            "You carry the archetype of nurturer and sacred guardian. Balance devotion to others with devotion to self. You cannot pour from an empty chalice."),
        7: ("The Mystic Scholar",
            "You seek truth beneath the surface, wisdom in the silence. Solitude nourishes you—but don't forget to share your revelations with the world."),
        8: ("The Power Alchemist",
            "Mastery of material and energetic power is your birthright. Let integrity be your signature; abundance follows aligned purpose."),
        9: ("The Sacred Humanitarian",
            "Ancient, tender soul. You heal through compassion and creative service. Release the past to move freely into your purpose."),
    }

    expression_meanings = {
        1: "You express as a pioneer—direct, bold, and self-assured.",
        2: "You communicate with empathy, grace, and emotional depth.",
        3: "You radiate charisma and creative fire—people feel your spark.",
        4: "You bring ideas into form with reliability, order, and grounded wisdom.",
        5: "You inspire adventure with versatile, dynamic, magnetic energy.",
        6: "You lead with heart; devotion and service are your native languages.",
        7: "You speak with depth and intention; your silence also speaks volumes.",
        8: "You project strategy, authority, and purposeful power.",
        9: "You're a voice of compassion, emotional wisdom, and universal love.",
    }

    soul_urge_meanings = {
        1: "Craves autonomy, leadership, and the freedom to lead authentically.",
        2: "Longs for connection, sacred partnership, and emotional intimacy.",
        3: "Yearns to create, express, and be unfiltered in your truth.",
        4: "Desires safety, consistency, and integrity-built foundations.",
        5: "Thirsts for change and experience; freedom as a frequency, not a destination.",
        6: "Fulfilled by service—when giving and receiving are balanced.",
        7: "Seeks contemplation, spiritual understanding, and sacred solitude.",
        8: "Longs for sovereignty—material, emotional, and spiritual mastery.",
        9: "Fulfilled by compassion, healing, and service to humanity's evolution.",
    }

    personality_meanings = {
        1: "Seen as confident, initiating, and a natural leader.",
        2: "Perceived as gentle, emotionally aware, and deeply intuitive.",
        3: "Warm, expressive, inviting—you light up the room.",
        4: "Grounded, reliable, stabilizing—the anchor in the storm.",
        5: "Energetic, exciting, a catalyst for change and adventure.",
        6: "Nurturing, wise, approachable—the safe space people crave.",
        7: "Insightful, private, quietly powerful—mystery incarnate.",
        8: "Magnetic, purposeful, commanding—you own your presence.",
        9: "Compassionate, deep, old-soul presence—people feel seen by you.",
    }

    lp_title, lp_body = life_path_meanings.get(life_path, ("Your Sacred Path", "Your lessons are unfolding in divine timing."))

    report = f"""
🌙 **Sacred Numerology Report for {name}**
Date of Birth: {birthdate}
Prepared with cosmic reverence by: *Athyna Luna | SacredSpace: Through The Cosmic Lens*

---

### ✨ Introduction
Dear {name},

You've walked through lifetimes of conditioning—stories that asked you to dim your light, shrink your magic, apologize for your power. This season, your soul whispers: *no more hiding.* 

What follows is not prophecy—it's **remembrance**. These numbers aren't random; they're the frequency your soul chose before you arrived. Trust what resonates. Release what doesn't. You know your truth better than anyone.

---

### 🔢 Life Path {life_path}: {lp_title}
{lp_body}

---

### 🔠 Expression Number {expression}
{expression_meanings.get(expression, "Your expression is unfolding in divine timing.")}

---

### 💓 Soul Urge Number {soul_urge}
{soul_urge_meanings.get(soul_urge, "Your soul's deepest longing is awakening.")}

---

### 🌀 Personality Number {personality}
{personality_meanings.get(personality, "Your outer presence is evolving.")}

---

### 🌑 Shadow Work Invitations
These aren't questions to answer once—they're portals to return to again and again:

1. Where am I mistaking control for safety?
2. Which emotions am I ready to **express** instead of suppress?
3. What belief about my voice, my power, or my worthiness is ready to be released?

---

### 🌕 Ritual Practice (Waxing Moon Energy)
Write your full name on a slip of paper. Hold it to your heart. Speak aloud:  
*"I reclaim my power, my voice, my divine authority. I am both human and holy."*

Burn the paper safely (cauldron, fireproof dish, or candle flame). Let the smoke rise like your new beginning. Watch it transform. So are you.

---

### 🌟 Closing Affirmation
*"I trust my cosmic blueprint. I lead with courage, create with love, and remember that I am both human and divine. My presence is my power. My voice is my magic."*

Trust your cosmic blueprint, {name}. You were made for this. The universe doesn't make mistakes—and neither did you when you chose this path.

🌙 **You are the magic you've been searching for.**  
— *Athyna Luna | SacredSpace: Through The Cosmic Lens*
"""
    return report.strip()

# ----------------- API Routes -----------------
from fastapi.responses import HTMLResponse

@app.post("/numerology/", response_class=HTMLResponse)
def numerology_report(data: BirthData):
    report = generate_numerology_text(data)
    styled_html = f"""
    <div style='background:#f9f7ff;padding:40px;border-radius:18px;
                font-family:Georgia,serif;color:#2d2056;line-height:1.8;'>
        <h2 style='text-align:center;color:#7b4fff;'>🌙 Your Sacred Numerology Report 🌙</h2>
        <div style='white-space:pre-wrap;background:white;padding:24px;
                    border-radius:12px;margin-top:16px;
                    font-family:"Courier New",monospace;
                    box-shadow:0 2px 6px rgba(0,0,0,0.1);'>
            {report}
        </div>
        <p style='margin-top:24px;'>With love,<br><strong>Athyna Luna</strong><br>
        <em>SacredSpace: Through The Cosmic Lens ✨</em></p>
    </div>
    """
    return styled_html


@app.post("/numerology/")
def numerology_report(data: BirthData):
    """Generate a sacred numerology report—soul medicine in digital form."""
    return {"report": generate_numerology_text(data)}