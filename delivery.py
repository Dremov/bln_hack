# Import the library to make the request to the TomTom API
import requests
import json

MOCK_AGENT_URL = "http://mockbcknd.tk/"
TOM_TOM_API_KEY = "j48lgjJAY1GP2zPa6owAmA3hlia8AImR"
REQUEST_HEADER = "https://api.tomtom.com/routing/1/calculateRoute/"


class Location:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def get_locations_as_string(self):
        return str(self.latitude) + "," + str(self.longitude)

    def to_string(self):
        print("latitude = ", self.latitude, "longitude = ", self.longitude)


class Agent:
    def __init__(self, location, vehicleType, status):
        self.location = location
        self.vehicleType = vehicleType
        self.status = status

    def to_string(self):
        print("Location: ", end="")
        self.location.to_string()
        print("type: ", self.vehicleType, "status: ", self.status)


def vehicle_name_to_backend_name(name):
    if name == "pedestrian":
        return "pedestrian"
    if name == "EV":
        return "car&vehicleEngineType=electric"
    if name == "bicycle":
        return "bicycle"
    if name == "e-bike":
        return "bicycle&vehicleEngineType=electric"
    if name == "auto":
        return "car"


#### test code
# Make the Request (Dont foreget to change the API key)
# response = requests.get("https://api.tomtom.com/routing/1/calculateRoute/37.773412,-122.430929:37.787402,-122.396555/xml?avoid=unpavedRoads&key=j48lgjJAY1GP2zPa6owAmA3hlia8AImR")
# Print out the response to make sure it went through
# print(response.content)

def calculate_best_routes(start, finish, listOfAgents):
    startLocString = start.get_locations_as_string()
    finishLocString = finish.get_locations_as_string()

    jsonResponces = []
    for freeAgent in listOfAgents:
        requestStr = REQUEST_HEADER
        requestStr += freeAgent.location.get_locations_as_string() + ":"
        requestStr += startLocString + ":"
        requestStr += finishLocString
        requestStr += "/json?maxAlternatives=1&traffic=true&avoid=unpavedRoads&travelMode="
        requestStr += freeAgent.vehicleType
        requestStr += "&key="
        requestStr += TOM_TOM_API_KEY
        # print ("Request: ", requestStr)
        response = requests.get(requestStr)
        jsonResponces.append(response.content)
        # print (response.content)

    # return list with best routes in JSON. 
    return jsonResponces


def parse_agents(data):
    agents = []
    json_agents = data["features"]
    # print (json_agents)
    for dictAgent in json_agents:
        # print (dictAgent)
        agentProperties = dictAgent["properties"]
        # print (agentProperties)
        vehicleId = vehicle_name_to_backend_name(agentProperties["vehicleType"])
        status = agentProperties["status"]
        agentCoords = dictAgent["geometry"]["coordinates"]
        newAgent = Agent(Location(agentCoords[1], agentCoords[0]), vehicleId, status)
        agents.append(newAgent)

    return agents


def get_free_agents(agents):
    freeAgents = []

    for agent in agents:
        if agent.status == "Free":
            freeAgents.append(agent)

    return freeAgents


# 1. Read agents and parse to list
mockAgents = requests.get(MOCK_AGENT_URL)
data = json.loads(mockAgents.content)
agentsList = parse_agents(data)
# pick only free agents
freeAgents = get_free_agents(agentsList)
print("We have ", len(freeAgents), " free agents")
for agent in freeAgents:
    agent.to_string()

if len(freeAgents) == 0:
    print("Unfortunatelly no free courier")
    exit()

# 2. fake start point and finish point
startLocation = Location(52.522156, 13.411048)  # fake Alexander Platz
finishLocation = Location(52.506321, 13.277549)  # fake Brandenburg Tor


# 3. calculate best routes
def get_best_routes():
    best_routes = calculate_best_routes(startLocation, finishLocation, freeAgents)
    return best_routes


# TODO  provide best rotes to frontend
mockAgents = requests.get("http://mockbcknd.tk/")
# print(mockAgents.content)
print(get_best_routes())
