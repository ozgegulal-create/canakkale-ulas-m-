import streamlit as st

# Sayfa Yapılandırması (Mobil uyumlu görünüm için)
st.set_page_config(
    page_title="Çanakkale Ulaşım Asistanı",
    page_icon="🚌",
    layout="centered"
)

# Mobil dostu şık bir başlık
st.markdown("<h2 style='text-align: center; color: #2563eb;'>🚌 Çanakkale Ulaşım Asistanı</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; font-size: 14px;'>Nereye gideceğini seç, otobüsünü ve kalan durakları anında gör.</p>", unsafe_allow_html=True)

st.divider()

# Rota Veritabanı Simülasyonu
routes = {
    "İskele Meydanı ➔ Terzioğlu Kampüsü": {
        "line": "Hat Ç-1",
        "stops": ["İskele Meydanı", "Çarşı", "Eski Devlet Hastanesi", "KYK Yurtlar", "Kampüs Girişi"],
        "remaining": 3,
        "time": "12 dk",
        "next": "4 dk sonra"
    },
    "Terzioğlu Kampüsü ➔ İskele Meydanı": {
        "line": "Hat Ç-1",
        "stops": ["Kampüs Girişi", "KYK Yurtlar", "Eski Devlet Hastanesi", "Çarşı", "İskele Meydanı"],
        "remaining": 2,
        "time": "10 dk",
        "next": "2 dk sonra"
    },
    "İskele Meydanı ➔ Çanakkale Otogar": {
        "line": "Hat Ç-4",
        "stops": ["İskele Meydanı", "Çarşı", "Demircioğlu", "Kipa AVM", "Otogar"],
        "remaining": 4,
        "time": "18 dk",
        "next": "8 dk sonra"
    },
    "Çanakkale Otogar ➔ İskele Meydanı": {
        "line": "Hat Ç-4",
        "stops": ["Otogar", "Kipa AVM", "Demircioğlu", "Çarşı", "İskele Meydanı"],
        "remaining": 3,
        "time": "15 dk",
        "next": "6 dk sonra"
    }
}

# Arayüz Seçimleri
col1, col2 = st.columns(2)

with col1:
    origin = st.selectbox("Neredesin?", ["İskele Meydanı", "Terzioğlu Kampüsü", "Çanakkale Otogar"])

with col2:
    destination = st.selectbox("Nereye gideceksin?", ["Terzioğlu Kampüsü", "İskele Meydanı", "Çanakkale Otogar"])

route_key = f"{origin} ➔ {destination}"

if st.button("Otobüsü ve Durakları Göster", use_container_width=True):
    if origin == destination:
        st.warning("⚠️ Bulunduğun yer ile gideceğin yer aynı olamaz!")
    elif route_key in routes:
        data = routes[route_key]
        
        st.success(f"**{data['line']}** bulundu!")
        
        # Bilgi Kartları
        m1, m2 = st.columns(2)
        with m1:
            st.metric(label="Kalan Durak", value=f"{data['remaining']} Durak")
        with m2:
            st.metric(label="Tahmini Süre", value=data['time'])
            
        st.info(f"⏰ Sonraki Sefer: **{data['next']}**")
        
        st.markdown("### 📍 Güzergah Durumu")
        for i, stop in enumerate(data["stops"]):
            is_current = i == (len(data["stops"]) - data["remaining"])
            if is_current:
                st.markdown(f"- **📍 {stop} (Otobüs Burada!)**")
            elif i < (len(data["stops"]) - data["remaining"]):
                st.markdown(f"- ~~{stop}~~ *(Geçildi)*")
            else:
                st.markdown(f"- {stop}")
    else:
        st.error("Bu güzergah için doğrudan hat bulunamadı. Merkez aktarmalı gidebilirsiniz.")

st.divider()
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 12px;'>Çanakkale Mobil Ulaşım Projesi</p>", unsafe_allow_html=True)
