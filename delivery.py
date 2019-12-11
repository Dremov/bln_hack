# Import the library to make the request to the TomTom API
import requests

class Location:
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude



# mock some locations



# Make the Request (Dont foreget to change the API key)
response = requests.get("https://api.tomtom.com/routing/1/calculateRoute/37.773412,-122.430929:37.787402,-122.396555/xml?avoid=unpavedRoads&key=j48lgjJAY1GP2zPa6owAmA3hlia8AImR")
# Print out the response to make sure it went through
print(response.content)


mockAgents = requests.get("http://mockbcknd.tk/")
print (mockAgents.content)
