import requests
import streamlit as st
import base64

st.set_page_config(page_title="Weather App", page_icon="🌤️", layout="centered")

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

bg_image = get_base64_image('photo-1496450681664-3df85efbd29f.jpg')
bg_image_card = get_base64_image('photo-1558486012-817176f84c6d (1).jpg')

def get_weather_icon(condition):
    weather_icons = {
        "Clear": "☀️",
        "Clouds": "☁️",
        "Rain": "🌧️",
        "Drizzle": "🌦️",
        "Thunderstorm": "⛈️",
        "Snow": "❄️",
        "Mist": "🌫️",
    }
    return weather_icons.get(condition, "🌍")

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{bg_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    .weather-card {{
        text-align: center;
        background: url("data:image/jpeg;base64,{bg_image_card}") no-repeat center center;
        background-size: cover;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 2px 4px 10px rgba(0, 0, 0, 0.1);
        max-width: 400px;
        margin: auto;
        position: relative;
        color: white;
        font-weight: bold;
    }}
    .weather-icon {{
        font-size: 75px;  
        display: block;
        text-align: center;
    }}
    .temp {{
        font-size: 5.0em;
        font-weight: bold;
        color: #333;
    }}
    .details {{
        font-size: 1.2em;
        color: #000000;
        text-align: left;
    }}
    .footer {{
        margin-top: 50px;
        font-size: 0.9em;
        color: #777;
        text-align: center;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h1 style='text-align: center;'>🌦️ Weather App</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    city = st.text_input("", placeholder="Enter city name (e.g., Mumbai, Tokyo)", label_visibility="collapsed")
with col2:
    search = st.button("Get Weather")

def fetch_weather(city):
    api_key = "94d77cd3cf9a83a5abaf62b6e640aabf"
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        weather_data = response.json()

        return {
            "city": weather_data["name"],
            "country": weather_data["sys"]["country"],
            "temp": weather_data["main"]["temp"],
            "feels_like": weather_data["main"]["feels_like"],
            "temp_min": weather_data["main"]["temp_min"],
            "temp_max": weather_data["main"]["temp_max"],
            "humidity": weather_data["main"]["humidity"],
            "pressure": weather_data["main"]["pressure"],
            "wind_speed": weather_data["wind"]["speed"],
            "weather": weather_data["weather"][0]["main"],
            "icon": weather_data["weather"][0]["icon"]
        }
    except requests.exceptions.RequestException:
        return {"error": "Failed to retrieve weather data"}
    except KeyError:
        return {"error": "City not found"}

if search:
    if city.strip() == "":
        st.error("Please enter a city name.")
    else:
        weather = fetch_weather(city)

        if "error" in weather:
            st.error(weather["error"])
        else:
            custom_weather_icon = get_weather_icon(weather["weather"])
            weather_icon_url = f"http://openweathermap.org/img/wn/{weather['icon']}@2x.png"

            st.markdown(
                f"""
                <div class="weather-card">
                    <h2>{weather['city']}, {weather['country']}</h2>
                    <p style="font-size: 100px; text-align: center;">{custom_weather_icon}</p>  <!-- BIGGER ICON -->
                    <div style="font-size: 3.5em; font-weight: bold; color: #222; text-align: center;">{weather['temp']}°C</div> 
                    <p>{weather['weather']}</p>
                    <hr>
                    <div class="details">
                        <p><strong>Feels Like:</strong> {weather['feels_like']}°C</p>
                        <p><strong>Min:</strong> {weather['temp_min']}°C | <strong>Max:</strong> {weather['temp_max']}°C</p>
                        <p><strong>Humidity:</strong> {weather['humidity']}%</p>
                        <p><strong>Pressure:</strong> {weather['pressure']} hPa</p>
                        <p><strong>Wind Speed:</strong> {weather['wind_speed']} m/s</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.markdown(
    '<div style="margin-top: 50px; font-size: 0.9em; text-align: center; color: black;">'
    'Made with ❤️ using Streamlit'
    '</div>',
    unsafe_allow_html=True
)
