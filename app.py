import streamlit as st
import urllib.parse

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Çanakkale & Kepez Akıllı Ulaşım",
    page_icon="🚌",
    layout="centered"
)

# Başlık
st.markdown("<h2 style='text-align: center; color: #2563eb;'>🚌 Çanakkale & Kepez Akıllı Ulaşım Asistanı</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; font-size: 13px;'>Tüm hatlar, durak listeleri ve Google Maps destekli yürüyüş rotaları</p>", unsafe_allow_html=True)

st.divider()

# Sekmeler
tab1, tab2 = st.tabs(["📍 Rota & Google Maps Rehberi", "📋 Tüm Hatlar ve Duraklar"])

# --- TAB 1: ROTA VE GOOGLE MAPS ENTEGRASYONU ---
with tab1:
    st.markdown("### 🗺️ Nereden Nereye Gideceksiniz?")
    
    origin_input = st.text_input("Kalkış Yeri (Neredesiniz?)", placeholder="Örn: Kepez Toki, Kepez Sahil, İskele...")
    destination_input = st.text_input("Varış Yeri (Nereye gideceksiniz?)", placeholder="Örn: Çanakkale Belediyesi, Araştırma Hastanesi, Çarşı...")

    if st.button("Rotayı ve Haritayı Hesapla", use_container_width=True):
        if not origin_input or not destination_input:
            st.warning("⚠️ Lütfen hem nereden hem nereye gideceğinizi yazın!")
        else:
            dest_lower = destination_input.lower()
            
            # Akıllı Durak ve Hat Eşleştirmesi
            nearest_stop = "İskele Meydanı / Merkez Duraklar"
            line_suggestion = "Kepez - Merkez Hatları / Ç-1"
            
            if "belediye" in dest_lower:
                nearest_stop = "İskele Meydanı Durağı"
                line_suggestion = "Kepez - Merkez Sahil Hattı"
            elif "hastane" in dest_lower:
                nearest_stop = "ÇOMÜ Araştırma Hastanesi Durağı"
                line_suggestion = "Kepez - Üniversite / Hastane Hattı"
            elif "çarşı" in dest_lower or "aynalı" in dest_lower:
                nearest_stop = "Çarşı / Truva Atı Durağı"
                line_suggestion = "Kepez - Çarşı Hatları (Ç-4)"
            elif "kampüs" in dest_lower or "üniversite" in dest_lower:
                nearest_stop = "Terzioğlu Kampüsü Ana Kapı Durağı"
                line_suggestion = "Kepez - Kampüs Direkt Hattı"
            elif "avm" in dest_lower or "17 burda" in dest_lower:
                nearest_stop = "17 Burda AVM Önü Durağı"
                line_suggestion = "Ç-3 / Kepez Ringleri"

            st.success(f"🎯 Hedef: **{destination_input.title()}**")
            
            # Bilgi Kartları
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Önerilen En Yakın Durak", value=nearest_stop)
            with col2:
                st.metric(label="Tavsiye Edilen Hat", value=line_suggestion)
            
            # Google Maps Entegrasyonu (Yürüyüş ve Konum Linki Oluşturma)
            # Kullanıcının ineceği duraktan hedefine Google Maps üzerinden yürüyüş rotası açar
            maps_query = urllib.parse.quote(f"{destination_input} Çanakkale")
            maps_url = f"https://www.google.com/maps/search/?api=1&query={maps_query}"
            
            st.markdown("---")
            st.markdown("#### 🚶‍♂️ Google Maps ile Yürüyüş ve Yol Tarifi")
            st.markdown(f"İneceğiniz duraktan (`{nearest_stop}`) hedefinize (`{destination_input.title()}`) yürüyüş rotasını görmek için aşağıdaki butona tıklayabilirsiniz:")
            
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

# --- TAB 2: TÜM HATLAR VE TEK TEK DURAKLARI ---
with tab2:
    st.markdown("### 📋 Çanakkale & Kepez Tüm Hatlar ve Durak Listesi")
    st.markdown("Annenlerin ve senin sık kullanacağı tüm hatların güzergahları ve durakları:")

    # Kepez ve Merkez Hatlarının Detaylı Durak Listeleri
    all_lines = {
        "Kepez - Merkez (Sahil Yolu Hattı)": [
            "Kepez Toki / Kalabaklı",
            "Kepez Belde Kafe",
            "Kepez İskele",
            "Hamidiye Tabyaları",
            "Dardanel Önü",
            "Eski Devlet Hastanesi",
            "Çarşı",
            "İskele Meydanı (Merkez)"
        ],
        "Kepez - Üniversite / Araştırma Hastanesi Hattı": [
            "Kepez Merkez",
            "Güzelyalı / Dardanos Ayrımı",
            "Öğretmenevi",
            "Troya Caddesi",
            "17 Burda AVM",
            "ÇOMÜ Terzioğlu Kampüsü (Ana Kapı)",
            "ÇOMÜ Araştırma Hastanesi"
        ],
        "Ç-1 / Ç-2 (Mavi Hat - Esenler / Kampüs)": [
            "Esenler Mahallesi (Son Durak)",
            "Atatürk Caddesi",
            "Demircioğlu Caddesi",
            "Çarşı",
            "İskele Meydanı",
            "Eski Devlet Hastanesi",
            "KYK Yurtlar",
            "Terzioğlu Kampüsü"
        ],
        "Ç-3 (Kırmızı Hat - Esenler / AVM)": [
            "Esenler",
            "Troya Caddesi",
            "17 Burda AVM",
            "SSK İstasyon",
            "İskele Meydanı",
            "Çarşı"
        ],
        "Ç-4 (Otogar Hattı)": [
            "İskele Meydanı",
            "Çarşı",
            "Demircioğlu Caddesi",
            "Salı Pazarı",
            "Pirireis Caddesi",
            "Çanakkale Yeni Otogar"
        ]
    }

    for line_name, stops in all_lines.items():
        with st.expander(line_name):
            st.markdown(f"**Hat Güzergahı ve Durak Sıralaması:**")
            for index, stop in enumerate(stops, 1):
                st.markdown(f"{index}. 🚏 {stop}")

st.divider()
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 11px;'>Çanakkale & Kepez Toplu Taşıma Bilgi Ağı</p>", unsafe_allow_html=True)
