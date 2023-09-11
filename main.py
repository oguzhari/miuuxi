import streamlit as st
import folium as fl
from streamlit_folium import st_folium
from folium import Popup
from datetime import datetime, timedelta
import random
from model_prediction import *

# Session state tanımlama
if 'current_state' not in st.session_state:
    st.session_state.current_state = 'get_pickup_location'
    st.session_state.pickup_lat = None
    st.session_state.pickup_lon = None
    st.session_state.dropoff_lat = None
    st.session_state.dropoff_lon = None
    st.session_state.distance_error = False

st.write(f'Current state: {st.session_state.current_state}')

# Başlangıç ve bitiş tarihlerini tanımla
start_date = datetime(2010, 1, 1)
end_date = datetime(2015, 6, 30)

# Rastgele bir tarih seç
random_days = random.randint(0, (end_date - start_date).days)
random_date = start_date + timedelta(days=random_days)


# Uygulama mantığı
try:
    if st.session_state.current_state == 'get_pickup_location':
        st.title("Alış Noktası Seçiniz")
        st.text(f"Rastgele bir tarih seçildi: {random_date}")
        m = fl.Map(tiles="OpenStreetMap", zoom_start=10, location=[40.7128, -74.0060])
        m.add_child(fl.LatLngPopup())
        map_ny = st_folium(m, height=350, width=700)

        if st.session_state.distance_error:
            st.error("Alış ve varış noktaları arası mesafe 1.5 km'den az olamaz! Lütfen tekrar seçim yapınız.")
            st.session_state.distance_error = False

        if map_ny["last_clicked"]:
            st.session_state.pickup_lat = map_ny["last_clicked"]["lat"]
            st.session_state.pickup_lon = map_ny["last_clicked"]["lng"]
            st.session_state.current_state = 'get_dropoff_location'
            st.experimental_rerun()

    elif st.session_state.current_state == 'get_dropoff_location':
        st.title("Varış Noktası Seçiniz")
        st.text("Alış noktası seçildi")
        st.text(f"{st.session_state.pickup_lat}, {st.session_state.pickup_lon}")
        st.text(f"Rastgele bir tarih seçildi: {random_date}")
        m = fl.Map(tiles="OpenStreetMap", zoom_start=10, location=[40.7128, -74.0060])
        popup = Popup("Alış", parse_html=True, show=True)
        fl.Marker([st.session_state.pickup_lat, st.session_state.pickup_lon], popup=popup).add_to(m)
        m.add_child(fl.LatLngPopup())
        map_ny = st_folium(m, height=350, width=700)

        if map_ny["last_clicked"]:
            st.session_state.dropoff_lat = map_ny["last_clicked"]["lat"]
            st.session_state.dropoff_lon = map_ny["last_clicked"]["lng"]
            st.session_state.current_state = 'get_passenger_count_and_time'
            distance = haversine([st.session_state.pickup_lat, st.session_state.pickup_lon],
                                 [st.session_state.dropoff_lat, st.session_state.dropoff_lon])
            if distance < 1.5:
                st.session_state.current_state = 'get_pickup_location'
                st.session_state.distance_error = True
            st.experimental_rerun()
    elif st.session_state.current_state == 'get_passenger_count_and_time':
        # Get Passenger count and hour and minute time
        st.title("Yolcu Sayısı ve Tarih Seçiniz")

        st.text(f"Rastgele bir tarih seçildi: {random_date}")

        st.text("Alış noktası seçildi")
        st.text(f"{st.session_state.pickup_lat}, {st.session_state.pickup_lon}")

        st.text("Varış noktası seçildi")
        st.text(f"{st.session_state.dropoff_lat}, {st.session_state.dropoff_lon}")

        st.text("Hesaplanan Mesafe")
        st.text(f"{haversine([st.session_state.pickup_lat, st.session_state.pickup_lon],[st.session_state.dropoff_lat, st.session_state.dropoff_lon])} km")

        passenger_count = st.number_input("Yolcu Sayısı", min_value=1, max_value=10, value=1)
        # Saat seçiniz
        time_input = st.time_input("Bir saat ve dakika seçin")

        # Saat ve dakika bilgilerini ayıkla
        if time_input is not None:
            hour = time_input.hour
            minute = time_input.minute
            st.write(f"Seçilen saat: {hour}:{minute}")

        if st.button("Tahminle!"):
            st.text("Velev ki tahmin ediyorum...")
        if st.button("Sıfırla"):
            st.session_state.current_state = 'get_pickup_location'
            st.session_state.pickup_lat = None
            st.session_state.pickup_lon = None
            st.session_state.dropoff_lat = None
            st.session_state.dropoff_lon = None
            st.session_state.distance_error = False
            st.experimental_rerun()


except Exception as e:
    st.write(f"An error occurred: {e}")
