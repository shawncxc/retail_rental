import os
import json
import folium
from redis_client import redis_client

def get_color(rate):
    if rate < 20:
        return "#66cd00"
    elif rate < 40:
        return "#ffd700"
    elif rate < 60:
        return "#ff8c00"
    else:
        return "#ff3030"

map_sf = folium.Map(location=[37.7676457, -122.4184106], zoom_start=13)

redis_db = redis_client()
redis_db.connect()
for key in redis_db.conn.scan_iter():
    temp = redis_db.get(key)
    lat = temp["geo"]["lat"]
    lng = temp["geo"]["lng"]
    rate = temp["rate"]
    color = get_color(rate)
    folium.RegularPolygonMarker(
        location=[lat, lng],
        popup=str(rate) + " $/sqft",
        fill_color=color,
        number_of_sides=20,
        radius=4
    ).add_to(map_sf)

map_sf.save('map.html')