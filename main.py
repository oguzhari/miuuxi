import streamlit as st
import folium as fl
from streamlit_folium import st_folium
from folium import Popup
from datetime import timedelta
import random
from model_prediction import *
from save_map_figures import *

# Session state tanımlama
if "current_state" not in st.session_state:
    st.session_state.current_state = "get_pickup_location"
    st.session_state.pickup_lat = None
    st.session_state.pickup_lon = None
    st.session_state.dropoff_lat = None
    st.session_state.dropoff_lon = None
    st.session_state.distance_error = False
    st.session_state.out_of_range_error = False
    st.session_state.random_date = "2010-01-01 00:00:00 UTC"
    st.session_state.hour = None

st.write(f"Current state: {st.session_state.current_state}")


def get_date():
    # Başlangıç ve bitiş tarihlerini tanımla
    start_date = datetime(2010, 1, 1)
    end_date = datetime(2015, 6, 30)

    # Rastgele bir tarih seç
    random_days = random.randint(0, (end_date - start_date).days)
    random_date = start_date + timedelta(days=random_days)
    return random_date


# Uygulama mantığı
try:
    if (
        st.session_state.current_state == "get_pickup_location"
        or st.session_state.current_state == "get_pickup_location_with_distance_error"
        or st.session_state.current_state
        == "get_pickup_location_with_out_of_range_error"
    ):
        st.session_state.random_date = get_date()
        st.title("Alış Noktası Seçiniz")
        st.text(f"Rastgele bir tarih seçildi: {st.session_state.random_date}")

        m = fl.Map(
            tiles="OpenStreetMap",
            zoom_start=11,
            location=[40.78910688411592, -73.98452568420909],
        )
        m.add_child(fl.LatLngPopup())
        map_ny = st_folium(m, height=400, width=700)

        if st.session_state.current_state == "get_pickup_location_with_distance_error":
            st.error("Alış ve varış noktaları arası mesafe çok kısa!")
        if (
            st.session_state.current_state
            == "get_pickup_location_with_out_of_range_error"
        ):
            st.error("Alış ve varış noktaları NYC dışında!")

        if map_ny["last_clicked"]:
            st.session_state.pickup_lat = map_ny["last_clicked"]["lat"]
            st.session_state.pickup_lon = map_ny["last_clicked"]["lng"]
            st.session_state.current_state = "get_dropoff_location"
            st.experimental_rerun()

    elif st.session_state.current_state == "get_dropoff_location":
        st.title("Varış Noktası Seçiniz")
        st.text("Alış noktası seçildi")
        st.text(f"{st.session_state.pickup_lat}, {st.session_state.pickup_lon}")
        st.text(f"Rastgele bir tarih seçildi: {st.session_state.random_date}")
        m = fl.Map(
            tiles="OpenStreetMap",
            zoom_start=11,
            location=[40.78910688411592, -73.98452568420909],
        )
        popup = Popup("Alış", parse_html=True, show=True)
        fl.Marker(
            [st.session_state.pickup_lat, st.session_state.pickup_lon], popup=popup
        ).add_to(m)
        m.add_child(fl.LatLngPopup())
        map_ny = st_folium(m, height=400, width=700)

        if map_ny["last_clicked"]:
            st.session_state.dropoff_lat = map_ny["last_clicked"]["lat"]
            st.session_state.dropoff_lon = map_ny["last_clicked"]["lng"]
            distance = haversine(
                [st.session_state.pickup_lat, st.session_state.pickup_lon],
                [st.session_state.dropoff_lat, st.session_state.dropoff_lon],
            )
            if distance < 1.5:
                st.session_state.current_state = (
                    "get_pickup_location_with_distance_error"
                )
                st.session_state.distance_error = True
                st.experimental_rerun()
            if check_is_in_nyc(
                st.session_state.pickup_lat,
                st.session_state.pickup_lon,
                st.session_state.dropoff_lat,
                st.session_state.dropoff_lon,
            ):
                pass
            else:
                st.session_state.current_state = (
                    "get_pickup_location_with_out_of_range_error"
                )
                st.experimental_rerun()
            st.session_state.current_state = "get_passenger_count_and_time"
            st.experimental_rerun()

    elif st.session_state.current_state == "get_passenger_count_and_time":
        # Get Passenger count and hour and minute time
        st.title("Yolcu Sayısı ve Tarih Seçiniz")

        st.text(f"Rastgele bir tarih seçildi: {st.session_state.random_date}")

        st.text("Alış noktası seçildi")
        st.text(f"{st.session_state.pickup_lat}, {st.session_state.pickup_lon}")

        st.text("Varış noktası seçildi")
        st.text(f"{st.session_state.dropoff_lat}, {st.session_state.dropoff_lon}")

        st.text("Hesaplanan Mesafe")
        st.text(
            f"{haversine([st.session_state.pickup_lat, st.session_state.pickup_lon],[st.session_state.dropoff_lat, st.session_state.dropoff_lon])} km"
        )

        passenger_count = st.number_input(
            "Yolcu Sayısı", min_value=1, max_value=10, value=1
        )
        # Saat seçiniz
        time_input = st.time_input("Bir saat ve dakika seçin")

        # Saat ve dakika bilgilerini ayıkla
        if time_input is not None:
            st.session_state.hour = time_input.hour
            minute = time_input.minute
            st.write(f"Seçilen saat: {st.session_state.hour}:{minute}")

        if st.button("Tahminle!"):
            pickup = [st.session_state.pickup_lon, st.session_state.pickup_lat]
            dropoff = [st.session_state.dropoff_lon, st.session_state.dropoff_lat]
            passenger_count = passenger_count
            # Add hour to date
            st.session_state.random_date = st.session_state.random_date + timedelta(
                hours=st.session_state.hour
            )

            # 2. Prepare the data
            data = prepare_data(
                pickup,
                dropoff,
                passenger_count,
                st.session_state.random_date,
            )
            st.text("Velev ki tahmin ediyorum...")
            st.text(data)
            prediction = make_prediction(data)
            st.text(f"Tahmini ücret: {prediction[0]:.2f} $")
            create_image(
                st.session_state.pickup_lat,
                st.session_state.pickup_lon,
                st.session_state.dropoff_lat,
                st.session_state.dropoff_lon,
            )
            st.image("model.png", width=700)

        if st.button("Sıfırla"):
            st.session_state.current_state = "get_pickup_location"
            st.session_state.pickup_lat = None
            st.session_state.pickup_lon = None
            st.session_state.dropoff_lat = None
            st.session_state.dropoff_lon = None
            st.session_state.distance_error = False
            st.session_state.out_of_range_error = False
            st.session_state.random_date = "2010-01-01 00:00:00 UTC"
            st.session_state.hour = None
            st.experimental_rerun()

except Exception as e:
    st.write(f"An error occurred: {e}")

st.caption(
    """
                <p style='text-align: center;'><font size="2">version 0.3</font>
                </p>
            """,
    unsafe_allow_html=True,
)
