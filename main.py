from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# --- allow your site to call the API (adjust origins later) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev mode: open; lock down to your domain when deployed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BirthData(BaseModel):
    full_name: str
    birthdate: str  # YYYY-MM-DD

# ----------------- numerology helpers -----------------
def _reduce(n: int) -> int:
    while n > 9 and n not in (11, 22, 33):
        n = sum(int(d) for d in str(n))
    return n

def calculate_life_path(birthdate: str) -> int:
    total = sum(int(d) for d in birthdate.replace("-", ""))
    return _reduce(total)

def calculate_expression(name: str) -> int:
    name = name.upper().replace(" ", "")
    total = sum((ord(c) - 64) for c in name if c.isalpha())
    return _reduce(total)

def calculate_soul_urge(name: str) -> int:
    vowels = "AEIOU"
    name = name.upper()
    total = sum((ord(c) - 64) for c in name if c in vowels)
    return _reduce(total)

def calculate_personality(name: str) -> int:
    vowels = "AEIOU"
    name = name.upper()
    total = sum((ord(c) - 64) for c in name if c.isalpha() and c not in vowels)
    return _reduce(total)

# ----------------- report generator -----------------
def generate_numerology_text(data: BirthData):
    name = data.full_name
    birthdate = data.birthdate
    life_path = calculate_life_path(birthdate)
    expression = calculate_expression(name)
    soul_urge = calculate_soul_urge(name)
    personality = calculate_personality(name)

    life_path_meanings = {
        1: ("The Sacred Pioneer",
            "You came to lead, to carve paths through unknown landscapes. Your journey is radical independence guided by an inner compass."),
        2: ("The Peacemaker Priestess",
            "You incarnated to model harmony and emotional intelligence. Gentleness is spiritual mastery, not weakness."),
        3: ("The Sacred Storyteller",
            "You give language to emotion and color to truth. When you silence your voice, your soul aches. Create and share."),
        4: ("The Temple Builder",
            "You create foundations. Build structures that serve spirit—not cage it."),
        5: ("The Freedom Dancer",
            "Change is your teacher. Learn freedom with focus—be both the wind and the wings."),
        6: ("The Hearth Keeper",
            "You carry the archetype of nurturer. Balance devotion to others with devotion to self."),
        7: ("The Mystic Scholar",
            "You seek truth beneath the surface. Solitude nourishes you—share your wisdom with the world."),
        8: ("The Power Alchemist",
            "Mastery of material and energetic power. Let integrity be your signature; abundance follows aligned purpose."),
        9: ("The Sacred Humanitarian",
            "Ancient, tender soul. Heal through compassion and creative service; release the past to move freely."),
    }

    expression_meanings = {
        1: "You express as a pioneer—direct and self-assured.",
        2: "You communicate with empathy and grace.",
        3: "You radiate charisma and creative expression.",
        4: "You bring ideas into form with reliability and order.",
        5: "You inspire adventure with versatile, dynamic energy.",
        6: "You lead with heart; devotion is your language.",
        7: "You speak with depth; your silence also speaks.",
        8: "You project strategy, authority, and purpose.",
        9: "You’re a voice of compassion and emotional wisdom.",
    }

    soul_urge_meanings = {
        1: "Craves autonomy to lead authentically.",
        2: "Longs for connection and sacred partnership.",
        3: "Yearns to create and be unfiltered.",
        4: "Desires safety, consistency, and integrity-built foundations.",
        5: "Thirsts for change and experience; freedom as a frequency.",
        6: "Fulfilled by service—balanced giving/receiving.",
        7: "Seeks contemplation and spiritual understanding.",
        8: "Longs for sovereignty—material, emotional, spiritual.",
        9: "Fulfilled by compassion and service to humanity.",
    }

    personality_meanings = {
        1: "Seen as confident and initiating.",
        2: "Perceived as gentle and emotionally aware.",
        3: "Warm, expressive, and inviting.",
        4: "Grounded, reliable, stabilizing.",
        5: "Energetic, exciting, a catalyst.",
        6: "Nurturing, wise, approachable.",
        7: "Insightful, private, quietly powerful.",
        8: "Magnetic, purposeful, commanding.",
        9: "Compassionate, deep, old-soul presence.",
    }

    lp_title, lp_body = life_path_meanings.get(life_path, ("Your Path", "Your lessons are unfolding."))

    report = f"""
🌙 **Sacred Numerology Report for {name}**
Date of Birth: {birthdate}
Prepared by: *Athyna Luna | SacredSpace: Through The Cosmic Lens*

---

### ✨ Introduction
Dear {name},

You’ve walked through lifetimes of conditioning—stories that asked you to dim your light. This season, your soul whispers: *no more hiding.* What follows is not prophecy—it’s remembrance.

---

### 🔢 Life Path {life_path}: {lp_title}
{lp_body}

---

### 🔠 Expression Number {expression}
{expression_meanings.get(expression, "")}

---

### 💓 Soul Urge Number {soul_urge}
{soul_urge_meanings.get(soul_urge, "")}

---

### 🌀 Personality Number {personality}
{personality_meanings.get(personality, "")}

---

### 🌑 Shadow Work Invitations
1) Where am I mistaking control for safety?
2) Which emotions am I ready to express instead of suppress?
3) What belief about my voice/power is ready to be released?

---

### 🌕 Ritual Practice (Waxing Moon)
Write your name on a slip of paper. Speak aloud: *“I reclaim my power, my voice, my divine authority.”* Burn safely and let the smoke rise like your new beginning.

---

### 🌟 Closing Affirmation
*“I trust my cosmic blueprint. I lead with courage, create with love, and remember that I am both human and divine.”*

Trust your cosmic blueprint. You were made for this. 🌙  
— *Athyna Luna | SacredSpace: Through The Cosmic Lens*
"""
    return report.strip()

# ----------------- routes -----------------
@app.get("/")  # quick health check
def root():
    return {"ok": True, "msg": "Soul API is alive"}

@app.post("/numerology/")
def numerology_report(data: BirthData):
    return {"report": generate_numerology_text(data)}
