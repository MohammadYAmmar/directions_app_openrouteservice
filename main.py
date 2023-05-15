import openrouteservice
import folium
import tkinter as tk
from tkinter import messagebox
import webbrowser

# Define your API key
api_key = '5b3ce3597851110001cf62480d7ec5c3c8ff4a5989edbd6e61cfd2f0'

# Create a client object
client = openrouteservice.Client(key=api_key)

# Define the GUI window
window = tk.Tk()
window.title("OpenRouteService Directions")
window.geometry("600x600")

# Define the start and end location labels and entry fields
start_label = tk.Label(window, text="Start Location (lat, lon):")
start_label.pack()
start_entry = tk.Entry(window, width=50)
start_entry.pack()

end_label = tk.Label(window, text="End Location (lat, lon):")
end_label.pack()
end_entry = tk.Entry(window, width=50)
end_entry.pack()

# Define the layer view options
layer_options = {
    "OpenStreetMap": folium.TileLayer("OpenStreetMap"),
    "Stamen Terrain": folium.TileLayer("Stamen Terrain"),
    "Stamen Toner": folium.TileLayer("Stamen Toner"),
    "Stamen Watercolor": folium.TileLayer("Stamen Watercolor"),
    "CartoDB Positron": folium.TileLayer("CartoDB Positron"),
    "CartoDB Dark_Matter": folium.TileLayer("CartoDB Dark_Matter")
}

# Define the function to get the directions and display the map
def get_directions():
    # Get the start and end locations from the entry fields
    start = start_entry.get().split(",")
    end = end_entry.get().split(",")

    # Check if the input is valid
    if len(start) != 2 or len(end) != 2:
        messagebox.showerror("Error", "Invalid input. Please enter the coordinates in the format 'lat, lon'.")
        return

    try:
        start = [float(start[1]), float(start[0])]
        end = [float(end[1]), float(end[0])]
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter the coordinates in the format 'lat, lon'.")
        return

    # Get the directions
    try:
        directions = client.directions(coordinates=[start, end], profile='driving-car', format='geojson')
    except openrouteservice.exceptions.ApiError:
        messagebox.showerror("Error", "Unable to get directions. Please check your API key and input.")
        return

    # Create a map object
    m = folium.Map(zoom_start=13)

    # Add the route to the map
    folium.GeoJson(directions).add_to(m)

    # Fit the map to the bounds of the route
    bounds = folium.GeoJson(directions).get_bounds()
    m.fit_bounds(bounds)

    # Add the layer view options to the map
    layer_control = folium.LayerControl()
    for name, layer in layer_options.items():
        layer_control.add_child(layer)
        layer_control.add_child(folium.Element(name))

    # Add the layer control to the map
    m.add_child(layer_control)

    # Save the map to an HTML file
    map_file = "map.html"
    m.save(map_file)

    # Open the map in a web browser
    webbrowser.open(map_file)

# Define the "Get Directions" button
button = tk.Button(window, text="Get Directions", command=get_directions)
button.pack()

# Run the GUI window
window.mainloop()