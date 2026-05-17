import streamlit as st
import requests
import base64

# =======================
# Setup
# =======================
st.set_page_config(page_title="Quran Mood Agent", page_icon="🤎")

# =======================
# Background Image (Base64 FIX)
# =======================
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img_base64 = get_base64("quranwallp.jpeg")

st.markdown(f"""
<style>
.stApp {{
    background-image: url("data:image/jpeg;base64,{img_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
</style>
""", unsafe_allow_html=True)

# =======================
# Style (RTL)
# =======================
st.markdown("""
<style>
html, body, [class*="css"] {
    direction: rtl;
    text-align: right;
    font-size: 22px;
}
</style>
""", unsafe_allow_html=True)

st.title("🤎 Quran Mood Agent")

# =======================
# Moods
# =======================
moods_list = [
    "حزن","قلق","خوف","ضيق","شكر",
    "فرح","سعادة","راحة","غضب","احباط",
    "توتر","دهشة","ارتباك","خجل","أمل","طمأنينة"
]

selected_mood = st.selectbox("📋 اختر شعورك:", moods_list)

# =======================
# Get Quran text API
# =======================
def get_ayah_text(surah, ayah):
    url = f"https://api.alquran.cloud/v1/ayah/{surah}:{ayah}/ar"
    res = requests.get(url).json()
    return res["data"]["text"]

# =======================
# Audio function
# =======================
def play_audio(surah, ayah):
    url = f"https://everyayah.com/data/Abdul_Basit_Mujawwad_128kbps/{surah:03d}{ayah:03d}.mp3"
    st.audio(url)

# =======================
# UI Card
# =======================
def show_card(text):
    st.markdown(f"""
    <div style="
        background: rgba(255,255,255,0.92);
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 10px;
        text-align: right;
        direction: rtl;
        line-height: 1.8;
    ">
        {text}
    </div>
    """, unsafe_allow_html=True)

# =======================
# Mood Mapping
# =======================
mapping = {
    "حزن": [(2,153), (94,5)],
    "قلق": [(13,28), (94,6)],
    "خوف": [(3,173), (9,51)],
    "ضيق": [(94,5), (2,286)],
    "شكر": [(14,7), (2,152)],
    "فرح": [(10,58), (39,73)],
    "سعادة": [(13,28), (16,97)],
    "راحة": [(13,28), (2,286)],
    "غضب": [(3,134), (42,37)],
    "احباط": [(39,53), (12,87)],
    "توتر": [(94,5), (94,6)],
    "دهشة": [(21,30), (3,190)],
    "ارتباك": [(2,286), (2,286)],
    "خجل": [(24,30), (24,31)],
    "أمل": [(39,53), (94,6)],
    "طمأنينة": [(13,28), (89,27)]
}

# =======================
# MAIN
# =======================
if st.button("🔍 تحليل"):

    verses = mapping.get(selected_mood, [(2,153), (3,139)])

    st.success(f"✨ الشعور: {selected_mood}")
    st.info("📖 الآيات المناسبة:")

    for surah, ayah in verses:
        try:
            text = get_ayah_text(surah, ayah)
            show_card(f"{text} ({surah}:{ayah})")
            play_audio(surah, ayah)
        except Exception as e:
            st.error(f"خطأ في جلب الآية: {e}")