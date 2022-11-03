# import interfaces here
import time
import sys
import requests
from luma.core.render import canvas
from PIL import ImageFont
import geocoder

from hexi.interfaces.display import display, icons


class WeatherDisplay(display.Display):
    def show(self, icon, temp):
        text_font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 20)
        temp_symbol = "°C"

        with canvas(self.virtual) as draw:
            w, h = draw.textsize(text=icon, font=self.font)
            x = ((self.width - w) / 2) - 30
            y = (self.height - h) / 2

            draw.text((x, y), text=icon, font=self.font, fill="white")

            draw.text((75, 25), text=temp+temp_symbol, fill="white", font=text_font)


def get_weather(url):
    ret = requests.get(url)
    data = ret.json()

    weather_code = data['daily']['weathercode'][0]
    print(f"{weather_code=}")
    temp_max = data['daily']['temperature_2m_max'][0]
    temp_min = data['daily']['temperature_2m_min'][0]
    avg_temp = int((temp_min + temp_max) / 2)

    return weather_code, avg_temp


def get_weather_icon(code_to_icon, code):
    code = int(code)
    for codes, icon in code_to_icon.items():
        if code in codes:
            return icon
    return None



# entry point of skill
def start(command=None):
    geo_data = geocoder.ip('me')
    lat, lon = geo_data.latlng
    #lon="-3.0174"
    #lat="51.8209"
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=weathercode,temperature_2m_max,temperature_2m_min&timezone=Europe%2FLondon"

    weather_code_map = {
            (0,): icons.Sun,
            (1, 2, 3): icons.CloudSun,
            (45, 48): icons.CloudSmog,
            (51, 53, 55, 56, 57, 80, 81, 82): icons.CloudSunRain,
            (61, 63, 65, 66, 67): icons.CloudRain,
            (77, 85, 86): icons.Snowflake,
            (95, 96, 99): icons.CloudBolt
            }
    weather_code, temperature = get_weather(url)

    screen = WeatherDisplay(font="fontawesome2.ttf")

    weather_icon = get_weather_icon(weather_code_map, weather_code)
    if weather_icon:
        screen.show(weather_icon, str(temperature))
        time.sleep(6)


if __name__ == "__main__":
    command = sys.argv[1:]
    if len(command) == 0: command = None
    start(command)
