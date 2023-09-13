# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 17:15:17 2023

@author: iecet
"""

import streamlit as st

st.image("images/logo_head.png", use_column_width=True)

st.title(
    "Taksi Ücret Tahmini Uygulaması: Kullanıcıların Binme ve İnme Lokasyonlarına Dayalı Makine Öğrenmesi Modeli"
)

st.markdown(
    """
**Ece Titiz**, **Oğuzhan Arı** , **Tuğba Aktaş**,  **Elmira Kaya**

*Source Code: https://github.com/oguzhari/miuuxy*

"""
)

st.header("Özet")
st.info(
    """
Bu çalışmada, kullanıcıların seyahat etmek istedikleri yerlerin binme ve inme lokasyon bilgileri, 
seyahat saati ve yolcu sayısı girdikleri kullanılarak makine öğrenmesi algoritmalarıyla tahmini ücreti hesaplamak için 
bir model oluşturulmuştur.
Model, Kaggle platformundan alınan yaklaşık 55 milyon satırlık New York City Taxi Fare Prediction 
veri seti kullanılarak eğitilmiştir. RandomForestRegressor ve LightGBM algoritmaları kullanılmıştır, LightGBM ile 
0.87 r2 score'u elde edilmiştir. Şu an çalışan model, LightGBM'dir.

"""
)

st.markdown(
    "**Anahtar Kelimeler:** *Makine Öğrenmesi*, *Streamlit*, *Veri Bilimi*, *Python*"
)

st.header("Giriş")
st.markdown(
    """
**Konu:** Bu çalışma, coğrafi konum bilgileri, yolcu sayısı ve seyahat saati bilgilerini kullanarak taksi ücreti tahmin etme yöntemlerine odaklanmaktadır.

**Amaç:** Bu projenin temel amacı, taksi yolcularına daha önceden belirlenmiş koordinatların, 
yolcu sayısı, saat ve tarih bilgileri gibi değişkenlere dayanarak tahmini taksi ücreti sunarak 
kullanıcı deneyimini iyileştirmek ve ödeyecekleri taksi ücretini daha öngörülebilir hale getirmektir.

**Önem:** Turizm endüstrisinde rota planlaması, lojistik yönetiminde taşıma maliyetlerinin hesaplanması 
gibi birçok alanda bu yöntemlere ihtiyaç vardır. Bu çalışma, bu önemli aracın anlaşılmasına ve etkin kullanılmasına 
katkı sağlamayı amaçlamaktadır.

**Varsayımlar:** Bu proje geliştirilirken, trafik koşullarının sabit olduğu, 
GPS koordinatlarının doğru ve hassas olduğu, kullanıcıların verdiği başlangıç ve bitiş noktalarının 
tam ve doğru olduğu, ücret tarifelerinin değişmediği, makine öğrenme modelinin güvenilir tahminler sunduğu,
kullanıcıların tahminin sadece bir yaklaşım olduğunu bilincinde olduğu, kişisel verilerin güvenliği ve 
gizliliğinin korunduğu, yerel düzenlemelere ve yasalara uyum sağlandığı varsayımlarına dayalı olarak, 
kullanıcıların tahmini taksi ücretlerini hesaplamak ve yolculuklarını daha iyi planlamak için bu 
uygulamayı kullandığı varsayımlarında bulunulmuştur. 

**Sınırlılıklar:** Bu çalışma, sadece belirli coğrafi mesafe hesaplama yöntemlerine odaklanmaktadır ve daha karmaşık coğrafi analizlerin veya çoklu veri kaynaklarının kullanımını ele almamaktadır. Ayrıca, kullanılan coğrafi verilerin kesinliği ve tamamlığı, hesaplamanın doğruluğunu etkileyebilir.

"""
)

st.header("Kullanılan Yöntemler")
st.markdown(
    """
    Bu çalışmada toplam 55 milyon satırlık bir veri seti kullanılmıştır. Ön işleme ve Öznitelik Çıkarımı adımlarına
    bütün veri seti dahil edilmiştir. Bütün verinin temizlenmesi, öznitelik çıkarımı ve model eğitimi için toplam 2 saat
    57 dakika sürmüştür. Modelin R2 skoru 0.87 olarak ölçülmüştür. Modelin tahmin yapabilmesi için her kullanıcı 
    uygulamaya girdiğinde, rastgele bir tarih atanmaktadır. Bu tarihin atanma sebebi, modeldeki son verinin 30 Haziran 
    2015 tarihinde olmasıdır.
    
    Daha net ve duyarlı tahminler gerçekleştirebilmesi için böyle bir kısıtlamaya gidilmiştir.
    """
)

st.header("Sıkça Sorulabilecek Sorular")
with st.expander("İki lokasyon arasındaki kilometreyi nasıl hesapladınız?"):
    st.write(
        """
        Haversine Formülü aracılığı ile yaptık. Bu formül, iki nokta arasındaki en kısa mesafeyi hesaplamak için 
        kullanılır. Bu formül, iki nokta arasındaki en kısa mesafeyi hesaplamak için kullanılır. Detayları Özellik 
        Mühendisliği bölümünde bulabilirsiniz.
    """
    )

with st.expander("Neden tarih rastgele olarak seçiliyor?"):
    st.write(
        """
        Eğitim verimiz 2010 Ocak ile 2015 Haziran arasındaki verileri içermektedir. Bu sebeple, modelin tahmin 
        yapabilmesi için her kullanıcı uygulamaya girdiğinde, rastgele bir tarih atanmaktadır. Bu tarihin atanma
        sebebi, modeldeki son verinin 30 Haziran 2015 tarihinde olmasıdır. Daha net ve duyarlı tahminler
        gerçekleştirebilmesi için böyle bir kısıtlamaya gidilmiştir.
    """
    )

with st.expander("Neden sadece New York içerisinde konum seçilebiliyor?"):
    st.write(
        """
        Çünkü öyle istedik. 😌😌
        
        Şaka bir yana, tahminlerin New York şehir içi taksi ücretleri hesaplamanız beklendiğinden, New York dışında
        inme veya binme koordinatları içeren kayıtlar veri setinden çıkarılmıştır.
        
        Veri seti, New York dışında bir konum içermediğinden, tahminler de bu aralık içerisinde tutulmaya çalışılıyor.
    """
    )

with st.expander("Neden sadece 1-6 arası yolcu sayısı seçilebiliyor?"):
    st.write(
        """
        Bir taksi minimum 1 maximum 6 altı yolcu taşıyabileceğinden bu yolcu aralığının dışındaki kayıtlar veri setinden 
        çıkarılmıştır. Tahminlerin New York şehir içi taksi ücretleri hesaplamanız beklendiğinden, 1-6 arası yolcu
        sayısı seçilebilmektedir.
        """
    )

st.subheader("Girilen Koordinatların Haversine Formülü ile Kilometreye Çevrilmesi")

code = '''def haversine(pickup_, dropoff_):
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
    return c * r'''
st.code(code, language="python")

st.markdown(
    """
Haversine formülü, iki koordinat arasındaki mesafenin hassas bir şekilde hesaplamasına olanak sağlamaktadır.
Coğrafi verileri daha anlamlı ve kullanışlı bir şekilde işleyebilmek adına girilen koordinatlar
bu formül ile kilometreye çevrilmiştir. 
"""
)
st.image("images/haversine.png", caption="Haversine Hesaplaması")


st.header("Veri Önişleme Adımları")
st.subheader("2.5$ Altı Kayıtların Veri Setinden Çıkarılması")

code = """def remove_under_2_5_dollars(data):
    eski_boyut = len(data)
    print('Eski boyut: %d' % eski_boyut)
    data = data.drop(data[data['fare_amount']<2.5].index, axis=0)
    print('Yeni boyut: %d' % len(data))
    print('Silinen veri sayısı: %d' % (eski_boyut - len(data)))"""
st.code(code, language="python")

st.markdown(
    """
Tutarı 2.5$ altında olan kayıtlar New York taksi ücretlerinde minimum ücretin 2.5 dolar olması sebebiyle 
veri setinden çıkarılmıştır. 
"""
)

st.subheader("Eksik Değer İçeren Verilerin Silinmesi")
code = """
def remove_null_values(data):
    eski_boyut = len(data)
    print('Eski boyut: %d' % eski_boyut)
    data = data.dropna(how='any', axis=0)
    print('Yeni boyut: %d' % len(data))
    print('Silinen veri sayısı: %d' % (eski_boyut - len(data)))"""
st.code(code, language="python")

st.markdown(
    """
Eksik veri içeren gözlemler veri setinden çıkarılmıştır. 
"""
)

st.subheader("New York Dışında Kalan Koordinatlar İçeren Kayıtların Silinmesi")
code = """
# Sınırlar:
# Kuzey Enlem: 40.917577
# Güney Enlem: 40.477399
# Doğu Boylam: -73.700272
# Batı Boylam: -74.259090

def remove_outside_nyc(data):
    eski_boyut = len(data)
    print('Eski boyut: %d' % eski_boyut)
    data = data[(data['pickup_longitude'] >= -74.259090) & (data['pickup_longitude'] <= -73.700272)]
    data = data[(data['dropoff_longitude'] >= -74.259090) & (data['dropoff_longitude'] <= -73.700272)]
    data = data[(data['pickup_latitude'] >= 40.477399) & (data['pickup_latitude'] <= 40.917577)]
    data = data[(data['dropoff_latitude'] >= 40.477399) & (data['dropoff_latitude'] <= 40.917577)]
    print('Yeni boyut: %d' % len(data))
    print('Silinen veri sayısı: %d' % (eski_boyut - len(data)))
"""
st.code(code, language="python")

st.markdown(
    """
Tahminlerin New York şehir içi taksi ücretlerini kapsaması amaçlandığından New York dışında inme
veya binme koordinatları içeren kayıtlar veri setinden çıkarılmıştır. 
"""
)

st.subheader("Biniş ve İniş Koordinatları Birebir Aynı Olan Kayıtların Silinmesi")
code = """
def remove_same_location(data):
    eski_boyut = len(data)
    print('Eski boyut: %d' % eski_boyut)
    data = data[(data['pickup_longitude'] != data['dropoff_longitude']) | (data['pickup_latitude'] != data['dropoff_latitude'])]
    print('Yeni boyut: %d' % len(data))
    print('Silinen veri sayısı: %d' % (eski_boyut - len(data)))
"""
st.code(code, language="python")

st.markdown(
    """
Coğrafi mesafe hesaplamalarında gereksiz tekrarları önlemek ve sonuçların daha anlamlı olmasını sağlamak
amacıyla biniş ve iniş koordinatları aynı olan kayıtlar veri setinden çıkarılmıştır.
"""
)

st.subheader("Yolcu Sayısı 1'den az ve 6'dan Büyük Olan Kayıtların Silinmesi")
code = """
def rmeove_outlier_passenger(data):
    eski_boyut = len(data)
    print('Eski boyut: %d' % eski_boyut)
    data = data.drop(data[data['passenger_count']>7].index, axis = 0)
    data = data.drop(data[data['passenger_count']<1].index, axis = 0)
    print('Yeni boyut: %d' % len(data))
    print('Silinen veri sayısı: %d' % (eski_boyut - len(data)))"""
st.code(code, language="python")

st.markdown(
    """
Bir taksi minimum 1 maximum 6 altı yolcu taşıyabileceğinden bu yolcu aralığının dışındaki kayıtlar veri setinden çıkarılmıştır. 
"""
)


st.subheader("Taksi Ücreti 250den Büyük Olan Verilerin Silinmesi")
code = """
def remove_outlier_fare(data):
    eski_boyut = len(data)
    data = data.drop(data[data['fare_amount']>250].index, axis = 0)
    print('Yeni boyut: %d' % len(data))
    print('Silinen veri sayısı: %d' % (eski_boyut - len(data)))"""
st.code(code, language="python")

st.markdown(
    """
Aykırı değer aralığı olan 250 dolar ve üzeri taksi ücreti içeren kayıtlar veri setinden çıkarılmıştır. 
"""
)


st.header("Özellik Mühendisliği")
st.subheader("Yeni Bir Tarife Sütunu Olan Tarife_Yeni Sütununun Oluşturulması")
code = """
def add_hour_feature(data):
    data['hour'] = data['pickup_datetime'].str[11:13].astype(int)
    data['tarife_yeni'] = None

    # Saate göre 'tarife_yeni' sütununu doldurulması
    data.loc[(data['hour'] >= 0) & (data['hour'] < 6), 'tarife_yeni'] = 'gece'
    print('gece tamam')
    data.loc[(data['hour'] >= 6) & (data['hour'] < 12), 'tarife_yeni'] = 'sabah'
    print('sabah tamam')
    data.loc[(data['hour'] >= 12) & (data['hour'] < 17), 'tarife_yeni'] = 'öğlen'
    print('öğlen tamam')
    data.loc[(data['hour'] >= 17) & (data['hour'] < 24), 'tarife_yeni'] = 'akşam'
    print('akşam tamam')"""
st.code(code, language="python")

st.markdown(
    """
Alış tarihi olan pickup_datetime sütunu kullanılarak 24 saatlik zaman dilimi gece, sabah, öğlen ve akşam
dilimlerine ayrılmıştır. Bu sayede günün hangi bölümünün taksi ücreti tahmininde daha anlamlı bir etkiye sahip olduğu
belirlenmek istenmiştir.   
"""
)

st.subheader("Zamana Dayalı Yeni Feature Çıkarımlarının Yapılması")
code = """
def time_features(dataframe):
    dataframe['hour_of_day'] = dataframe.pickup_datetime.dt.hour
    dataframe['month'] = dataframe.pickup_datetime.dt.month
    dataframe["year"] = dataframe.pickup_datetime.dt.year
    dataframe["weekday"] = dataframe.pickup_datetime.dt.weekday    
    return dataframe"""
st.code(code, language="python")

st.markdown(
    """
Alış tarihi olan pickup_datetime sütunu kullanılarak yolcunun alındığı saat, ay, yıl ve haftanın günü
bilgileri birer sütun olarak eklenmiştir. Bu sayede bu özelliklerin taksi ücreti tahmininde nasıl bir etkiye sahip olduğu
belirlenmek istenmiştir.   
"""
)

st.header("Sonuç")
st.markdown(
    """
Bu çalışma, yolculuk ücret tahmini konusunda Kaggle veri setleri ve Streamlit arayüzü kullanarak 
yenilikçi bir yaklaşım sunmaktadır. Elde edilen sonuçlar ve bulgular, bu uygulamanın kullanıcılara 
seyahat maliyetlerini daha doğru bir şekilde tahmin etmelerine yardımcı olduğunu göstermektedir.

Kullanıcılarımız, kolayca yolculuk planları yapabilir ve tahmini maliyetleri önceden görebilirler. 
 Bu, kullanıcıların daha bilinçli seyahat kararları almasına yardımcı oldu.

Sonuç olarak, bu çalışma, büyük veri analitiği, makine öğrenmesi ve kullanıcı dostu arayüz tasarımının 
birleşimini kullanarak yolculuk ücret tahmini konusunda önemli bir adım atmaktadır. Kaggle'dan alınan 
veri setleri, bu alandaki potansiyel kaynakları vurgulamakta ve Streamlit arayüzü, benzer uygulamaların 
daha fazla kullanıcı tarafından benimsenmesine yol açabilecek bir arayüz tasarımı örneği sunmaktadır.

Gelecekteki çalışmalar, daha fazla veri kaynağına erişim ve daha karmaşık makine öğrenmesi teknikleri 
kullanarak tahmin modellerinin iyileştirilmesine odaklanabilir. Ayrıca, kullanıcı geri bildirimleri
dikkate alarak uygulamanın kullanıcı geliştirebilir. 

Bu çalışma, seyahat maliyeti tahminindeki potansiyel gelişmeler için bir temel oluştururken, 
büyük veri ve yapay zeka konularındaki gelecekteki araştırmalara da ilham kaynağı olabilecektir."""
)

st.header("Model")
st.download_button(
    label="Modeli İndir",
    data="model/model.pkl",
    file_name="NYC_Taxi_Fare_Prediction_Model.pkl",
    mime="text/plain",
)
