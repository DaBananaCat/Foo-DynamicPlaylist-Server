
# Imports
import ujson as json
import os
import requests
import time
import random
import geocoder

"""
Part 1:
Files
"""

def read_json(filepath, filename=False):
    
    # File is part of the path
    if filename == False:
        with open(filepath) as file:
            data = json.load(file)
        return data
    
    # File isn't part of the path
    else:
        with open(os.path.join(filepath,filename)) as file:
            data = json.load(file)
        return data


def write_json(value, filepath, filename=False):
    
    # File is part of the path
    if filename == False:
        with open(filepath,"w") as file:
            json.dump(value,file)
        return data
    
    # File isn't part of the path
    else:
        with open(os.path.join(filepath,filename),"w") as file:
            data = json.dump(value,file)
        return data

"""
Part 2:
Number Operations
"""

def average(*nums):
    total = 0
    
    # If list is inputted
    if type(nums[0]) == list:
        for num in nums[0]:
            total += num
            average = total / len(nums[0])
    
    # If not not inputted list
    else:
        for num in nums:
            total += num
            average = total / len(nums)

    return average


def total(*nums):
    total = 0
    # If list is inputted
    if type(nums[0]) == list:
        for num in nums[0]:
            total += num
            
    # If not not inputted list
    else:
        for num in nums:
            total += num

    return total

def chance(odds):
    computer_choice = random.randint(0,100000)/1000
    if odds > computer_choice:
        return True
    
    return False

"""
Part 3:
Text-Based
"""

def ask(question,*choices):
    
    # Free responce if no choices are given
    print(choices)
    if choices == ():
        print(question)
        return input()
    
    # Multiple choice if choices are given
    else:
        while True:
            print(question)
            for choice in choices:
                print(str(choices.index(choice)+1) + ": " + choice)
            user_choice = input()
            
            # Check if input is correct
            try:
                if int(user_choice) <= len(choices) and int(user_choice) > 0:
                    return int(user_choice)
                else:
                    print("Not a valid number")
            except:
                print("Input a number")
            input("Press enter to try again")
            print("\n"*100)
        
"""
Part 4:
Requests
"""
def request(url,*paramaters):
    response = requests.get(url,params=paramaters)
    response = response.json()
    
    return response




"""
Part 5:
Ect
"""


def get_time(quantity="all"): 
    
    # Obtain time
    current_time = time.ctime(time.time()).split(" ")
    time_split = current_time[3].split(":")
    
    # Get the hours, sec, and mins seperate
    time_split_dict = {
        "hour": time_split[0],
        "minute": time_split[1],
        "second": time_split[2]
        }
    
    # Create a dict of all the data
    current_time = {
        "day_of_week": current_time[0],
        "month": current_time[1],
        "day": current_time[2],
        "time": current_time[3],
        "hour": time_split_dict["hour"],
        "minute": time_split_dict["minute"],
        "second": time_split_dict["second"],
        "year": current_time[4],
        "time_split": time_split
        }
    
    # If user wants all return the dict
    if quantity == "all":
        return current_time
    # If user wants one, return the one
    else:
        return current_time[quantity]
    
        
def get_weather(ip=True,zip_code=None, data_return="current"):
    
    if zip_code:
        # Convert input to string if it isn't
        if type(zip_code) == int:
            zip_code = str(zip_code)
        
        # Get latitude and longitude
        result = request("https://api.zippopotam.us/us/" + zip_code)
        lat = result["places"][0]["latitude"]
        long = result["places"][0]["longitude"]
    
    elif ip:
        coords = geocoder.ip('me')
        lat, long = str(coords.latlng[0]), str(coords.latlng[1]) 
    
    else:
        raise Exception("No valid location data")
    
    # Get weather grid points
    # Weather grid points are what weather.gov uses to organize forecasts, think of it
    # like a location's ID
    grid_data = request("https://api.weather.gov/points/" + lat + "," + long)
    grid_points = (grid_data["properties"]["gridX"],grid_data["properties"]["gridY"])
    
    # Get weather
    weather = request(f"https://api.weather.gov/gridpoints/{grid_data['properties']['gridId']}/{str(grid_points[0])},{str(grid_points[1])}/forecast")["properties"]
    
    if data_return == "all":
        return weather
    else:
        weather = weather["periods"][0]
        precip_chance = weather["probabilityOfPrecipitation"]["value"]
        if precip_chance == None:
            precip_chance = 0
        simp_weather = {
            "temperature": weather["temperature"],
            "wind_speed": weather["windSpeed"],
            "short_forecast": weather["shortForecast"],
            "precipitation": precip_chance
            }
        return simp_weather

"""
Testing
"""

if __name__ == "__main__":
    #var = f"https://api.weather.gov/gridpoints/{grid_data['properties']['gridId']}/{str(grid_points[0])},{str(grid_points[1])}/forecast"
    #print(var)
    
    #print(get_weather())


    print(get_time(quantity="year"))