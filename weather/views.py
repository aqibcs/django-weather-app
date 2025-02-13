import requests
from django.shortcuts import render
from django.conf import settings

def fetch_weather_data(endpoint, params):
    """Fetches weather data from OpenWeather API for a given endpoint."""
    api_key = getattr(settings, "OPENWEATHER_API_KEY", None)
    if not api_key:
        return {"error": "API key is missing. Please configure it in settings."}

    base_url = f"https://api.openweathermap.org/data/2.5/{endpoint}"
    params.update({"appid": api_key, "units": "metric"})

    try:
        response = requests.get(base_url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

def parse_weather_data(data):
    """Parses current weather data into a structured dictionary."""
    if "error" in data:
        return data
    
    return {
        "city": data.get("name", "Unknown"),
        "temperature": f"{data['main']['temp']}°C",
        "feels_like": f"{data['main']['feels_like']}°C",
        "weather": data["weather"][0]["description"].capitalize(),
        "humidity": f"{data['main']['humidity']}%",
        "pressure": f"{data['main']['pressure']} hPa",
        "wind_speed": f"{data['wind']['speed']} km/h",
        "icon": f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png",
    }

def parse_forecast_data(data):
    """Parses forecast data into a structured dictionary."""
    if "error" in data:
        return data
    
    forecast_list = {}
    for item in data.get("list", []):
        date = item["dt_txt"].split(" ")[0]
        if date not in forecast_list:
            forecast_list[date] = {
                "temperature": f"{item['main']['temp']}°C",
                "weather": item["weather"][0]["description"].capitalize(),
                "humidity": f"{item['main']['humidity']}%",
                "pressure": f"{item['main']['pressure']} hPa",
                "wind_speed": f"{item['wind']['speed']} km/h",
                "icon": f"https://openweathermap.org/img/wn/{item['weather'][0]['icon']}@2x.png",
            }
    return list(forecast_list.items())[:4]

def weather_view(request):
    """Handles the weather page view, fetching current and forecast data."""
    city = request.GET.get('city')
    lat, lon = request.GET.get('lat'), request.GET.get('lon')
    params = {"lat": lat, "lon": lon} if lat and lon else {"q": city} if city else None

    weather_data = parse_weather_data(fetch_weather_data("weather", params)) if params else None
    forecast_data = parse_forecast_data(fetch_weather_data("forecast", params)) if params else None

    return render(request, "weather_app/weather.html", {"weather": weather_data, "forecast": forecast_data})
