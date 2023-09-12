from PIL import Image, ImageDraw, ImageFont
from datetime import timedelta, datetime
import random


def create_random_plate():
    # 100 ile 999 arasında rastgele bir plaka harf grubu oluştur
    letters = random.randint(1000, 9999)
    # plakayı birleştir
    plate = f"MVK {letters}"
    return plate


def custom_dice_roll():
    roll = random.uniform(0, 1)  # 0 ile 1 arasında bir sayı üretir
    if roll < 0.99:
        return 1
    else:
        return 2


def create_result_image(
    pickup_lat,
    pickup_lon,
    dropoff_lat,
    dropoff_lon,
    passenger_count,
    date,
    prediction,
    distance,
):
    # Görselleri oku
    template = Image.open("images/template.png")
    # %99'a %1 olasılıklı random
    zar = custom_dice_roll()

    if zar == 1:
        model = Image.open("images/model.png")
    else:
        model = Image.open("images/easter_egg.png")

    if type(date) == str:
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S UTC")

    # model görselini yeniden boyutlandır
    model_resized = model.resize((1022, 617))

    # Yapıştırılacak konumu belirle
    x, y = 29, 208

    # Yapıştırma işlemi
    template.paste(model_resized, (x, y))

    # pickup_lat ile picup_lon'u yazdır birleştirerek virgülden sonra 5 basamak gösterekrek string oluştur
    pickup = f"[{pickup_lat:.5f}, {pickup_lon:.5f}]"

    # dropoff_lat ile dropoff_lon'u yazdır birleştirerek virgülden sonra 5 basamak gösterekrek string oluştur
    dropoff = f"[{dropoff_lat:.5f}, {dropoff_lon:.5f}]"

    # Yolcu sayısını yazdır
    passenger_count = str(passenger_count)

    # tahmini ücreti yazdır
    prediction = f"{prediction[0]:.2f} $"

    # pickup metnini template metni üzerine yaz
    drawable = ImageDraw.Draw(template)
    drawable.text(
        (134.8, 1310.8),
        pickup,
        fill=(255, 255, 255),
        font=ImageFont.truetype("fonts/arial.ttf", 35),
    )
    # dropoff metnini template metni üzerine yaz
    drawable.text(
        (134.8, 1462.6),
        dropoff,
        fill=(255, 255, 255),
        font=ImageFont.truetype("fonts/arial.ttf", 35),
    )

    # passenger_count metnini template metni üzerine yaz
    drawable.text(
        (876.8, 1316.9),
        passenger_count + " kişi",
        fill=(255, 255, 255),
        font=ImageFont.truetype("fonts/arial.ttf", 30),
        anchor="ra",
    )

    # date içerisinden sadece gün, ay ve yılı al ve template metni üzerine yaz
    drawable.text(
        (876.8, 1405.8),
        date.strftime("%d.%m.%Y"),
        fill=(255, 255, 255),
        font=ImageFont.truetype("fonts/arial.ttf", 30),
        anchor="ra",
    )

    # date içerisinden sadece saat ve dakikayı al ve template metni üzerine yaz
    drawable.text(
        (876.8, 1487.9),
        date.strftime("%H:%M"),
        fill=(255, 255, 255),
        font=ImageFont.truetype("fonts/arial.ttf", 30),
        anchor="ra",
    )

    # prediction metnini template metni üzerine yaz
    drawable.text(
        (545 + 150, 1650 + 50),
        prediction,
        fill=(100, 255, 100),
        font=ImageFont.truetype("fonts/arial-bold.ttf", 75),
        anchor="mm",
    )

    distance = f"Yaklaşık {distance:.2f} km"
    drawable.text(
        (515, 1600),
        distance,
        fill=(255, 255, 255),
        font=ImageFont.truetype("fonts/arial.ttf", 35),
        anchor="mm",
    )

    if zar == 1:
        plate = create_random_plate()
    else:
        plate = "MVK GOLDEN"

    drawable.text(
        (876.8, 1228.7),
        plate,
        fill=(255, 255, 255),
        font=ImageFont.truetype("fonts/plate.otf", 45),
        anchor="ra",
    )

    # Hepsini yazdır
    print(pickup, dropoff, passenger_count, date, prediction)

    # Sonucu kaydet
    template.save("images/result.png")
