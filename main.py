import streamlit as st
import folium as fl
from streamlit_folium import st_folium
from folium import Popup
from datetime import timedelta
import random
from model_prediction import *
from save_map_figures import *
from create_final_image import *

st.set_page_config(
    page_title="Miuuxy",
    page_icon=":hatched_chick:",
    initial_sidebar_state="expanded",
)


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
    st.session_state.minute = None
    st.session_state.distance = None


def get_date():
    # Başlangıç ve bitiş tarihlerini tanımla
    start_date = datetime(2010, 1, 1)
    end_date = datetime(2015, 6, 30)

    # Rastgele bir tarih seç
    random_days = random.randint(0, (end_date - start_date).days)
    random_date = start_date + timedelta(days=random_days)
    return random_date


# Uygulama mantığı

if (
    st.session_state.current_state == "get_pickup_location"
    or st.session_state.current_state == "get_pickup_location_with_distance_error"
    or st.session_state.current_state == "get_pickup_location_with_out_of_range_error"
):
    st.session_state.random_date = get_date()
    st.title("Alış Noktası Seçiniz")

    m = fl.Map(
        tiles="OpenStreetMap",
        zoom_start=11,
        location=[40.78910688411592, -73.98452568420909],
    )
    m.add_child(fl.LatLngPopup())
    map_ny = st_folium(m, height=400, width=700)

    if st.session_state.current_state == "get_pickup_location_with_distance_error":
        st.error("Alış ve varış noktaları arası mesafe çok kısa!")
    if st.session_state.current_state == "get_pickup_location_with_out_of_range_error":
        st.error("Alış ve varış noktaları NYC dışında!")

    if map_ny["last_clicked"]:
        st.session_state.pickup_lat = map_ny["last_clicked"]["lat"]
        st.session_state.pickup_lon = map_ny["last_clicked"]["lng"]
        st.session_state.current_state = "get_dropoff_location"
        st.experimental_rerun()

elif st.session_state.current_state == "get_dropoff_location":
    st.title("Varış Noktası Seçiniz")

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
        st.session_state.distance = haversine(
            [st.session_state.pickup_lat, st.session_state.pickup_lon],
            [st.session_state.dropoff_lat, st.session_state.dropoff_lon],
        )
        if st.session_state.distance < 1.5:
            st.session_state.current_state = "get_pickup_location_with_distance_error"
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

    passenger_count = st.number_input(
        "Yolcu Sayısı", min_value=1, max_value=10, value=1
    )
    # Saat seçiniz
    time_input = st.time_input("Bir saat ve dakika seçin")

    # Saat ve dakika bilgilerini ayıkla
    if time_input is not None:
        st.session_state.hour = time_input.hour
        st.session_state.minute = time_input.minute

    if st.button("Tahminle!"):
        pickup = [st.session_state.pickup_lon, st.session_state.pickup_lat]
        dropoff = [st.session_state.dropoff_lon, st.session_state.dropoff_lat]
        passenger_count = passenger_count
        # Add hour to date
        print(st.session_state.random_date)
        st.session_state.random_date = st.session_state.random_date + timedelta(
            hours=st.session_state.hour, minutes=st.session_state.minute
        )
        print(st.session_state.random_date)

        # 2. Prepare the data
        data = prepare_data(
            pickup,
            dropoff,
            passenger_count,
            st.session_state.random_date,
        )
        with st.status("Tahmin hazırlanıyor!", expanded=True) as status:
            st.write("Veri hazırlanıyor...")
            prediction = make_prediction(data)
            st.write("Tahmin hazır! Harita görseli oluşturuluyor...")
            create_image(
                st.session_state.pickup_lat,
                st.session_state.pickup_lon,
                st.session_state.dropoff_lat,
                st.session_state.dropoff_lon,
            )
            st.write("Harita görseli oluşturuldu! Tahmin görseli oluşturuluyor...")
            create_result_image(
                st.session_state.pickup_lat,
                st.session_state.pickup_lon,
                st.session_state.dropoff_lat,
                st.session_state.dropoff_lon,
                passenger_count,
                st.session_state.random_date,
                prediction,
                st.session_state.distance,
            )
            status.update(label="Bitti!", state="complete", expanded=False)
        st.image("images/result.png")

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

st.caption(
    """
                <p style='text-align: center;'><font size="2">version 0.5</font>
                </p>
            """,
    unsafe_allow_html=True,
)
