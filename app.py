import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

# =========================================================
# LOAD ENVIRONMENT
# =========================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("GEMINI_API_KEY belum ditemukan di file .env")
    st.stop()

# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-3.6-flash"

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🤖 AI Chatbot")

    st.write("Chatbot menggunakan Gemini AI")

    st.divider()

    if st.button("＋ Chat Baru", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption("Contoh pertanyaan")

    if st.button("Apa itu Python?", use_container_width=True):
        st.session_state.messages.append({
            "role": "user",
            "content": "Apa itu Python?"
        })
        st.rerun()

    if st.button("Apa itu jaringan komputer?", use_container_width=True):
        st.session_state.messages.append({
            "role": "user",
            "content": "Apa itu jaringan komputer?"
        })
        st.rerun()

    if st.button("Apa itu Artificial Intelligence?", use_container_width=True):
        st.session_state.messages.append({
            "role": "user",
            "content": "Apa itu Artificial Intelligence?"
        })
        st.rerun()

    st.divider()

    if st.button("🗑️ Hapus Percakapan", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# =========================================================
# HEADER
# =========================================================

st.title("🤖 AI Assistant")

st.caption("Asisten AI berbasis Gemini + Streamlit")


# =========================================================
# WELCOME SCREEN
# =========================================================

if len(st.session_state.messages) == 0:

    st.markdown("# 🤖")

    st.title("Halo! Ada yang bisa saya bantu?")

    st.write(
        "Tanyakan apa saja kepada AI Assistant."
    )


# =========================================================
# TAMPILKAN RIWAYAT CHAT
# =========================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        with st.chat_message("user", avatar="👨‍💻"):
            st.markdown(message["content"])

    else:

        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(message["content"])


# =========================================================
# INPUT USER
# =========================================================

prompt = st.chat_input("Ketik pertanyaan Anda...")


if prompt:

    # -----------------------------------------------------
    # Tampilkan pertanyaan user
    # -----------------------------------------------------

    with st.chat_message("user", avatar="👨‍💻"):
        st.markdown(prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })


    # -----------------------------------------------------
    # Siapkan riwayat percakapan
    # -----------------------------------------------------

    conversation = []

    for message in st.session_state.messages:

        conversation.append(
            {
                "role": message["role"],
                "parts": [
                    {
                        "text": message["content"]
                    }
                ]
            }
        )


    # -----------------------------------------------------
    # Kirim ke Gemini
    # -----------------------------------------------------

    with st.chat_message("assistant", avatar="🤖"):

        with st.spinner("AI sedang berpikir..."):

            try:

                response = client.models.generate_content(
                    model=MODEL,
                    contents=conversation
                )

                answer = response.text

                st.markdown(answer)

            except Exception as e:

                answer = f"Terjadi kesalahan: {e}"

                st.error(answer)


    # -----------------------------------------------------
    # Simpan jawaban AI
    # -----------------------------------------------------

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })