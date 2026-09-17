import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Çanakkale & Kepez Ulaşım Asistanı",
    page_icon="🚌",
    layout="centered"
)

# Başlık
st.markdown("<h2 style='text-align: center; color: #2563eb;'>🚌 Çanakkale & Kepez Ulaşım Rehberi</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; font-size: 13px;'>Kepez ve Merkez arası tüm hatlar, en yakın duraklar ve yürüyüş rotaları</p>", unsafe_allow_html=True)

st.divider()

# Sekmeler
tab1, tab2 = st.tabs(["📍 Kepez & Merkez Rota Bulucu", "📋 Tüm Hatlar Listesi"])

# --- TAB 1: ROTA BULUCU ---
with tab1:
    st.markdown("### Nereye gideceksiniz?")
    
    # Kalkış Noktaları (Kepez ağırlıklı ve merkez duraklar)
    origins = [
        "Kepez Belediyesi / Merkez", 
        "Kepez Sahil / Toki", 
        "Terzioğlu Kampüsü (Ana Kapı)", 
        "ÇOMÜ Araştırma Hastanesi", 
        "İskele Meydanı",
        "Çanakkale Otogar"
    ]
    
    origin = st.selectbox("Neredesiniz? (Kalkış Noktası)", origins)

    # Gitmek İstenen Özel Noktalar ve Kepez Bağlantıları
    destinations_info = {
        "Çanakkale Belediyesi (Merkez)": {
            "nearest_stop": "İskele Meydanı",
            "walk_time": "3 dakika (250m)",
            "direction": "İskele'den sahile doğru yürüyerek belediye binasına ulaşabilirsiniz.",
            "line": "Kepez - Merkez Minibüsleri / Ç-1 / Ç-3"
        },
        "Aynalı Çarşı": {
            "nearest_stop": "Çarşı / Truva Atı",
            "walk_time": "2 dakika (150m)",
            "direction": "Çarşı durağında indikten sonra Saat Kulesi istikametine yürüyün.",
            "line": "Kepez - Çarşı Hatları"
        },
        "ÇOMÜ Araştırma Hastanesi": {
            "nearest_stop": "Hastane Önü Durağı",
            "walk_time": "0 dakika (Kapıda İniş)",
            "direction": "Doğrudan hastane önündeki durakta inebilirsiniz.",
            "line": "ÇT-1 / Kepez-Hastane Direkt Hat"
        },
        "ÇOMÜ Terzioğlu Kampüsü": {
            "nearest_stop": "Kampüs Ana Kapı",
            "walk_time": "0 dakika (Kampüs İçi)",
            "direction": "Ana kapıda inebilirsiniz.",
            "line": "Kepez - Kampüs Hatları"
        },
        "17 Burda AVM": {
            "nearest_stop": "17 Burda AVM Önü",
            "walk_time": "0 dakika (Kapıda İniş)",
            "direction": "AVM'nin önündeki durakta inebilirsiniz.",
            "line": "Ç-3 / Kepez Ringleri"
        },
        "Kepez Sahil / Ev": {
            "nearest_stop": "Kepez Merkez Durakları",
            "walk_time": "2-5 dakika",
            "direction": "Kepez içi hatlarla evinize en yakın noktaya ulaşabilirsiniz.",
            "line": "Kepez İçi Hatlar"
        }
    }

    destination_name = st.selectbox("Nereye varacaksınız? (Hedef Yer)", list(destinations_info.keys()))

    if st.button("Ulaşım ve Yürüyüş Rotasını Göster", use_container_width=True):
        target = destinations_info[destination_name]
        
        st.success(f"🎯 Hedef: **{destination_name}**")
        
        # Bilgi Kutuları
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Önerilen En Yakın Durak", value=target["nearest_stop"])
        with col2:
            st.metric(label="Sonrası Yürüyüş", value=target["walk_time"])
            
        st.info(f"🚌 Binmeniz Gereken Hat: **{target['line']}**")
        
        st.markdown("#### 🚶‍♂️ Yürüyüş ve Rota Rehberi")
        st.markdown(f"> {target['direction']}")
        
        st.markdown("#### 📍 Güzergah Özeti")
        st.markdown(f"- 🟢 Kalkış: **{origin}**")
        st.markdown(f"- 🔵 İneceğiniz Yer: **{target['nearest_stop']}**")
        st.markdown(f"- 🎯 Son Nokta: **{destination_name}**")

# --- TAB 2: TÜM HATLAR LİSTESİ (KEPEZ DAHİL) ---
with tab2:
    st.markdown("### 📋 Kepez ve Merkez Hat Listesi")
    
    lines_info = {
        "Kepez - Merkez (Sahil Yolu)": "Kepez Belde Kafe - Hamidiye - İskele Meydanı (Annenlerin en sık kullanacağı hat)",
        "Kepez - Üniversite / Hastane": "Kepez - Troya Caddesi - Terzioğlu Kampüsü - Araştırma Hastanesi",
        "Ç-1 / Ç-2 (Mavi Hat)": "Esenler - Terzioğlu Kampüsü - İskele - Gazi Meclisi",
        "Ç-3 (Kırmızı Hat)": "Esenler - Terzioğlu Kampüsü - İskele - 17 Burda AVM",
        "Ç-4": "İskele - Çarşı - Salı Pazarı - Yeni Otogar",
        "ÇT-1 / ÇT-3": "Araştırma Hastanesi - İskele - Troya Caddesi - Kampüs",
    }

    for line_code, desc in lines_info.items():
        with st.expander(line_code):
            st.write(f"**Güzergah Özeti:** {desc}")
            st.write("Durum: Aktif Seferde ✅")

st.divider()
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 11px;'>Çanakkale & Kepez Toplu Taşıma Bilgi Ağı</p>", unsafe_allow_html=True)
