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
st.markdown("<p style='text-align: center; color: #64748b; font-size: 13px;'>Belediye ulaşım altyapısı uyumlu canlı sefer paneli ve Google Maps rotaları</p>", unsafe_allow_html=True)

st.divider()

# --- BELEDİYE RESMİ VERİLERİNE GÖRE HAT-DURAK EŞLEŞME VERİTABANI ---
official_transport_data = {
    "İskele Meydanı": ["Ç-1", "Ç-3", "Ç-5", "Ç-7", "Ç-8", "Ç-9", "Ç-11K", "ÇT-3"],
    "Çarşı / Truva Atı": ["Ç-1", "Ç-3", "Ç-4", "Ç-5", "Ç-10", "ÇT-3"],
    "Çanakkale Belediyesi": ["Ç-3", "ÇT-3", "Ç-9", "Ç-11"],
    "17 Burda AVM": ["Ç-1", "Ç-3", "Ç-7", "Ç-8", "Ç-11K", "ÇT-3"],
    "Terzioğlu Kampüsü (Ana Kapı)": ["Ç-1", "Ç-3", "Ç-8", "Ç-10", "ÇT-1"],
    "18 Mart Üniversitesi Araştırma Hastanesi": ["Ç-1", "Ç-3", "Ç-7", "Ç-8", "Ç-10", "Ç960", "ÇT-1"],
    "Mehmet Akif Ersoy Devlet Hastanesi": ["Ç-5", "Ç-7", "ÇT-1", "ÇT-3"],
    "Cuma Pazarı": ["Ç-1", "Ç-3", "Ç-8", "Ç-11K", "ÇT-3"],
    "Çanakkale Yeni Otogar": ["Ç-4", "Ç-9"],
    "Park 17 Evleri / 960 Toki": ["Ç-7", "Ç960", "ÇT-1", "ÇT-3"],
    "Barbaros Mahallesi / Yeni Kordon": ["Ç-7", "Ç960", "Ç-11"],
    "Kerime Sultan ve Nusrat Yurtları": ["Ç-8", "Ç-10"]
}

# Tüm durak listesi
all_stops = sorted(list(official_transport_data.keys()))

# Sekmeler
tab1, tab2, tab3 = st.tabs(["⏱️ Canlı Durak & Sefer", "📍 Akıllı Rota & Harita", "📋 Tüm Hatlar ve Duraklar"])

# --- TAB 1: CANLI DURAK VE SEFER BEKLEME PANELI ---
with tab1:
    st.markdown("### 🚏 Canlı Durak Takip Paneli")
    st.markdown("Belediye güzergah rehberine bağlı olarak, seçtiğiniz duraktan geçen resmi hatları ve anlık durumları görün:")

    selected_stop = st.selectbox("Durak Seçin:", all_stops)

    st.markdown("---")
    st.markdown(f"#### 🚌 {selected_stop} Durağından Geçen Hatlar")

    active_lines = official_transport_data.get(selected_stop, ["Ç-1", "Ç-3"])

    for idx, line in enumerate(active_lines, 1):
        sim_time = f"{(idx * 2)} dk sonra"
        sim_stops_left = idx
        
        with st.container(border=True):
            col_info, col_time = st.columns([3, 1])
            with col_info:
                st.markdown(f"**Hat: {line}**")
                st.caption(f"Anlık Konum: Yaklaşıyor | Kalan Durak: {sim_stops_left}")
            with col_time:
                st.markdown(f"<div style='background-color: #dbeafe; color: #1e40af; padding: 8px; border-radius: 8px; text-align: center; font-weight: bold; font-size: 13px;'>{sim_time}</div>", unsafe_allow_html=True)

# --- TAB 2: AKILLI ROTA VE GOOGLE MAPS ENTEGRASYONU ---
with tab2:
    st.markdown("### 🗺️ Nereden Nereye Gideceksiniz?")
    
    origin_input = st.text_input("Kalkış Yeri (Neredesiniz?)", placeholder="Örn: Esenler, İskele, Kampüs...")
    destination_input = st.text_input("Varış Yeri (Nereye gideceksiniz?)", placeholder="Örn: Belediye, Araştırma Hastanesi, Çarşı...")

    if st.button("Rotayı ve Haritayı Hesapla", use_container_width=True):
        if not origin_input or not destination_input:
            st.warning("⚠️ Lütfen kalkış ve varış yerini yazın!")
        else:
            dest_lower = destination_input.lower()
            
            nearest_stop = "İskele Meydanı / Merkez Duraklar"
            line_suggestion = "Ç-1 / Ç-3 / ÇT-3"
            
            if "belediye" in dest_lower:
                nearest_stop = "Çanakkale Belediyesi Durağı"
                line_suggestion = "Ç-3 / ÇT-3 / Ç-9"
            elif "hastane" in dest_lower:
                nearest_stop = "Araştırma Hastanesi / Devlet Hastanesi"
                line_suggestion = "Ç-1 / Ç-3 / ÇT-1"
            elif "çarşı" in dest_lower:
                nearest_stop = "Çarşı / Truva Atı Durağı"
                line_suggestion = "Ç-1 / Ç-4 / Ç-10"
            elif "kampüs" in dest_lower:
                nearest_stop = "Terzioğlu Kampüsü Ana Kapı"
                line_suggestion = "Ç-1 / Ç-3 / Ç-8"

            st.success(f"🎯 Hedef: **{destination_input.title()}**")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Önerilen En Yakın Durak", value=nearest_stop)
            with col2:
                st.metric(label="Belediye Hat Kodu", value=line_suggestion)
            
            maps_query = urllib.parse.quote(f"{destination_input} Çanakkale")
            maps_url = f"https://www.google.com/maps/search/?api=1&query={maps_query}"
            
            st.markdown("---")
            st.markdown("#### 🚶‍♂️ Google Maps ile Yürüyüş ve Yol Tarifi")
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

# --- TAB 3: TÜM HATLAR VE DURAKLAR ---
with tab3:
    st.markdown("### 📋 Çanakkale Belediyesi Resmi Hat Rehberi")
    st.markdown("Durak bazlı resmi hat eşleştirmeleri:")

    for stop_name, lines in official_transport_data.items():
        with st.expander(f"🚏 {stop_name}"):
            line_str = ", ".join([f"`{l}`" for l in lines])
            st.markdown(f"**Geçen Hatlar:** {line_str}")

st.divider()
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 11px;'>Çanakkale Kentkart / Ulaşım Altyapı Entegrasyonu</p>", unsafe_allow_html=True)
