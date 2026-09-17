import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Çanakkale Ulaşım Rehberi",
    page_icon="🚌",
    layout="centered"
)

# Başlık
st.markdown("<h2 style='text-align: center; color: #2563eb;'>🚌 Çanakkale Merkez Ulaşım Asistanı</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; font-size: 13px;'>Tüm merkez hatları, kampüs seferleri ve durak takip sistemi</p>", unsafe_allow_html=True)

st.divider()

# Sekmeler: 1. Rota Bulucu (Nereye Nereden?), 2. Tüm Hatlar Rehberi
tab1, tab2 = st.tabs(["📍 Rota Bulucu & Durak Takibi", "📋 Tüm Hatlar Listesi"])

# --- TAB 1: ROTA BULUCU ---
with tab1:
    st.markdown("### Nereye gitmek istiyorsun?")
    
    # Çanakkale Merkez Önemli Durak / Noktaları
    locations = [
        "İskele Meydanı", 
        "Terzioğlu Kampüsü (Ana Kapı)", 
        "ÇOMÜ Araştırma Hastanesi", 
        "Çarşı / Truva Atı", 
        "Çanakkale Otogar", 
        "17 Burda AVM", 
        "Esenler / Demircioğlu", 
        "Nusrat Yurdu / KYK",
        "Halk Bahçesi"
    ]

    col1, col2 = st.columns(2)
    with col1:
        origin = st.selectbox("Neredesin?", locations, index=0)
    with col2:
        destination = st.selectbox("Nereye gideceksin?", locations, index=1)

    # Kapsamlı Rota Veritabanı Simülasyonu
    routes_db = {
        ("İskele Meydanı", "Terzioğlu Kampüsü (Ana Kapı)"): {
            "line": "Ç-1 / Ç-3 (Mavi / Kırmızı)",
            "name": "İskele ➔ Terzioğlu Kampüsü",
            "stops": ["İskele Meydanı", "Çarşı", "Demircioğlu Caddesi", "Eski Devlet Hastanesi", "KYK Yurtlar", "Terzioğlu Kampüsü (Ana Kapı)"],
            "remaining": 3,
            "time": "12 dk",
            "next": "3 dk sonra"
        },
        ("Terzioğlu Kampüsü (Ana Kapı)", "İskele Meydanı"): {
            "line": "Ç-1 / Ç-3 (Mavi / Kırmızı)",
            "name": "Terzioğlu Kampüsü ➔ İskele",
            "stops": ["Terzioğlu Kampüsü (Ana Kapı)", "KYK Yurtlar", "Eski Devlet Hastanesi", "Çarşı", "İskele Meydanı"],
            "remaining": 2,
            "time": "10 dk",
            "next": "5 dk sonra"
        },
        ("İskele Meydanı", "Çanakkale Otogar"): {
            "line": "Ç-4 / Ç-9",
            "name": "İskele ➔ Yeni Otogar",
            "stops": ["İskele Meydanı", "Çarşı", "Dörtyol", "Pirireis Caddesi", "Çanakkale Otogar"],
            "remaining": 4,
            "time": "18 dk",
            "next": "7 dk sonra"
        },
        ("Çanakkale Otogar", "İskele Meydanı"): {
            "line": "Ç-4 / Ç-9",
            "name": "Yeni Otogar ➔ İskele",
            "stops": ["Çanakkale Otogar", "Pirireis Caddesi", "Dörtyol", "Çarşı", "İskele Meydanı"],
            "remaining": 3,
            "time": "15 dk",
            "next": "10 dk sonra"
        },
        ("İskele Meydanı", "17 Burda AVM"): {
            "line": "Ç-3 / ÇT-3",
            "name": "İskele ➔ 17 Burda AVM",
            "stops": ["İskele Meydanı", "Çarşı", "Troya Caddesi", "Gazi Meclisi", "17 Burda AVM"],
            "remaining": 3,
            "time": "14 dk",
            "next": "4 dk sonra"
        },
        ("Terzioğlu Kampüsü (Ana Kapı)", "ÇOMÜ Araştırma Hastanesi"): {
            "line": "ÇT-1 / ÇT-3",
            "name": "Kampüs ➔ Araştırma Hastanesi",
            "stops": ["Terzioğlu Kampüsü (Ana Kapı)", "Teknik Bilimler MYO", "Yeni Adliye", "ÇOMÜ Araştırma Hastanesi"],
            "remaining": 1,
            "time": "5 dk",
            "next": "2 dk sonra"
        }
    }

    if st.button("En Uygun Otobüsü ve Durakları Göster", use_container_width=True):
        if origin == destination:
            st.warning("⚠️ Bulunduğun yer ile gideceğin yer aynı olamaz!")
        else:
            # Doğrudan eşleşme arama
            route_key = (origin, destination)
            data = routes_db.get(route_key)
            
            # Ters eşleşme veya genel mantık üretme
            if not data:
                # Varsayılan akıllı aktarmalı / standart şablon
                data = {
                    "line": "Ç-Genel Merkez Hattı",
                    "name": f"{origin} ➔ {destination}",
                    "stops": [origin, "Merkez Durak / Çarşı", "Aktarma Noktası", destination],
                    "remaining": 2,
                    "time": "15-20 dk",
                    "next": "6 dk sonra"
                }

            st.success(f"Önerilen Hat: **{data['line']}**")
            
            m1, m2 = st.columns(2)
            with m1:
                st.metric(label="Kalan Durak", value=f"{data['remaining']} Durak")
            with m2:
                st.metric(label="Tahmini Süre", value=data['time'])
                
            st.info(f"⏰ Sıradaki Sefer: **{data['next']}**")
            
            st.markdown("#### 📍 Canlı Güzergah İlerlemesi")
            for i, stop in enumerate(data["stops"]):
                is_current = i == (len(data["stops"]) - data["remaining"])
                if is_current:
                    st.markdown(f"- **📍 {stop} (Otobüs Şuan Burada!)**")
                elif i < (len(data["stops"]) - data["remaining"]):
                    st.markdown(f"- ~~{stop}~~ *(Geçildi)*")
                else:
                    st.markdown(f"- {stop}")

# --- TAB 2: TÜM HATLAR REHBERİ ---
with tab2:
    st.markdown("### 📋 Çanakkale Merkez Hat Listesi")
    
    lines_info = {
        "Ç-1 / Ç-2 (Mavi Hat)": "Esenler - Terzioğlu Kampüsü - İskele - Gazi Meclisi",
        "Ç-3 (Kırmızı Hat)": "Esenler - Terzioğlu Kampüsü - İskele - SSK İstasyon",
        "Ç-4": "İskele - Çarşı - Salı Pazarı - Yeni Otogar",
        "Ç-7": "Park 17 Evleri - Plaj Yolu - Esenler",
        "Ç-8": "Nusrat Yurdu - Havaalanı - Üniversite",
        "Ç-10": "Nusrat Öğrenci Yurdu - Terzioğlu Kampüsü",
        "ÇT-1 / ÇT-3": "Araştırma Hastanesi - İskele - Troya Caddesi - Kampüs",
    }

    for line_code, desc in lines_info.items():
        with st.expander(line_code):
            st.write(f"**Güzergah Özeti:** {desc}")
            st.write("Durum: Aktif Seferde ✅")

st.divider()
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 11px;'>Çanakkale Toplu Taşıma Bilgi Ağı</p>", unsafe_allow_html=True)
