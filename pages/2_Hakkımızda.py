import streamlit as st

st.set_page_config(page_title="Hakkımızda", page_icon="images/icon.png")
st.image("images/merge.png", use_column_width=True)


# Kişi bilgileri
kisiler = [
    {"ad": "Ece Titiz", "aciklama": "kisi bilgisi", "resim_linki": "images/ece_pp.png"},
    {
        "ad": "Oğuzhan Arı",
        "aciklama": "kisi bilgisi",
        "resim_linki": "images/oguzhan_ari_pp.png",
    },
    {
        "ad": "Tuğba Aktaş",
        "aciklama": "kisi bilgisi",
        "resim_linki": "images/tugba_pp.png",
    },
    {
        "ad": "Elmira Kaya",
        "aciklama": "kisi bilgisi",
        "resim_linki": "images/oguzhan_ari_pp.png",
    },
]

title_alignment = """
        <style>
        #the-title {
          text-align: center
        }
        </style>
        """
st.markdown(title_alignment, unsafe_allow_html=True)

for kisi in kisiler:
    col1, col2 = st.columns(2)
    with col1:
        st.image(kisi["resim_linki"], caption=kisi["ad"], width=150)
    with col2:
        st.write(f"**{kisi['ad']}**")
        st.write(kisi["aciklama"])
