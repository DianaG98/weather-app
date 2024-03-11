#Made By Diana Gonzalez:)

import requests
import json

#First, we import the Flask object and create the functions for the HTTPS responses

from flask import Flask, render_template, request

app = Flask(__name__)

#Function for the main page, where the user will enter the city 
@app.route("/")
def welcome_page():
    return render_template("index.html")
#Funcion where we will receive the city and search the weather for the next 5 days
@app.route("/weather", methods=['POST'])
def weather():
    city = request.form["city_name"]
    #we transform the input to lowercase, since that's how we the name appears on the API results
    result=get_weather(city.lower())
    #show the results on the HTML file
    return render_template("weather.html", html_data_0=result[0],html_data_1=result[1],html_data_2=result[2],html_data_3=result[3], html_data_4=result[4], html_data_5=result[5])

#function for getting the weather
def get_weather(city):

#parameters for the Reservamos API, the city name
    parametersReservamos = {
        "q":city
    }

#get the API results
    responseReservamos = requests.get("https://search.reservamos.mx/api/v2/places", params=parametersReservamos)
    resultsReservamos = responseReservamos.json()

    #Latitude and longitud used for testing, this can be used in case we don't want to make the request to the Reservamos API
    #lat=25.6866142
    #long=-100.3161126

#we initialize the variables 
    lat=0
    long=0
    display_name=""
#print results for debugging 
    print(resultsReservamos)
#we search on the JSON the city and if we found it we get the latitude, longitud and name 
    for item in resultsReservamos:
        if item['result_type']=="city" and item['ascii_display']==city:
            print("City Found!")
            lat=item['lat']
            long=item['long']
            display_name=item['display']
#now we set the parameters for the OpenWeather's API, in this case we used metric units, Celsius
    parameters = {
        "lat": lat,
        "lon": long,
        "units": "metric",
        "appid": "0eebd1fcf852d29ca0340c5c451d4c9a"
    }
#get the API response
    response = requests.get("https://api.openweathermap.org/data/2.5/forecast", params=parameters)

    results = response.json()
#get the JSON with dates and all the weather data
    results_list = response.json()['list']
#print resuls for debugging
    print(results_list)
#list to save the dates of the next 5 days
    dates_list=[]
#save only the date portion, not including the hour
    for i in range(results['cnt']):
        dates_list.append(results_list[i]['dt_txt'][0:10])
#create a dictionary and convert it again to list to remove the repeated dates
    dates_list = list(dict.fromkeys(dates_list))
#print results for debugging    
    print(dates_list)
#get the size of the dates list, because depending on the hour we request the response, sometimes we get data from 6 days
    length=len(dates_list)
#initialize list for saving the temperatures
    min_temps = [[] for i in range(length)]
    max_temps = [[] for i in range(length)]
    cont=0
#save the temperatures for each day
    for i in range(results['cnt']):
        if results_list[i]['dt_txt'][0:10]==dates_list[cont] :
            min_temps[cont].append(results_list[i]['main']['temp_min'])
            max_temps[cont].append(results_list[i]['main']['temp_max'])
        else:
            cont=cont+1
            min_temps[cont].append(results_list[i]['main']['temp_min'])
            max_temps[cont].append(results_list[i]['main']['temp_max'])
#print results for debugging
    print(min_temps)
    print(max_temps)
#initialize list for saving the min and max temperatures for each day
    min_temp_by_day = []
    max_temp_by_day = []
#get the max and min temps
    for i in range(length):
        min_temp_by_day.append(min(min_temps[i]))
        max_temp_by_day.append(max(max_temps[i]))
#print for debugging
    print (min_temp_by_day)
    print (max_temp_by_day)
#initilize varaibles we will use for showing the results
    html_string_list=[]
    html_string_list.append(display_name)
#concatenate strings with all the results    
    for i in range(5):
        html_string_list.append(dates_list[i]+"- Min:"+str(min_temp_by_day[i])+" Max: "+str(max_temp_by_day[i]))
#return the string with the results    
    return html_string_list

