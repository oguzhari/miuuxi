# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 17:15:17 2023

@author: iecet
"""

import streamlit as st

st.title(
    "Taksi Ücret Tahmini Uygulaması: Kullanıcıların Binme ve İnme Lokasyonlarına Dayalı Makine Öğrenmesi Modeli"
)

st.markdown(
    """
**Oğuzhan Arı** , **Tuğba Aktaş**, **İ.Ece Titiz**, **Elmira Kaya**

*Source Code: https://github.com/oguzhari/CD_Proje_Alpha*

"""
)

st.header("Özet")
st.info(
    """
Bu çalışmada, kullanıcıların seyahat etmek istedikleri yerlerin binme ve inme lokasyon bilgileri, 
seyahat saati ve yolcu sayısı girdikleri kullanılarak makine öğrenmesi algoritmalarıyla tahmini ücreti hesaplamak için 
bir model oluşturulmuştur.
Model, Kaggle platformundan alınan yaklaşık 55 milyon satırlık New York City Taxi Fare Prediction 
veri seti kullanılarak eğitilmiştir. x,y,z algoritmaları kullanılmıştır. ve k r2 score'u elde edilmiştir.

"""
)

st.markdown(
    "**Anahtar Kelimeler:** *Makine Öğrenmesi*, *Streamlit*, *Veri Bilimi*, *Python*"
)

st.header("Giriş")
st.markdown(
    """
**Konu:** Bu çalışma, coğrafi konum bilgileri, yolcu sayısı ve seyahat saati bilgilerini kullanarak taksi ücreti tahmin etme yöntemlerine odaklanmaktadır.

**Amaç:** Yerel ve küresel ölçekte, coğrafi konum bilgilerinin işlenmesi ve anlamlandırılması giderek 
daha önemli hale gelmektedir. Bu nedenle, coğrafi verilerle çalışırken iki nokta arasındaki mesafeyi 
hesaplama yeteneği, coğrafi bilgi sistemleri, seyahat planlaması, yakınlık analizi ve diğer birçok 
uygulama için temel bir öneme sahiptir. Bu çalışmanın amacı, Haversine formülü gibi popüler coğrafi 
mesafe hesaplama yöntemlerini incelemek ve bu yöntemlerin pratik uygulamalarını vurgulamaktır.

**Önem:** Turizm endüstrisinde rota planlaması, lojistik yönetiminde taşıma maliyetlerinin hesaplanması 
gibi birçok alanda bu yöntemlere ihtiyaç vardır. Bu çalışma, bu önemli aracın anlaşılmasına ve etkin kullanılmasına 
katkı sağlamayı amaçlamaktadır.

**Varsayımlar:** Bu çalışma, coğrafi konumların yüzeydeki küresel bir düzlemde modellediği kabulüne dayanmaktadır. 
Ayrıca, hesaplama yöntemlerinin hesaplamalarının hassaslığı ve doğruluğu, kullanılan 
coğrafi verilerin kalitesine bağlı olarak değişebilir.

**Sınırlılıklar:** Bu çalışma, sadece belirli coğrafi mesafe hesaplama yöntemlerine odaklanmaktadır ve daha karmaşık coğrafi analizlerin veya çoklu veri kaynaklarının kullanımını ele almamaktadır. Ayrıca, kullanılan coğrafi verilerin kesinliği ve tamamlığı, hesaplamanın doğruluğunu etkileyebilir.

Bu çalışmanın giriş bölümü, çalışmanın konusunu, amacını, önemini, varsayımlarını ve sınırlılıklarını özetlemektedir. Bu bölüm, okuyuculara çalışmanın genel bağlamını ve önemini açıklamak için kullanılır."""
)

st.header("Kullanılan Yöntemler")

st.subheader(
    "Girilen Binme Ve İnme Koordinatlarının Haversine Formülü ile Kilometreye Çevrilmesi"
)

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
Coğrafi verileri daha anlamlı ve kullanışlı bir şekilde işleyebilmek adına girilen inme ve binme koordinatları
bu formül ile kilometreye çevrilmiştir. 
"""
)

st.header("Veri Önişleme Adımları")
st.subheader("2.5 Dolar Altı Kayıtların Veri Setinden Çıkarılması")

code = """def remove_under_2_5_dollars(data):
    eski_boyut = len(data)
    print('Eski boyut: %d' % eski_boyut)
    data = data.drop(data[data['fare_amount']<2.5].index, axis=0)
    print('Yeni boyut: %d' % len(data))
    print('Silinen veri sayısı: %d' % (eski_boyut - len(data)))"""
st.code(code, language="python")

st.markdown(
    """
Tutarı 2.5 doların altında olan kayıtlar New York taksi ücretlerinde minimum ücretin 2.5 dolar olması sebebiyle 
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
#Sınırlar:
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
olmasına yardımcı oldu."
"""
)

st.subheader("Yolcu sayısı 1den az ve 6dan Büyük Olan Kayıtların Silinmesi")
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


st.header("References")
st.markdown(
    """
1. Li H, Tamang T, Nantasenamat C. Toward insights on antimicrobial selectivity of host defense peptides via machine learning model interpretation. Genomics. 2021;113(6):3851-3863.

2. Schaduangrat N, Malik AA, Nantasenamat C. ERpred: a web server for the prediction of subtype-specific estrogen receptor antagonists. PeerJ. 2021;9:e11716.

3. Schaduangrat N, Lampa S, Simeon S, Gleeson MP, Spjuth O, Nantasenamat C. Towards reproducible computational drug discovery. J Cheminform. 2020;12(1):9. 

4. Li H, Nantasenamat C. Toward insights on determining factors for high activity in antimicrobial peptides via machine learning. PeerJ. 2019;7:e8265.

5. Suvannang N, Preeyanon L, Malik AA, Schaduangrat N, Shoombuatong W, Worachartcheewan A, Tantimongcolwat T, Nantasenamat C. Probing the origin of estrogen receptor alpha inhibition via large-scale QSAR study. RSC Adv. 2018;8(21):11344-11356.
"""
)
