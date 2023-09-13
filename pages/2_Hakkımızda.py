import streamlit as st

st.set_page_config(page_title="Hakkımızda", page_icon="images/icon.png")
st.image("images/merge.png", use_column_width=True)


# Kişi bilgileri
kisiler = [
    {
        "ad": "**Ece Titiz**",
        "aciklama": "Penguyen sever, kurbağa sevmez, veri bilemeyici.",
        "resim_linki": "images/ece_pp.png",
    },
    {
        "ad": "**Oğuzhan Arı**",
        "aciklama": "Veteran kedi sever, kısmi zamanlı kahve bağımlısı, tam zamansız veri bilimci.",
        "resim_linki": "images/oguzhan_ari_pp.png",
    },
    {
        "ad": "**Tuğba Aktaş**",
        "aciklama": "%99 GYM, %1 Aslan burcu, %100 veri bilimci.",
        "resim_linki": "images/tugba_pp.png",
    },
    {
        "ad": "**Elmira Kaya**",
        "aciklama": "Atanamamış influencer.",
        "resim_linki": "images/elmira.png",
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
    empty_1, col1, col2, empty_2 = st.columns([1, 1.2, 1.5, 0.75])
    with col1:
        st.image(kisi["resim_linki"], width=100)
    with col2:
        st.subheader(f"**{kisi['ad']}**")
        st.write(kisi["aciklama"])


st.caption(
    """
                <p style='text-align: center;'><font size="2">Miuuxi maded with ❤️</font>

                </p>
            """,
    unsafe_allow_html=True,
)

with st.columns(9)[4]:
    st.image("images/icon.png", width=50)

if st.button(" "):
    st.image("images/common_pic.png")
