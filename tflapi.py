import requests
import json
import os
from BusPathfindingApp import MainMenu
import matplotlib.pyplot as plt
import networkx as nx
from mpl_toolkits.basemap import Basemap

# TFL API key
app_key = "4eb9d7e0620f4d4999cd66cc87d03f4a" # primary key


# dictionary of bus routes with their bus stops
busRoutesInbound = {"SL7": [],
                    "407": [],
                    "410": [],
                    "127": [],
                    "154": [],
                    "157": [],
                    "50": [],
                    "109": [],
                    "289": [],
                    "S4": [],
                    }

busRoutesOutbound = {"SL7": [],
                    "407": [],
                    "410": [],
                    "127": [],
                    "154": [],
                    "157": [],
                    "50": [],
                    "109": [],
                    "289": [],
                    "S4": [],
                    }

stopRangeInbound = {"SL7" : [9, 11], # start = Sutton Police Station, end = Croydon Road / Wallington Green
                    "407" : [20, 48], # start = Purley High Street / Purley Station, end = Wallington County Grammar School
                    "410" : [1, 4], # start = Wallington Town Centre, end = Croydon Road / Wallington Green 
                    "127" : [1, 34], # start = Tooting / the Mitre, end = Wallington Town Centre
                    "154" : [0, 29], # start = Morden Station, end = Stafford Road / Woodcote Road
                    "157" : [0, 21], # start = Morden Station, end = Wallington Town Centre
                    "50" : [27, 44], # start = Norbury Station, end = St Mary's Church / West Croydon
                    "109" : [21, 35], # start = Norbury Station, end = West Croydon Station
                    "289" : [1, 11], # start = Purley High Street / Purley Station, end = Waddon Station
                    "S4" : [3, 19], # start = Sutton Police Station, end = Wallington Town Centre
                    }

stopRangeOutbound = {"SL7": [0, 2], # start = West Croydon Bus Station, end = Croydon Road / Wallington Green
                    "407": [3, 9], # start = Sutton Police Station, end = Croydon Road / Wallington Green
                    "410": [30, 43], # start = West Croydon Bus Station, end = Wallington County Grammar School
                    "127": [1, 14], # start = Purley High Street / Purley Station, end = Wallington Town Centre
                    "154": [0, 18], # start = West Croydon Bus Station, end = Stafford Road / Woodcote Road
                    "157": [26, 43], # start = West Croydon Bus Station, end = Wallington Town Centre
                    "50": [None, None], # N/A for outbound
                    "109": [None, None], # N/A for outbound
                    "289": [None, None], # N/A for outbound
                    "S4": [None, None], # N/A for outbound
                    }


# creates the graph of the bus stops
class buses():

    def __init__(self, busRoutesInbound, busRoutesOutbound, stopRangeInbound, stopRangeOutbound):
        self.busRoutesInbound = busRoutesInbound
        self.busRoutesOutbound = busRoutesOutbound
        self.stopRangeInbound = stopRangeInbound
        self.stopRangeOutbound = stopRangeOutbound

    # gets the bus stops of the bus routes as json file
    def getStops(self, app_key):
        # iteration to get inbound and outbound bus stops of each bus route in busStops
        for id in busRoutesInbound:
            if os.path.isfile(f"{id}_inbound_stops.json") and os.path.isfile(f"{id}_outbound_stops.json"):
                continue

            urlInbound = f"https://api.tfl.gov.uk/Line/{id}/Route/Sequence/inbound" # API inbound URL
            urlOutbound = f"https://api.tfl.gov.uk/Line/{id}/Route/Sequence/outbound" # API outbound URL
            responseInbound = requests.get(urlInbound, params={"app_key": app_key}) # API request
            responseOutbound = requests.get(urlOutbound, params={"app_key": app_key}) # API request

            # checks if inbound API request is successful for inbound bus routes
            if responseInbound.status_code == 200:
                dataInbound = responseInbound.json() # converts API response to JSON
                
                # iteration to create json file for bus stops of each bus route
                with open(f"{id}_inbound_stops.json", "w") as file:
                    json.dump(dataInbound, file)
            else:
                print(f"API request failed for route {id}: {responseInbound.status_code}")

            # checks if outbound API request is successful for outbound bus routes
            if responseOutbound.status_code == 200:
                dataOutbound = responseOutbound.json()

                # iteration to create json file for bus stops of each bus route
                with open(f"{id}_outbound_stops.json", "w") as file:
                    json.dump(dataOutbound, file)
            else:
                print(f"API request failed for route {id}: {responseOutbound.status_code}")

    # gets stop points of inbound bus routes and appends it to busRoutesInbound dictionary
    def importInboundStops(self):
        busRoutesInboundIndex = {} # creates empty dictionary to append bus stops index to
        for id in self.busRoutesInbound: # iterates through routes in busRoutesInbound
            with open(f"{id}_inbound_stops.json", "r") as file:
                dataInbound = json.load(file) # loads each inbound route JSON file
                stopPoints = dataInbound["stopPointSequences"][0]["stopPoint"] # finds specific path of JSON file
                startIndex, endIndex = self.stopRangeInbound[id] # gets index range of bus route
                inboundIndex = list(range(startIndex, endIndex + 1)) # gets bus stop index of each bus route
                inboundCoords = [(stopPoints[index]["lat"], stopPoints[index]["lon"]) for index in inboundIndex]
                self.busRoutesInbound[id] = inboundCoords # appends bus stops to busRoutesInbound dictionary
                busRoutesInboundIndex[id] = inboundIndex # appends bus stops index to busRoutesInboundIndex dictionary
        return busRoutesInbound

    # gets stop points of outbound bus routes and appends it to busRoutesOutbound dictionary
    def importOutboundStops(self):
        busRoutesOutboundIndex = {} # creates empty dictionary to append bus stops index to
        for id in self.busRoutesOutbound: # iterates through routes in busRoutesOutbound
            with open(f"{id}_outbound_stops.json", "r") as file:
                dataOutbound = json.load(file) # loads each outbound route JSON file
                stopPoints = dataOutbound["stopPointSequences"][0]["stopPoint"] # finds specific path of JSON file
                startIndex, endIndex = self.stopRangeOutbound[id] # gets index range of bus route
                if startIndex == None: # checks if index range is None
                    continue
                outboundIndex = list(range(startIndex, endIndex + 1)) # gets bus stop index of each bus route
                outboundCoords = [(stopPoints[index]["lat"], stopPoints[index]["lon"]) for index in outboundIndex]
                self.busRoutesOutbound[id] = outboundCoords # appends bus stops to busRoutesOutbound dictionary
                busRoutesOutboundIndex[id] = outboundIndex # appends bus stops index to busRoutesOutboundIndex dictionary
        return busRoutesOutbound
            

    # gets the edges of the inbound bus routes
    def getEdgesInbound(self, app_key):
        for id in self.busRoutesInbound:

            # method not run if files already exist
            if os.path.isfile(f"{id}_inbound_edges.json"):
                continue
            
            with open(f"{id}_inbound_stops.json", "r") as file: # opens inbound bus route json file
                dataInbound = json.load(file)
                a = dataInbound["stopPointSequences"][0]["stopPoint"][0]["id"] # accesses first id
                b = dataInbound["stopPointSequences"][0]["stopPoint"][-1]["id"] # accesses last id

                urlInbound = f"https://api.tfl.gov.uk/Line/{id}/Timetable/{a}/to/{b}"
                responseInbound = requests.get(urlInbound, params={"app_key": app_key}) # API request

                 # checks if inbound API request is successful
                if responseInbound.status_code == 200:

                    dataInbound = responseInbound.json() # converts API response to JSON
                    # iteration to create json file for bus stops of each bus route
                    with open(f"{id}_inbound_edges.json", "w") as file:
                        json.dump(dataInbound, file) 

                else:
                    print(f"API request failed for route {id}: {responseInbound.status_code}") # prints error message

    # gets the edges of the outbound bus routes
    def getEdgesOutbound(self, app_key):
        for id in self.busRoutesOutbound:

            # method not run if files already exist
            if os.path.isfile(f"{id}_outbound_edges.json"):
                continue
                
            with open(f"{id}_outbound_stops.json", "r") as file: # opens outbound bus route json file
                dataOutbound = json.load(file)
                a = dataOutbound["stopPointSequences"][0]["stopPoint"][0]["id"] # accesses first id
                b = dataOutbound["stopPointSequences"][0]["stopPoint"][-1]["id"] # accesses last id
        
                urlOutbound = f"https://api.tfl.gov.uk/Line/{id}/Timetable/{a}/to/{b}"
                responseOutbound = requests.get(urlOutbound, params={"app_key": app_key})

                if responseOutbound.status_code == 200:

                    dataOutbound = responseOutbound.json()
                    with open(f"{id}_outbound_edges.json", "w") as file:
                        json.dump(dataOutbound, file)

                else:
                    print(f"API request failed for route {id}: {responseOutbound.status_code}") # prints error message



class graph():

    def __init__(self, busRoutesInbound, busRoutesOutbound):
        self.busRoutesInbound = busRoutesInbound
        self.busRoutesOutbound = busRoutesOutbound
        self.network = nx.MultiDiGraph() # creates empty multi directional graph

    def defineEastboundNodes(self, startingLocation):
        if startingLocation in ["Sutton", "Mitcham", "Morden", "Tooting"]: # list of starting locations for eastbound
            routeIdsInbound = ["SL7", "410", "127", "154", "157", "S4"] # eastbound bus routes
            routeIdsOutbound = ["407"] # westbound bus routes

            for routeId in routeIdsInbound: # loops over inbound eastbound bus routes
                coords = self.busRoutesInbound[routeId]
                for i, coord in enumerate(coords): # loops over list with index counter
                    nodeName = f"{routeId}_{i}" # creates node name
                    self.network.add_node(nodeName, pos=coord)
                    for j in range(i):
                        previousNode = f"{routeId}_{j}"
                        self.network.add_edge(previousNode, nodeName)

            for routeId in routeIdsOutbound: # loops over outbound eastbound bus routes
                coords = self.busRoutesOutbound[routeId]
                for i, coord in enumerate(coords): # loops over list with index counter
                    nodeName = f"{routeId}_{i}" # creates node name
                    self.network.add_node(nodeName, pos=coord)
                    for j in range(i):
                        previousNode = f"{routeId}_{j}"
                        self.network.add_edge(previousNode, nodeName)
        else:
            pass

    def defineWestboundNodes(self, startingLocation):
        if startingLocation in ["West Croydon", "Purley", "Norbury"]: # list of starting locations for westbound
            routeIdsInbound = ["407", "50", "109", "289", "410"] # westbound bus routes
            routeIdsOutbound = ["SL7", "410", "127", "154", "157"] # eastbound bus routes

            for routeId in routeIdsInbound: # loops over inbound westbound bus routes
                coords = self.busRoutesInbound[routeId]
                for i, coord in enumerate(coords): # loops over list with index counter
                    nodeName = f"{routeId}_{i}" # creates node name
                    self.network.add_node(nodeName, pos=coord)
                    for j in range(i):
                        previousNode = f"{routeId}_{j}"
                        self.network.add_edge(previousNode, nodeName)

            for routeId in routeIdsOutbound: # loops over outbound westbound bus routes
                coords = self.busRoutesOutbound[routeId]
                for i, coord in enumerate(coords): # loops over list with index counter
                    nodeName = f"{routeId}_{i}" # creates node name
                    self.network.add_node(f"{routeId}_{i}", pos=coord)
                    for j in range(i):
                        previousNode = f"{routeId}_{j}"
                        self.network.add_edge(previousNode, nodeName)

        else:
            pass  
         
        print(routeIdsInbound)
        print(routeIdsOutbound)


    def defineEastboundEdges(self, startingLocation):
        if startingLocation in ["Sutton", "Mitcham", "Morden", "Tooting"]:
            routeIdsInbound = ["410", "127", "154", "157", "S4"] # eastbound bus routes 
            sl7Inbound = ["SL7"]
            routeIdsOutbound = ["407"] # westbound bus routes

            for id in routeIdsInbound: # loops over inbound eastbound bus routes



                # accesses time to arrival path in each json file
                with open(f"{id}_inbound_edges.json", "r") as file:
                    dataInbound = json.load(file)
                    routes = dataInbound["timetable"]["routes"][0]
                    stationIntervals = routes["stationIntervals"]
                    
                    # loops over each bus stop in the bus route
                    print(len(stationIntervals))
                    for i, intervals in enumerate(stationIntervals) :
                        timeToArrival = intervals.get("timeToArrival")
                        stopId = i + 2 
                        currentNode = f"{id}_{stopId}" 
                        previousNode = f"{id}_{stopId - 1}" 

                        # adds node to graph if it is not the starting node
                        if i > 0:
                            print(previousNode, currentNode, timeToArrival)
                            self.network.add_edge(previousNode, currentNode, time = timeToArrival)
        


startingLocation = "Sutton" # temp startingLocation variable

stops = buses(busRoutesInbound, busRoutesOutbound, stopRangeInbound, stopRangeOutbound)
stops.getStops(app_key)
busRoutesInbound = stops.importInboundStops() # updates busRoutesInbound dictionary
busRoutesOutbound = stops.importOutboundStops() # updates busRoutesOutbound dictionary

# creates graph of bus stops
mainGraph = graph(busRoutesInbound, busRoutesOutbound)

# creates east or westbound graph depending on starting location
if startingLocation in ["Sutton", "Mitcham", "Morden", "Tooting"]:
    mainGraph.defineEastboundNodes(startingLocation)
    # mainGraph.defineEastboundEdges(startingLocation)
else:
    mainGraph.defineWestboundNodes(startingLocation)

pos = nx.get_node_attributes(mainGraph.network, "pos") # gets node attributes of graph

# max and min of basemap view
lats, lons = zip(*pos.values())
latMargin = (max(lats) - min(lats)) * 0.2
lonMargin = (max(lons) - min(lons)) * 0.9

# creates instance of basemap to show map
basemap = Basemap(epsg=4326, 
                  llcrnrlat = min(lats) - latMargin, urcrnrlat = max(lats) + latMargin, 
                  llcrnrlon = min(lons) - lonMargin, urcrnrlon = max(lons) + lonMargin, 
                  resolution="c")
basemap.drawcoastlines()
basemap.drawcountries()
basemap.fillcontinents(color = "darkgray", zorder=0)

basemap.arcgisimage(service="World_Street_Map", xpixels = 1000, verbose= True) # adds street map to basemap

# gets node attributes of graph
x, y = basemap(*zip(*[(lon, lat) for lat, lon in pos.values()])) # gets x and y coordinates of bus stops

# plots graph
basemap.scatter(x, y, marker = "o", color = "r", zorder = 10)

plt.show() # displays graph
print(mainGraph.network.edges(data = True))