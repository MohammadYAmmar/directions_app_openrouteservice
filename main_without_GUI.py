# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import openrouteservice
import folium

# Define your API key
api_key = 'your_api_key_here'

# Create a client object
client = openrouteservice.Client(key=api_key)

# Define the start and end locations
start = [8.34234, 48.23424]
end = [8.53456, 48.34567]

# Get the directions
directions = client.directions(coordinates=[start, end], profile='driving-car', format='geojson')

# Print the directions
print(directions)

# Create a map object
m = folium.Map(location=start, zoom_start=13)

# Add the route to the map
folium.GeoJson(directions).add_to(m)

# Display the map
m
