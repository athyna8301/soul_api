from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

app = FastAPI()

class BirthData(BaseModel):
    name: str
    birth_date: str  # Format: YYYY-MM-DD
    birth_time: str  # Format: HH:MM
    birth_place: str  # City, State, Country

@app.post("/generate-report")
def generate_report(data: BirthData):
    try:
        geolocator = Nominatim(user_agent="astro_api")
        location = geolocator.geocode(data.birth_place)
        if not location:
            raise HTTPException(status_code=400, detail="Invalid birth place")

        lat = location.latitude
        lon = location.longitude

        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lng=lon, lat=lat)
        if not timezone_str:
            raise HTTPException(status_code=400, detail="Time zone not found")

        timezone = pytz.timezone(timezone_str)
        naive_dt = datetime.strptime(f"{data.birth_date} {data.birth_time}", "%Y-%m-%d %H:%M")
        localized_dt = timezone.localize(naive_dt)
        utc_dt = localized_dt.astimezone(pytz.utc)
        utc_str = utc_dt.strftime("%Y/%m/%d %H:%M:%S")

        date = Datetime(utc_str, 'UTC')
        pos = GeoPos(str(lat), str(lon))
        chart = Chart(date, pos)

        report = {
            "name": data.name,
            "sun": str(chart.get("SUN")),
            "moon": str(chart.get("MOON")),
            "ascendant": str(chart.get("ASC")),
            "mercury": str(chart.get("MER")),
            "venus": str(chart.get("VEN")),
            "mars": str(chart.get("MAR"))
        }

        return report

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
