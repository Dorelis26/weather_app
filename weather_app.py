import requests
import json
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime

def get_weather_data(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()
    return data

# Create a GUI using tkinter
def update_weather():
    city = city_entry.get()
    if city:
        try:
            data = get_weather_data(api_key, city)
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            icon_code = data['weather'][0]['icon']

            # Update labels with weather data
            description_label.config(text=weather_description)
            temperature_label.config(text=f'Temperature: {temperature}°C')

            #weather icon using Pillow
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
            icon_response = requests.get(icon_url, stream=True)
            if icon_response.status_code == 200:
                icon_image = Image.open(icon_response.raw)
                icon_image = icon_image.resize((100, 100), Image.ANTIALIAS)
                icon_photo = ImageTk.PhotoImage(icon_image)
                icon_label.config(image=icon_photo)
                icon_label.image = icon_photo

            
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            time_label.config(text=f'Current Time: {current_time}')
        except KeyError:
            messagebox.showerror("Error", "City not found.")
    else:
        messagebox.showerror("Error", "Please enter a city.")

# API key from OpenWeatherMap
api_key = "b70c680a78c4e45a81514c34299b0662"

# GUI window
app = tk.Tk()
app.title("Weather App")

# GUI Labels
city_label = tk.Label(app, text="Enter City:")
city_label.pack()

city_entry = tk.Entry(app)
city_entry.pack()

get_weather_button = tk.Button(app, text="Get Weather", command=update_weather)
get_weather_button.pack()

description_label = tk.Label(app, text="", font=("Helvetica", 12))
description_label.pack()

temperature_label = tk.Label(app, text="", font=("Helvetica", 12))
temperature_label.pack()

icon_label = tk.Label(app)
icon_label.pack()

time_label = tk.Label(app, text="", font=("Helvetica", 12))
time_label.pack()

app.mainloop()
