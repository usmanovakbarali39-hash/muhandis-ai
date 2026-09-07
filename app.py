import streamlit as st
from google import genai
from google.genai import types

# ---------------------------------------------------------
# Sahifa sozlamalari
# ---------------------------------------------------------
st.set_page_config(
    page_title="muhandis.ai — TMJ AI Yordamchisi",
    page_icon="⚙️",
    layout="wide"
)

# ---------------------------------------------------------
# Tizim ko'rsatmasi (TMJ va Muhandislik eksperti)
# ---------------------------------------------------------
SYSTEM_INSTRUCTION = """
Siz "muhandis.ai" — Texnologik Mashinalar va Jihozlar (TMJ), mashinasozlik, qishloq xo'jaligi texnikasi, mexanika va payvandlash texnologiyalari bo'yicha yetakchi ekspert-muhandis va ilmiy maslahatchisiz.

ASOSIY VAZIFALAR:
1. HISOB-KITOB VA KONSTRUKSIYALASH: Detallar va mexanizmlar mustahkamligi, tebranishlar, nagruzka parametrlarini tahlil qiling. Formulalarni LaTeX formatida va aniq ko'rsating.
2. ILMIY HUJJATLAR (IMRAD / DISSERTATSIYA): Maqola va dissertatsiyalarni IMRAD standartlariga mos rasmiylashtirishda yordam bering.
3. EXSPLUATATSIYA VA TIKLASH: Detallar yeyilishi, nosozliklar va qattiq qatlam berib payvandlash (Sormayt, T-590, T-620 va boshqalar) bo'yicha amaliy tavsiyalar bering.

Har doim professional, ilmiy-texnik va aniq tilda javob bering.
"""

# ---------------------------------------------------------
# Yon panel (Sidebar)
# ---------------------------------------------------------
with st.sidebar:
    st.title("⚙️ muhandis.ai")
    st.caption("TMJ bo'yicha sun'iy intellekt platformasi")
    st.markdown("---")
    
    api_key = st.text_input("Google AI Studio API Key:", type="password")
    
    st.markdown("---")
    if st.button("🗑️ Chatni tozalash", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("**Aktiv yo'nalishlar:**")
    st.markdown("- 🛠️ Detallar va mexanizmlar hisobi")
    st.markdown("- 📄 IMRAD / Ilmiy maqolalar")
    st.markdown("- 🔥 Yeyilish va qattiq qatlam berib payvandlash")

# ---------------------------------------------------------
# Asosiy chat interfeysi
# ---------------------------------------------------------
st.header("⚙️ muhandis.ai — Muhandislik Maslahatchisi")

# Chat tarixini xotirada saqlash
if "messages" not in st.session_state:
    st.session_state.messages = []

# Avvalgi suhbatlarni ekranga chiqarish
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Fayl yuklash va matn kiritish
uploaded_file = st.file_uploader("Rasm yoki hujjat biriktirish (ixtiyoriy):", type=["png", "jpg", "jpeg", "pdf"])
user_input = st.chat_input("Savolingizni yozing...")

if user_input:
    if not api_key:
        st.error("Iltimos, chap paneldan API kalitingizni kiriting!")
        st.stop()

    # Foydalanuvchi xabarini ko'rsatish
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Gemini API ga so'rov yuborish
    try:
        client = genai.Client(api_key=api_key)
        
        contents = [user_input]
        if uploaded_file:
            bytes_data = uploaded_file.getvalue()
            contents.append(types.Part.from_bytes(data=bytes_data, mime_type=uploaded_file.type))

        with st.chat_message("assistant"):
            with st.spinner("Muhandislik tahlili bajarilmoqda..."):
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.3,
                    )
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"Xatolik yuz berdi: {e}")