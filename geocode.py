#Import Geocoder 
import geocoder
import folium

#Assign IP address to a variable
ip = geocoder.ip("me")

# #Obtain the city
# print(ip.city)

# #Obtain the coordinates: 
# print(ip.latlng)

#Extract the coordinates from the 'ip' variable, which was previously obtained
location = ip.latlng
print(type(location))
print(location)

#Create a new Folium map centered around the extracted location coordinates
map = folium.Map(location=location, zoom_start=10)

#Add a red circle marker to the map at the specified 'location' 
folium.CircleMarker(location=location, radius=50, color="red").add_to(map)

#Add a standard marker (pin) to the map at the same 'location' coordinates
folium.Marker(location).add_to(map)

#Render the map
map.save("map.html")