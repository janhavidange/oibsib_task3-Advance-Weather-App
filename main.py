import tkinter as tk
from tkinter import messagebox
import requests
from PIL import ImageTk, Image
from datetime import datetime

# Initialize main window
base = tk.Tk()
base.title("Weather App")
base.geometry("850x600")
base.configure(bg="#1E1E1E")  # Dark theme

# Load and display weather icon
img = Image.open("weather.png")
img = img.resize((120, 120))
img = ImageTk.PhotoImage(img)
weather_logo = tk.Label(base, image=img, bg="#1E1E1E")
weather_logo.pack(pady=10)

# Title Label
title_label = tk.Label(base, text="Weather App", font=("Arial", 24, "bold"), fg="#00BFFF", bg="#1E1E1E")
title_label.pack()

# Date Display
current_date = tk.Label(base, text=datetime.now().strftime('%d-%m-%Y %H:%M:%S'), font=("Arial", 14), fg="white", bg="#1E1E1E")
current_date.pack()

# Entry and Search Button Frame
frame = tk.Frame(base, bg="#1E1E1E")
frame.pack(pady=10)

tk.Label(frame, text="Enter City Name:", font=("Arial", 14), fg="white", bg="#1E1E1E").grid(row=0, column=0, padx=10)

city_name = tk.StringVar()
search_city = tk.Entry(frame, textvariable=city_name, font=("Arial", 14), width=20, bg="#333333", fg="white", insertbackground="white")
search_city.grid(row=0, column=1, padx=5)
search_city.focus()

def search_weather():
    api_key = "44fc83b37a87abfc655f50915cc91733"
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    city = city_name.get().strip()
    if not city:
        messagebox.showwarning("Warning", "Please enter a city name!")
        return

    complete_url = f"{base_url}appid={api_key}&q={city}&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    
    if data.get("cod") != 200:
        messagebox.showerror("Error", "City not found! Try again.")
        return
    
    weather_data = {
        "Temperature": f"{data['main']['temp']}°C",
        "Humidity": f"{data['main']['humidity']}%",
        "Pressure": f"{data['main']['pressure']} hPa",
        "Weather": data['weather'][0]['description'].capitalize(),
        "Country": data['sys']['country']
    }
    
    for key, value in weather_data.items():
        weather_labels[key].config(text=value)
    
search_button = tk.Button(frame, text="Search", font=("Arial", 14), bg="#00BFFF", fg="white", command=search_weather)
search_button.grid(row=0, column=2, padx=5)

# Bind Enter key to search function
search_city.bind("<Return>", lambda event: search_weather())

# Weather Data Frame
weather_frame = tk.Frame(base, bg="#1E1E1E")
weather_frame.pack(pady=20)

labels = ["Temperature", "Humidity", "Pressure", "Weather", "Country"]
weather_labels = {}

for i, label in enumerate(labels):
    tk.Label(weather_frame, text=label + " :", font=("Arial", 16), fg="#00BFFF", bg="#1E1E1E").grid(row=i, column=0, sticky="w", padx=20, pady=5)
    weather_labels[label] = tk.Label(weather_frame, text="--", font=("Arial", 16), fg="white", bg="#1E1E1E")
    weather_labels[label].grid(row=i, column=1, padx=10, pady=5)

# Footer Instructions
footer = tk.Label(base, text="Temperature in Celsius | Pressure in hPa | Humidity in %", font=("Arial", 10), fg="gray", bg="#1E1E1E")
footer.pack(pady=10)

# Menu Bar
menu_bar = tk.Menu(base)
base.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Exit", command=base.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

def show_credits():
    messagebox.showinfo("Credits","Developed By Janhavi Dange")

help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=show_credits)
menu_bar.add_cascade(label="Help", menu=help_menu)

base.mainloop()
