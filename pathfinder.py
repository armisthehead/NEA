from BusPathfindingApp import startingCoords, MainMenu
from datetime import datetime, timedelta
import json
import requests
import os

# TFL API key
app_key = "4eb9d7e0620f4d4999cd66cc87d03f4a" # primary key

# temp startingLocation for testing
# startingLocation = "Sutton"
instance = MainMenu()
startingLocation = instance.startingLocation
print(startingLocation)

startingLocationCoords = startingCoords[startingLocation]
schoolCoords = startingCoords["School"]

# gets system date and time
now = datetime.now()
urlDate = now.strftime("%Y%m%d")
urlTime = now.strftime("%H%M")

# checks if the time is after 8:30
if str(urlTime) > "0830":
    print("School starts at 8:30. You will be late.") # will be turned to label when integrating with Kivy

    # if the time is after 8:30, it checks for the next day
    date = datetime.strptime(urlDate, "%Y%m%d")
    date += timedelta(days=1)
    urlDate = date.strftime("%Y%m%d")
    print(urlTime)
    print(urlDate)

'''

No longer needed

nationalSearch = "false" # keeps search in London
timeIs = "Arriving" # user should arrive before 8:30
journeyPreference = "LeastTime" # user wants to get to school as fast as possible
mode = "bus,walking" # user wants to walk and take the bus
fromName = startingLocation # gets starting location from variable
toName = "School" # gets destination from variable
walkingSpeed = "average" # user walks slowly
cyclePreference = "None" # user doesn't want to cycle
bikeProficiency = "Easy" # not needed
applyHtmlMarkup = "false" # doesn't apply HTML markup
useMultiModalCall = "false" # only uses buses and walking
walkingOptimization = "false" # emphesis on public transport
taxiOnlyTrip = "false" # route doesnt make use of taxis
routeBetweenEntrances = "false" # not needed

'''

if startingLocation == "Sutton":
    journeyPlannerURL = f"https://api.tfl.gov.uk/Journey/JourneyResults/51.361759014416776,%20-0.1907937142595224/to/51.368851620000235,%20-0.14820670713778916?nationalSearch=false&date={urlDate}&time={urlTime}&timeIs=Arriving&journeyPreference=LeastTime&mode=bus&accessibilityPreference=NoRequirements&fromName=Sutton&toName=School&walkingSpeed=Average&cyclePreference=None&bikeProficiency=Easy"
elif startingLocation == "West Croydon":
    journeyPlannerURL = f"https://api.tfl.gov.uk/Journey/JourneyResults/51.378922499392225,%20-0.10153662178916567/to/51.368851620000235,%20-0.14820670713778916?nationalSearch=false&date={urlDate}&time={urlTime}&timeIs=Arriving&journeyPreference=LeastTime&mode=bus&accessibilityPreference=NoRequirements&fromName=Croydon&toName=School&walkingSpeed=Average&cyclePreference=None&bikeProficiency=Easy"
elif startingLocation == "Mitcham":
    journeyPlannerURL = f"https://api.tfl.gov.uk/Journey/JourneyResults/51.40570367549265,%20-0.16392979278891082/to/51.368851620000235,%20-0.14820670713778916?nationalSearch=false&date={urlDate}&time={urlTime}&timeIs=Arriving&journeyPreference=LeastTime&mode=bus&accessibilityPreference=NoRequirements&fromName=Mitcham&toName=School&walkingSpeed=Average&cyclePreference=None&bikeProficiency=Easy"
elif startingLocation == "Morden":
    journeyPlannerURL = f"https://api.tfl.gov.uk/Journey/JourneyResults/51.402562320103065,%20-0.19400769935807244/to/51.368851620000235,%20-0.14820670713778916?nationalSearch=false&date={urlDate}&time={urlTime}&timeIs=Arriving&journeyPreference=LeastTime&mode=bus&accessibilityPreference=NoRequirements&fromName=Morden&toName=School&walkingSpeed=Average&cyclePreference=None&bikeProficiency=Easy"
elif startingLocation == "Norbury":
    journeyPlannerURL = f"https://api.tfl.gov.uk/Journey/JourneyResults/51.41285125039685,%20-0.12403806292985538/to/51.368851620000235,%20-0.14820670713778916?nationalSearch=false&date={urlDate}&time={urlTime}&timeIs=Arriving&journeyPreference=LeastTime&mode=bus&accessibilityPreference=NoRequirements&fromName=Norbury&toName=School&walkingSpeed=Average&cyclePreference=None&bikeProficiency=Easy"
elif startingLocation == "Purley":
    journeyPlannerURL = f"https://api.tfl.gov.uk/Journey/JourneyResults/51.337361922009116,%20-0.11644325716155643/to/51.368851620000235,%20-0.14820670713778916?nationalSearch=false&date={urlDate}&time={urlTime}&timeIs=Arriving&journeyPreference=LeastTime&mode=bus&accessibilityPreference=NoRequirements&fromName=Purley&toName=School&walkingSpeed=Average&cyclePreference=None&bikeProficiency=Easy"
elif startingLocation == "Tooting":
    journeyPlannerURL = f"https://api.tfl.gov.uk/Journey/JourneyResults/51.427162944730775,%20-0.16662604910727977/to/51.368851620000235,%20-0.14820670713778916?nationalSearch=false&date={urlDate}&time={urlTime}&timeIs=Arriving&journeyPreference=LeastTime&mode=bus&accessibilityPreference=NoRequirements&fromName=Tooting&toName=School&walkingSpeed=Average&cyclePreference=None&bikeProficiency=Easy"
else:
    pass

response = requests.get(journeyPlannerURL)
data = response.json()
with open(f"journeyPlanner.json", "w") as file:
    json.dump(data, file)

# checks if the request was successful
if response.status_code == 200:
    print("Journey planner request successful")
else:
    print("Journey planner request failed")