import swisseph as swe
from datetime import datetime
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
import pytz
import logging

logger = logging.getLogger(__name__)

# Set ephemeris path (Render will use default)
import os
ephe_path = os.path.join(os.path.dirname(__file__), 'ephe')
swe.set_ephe_path(ephe_path)

def get_coordinates_and_timezone(location_string):
    """Convert location string to coordinates and timezone"""
    try:
        geolocator = Nominatim(user_agent="soul_api", timeout=10)
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
