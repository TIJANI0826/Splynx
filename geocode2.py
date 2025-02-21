import requests
import geocoder
import folium
ip = geocoder.ip("me")

def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]


def get_location():
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name"),
        "latitude": response.get("latitude"),
        "longitude": response.get("longitude"),
        "postal_code": response.get("postal"),
    }
    return location_data


print(get_location()['latitude'])
print(get_location()['longitude'])
location = [get_location()['latitude'], get_location()['longitude']]
print(type(location))

#Create a new Folium map centered around the extracted location coordinates
map = folium.Map(location=location, zoom_start=10)

#Add a red circle marker to the map at the specified 'location' 
folium.CircleMarker(location=location, radius=50, color="red").add_to(map)

#Add a standard marker (pin) to the map at the same 'location' coordinates
folium.Marker(location).add_to(map)

#Render the map
map.save("map2.html")