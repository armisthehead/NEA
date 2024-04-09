# imports kivy library and classes from modules
import kivy
from kivy.core.window import Window
from kivy.utils import platform
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.app import Widget 
from kivy.uix.label import Label 
from kivy.lang import Builder 
from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
from kivy_garden.mapview import MapView, MapMarker
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty 
from kivy.properties import StringProperty
import os, shutil
from kivymd.app import MDApp
import runpy

# list of starting locations as a List Property so it can be used in Kivy files
startingList = ("Sutton", "West Croydon", "Mitcham", "Morden", "Norbury", "Purley", "Tooting")

# dictionary of markers for the map
startingCoords = {
    "School": [51.368851620000235, -0.14820670713778916], # WCGS
    "Sutton": [51.361759014416776, -0.1907937142595224], # Sutton Police Station
    "West Croydon": [51.378922499392225, -0.10153662178916567], # West Croydon Bus Station (Stop B3)
    "Mitcham": [51.40570367549265, -0.16392979278891082], # Mitcham Fair Green (Stop G)
    "Morden": [51.402562320103065, -0.19400769935807244], # Morden Station (Stop C)
    "Norbury": [51.41285125039685, -0.12403806292985538], # Norbury Station (Stop A)
    "Purley": [51.337361922009116, -0.11644325716155643], # Purley High Street / Purley Station (Stop P)
    "Tooting": [51.427162944730775, -0.16662604910727977] # Mitcham Road / Tooting Broadway Station (Stop C)
}

# max resolution for Android and IOS but for development 540, 960
def windowSize():
    if platform == "android" or platform == "ios":
        Window.maximize()
    else:
        Window.size = (540, 960)

# different screens can inherit this class to improve modularity
class ScreenChanger():

    # changes screen to the screenName from kivy files
    def changeScreen(self, screenName):
        self.manager.current = screenName

# placeholder for starting map in popup
class startingMap(Widget):
    pass

# attibutes and methods for map in mainmenu
class StartingMap(MapView):
    mapWidget = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(StartingMap, self).__init__(**kwargs)
        self.lat = 51.368851620000235
        self.lon = -0.14820670713778916
        self.zoom = 12

        # iteration to add starting locations to map
        for location, coords in startingCoords.items():
            marker = MapMarker(lat=coords[0], lon=coords[1])
            self.add_widget(marker)

        # creates instance of startingMap class in mapWidget
        if self.mapWidget is not None:
            self.mapWidget.add_widget(StartingMap())


# placeholder in this file, defined in mainmenu.kv
class MainMenu(Screen, FloatLayout, MDApp, ScreenChanger):
    startingList = ListProperty(startingList) # local variable to be used as values for drop down
    infoText = StringProperty("Start by choosing a location from the dropdown menu. When you're happy, press Continue. You will have the option to avoid 'traffic', 'road incidents ', and 'bus disruptions'. After the program has given you directions, you will have the option to download the route for offline use. Don't worry, you can always go back and change your starting location or preferences, or see information about the app. Click outside this popup to close it. Sutton: Sutton Police Station, West Croydon: West Croydon Bus Station Stop B3, Mitcham: Mitcham Fair Green Stop G, Morden: Morden Station Stop C, Norbury: Norbury Station Stop A, Purley: Purley High Street / Purley Station Stop P, Tooting: Mitcham Road / Tooting Broadway Station Stop C")
    startingLocation = None

    # stores the selected location to startingLocation
    def dropDownMenuSelected(self, text):
        self.startingLocation = text
        print ("test:", self.startingLocation)
        self.ids.mainMenuContinue.disabled = False # enables mainMenucontinue button
        return self.startingLocation

    # shows the info popup when infoBtn is pressed
    def showInfo(self):
        infoLabel = Label(text=self.infoText) # creates label with infoText as text
        infoLabel.text_size = (Window.width * 0.6, None) # text size 60% of window width
        infoLabel.halign = "left" # alighns text to left
        infoLabel.valign = "top" # alighns text to top
        # creates popup with infoLabel as content and sets it in middle of window
        infoPopup = Popup(title = "Guide", 
                          content = infoLabel, 
                          size_hint = (.7, .7), 
                          pos_hint = {"center_x": .5, "center_y": .5})
        infoPopup.open()


    def journeyPlanner(self):

        from datetime import datetime, timedelta
        import json
        import requests
        import os

        # TFL API key
        app_key = "4eb9d7e0620f4d4999cd66cc87d03f4a" # primary key

        print(self.startingLocation)

        #startingLocationCoords = startingCoords[startingLocation]
        #schoolCoords = startingCoords["School"]

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
            time = "0830"

        if self.startingLocation == "Sutton":
            journeyPlannerURL = f"https://api.tfl.gov.uk/Journey/JourneyResults/51.361759014416776,%20-0.1907937142595224/to/51.368851620000235,%20-0.14820670713778916?nationalSearch=false&date={urlDate}&time=0830&timeIs=Arriving&journeyPreference=LeastTime&mode=bus&accessibilityPreference=NoRequirements&fromName=Sutton&toName=School&walkingSpeed=Average&cyclePreference=None&bikeProficiency=Easy"
        elif self.startingLocation == "West Croydon":
            journeyPlannerURL = f"https://api.tfl.gov.uk/Journey/JourneyResults/51.378922499392225,%20-0.10153662178916567/to/51.368851620000235,%20-0.14820670713778916?nationalSearch=false&date={urlDate}&time=0830&timeIs=Arriving&journeyPreference=LeastTime&mode=bus&accessibilityPreference=NoRequirements&fromName=Croydon&toName=School&walkingSpeed=Average&cyclePreference=None&bikeProficiency=Easy"
        elif self.startingLocation == "Mitcham":
            journeyPlannerURL = f"https://api.tfl.gov.uk/Journey/JourneyResults/51.40570367549265,%20-0.16392979278891082/to/51.368851620000235,%20-0.14820670713778916?nationalSearch=false&date={urlDate}&time=0830&timeIs=Arriving&journeyPreference=LeastTime&mode=bus&accessibilityPreference=NoRequirements&fromName=Mitcham&toName=School&walkingSpeed=Average&cyclePreference=None&bikeProficiency=Easy"
        elif self.startingLocation == "Morden":
            journeyPlannerURL = f"https://api.tfl.gov.uk/Journey/JourneyResults/51.402562320103065,%20-0.19400769935807244/to/51.368851620000235,%20-0.14820670713778916?nationalSearch=false&date={urlDate}&time=0830&timeIs=Arriving&journeyPreference=LeastTime&mode=bus&accessibilityPreference=NoRequirements&fromName=Morden&toName=School&walkingSpeed=Average&cyclePreference=None&bikeProficiency=Easy"
        elif self.startingLocation == "Norbury":
            journeyPlannerURL = f"https://api.tfl.gov.uk/Journey/JourneyResults/51.41285125039685,%20-0.12403806292985538/to/51.368851620000235,%20-0.14820670713778916?nationalSearch=false&date={urlDate}&time=0830&timeIs=Arriving&journeyPreference=LeastTime&mode=bus&accessibilityPreference=NoRequirements&fromName=Norbury&toName=School&walkingSpeed=Average&cyclePreference=None&bikeProficiency=Easy"
        elif self.startingLocation == "Purley":
            journeyPlannerURL = f"https://api.tfl.gov.uk/Journey/JourneyResults/51.337361922009116,%20-0.11644325716155643/to/51.368851620000235,%20-0.14820670713778916?nationalSearch=false&date={urlDate}&time=0830&timeIs=Arriving&journeyPreference=LeastTime&mode=bus&accessibilityPreference=NoRequirements&fromName=Purley&toName=School&walkingSpeed=Average&cyclePreference=None&bikeProficiency=Easy"
        elif self.startingLocation == "Tooting":
            journeyPlannerURL = f"https://api.tfl.gov.uk/Journey/JourneyResults/51.427162944730775,%20-0.16662604910727977/to/51.368851620000235,%20-0.14820670713778916?nationalSearch=false&date={urlDate}&time=0830&timeIs=Arriving&journeyPreference=LeastTime&mode=bus&accessibilityPreference=NoRequirements&fromName=Tooting&toName=School&walkingSpeed=Average&cyclePreference=None&bikeProficiency=Easy"
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
        
        return urlTime, urlDate, response.status_code

# placeholder in this file, defined in optionscreen.kv
class OptionScreen(Screen, ScreenChanger, MDApp):
    
    # indicates that the back button has been pressed
    def optionsBackPressed(self):
        self.ids.backButtonImage.source = "backbuttonpressed.png"

    def optionsBackUnpressed(self):
        self.ids.backButtonImage.source = "backbuttonunpressed.png"

    def RouteFinder():
        runpy.run_path("pathfinder.py")

    # stores values on switches
    def switchValues(self):
        roadBlock = (self.ids.roadBlockSwitch.active)
        busyRoads = (self.ids.busyRoadsSwitch.active)
        busDelays = (self.ids.busDelaySwitch.active)

        # checks if any of the switches are active
        print ("avoid road blocks: " + str(roadBlock) + "\n"
               "avoid busy roads: " + str(busyRoads) + "\n"
               "avoid bus delays: " + str(busDelays))

class RouteScreen(Screen, ScreenChanger, App):

    def __init__(self, **kwargs):
        super(RouteScreen, self).__init__(**kwargs)
    
        # iteration to get instructions from JSON file
 #       for leg in data["journeys"][0]["legs"][0]:
  #          departureTime = leg[0]["departureTime"]
   #         instruction = leg["instruction"]["summary"]
    #        instructionLabel = Label(text = instruction)
     #       if "bus" in instruction:
      #          busStop = leg["instruction"]["busStops"][0]["name"] 
       #         busStopLabel = Label(text = busStop) 
        #        RouteScreenLayout.add_widget(busStopLabel) 
         #   else: 
          #      pass
           # RouteScreenLayout.add_widget(instructionLabel) 
        
    # special Kivy method that is called when the screen is entered
    def on_enter(self):
        self.manager.get_screen("mainMenu").journeyPlanner()
        urlTime = self.manager.get_screen("mainMenu").journeyPlanner()[0] # gets time from journeyPlanner method
        urlDate = self.manager.get_screen("mainMenu").journeyPlanner()[1] # gets date from journeyPlanner method
        response = self.manager.get_screen("mainMenu").journeyPlanner()[2] # gets response from journeyPlanner method

        # imports for RouteScreen
        from kivy.uix.boxlayout import BoxLayout
        import json
        from kivy.utils import get_color_from_hex

        # creates layout for RouteScreen
        RouteScreenLayout = BoxLayout(orientation="vertical")

        titleLabel = Label(text = "Route Instructions", font_size = 30, color = get_color_from_hex("#12428c"))
        RouteScreenLayout.add_widget(titleLabel)

        if response == 200:

            if urlTime > "0830":
                lateLabel = Label(text = "This journey will be for the next day as you will be late today.")
                RouteScreenLayout.add_widget(lateLabel)

            with open("journeyPlanner.json", "r") as file:
                journeyPlanner = json.load(file)

            # gets duration of journey from JSON file
            duration = str(journeyPlanner["journeys"][0]["duration"])
            durationLabel = Label(text = f"The duration of your journey is {duration} minutes")
            RouteScreenLayout.add_widget(durationLabel)

            # iteration to get instructions from JSON file
            for leg in journeyPlanner["journeys"][0]["legs"]:
                departureTime = leg["departureTime"] # gets departure time for each leg
                HHMM = departureTime[11:16] # gets hours:minutes from departure time
                arrivalPoint = leg["arrivalPoint"]["commonName"] # gets arrival point for each leg
                #instructionLabel = Label(text = f"Go to {arrivalPoint} at {HHMM}")

                # checks if the instruction is to take a bus
                if leg["mode"]["id"] == "walking":
                    if leg["arrivalPoint"]["commonName"] == "School, Carshalton":
                        actionLabel = Label(text = f"{HHMM}: Walk to School")
                    else:
                        actionLabel = Label(text = f"{HHMM}: Walk to {arrivalPoint}")
                    RouteScreenLayout.add_widget(actionLabel)
                else:
                    busName = leg["routeOptions"][0]["name"]
                    startBusStop = leg["departurePoint"]["commonName"]
                    endBusStop = leg["arrivalPoint"]["commonName"]
                    busDirection = leg["routeOptions"][0]["directions"]
                    realbusDirection = busDirection[0]
                    actionLabel = Label(text = f"{HHMM}: Take the {busName} at {startBusStop}\n towards {realbusDirection}. Get off at {endBusStop}")
                    RouteScreenLayout.add_widget(actionLabel)

            self.add_widget(RouteScreenLayout)

        # if the error is not OK (200) then an error message is outputted
        else:
            errorLabel = Label(text = "There is an error with the TFL API.\nPlease refer to the TFL website for more information.")
            RouteScreenLayout.add_widget(errorLabel)
            self.add_widget(RouteScreenLayout)
        

# run loop of app
class BusPathfindingApp(MDApp):
    #startingList = startingList

    def build(self):
        windowSize()

        # loads Kivy file into main Python file so elements can be used
        gui = Builder.load_file("main.kv")

        # changes background colour to black
        self.theme_cls.theme_style = "Dark"

        self.root = gui

        # creates instance of RouteScreen class
        routeScreen = RouteScreen(name = "routeScreen")
        
        # define the variable sm as screen manager
        sm = self.root.ids.screenManager
        
        # add the widget to sm
        sm.add_widget(routeScreen)

        # returns main.kv file
        return self.root
        
    
    # clears cache of map
    def clearMapCache(self):
        folder = "cache" # cache folder name 
        # iteration to return all files in cache folder
        for fileName in os.listdir(folder):
            filePath = os.path.join(folder, fileName)
            try:
                if os.path.isfile(filePath) or os.path.islink(filePath):
                    os.unlink(filePath)
                elif os.path.isdir(filePath):
                    shutil.rmtree(filePath)
            # handles errors
            except Exception as e:
                print (e)
            
    # automatically called when app is closed
    def on_stop(self): 
        self.clearMapCache()

# runs app
if __name__ == "__main__":
    BusPathfindingApp().run()
