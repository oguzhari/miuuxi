import folium as fl
from streamlit_folium import st_folium
import streamlit as st

x = {"a": 37, "b": 42, "c": 927}


def get_pos(lat, lng):
    return lat, lng


m = fl.Map(tiles="OpenStreetMap", zoom_start=10, location=[40.7128, -74.0060])

m.add_child(fl.LatLngPopup())

st.title("Point - Loc Alpha")
# Örnek olarak New York'un koordinatları
map_ny = st_folium(m, height=350, width=700)

try:
    data = get_pos(map_ny["last_clicked"]["lat"], map_ny["last_clicked"]["lng"])
    st.write(data)
except TypeError:
    pass
