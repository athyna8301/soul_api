import swisseph as swe
from datetime import datetime
<<<<<<< HEAD
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
import pytz
=======
from zoneinfo import ZoneInfo
>>>>>>> 25c433ea8877f8fdfc8d7472a59d2ff4b4493f67
import logging

logger = logging.getLogger(__name__)

<<<<<<< HEAD
# Set ephemeris path (Render will use default)
swe.set_ephe_path('')

def get_coordinates_and_timezone(location_string):
    """Convert location string to coordinates and timezone"""
    try:
        geolocator = Nominatim(user_agent="sacredspace_astrology")
        location = geolocator.geocode(location_string)
        
        if not location:
            raise ValueError(f"Could not find location: {location_string}")
        
        lat, lon = location.latitude, location.longitude
        
        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lat=lat, lng=lon)
        
        return lat, lon, tz_name, location.address
    except Exception as e:
        logger.error(f"Geocoding error: {str(e)}")
        raise

def calculate_julian_day(date_str, time_str, tz_name):
    """Convert date/time to Julian Day (UT)"""
    try:
        dt_str = f"{date_str} {time_str}"
        local_tz = pytz.timezone(tz_name)
        local_dt = local_tz.localize(datetime.strptime(dt_str, "%Y-%m-%d %H:%M"))
        utc_dt = local_dt.astimezone(pytz.UTC)
        
        jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day,
                       utc_dt.hour + utc_dt.minute/60.0 + utc_dt.second/3600.0)
        return jd
    except Exception as e:
        logger.error(f"Julian day calculation error: {str(e)}")
        raise

def zodiac_sign(longitude):
    """Convert ecliptic longitude to zodiac sign and degree"""
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    sign_num = int(longitude / 30)
    degree = longitude % 30
    return signs[sign_num], degree

def calculate_houses(jd, lat, lon):
    """Calculate house cusps using Placidus system"""
    try:
        cusps, ascmc = swe.houses(jd, lat, lon, b'P')
        return {
            "cusps": cusps,
            "ascendant": ascmc[0],
            "mc": ascmc[1],
            "armc": ascmc[2],
            "vertex": ascmc[3]
        }
    except Exception as e:
        logger.error(f"House calculation error: {str(e)}")
        raise

def calculate_chart(birthdate, birthtime, birthplace):
    """Calculate complete birth chart"""
    try:
        lat, lon, tz_name, full_address = get_coordinates_and_timezone(birthplace)
        jd = calculate_julian_day(birthdate, birthtime, tz_name)
        houses = calculate_houses(jd, lat, lon)
        
        planets = {}
        planet_ids = {
            'Sun': swe.SUN,
            'Moon': swe.MOON,
            'Mercury': swe.MERCURY,
            'Venus': swe.VENUS,
            'Mars': swe.MARS,
            'Jupiter': swe.JUPITER,
            'Saturn': swe.SATURN,
            'Uranus': swe.URANUS,
            'Neptune': swe.NEPTUNE,
            'Pluto': swe.PLUTO,
            'North Node': swe.TRUE_NODE,
            'Chiron': swe.CHIRON
        }
        
        for name, planet_id in planet_ids.items():
            result = swe.calc_ut(jd, planet_id)
            longitude = result[0][0]
            sign, degree = zodiac_sign(longitude)
            
            planets[name] = {
                'longitude': longitude,
                'sign': sign,
                'degree': degree,
                'retrograde': result[0][3] < 0
            }
        
        return {
            'birthdate': birthdate,
            'birthtime': birthtime,
            'birthplace': birthplace,
            'full_address': full_address,
            'latitude': lat,
            'longitude': lon,
            'timezone': tz_name,
            'julian_day': jd,
            'planets': planets,
            'houses': houses
        }
    except Exception as e:
        logger.error(f"Chart calculation error: {str(e)}")
        raise
=======
# Initialize ephemeris
swe.set_ephe_path('/tmp/swisseph')

ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

PLANETS = {
    0: "Sun", 1: "Moon", 2: "Mercury", 3: "Venus", 4: "Mars",
    5: "Jupiter", 6: "Saturn", 7: "Uranus", 8: "Neptune", 9: "Pluto"
}

HOUSES = {
    1: "1st House (Self)", 2: "2nd House (Values)", 3: "3rd House (Communication)",
    4: "4th House (Home)", 5: "5th House (Creativity)", 6: "6th House (Work)",
    7: "7th House (Relationships)", 8: "8th House (Transformation)", 
    9: "9th House (Philosophy)", 10: "10th House (Career)", 
    11: "11th House (Community)", 12: "12th House (Spirituality)"
}

def get_sign(longitude):
    """Convert longitude to zodiac sign"""
    sign_index = int(longitude / 30)
    return ZODIAC_SIGNS[sign_index % 12]

def get_sign_degree(longitude):
    """Get degree within sign (0-30)"""
    return longitude % 30

def calculate_chart(name, birthdate, birthtime, birthplace, lat, lon, tz):
    """
    Calculate complete birth chart
    Returns dict with all planetary positions, houses, aspects
    """
    try:
        # Parse datetime
        date_parts = birthdate.split('-')
        time_parts = birthtime.split(':')
        
        year = int(date_parts[0])
        month = int(date_parts[1])
        day = int(date_parts[2])
        hour = int(time_parts[0])
        minute = int(time_parts[1])
        
        # Create timezone-aware datetime
        tz_obj = ZoneInfo(tz)
        dt = datetime(year, month, day, hour, minute, tzinfo=tz_obj)
        
        # Convert to UTC
        dt_utc = dt.astimezone(ZoneInfo("UTC"))
        
        # Calculate Julian Day Number
        jd = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, 
                        dt_utc.hour + dt_utc.minute/60)
        
        # Calculate planetary positions
        planets_data = {}
        for planet_id in range(10):
            pos, speed = swe.calc_ut(jd, planet_id)
            planets_data[planet_id] = {
                "name": PLANETS[planet_id],
                "longitude": pos[0],
                "sign": get_sign(pos[0]),
                "degree": get_sign_degree(pos[0]),
                "latitude": pos[1],
                "speed": speed[0]
            }
        
        # Calculate houses (Placidus system)
        cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P')  # P = Placidus
        
        houses_data = {}
        for i in range(1, 13):
            house_cusp = cusps[i-1]
            houses_data[i] = {
                "cusp": house_cusp,
                "sign": get_sign(house_cusp),
                "degree": get_sign_degree(house_cusp)
            }
        
        # Ascendant and Midheaven
        ascendant = ascmc[0]
        midheaven = ascmc[1]
        
        # Calculate Lunar Nodes
        nodes, _ = swe.calc_ut(jd, 10)  # Node = 10
        north_node = nodes[0]
        south_node = (north_node + 180) % 360
        
        # Calculate Chiron
        chiron, _ = swe.calc_ut(jd, 15)  # Chiron = 15
        
        chart = {
            "name": name,
            "birthdate": birthdate,
            "birthtime": birthtime,
            "birthplace": birthplace,
            "latitude": lat,
            "longitude": lon,
            "timezone": tz,
            "jd": jd,
            "planets": planets_data,
            "houses": houses_data,
            "ascendant": {
                "longitude": ascendant,
                "sign": get_sign(ascendant),
                "degree": get_sign_degree(ascendant)
            },
            "midheaven": {
                "longitude": midheaven,
                "sign": get_sign(midheaven),
                "degree": get_sign_degree(midheaven)
            },
            "north_node": {
                "longitude": north_node,
                "sign": get_sign(north_node),
                "degree": get_sign_degree(north_node)
            },
            "south_node": {
                "longitude": south_node,
                "sign": get_sign(south_node),
                "degree": get_sign_degree(south_node)
            },
            "chiron": {
                "longitude": chiron[0],
                "sign": get_sign(chiron[0]),
                "degree": get_sign_degree(chiron[0])
            }
        }
        
        logger.info(f"✅ Chart calculated for {name}")
        return chart
        
    except Exception as e:
        logger.error(f"Error calculating chart: {str(e)}")
        raise

def get_aspects(chart):
    """Calculate major aspects between planets"""
    aspects = []
    aspect_orbs = {
        0: 8,      # Conjunction
        60: 6,     # Sextile
        90: 8,     # Square
        120: 8,    # Trine
        180: 8     # Opposition
    }
    
    planets_list = list(chart["planets"].values())
    
    for i, planet1 in enumerate(planets_list):
        for planet2 in planets_list[i+1:]:
            lon1 = planet1["longitude"]
            lon2 = planet2["longitude"]
            
            diff = abs(lon1 - lon2)
            if diff > 180:
                diff = 360 - diff
            
            for aspect_angle, orb in aspect_orbs.items():
                if abs(diff - aspect_angle) <= orb:
                    aspect_name = {0: "Conjunction", 60: "Sextile", 90: "Square", 
                                  120: "Trine", 180: "Opposition"}[aspect_angle]
                    aspects.append({
                        "planet1": planet1["name"],
                        "planet2": planet2["name"],
                        "aspect": aspect_name,
                        "orb": abs(diff - aspect_angle)
                    })
    
    return aspects
>>>>>>> 25c433ea8877f8fdfc8d7472a59d2ff4b4493f67
