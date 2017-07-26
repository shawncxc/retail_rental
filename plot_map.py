import os
import json
import numpy as np
import folium
from folium.plugins import HeatMap
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

lat_sf = 37.767645
lng_sf = -122.4184106

# regular map
map_sf = folium.Map(location=[lat_sf, lng_sf], zoom_start=13)
redis_db = redis_client()
redis_db.connect()
data = []
for key in redis_db.conn.scan_iter():
    temp = redis_db.get(key)
    lat = temp["geo"]["lat"]
    lng = temp["geo"]["lng"]
    rate = temp["rate"]
    color = get_color(rate)
    folium.CircleMarker(
        location=[lat, lng],
        popup=str(rate) + " $/sqft",
        fill_opacity=1,
        fill_color=color,
        color="black",
        radius=4
    ).add_to(map_sf)
    data.append([lat, lng, rate])
map_sf.save('map.html')

# heatmap
heatmap_sf = folium.Map([lat_sf, lng_sf], tiles='stamentoner', zoom_start=13)
HeatMap(data).add_to(heatmap_sf)
heatmap_sf.save('heatmap.html')