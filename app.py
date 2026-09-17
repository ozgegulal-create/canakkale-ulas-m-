import streamlit as st
import urllib.parse

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Çanakkale Merkez Ulaşım Rehberi",
    page_icon="🚌",
    layout="centered"
)

# Başlık
st.markdown("<h2 style='text-align: center; color: #2563eb;'>🚌 Çanakkale Merkez Ulaşım Asistanı</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; font-size: 13px;'>Canlı durak takip paneli, otobüs varış süreleri ve Google Maps yürüyüş rotaları</p>", unsafe_allow_html=True)

st.divider()

# Sekmeler
tab1, tab2, tab3 = st.tabs(["⏱️ Canlı Durak & Sefer Saati", "📍 Akıllı Rota & Harita", "📋 Tüm Hatlar ve Duraklar"])

# --- TAB 1: CANLI DURAK VE SEFER BEKLEME PANELI ---
with tab1:
    st.markdown("### 🚏 Durakta Bekleme ve Sefer Takibi")
    st.markdown("Bulunduğunuz durağı seçerek yaklaşan otobüsleri ve tahmini varış sürelerini görün:")

    # Sık kullanılan ana merkez durakları
    popular_stops = [
        "İskele Meydanı",
        "Çarşı / Truva Atı",
        "Demircioğlu Caddesi",
        "Eski Devlet Hastanesi",
        "ÇOMÜ Terzioğlu Kampüsü (Ana Kapı)",
        "ÇOMÜ Araştırma Hastanesi",
        "17 Burda AVM",
        "Esenler Mahallesi (Son Durak)",
        "Çanakkale Yeni Otogar",
        "Park 17 Evleri / 960 Toki"
    ]

    selected_stop = st.selectbox("Beklediğiniz Durağı Seçin:", popular_stops)

    st.markdown("---")
    st.markdown(f"#### 🚌 `{selected_stop}` Durağına Yaklaşan Hatlar")

    # Duraklara göre simüle edilmiş canlı varış süreleri veritabanı
    stop_live_data = {
        "İskele Meydanı": [
            {"line": "Ç-1 Mavi Hat (Kampüs)", "time": "3 dk sonra", "stops_left": 1, "status": "Yaklaşıyor 🟢"},
            {"line": "Ç-3 Kırmızı Hat (Esenler)", "time": "7 dk sonra", "stops_left": 3, "status": "Normal 🔵"},
            {"line": "Ç-4 (Yeni Otogar)", "time": "12 dk sonra", "stops_left": 5, "status": "Yolda 🔵"},
            {"line": "Ç960 (Nusrat Yurdu)", "time": "15 dk sonra", "stops_left": 6, "status": "Normal 🔵"}
        ],
        "Çarşı / Truva Atı": [
            {"line": "Ç-1 Mavi Hat (Kampüs)", "time": "2 dk sonra", "stops_left": 1, "status": "Yaklaşıyor 🟢"},
            {"line": "Ç-3 Kırmızı Hat (AVM)", "time": "5 dk sonra", "stops_left": 2, "status": "Normal 🔵"},
            {"line": "Ç-10 (Kampüs Ring)", "time": "9 dk sonra", "stops_left": 4, "status": "Yolda 🔵"}
        ],
        "Demircioğlu Caddesi": [
            {"line": "Ç-1 Mavi Hat (Esenler)", "time": "4 dk sonra", "stops_left": 2, "status": "Normal 🔵"},
            {"line": "Ç-4 (Otogar)", "time": "6 dk sonra", "stops_left": 3, "status": "Normal 🔵"},
            {"line": "Ç-10 (Nusrat Yurdu)", "time": "11 dk sonra", "stops_left": 5, "status": "Yolda 🔵"}
        ],
        "Eski Devlet Hastanesi": [
            {"line": "Ç-1 Mavi Hat (Kampüs)", "time": "5 dk sonra", "stops_left": 2, "status": "Normal 🔵"},
            {"line": "Ç-2 Mavi Hat (İskele)", "time": "8 dk sonra", "stops_left": 3, "status": "Normal 🔵"},
            {"line": "Ç-11 (Kordon-Hastane)", "time": "14 dk sonra", "stops_left": 6, "status": "Yolda 🔵"}
        ],
        "ÇOMÜ Terzioğlu Kampüsü (Ana Kapı)": [
            {"line": "Ç-1 Mavi Hat (İskele/Esenler)", "time": "2 dk sonra", "stops_left": 1, "status": "Yaklaşıyor 🟢"},
            {"line": "Ç-3 Kırmızı Hat (AVM)", "time": "6 dk sonra", "stops_left": 3, "status": "Normal 🔵"},
            {"line": "ÇT-1 (Araştırma Hastanesi)", "time": "10 dk sonra", "stops_left": 4, "status": "Yolda 🔵"},
            {"line": "Ç-8 (Nusrat Yurdu)", "time": "15 dk sonra", "stops_left": 7, "status": "Normal 🔵"}
        ],
        "ÇOMÜ Araştırma Hastanesi": [
            {"line": "ÇT-1 / ÇT-3 (Kampüs-İskele)", "time": "4 dk sonra", "stops_left": 1, "status": "Yaklaşıyor 🟢"},
            {"line": "Ç960 (Park 17)", "time": "10 dk sonra", "stops_left": 4, "status": "Normal 🔵"}
        ],
        "17 Burda AVM": [
            {"line": "Ç-3 Kırmızı Hat", "time": "3 dk sonra", "stops_left": 1, "status": "Yaklaşıyor 🟢"},
            {"line": "Ç960", "time": "8 dk sonra", "stops_left": 3, "status": "Normal 🔵"},
            {"line": "ÇT-3 (Kampüs)", "time": "12 dk sonra", "stops_left": 5, "status": "Yolda 🔵"}
        ],
        "Esenler Mahallesi (Son Durak)": [
            {"line": "Ç-1 Mavi Hat (Kampüs)", "time": "1 dk sonra", "stops_left": 0, "status": "Kalkış Noktasında 🟢"},
            {"line": "Ç-3 Kırmızı Hat (AVM)", "time": "7 dk sonra", "stops_left": 2, "status": "Normal 🔵"}
        ],
        "Çanakkale Yeni Otogar": [
            {"line": "Ç-4 (İskele Meydanı)", "time": "5 dk sonra", "stops_left": 1, "status": "Yaklaşıyor 🟢"},
            {"line": "Ç-5 (Devlet Hastanesi)", "time": "12 dk sonra", "stops_left": 4, "status": "Normal 🔵"}
        ],
        "Park 17 Evleri / 960 Toki": [
            {"line": "Ç960 (Merkez-Belediye)", "time": "4 dk sonra", "stops_left": 1, "status": "Yaklaşıyor 🟢"},
            {"line": "Ç-7 (Plaj Yolu-Barbaros)", "time": "9 dk sonra", "stops_left": 3, "status": "Normal 🔵"}
        ]
    }

    current_buses = stop_live_data.get(selected_stop, [
        {"line": "Merkez Hatları", "time": "5-10 dk sonra", "stops_left": 2, "status": "Normal 🔵"}
    ])

    for bus in current_buses:
        st.markdown(
            f"""
            <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; padding: 12px 16px; border-radius: 12px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>{bus['line']}</strong><br>
                    <span style="font-size: 12px; color: #64748b;">Kalan Durak: <b>{bus['stops_left']} Durak</b> | Durum: {bus['status']}</span>
                </div>
                <div style="background-color: #dbeafe; color: #1e40af; padding: 6px 12px; border-radius: 8px; font-weight: bold; font-size: 14px;">
                    {bus['time']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# --- TAB 2: AKILLI ROTA VE GOOGLE MAPS ENTEGRASYONU ---
with tab2:
    st.markdown("### 🗺️ Nereden Nereye Gideceksiniz?")
    
    origin_input = st.text_input("Kalkış Yeri (Neredesiniz?)", placeholder="Örn: Esenler, İskele, 960 Toki, Barbaros...")
    destination_input = st.text_input("Varış Yeri (Nereye gideceksiniz?)", placeholder="Örn: Çanakkale Belediyesi, Araştırma Hastanesi, Çarşı...")

    if st.button("Rotayı ve Haritayı Hesapla", use_container_width=True):
        if not origin_input or not destination_input:
            st.warning("⚠️ Lütfen hem kalkış hem de varış yerini yazın!")
        else:
            dest_lower = destination_input.lower()
            
            nearest_stop = "İskele Meydanı / Merkez Duraklar"
            line_suggestion = "Ç-1 / Ç-3 / Ç-11 / Ç960"
            
            if "belediye" in dest_lower:
                nearest_stop = "İskele Meydanı Durağı"
                line_suggestion = "Ç-1 / Ç-3 / Ç960 / Ç-11 (Sahil Güzergahı)"
            elif "hastane" in dest_lower:
                nearest_stop = "ÇOMÜ Araştırma Hastanesi / Devlet Hastanesi"
                line_suggestion = "ÇT-1 / ÇT-3 / Ç960 / Ç-5"
            elif "çarşı" in dest_lower or "aynalı" in dest_lower:
                nearest_stop = "Çarşı / Truva Atı Durağı"
                line_suggestion = "Ç-1 / Ç-4 / Ç-10 / Ç960"
            elif "kampüs" in dest_lower or "üniversite" in dest_lower:
                nearest_stop = "Terzioğlu Kampüsü Ana Kapı Durağı"
                line_suggestion = "Ç-1 / Ç-3 / Ç-8 / Ç-10 / ÇT-3"
            elif "avm" in dest_lower or "17 burda" in dest_lower:
                nearest_stop = "17 Burda AVM Önü Durağı"
                line_suggestion = "Ç-3 / Ç-11 / Ç960 / ÇT-3"
            elif "barbaros" in dest_lower or "plaj" in dest_lower:
                nearest_stop = "Barbaros / Plaj Yolu Durakları"
                line_suggestion = "Ç-7 / Ç960"

            st.success(f"🎯 Hedef: **{destination_input.title()}**")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Önerilen En Yakın Durak", value=nearest_stop)
            with col2:
                st.metric(label="Tavsiye Edilen Hatlar", value=line_suggestion)
            
            # Google Maps Entegrasyonu
            maps_query = urllib.parse.quote(f"{destination_input} Çanakkale")
            maps_url = f"https://www.google.com/maps/search/?api=1&query={maps_query}"
            
            st.markdown("---")
            st.markdown("#### 🚶‍♂️ Google Maps ile Yürüyüş ve Yol Tarifi")
            st.markdown(f"İneceğiniz duraktan (`{nearest_stop}`) hedefinize (`{destination_input.title()}`) yürüyüş rotasını haritada açmak için aşağıdaki butona tıklayabilirsiniz:")
            
            st.markdown(
                f"""
                <a href="{maps_url}" target="_blank">
                    <div style="background-color: #2563eb; color: white; padding: 12px 20px; border-radius: 12px; text-align: center; font-weight: bold; text-decoration: none; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        🗺️ Google Maps'te Yürüyüş Rotasını Aç
                    </div>
                </a>
                """, 
                unsafe_allow_html=True
            )

# --- TAB 3: ÇANAKKALE MERKEZ TÜM HATLAR VE DURAKLARI ---
with tab3:
    st.markdown("### 📋 Çanakkale Merkez Tüm Hatlar ve Durak Listesi")
    st.markdown("Çanakkale merkezde hizmet veren tüm otobüs hatlarının tam durak sıralamaları:")

    all_central_lines = {
        "Ç-1 Mavi Hat (Esenler - Kampüs - İskele)": [
            "Esenler Mahallesi (Son Durak)", "Atatürk Caddesi", "Demircioğlu Caddesi", 
            "Çarşı", "İskele Meydanı", "Eski Devlet Hastanesi", "KYK Yurtlar", "ÇOMÜ Terzioğlu Kampüsü"
        ],
        "Ç-2 Mavi Hat (Kampüs - Esenler Dönüş)": [
            "ÇOMÜ Terzioğlu Kampüsü", "KYK Yurtlar", "Eski Devlet Hastanesi", 
            "İskele Meydanı", "Çarşı", "Demircioğlu Caddesi", "Atatürk Caddesi", "Esenler Mahallesi"
        ],
        "Ç-3 Kırmızı Hat (Esenler - AVM - İskele)": [
            "Esenler Mahallesi", "Troya Caddesi", "17 Burda AVM", 
            "SSK İstasyon", "İskele Meydanı", "Çarşı"
        ],
        "Ç-4 Hatı (İskele - Yeni Otogar)": [
            "İskele Meydanı", "Çarşı", "Demircioğlu Caddesi", 
            "Salı Pazarı", "Pirireis Caddesi", "Çanakkale Yeni Otogar"
        ],
        "Ç-5 Hattı (Otogar - Devlet Hastanesi)": [
            "Çanakkale Yeni Otogar", "Salı Pazarı", "Demircioğlu", 
            "Çarşı", "İskele Meydanı", "Devlet Hastanesi"
        ],
        "Ç-7 Hattı (Park 17 - Plaj Yolu - Barbaros - Esenler)": [
            "Park 17 Evleri", "Plaj Yolu Caddesi", "Barbaros Mahallesi", "Esenler Mahallesi"
        ],
        "Ç-8 Hattı (Nusrat Yurdu - Üniversite)": [
            "Nusrat Öğrenci Yurdu", "Havaalanı Kavşağı", "Troya Caddesi", "ÇOMÜ Terzioğlu Kampüsü"
        ],
        "Ç-10 Hattı (Nusrat Yurdu - Kampüs Ring)": [
            "Nusrat Öğrenci Yurdu", "Demircioğlu Caddesi", "Çarşı", "ÇOMÜ Terzioğlu Kampüsü"
        ],
        "Ç-11 Hattı (Esenler - Kordon - Hastane Ring)": [
            "Esenler Mahallesi", "Gazi Caddesi", "İskele Meydanı (Kordon)", 
            "Eski Devlet Hastanesi", "Yeni Devlet Hastanesi"
        ],
        "Ç960 (Park 17 - Devlet Hastanesi - Belediye - Nusrat Yurdu)": [
            "Park 17 Evleri", "Star Life Sitesi", "Oğuzkent", "Bahçeşehir Sitesi", 
            "Medigarden", "Devlet Hastanesi / Yeni Hastane", "İmam Hatip Lisesi", 
            "960 Askeri Lojmanlar", "Rauf Denktaş Caddesi", "960 TOKİ", 
            "17 Burda AVM", "Barbaros Mahallesi / Yeni Kordon", "İbrahim Bodur Lisesi", 
            "Cuma Pazarı", "Belediye / İskele Meydanı", "Nusrat Yurdu"
        ],
        "ÇT-1 / ÇT-3 Hattı (Hastane - Kampüs Ring)": [
            "ÇOMÜ Araştırma Hastanesi", "Yeni Adliye", "Teknik Bilimler MYO", 
            "ÇOMÜ Terzioğlu Kampüsü", "Troya Caddesi", "İskele Meydanı"
        ]
    }

    for line_name, stops in all_central_lines.items():
        with st.expander(line_name):
            st.markdown(f"**Güzergah Durak Sıralaması:**")
            for index, stop in enumerate(stops, 1):
                st.markdown(f"{index}. 🚏 {stop}")

st.divider()
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 11px;'>Çanakkale Merkez Toplu Taşıma Bilgi Ağı</p>", unsafe_allow_html=True)
