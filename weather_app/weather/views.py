import os
import requests
from django.shortcuts import render
from django.core.cache import cache
from django.http import HttpResponse
from .forms import CityForm


# Create your views here.
API_KEY = os.getenv("WEATHER_API_KEY")


def get_weather(request):
    print("view function called") # debugging step 1
    weather_data = None
    forecast_data = None

    if request.method == "POST":
        print("post request received") # debugging step 2
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data["city"].strip()
            

            # check if data is cached

            #if cache.get(city):
             #   weather_data = cache.get(city)
              #  print(f"cache hit for city:{city}") # debugging step 4
            
           
            url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"
            response = requests.get(url)
            print(f"APIResponse code: {response.status_code}") # debugging step 5

            forecast_url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=5&aqi=no&alerts=no"
            forecast_response = requests.get(forecast_url)

            if response.status_code == 200 and forecast_response.status_code == 200:
                data = response.json()
                forecast_data = forecast_response.json()

                print(f"API response: {data}") # debugging step 6
                weather_data = {
                    "city": city,
                    "temperature": data["current"]["temp_c"],
                    "humidity": data["current"]["humidity"],
                    "wind_speed": data["current"]["wind_kph"],
                    "description": data["current"]["condition"]["text"],
                    "icon": data["current"]["condition"]["icon"],  # Extract weather icon
                }

                
                
                forecast_days = []
                for day in forecast_data["forecast"]["forecastday"]:
                    forecast_days.append({
                        "date": day["date"],
                        "max_temp": day["day"]["maxtemp_c"],
                        "min_temp": day["day"]["mintemp_c"],
                        "condition": day["day"]["condition"]["text"],
                        "icon": day["day"]["condition"]["icon"],
                    })
                
                forecast_data = forecast_days # Pass processed data
                #cache.set(city, weather_data, timeout=60*10) #cache for 10 mins.
            else:
                print("API request failed") # debugging step 7
                weather_data = {"error":"City not found try another city or API issue"}

    
    else:
        form = CityForm()
    
    
    return render(request, "weather/weather.html", {"form": form, "weather_data": weather_data, "forecast": forecast_data})


         
