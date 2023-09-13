import joblib
from math import radians, cos, sin, asin, sqrt
from datetime import datetime


# Load the model
def load_model():
    return joblib.load("model/model.pkl")


def check_is_in_nyc(pic_lat, pic_lon, drop_lat, drop_lon):
    if (
        40.477399 <= pic_lat <= 40.917577
        and 40.477399 <= drop_lat <= 40.917577
        and -74.259090 <= pic_lon <= -73.700272
        and -74.259090 <= drop_lon <= -73.700272
    ):
        return True
    else:
        return False


def haversine(pickup_, dropoff_):
    """
    Calculate the great circle distance in kilometers between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = pickup_[0], pickup_[1], dropoff_[0], dropoff_[1]
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r


def get_date_info(date_):
    # Get hour, month, year, weekday, time_of_day_gece_, time_of_day_sabah_, time_of_day_öğlen_ from date_
    hour = date_.hour
    month = date_.month
    year = date_.year
    weekday = date_.weekday()
    time_of_day_gece_ = 0
    time_of_day_sabah_ = 0
    time_of_day_oglen_ = 0
    if 0 <= hour < 6:
        time_of_day_gece_ = 1
    elif 6 <= hour < 11:
        time_of_day_sabah_ = 1
    elif 11 <= hour < 16:
        time_of_day_oglen_ = 1

    return (
        hour,
        month,
        year,
        weekday,
        time_of_day_gece_,
        time_of_day_sabah_,
        time_of_day_oglen_,
    )


# Prepare Data
def prepare_data(pickup_, dropoff_, passenger_count_, date_):
    # 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude','dropoff_latitude', 'passenger_count',
    # 'hour', 'month', 'year', 'weekday', 'distance', 'time_of_day_gece', 'time_of_day_sabah', 'time_of_day_öğlen'

    # 1. Calculate the distance with haversine formula
    distance = haversine(pickup_, dropoff_)

    # 2. Get hour, month, year, weekday, time_of_day_gece_, time_of_day_sabah_, time_of_day_öğlen_ from date_
    (
        hour,
        month,
        year,
        weekday,
        time_of_day_gece_,
        time_of_day_sabah_,
        time_of_day_oglen_,
    ) = get_date_info(date_)

    data = [
        [
            pickup_[0],
            pickup_[1],
            dropoff_[0],
            dropoff_[1],
            passenger_count_,
            hour,
            month,
            year,
            weekday,
            distance,
            time_of_day_gece_,
            time_of_day_sabah_,
            time_of_day_oglen_,
        ]
    ]

    return data


# Predict the output
def make_prediction(data):
    model = load_model()
    return model.predict(data, verbose=0)


if __name__ == "__main__":
    # 1. Define the input variables
    pickup = [-73.844311, 40.721319]
    dropoff = [-73.84161, 40.712278]
    passenger_count = 1
    date = "2012-04-21 00:00:00 UTC"

    # 2. Prepare the data
    data = prepare_data(
        pickup,
        dropoff,
        passenger_count,
        datetime.strptime(date, "%Y-%m-%d %H:%M:%S UTC"),
    )

