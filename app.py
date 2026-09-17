import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Çanakkale & Kepez Ulaşım Asistanı",
    page_icon="🚌",
    layout="centered"
)

# Başlık
st.markdown("<h2 style='text-align: center; color: #2563eb;'>🚌 Çanakkale & Kepez Ulaşım Asistanı</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; font-size: 13px;'>Nereden nereye gideceğinizi kendi kelimelerinizle yazın, en uygun rotayı ve durakları bulalım.</p>", unsafe_allow_html=True)

st.divider()

# Sekmeler
tab1, tab2 = st.tabs(["📍 Serbest Rota Arama", "📋 Tüm Hatlar Listesi"])

# --- TAB 1: SERBEST ARAMA VE ROTA BULUCU ---
with tab1:
    st.markdown("### Rota Bilgisi")
    
    # Kullanıcının serbestçe metin girebileceği alanlar
    origin_input = st.text_input("Nereden kalkacaksınız?", placeholder="Örn: Kepez Toki, İskele, Esenler...")
    destination_input = st.text_input("Nereye gideceksiniz?", placeholder="Örn: Belediye binası, Araştırma Hastanesi, Çarşı...")

    if st.button("Rotayı ve Durakları Hesapla", use_container_width=True):
        if not origin_input or not destination_input:
            st.warning("⚠️ Lütfen hem nereden hem nereye gideceğinizi yazın!")
        else:
            # Aramayı küçük harfe çevirerek akıllı eşleştirme yapalım
            dest_lower = destination_input.lower()
            orig_lower = origin_input.lower()
            
            # Varsayılan akıllı yönlendirme şablonu
            nearest_stop = "İskele Meydanı / Merkez Duraklar"
            walk_time = "3-5 dakika"
            direction = f"'{origin_input}' bölgesinden hareket eden hatlarla merkeze ulaştıktan sonra kısa bir yürüyüşle varabilirsiniz."
            line_suggestion = "Kepez - Merkez Hatları / Ç-1 / Ç-3"
            
            # Özel nokta eşleştirmeleri (Annenlerin veya kullanıcıların sık arayabileceği yerler)
            if "belediye" in dest_lower:
                nearest_stop = "İskele Meydanı"
                walk_time = "3 dakika (250m)"
                direction = "İskele durağında indikten sonra sahil boyunca yürüyerek belediye binasına ulaşabilirsiniz."
                line_suggestion = "Kepez - Merkez Sahil Hattı"
            elif "hastane" in dest_lower:
                nearest_stop = "ÇOMÜ Araştırma Hastanesi Önü"
                walk_time = "0 dakika (Kapıda İniş)"
                direction = "Doğrudan hastane kapısının önündeki durakta inebilirsiniz."
                line_suggestion = "Kepez - Üniversite / Hastane Direkt Hattı"
            elif "çarşı" in dest_lower or "aynalı" in dest_lower:
                nearest_stop = "Çarşı / Truva Atı Durağı"
                walk_time = "2 dakika (150m)"
                direction = "Çarşı durağında inip Saat Kulesi yönüne yürüyebilirsiniz."
                line_suggestion = "Kepez - Çarşı Hatları (Ç-4)"
            elif "kampüs" in dest_lower or "üniversite" in dest_lower:
                nearest_stop = "Terzioğlu Kampüsü Ana Kapı"
                walk_time = "0 dakika (Kampüs İçi)"
                direction = "Kampüs girişinde inebilirsiniz."
                line_suggestion = "Kepez - Kampüs Direkt Hatları"
            elif "avm" in dest_lower or "17 burda" in dest_lower:
                nearest_stop = "17 Burda AVM Önü"
                walk_time = "0 dakika (Kapıda İniş)"
                direction = "AVM'nin önündeki durakta inebilirsiniz."
                line_suggestion = "Ç-3 / Kepez Ringleri"

            st.success(f"🎯 Hedef: **{destination_input.title()}**")
            
            # Bilgi Kartları
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Önerilen En Yakın Durak", value=nearest_stop)
            with col2:
                st.metric(label="Sonrası Yürüyüş", value=walk_time)
                
            st.info(f"🚌 Binmeniz Gereken Hat: **{line_suggestion}**")
            
            st.markdown("#### 🚶‍♂️ Yol Tarifi ve Yürüyüş Rehberi")
            st.markdown(f"> {direction}")
            
            st.markdown("#### 📍 Yolculuk Özeti")
            st.markdown(f"- 🟢 Kalkış: **{origin_input.title()}**")
            st.markdown(f"- 🔵 İneceğiniz Durak: **{nearest_stop}**")
            st.markdown(f"- 🎯 Varmak İstediğiniz Yer: **{destination_input.title()}**")

# --- TAB 2: TÜM HATLAR LİSTESİ ---
with tab2:
    st.markdown("### 📋 Kepez ve Merkez Hat Listesi")
    
    lines_info = {
        "Kepez - Merkez (Sahil Yolu)": "Kepez Belde Kafe - Hamidiye - İskele Meydanı (Kepez'den merkeze en direkt hat)",
        "Kepez - Üniversite / Hastane": "Kepez - Troya Caddesi - Terzioğlu Kampüsü - Araştırma Hastanesi",
        "Ç-1 / Ç-2 (Mavi Hat)": "Esenler - Terzioğlu Kampüsü - İskele - Gazi Meclisi",
        "Ç-3 (Kırmızı Hat)": "Esenler - Terzioğlu Kampüsü - İskele - 17 Burda AVM",
        "Ç-4": "İskele - Çarşı - Salı Pazarı - Yeni Otogar",
        "ÇT-1 / ÇT-3": "Araştırma Hastanesi - İskele - Troya Caddesi - Kampüs",
    }

    for line_code, desc in lines_info.items():
        with st.expander(line_code):
            st.write(f"**Güzergah Özeti:** {desc}")
            st.write("Status: Aktif Seferde ✅")

st.divider()
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 11px;'>Çanakkale & Kepez Toplu Taşıma Bilgi Ağı</p>", unsafe_allow_html=True)
