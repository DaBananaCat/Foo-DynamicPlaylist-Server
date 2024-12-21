# Imports
import BananaAPI as bapi
import os
import math
import random
import sys
import subprocess

# Pretty print for debug (techsmart names it pp, rename to pprint everywhere else)
import pprint as pp

# Get temperature
zip_code = ZIPCODE
weather = bapi.get_weather(zip_code)
temp = weather["temperature"]
print(temp)
# Get precipitation chance
precip = weather["precipitation"]

# Get time
user_date = bapi.get_time()
hours = int(user_date["hour"])
minutes = int(user_date["minute"])
# !!ADD CODE!!
mins = (hours*60) + minutes

# Weight Calc
def calc_weight(value):
    return abs((2/math.pi)*math.atan(value))

def read_data(data,value,type):
    filtered_data = [
    item for item in data["files"]
    if item["tags"]["custom"][type][value] == True
    ]
    return filtered_data

# Prepare weights
weights = {
    "hot": 0,
    "cold": 0,
    "rain": 0
    }

time_weights = {
    "night": 0,
    "morning": 0,
    "afternoon": 0
    }

# Temp Weighting
mtemp = (temp-60)/10

if temp > 60:
    weights["hot"] = calc_weight(mtemp)/2
else:
    weights["cold"] = calc_weight(mtemp)/1.5

# Precipitation Weighting

mprecip = (precip-20)/50
if mprecip < 0:
    mprecip = 0

weights["rain"] = calc_weight(mprecip)

# Get music data
music = bapi.read_json(os.path.join("data","data.json"))

morning_songs = read_data(music,0,"timeOfDay")
afternoon_songs = read_data(music,1,"timeOfDay")
night_songs = read_data(music,2,"timeOfDay")
rain_songs = read_data(music,"raining","weather")
hot_songs = read_data(music,"hot","temp")
cold_songs = read_data(music,"cold","temp")
music = {
    "morning": morning_songs,
    "afternoon": afternoon_songs,
    "night": night_songs,
    "rain": rain_songs,
    "hot": hot_songs,
    "cold": cold_songs
}


song_picked_yet = False

for weight in weights:
    if weights[weight] > 0:
        if random.randint(0,round(weights[weight]*100)) > random.randint(0,100):
            song_picked = random.choice(music[weight])
            print("Picked song", song_picked, "which is a",weight,"song")
            song_picked_yet = True
            break


# If the temp or weather didn't pick a song, pick a song based on time
if not song_picked_yet:
    print(mins, "minutes have passed")
    # Nightime music
    if mins > 1000:
        # 4:40 PM starts the possibility of night music
        time_weights["night"] = calc_weight((mins/10)-100)
        
    elif mins < 425:
        # 7:05 AM end the possibility of night music
        time_weights["night"] = calc_weight(((mins/10)-42.5))
    
    # Morning Music
    if mins > 360 and mins <= 600:
        # 6:00 AM starts the possibility of morning music
        time_weights["morning"] = calc_weight(((mins/10)-36))
    
    elif mins < 690 and mins >= 360:
        # 11:30 AM ends the possibility of morning music
        time_weights["morning"] = calc_weight(((mins/10)-69))
    
    # Afternoon music
    if mins >= 660 and mins <= 900:
        # 11:00 AM starts the possibility of afternoon music
        time_weights["afternoon"] = calc_weight(((mins/10)-66))
    elif mins < 1080 and mins > 660:
        # 6:00 PM ends the possibility of afternoon music
        time_weights["afternoon"] = calc_weight(((mins/10)-100.8))
    
    # Pick a song
    song_picking = True
    while song_picking:
        for weight in time_weights:
            if time_weights[weight] > 0:
                if random.randint(0,round(time_weights[weight]*100)) > random.randint(0,100):
                    song_picked = random.choice(music[weight])
                    print("Picked song", song_picked, "which is a",weight,"song")
                    song_picking = False
                    break
bapi.write_json(song_picked, "data", "next_song.json")

command = "foobar2000.exe /context_command:\"Add to playback queue\" \"" + song_picked["path"] + "\""
#command = "foobar2000.exe"
directory = "D:/Users/[USERNAME]/Documents/Foobar/"

subprocess.call(command, shell=True, cwd=directory)
