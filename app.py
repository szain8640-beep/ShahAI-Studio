import streamlit as st
import os
import requests
from groq import Groq

# Page Config
st.set_page_config(page_title="ShahAI Studio", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stTextInput input, .stTextArea textarea {
        background-color: #161b22;
        color: #ffffff;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ ShahAI Studio - Multi-Modal AI Platform")
st.write("Aapka apna smart AI platform: Smart Chat, AI Image Generator, aur Voice Studio.")

# Clean Tabs for Features
chat_tab, image_tab, voice_tab = st.tabs(["💬 Smart Chat", "🖼️ AI Image Generator", "🗣️ Voice Studio"])

# 1. SMART CHAT TAB
with chat_tab:
    st.subheader("ShahAI Intelligent Chat")
    
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets["GROQ_API_KEY"]
        except:
            pass

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Salam! Main ShahAI hoon. Batayein aaj main aapki kya madad kar sakta hoon?"}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Yahan apna sawal likhein..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if api_key:
                try:
                    client = Groq(api_key=api_key)
                    completion = client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=[{"role": "system", "content": "You are ShahAI, a professional assistant."}] + st.session_state.messages,
                        temperature=0.7,
                    )
                    reply = completion.choices[0].message.content
                except Exception as e:
                    reply = f"Error: {e}"
            else:
                reply = f"Aapne kaha: '{prompt}'. ShahAI smart chat active hai!"
            
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

# 2. IMAGE GENERATOR TAB
with image_tab:
    st.subheader("AI Image Studio")
    st.write("Apni pasand ki tasveer ka prompt likhein aur foran screen par hasil karein:")
    
    img_prompt = st.text_input("Misal: A futuristic cyberpunk city with neon lights", "A stunning futuristic cyberpunk city")
    if st.button("Generate Image Now"):
        if img_prompt:
            with st.spinner("Tasveer generate ho rahi hai, intezar karein..."):
                encoded = requests.utils.quote(img_prompt)
                img_url = f"https://image.pollinations.ai/prompt/{encoded}"
                st.success("Tasveer kamyabi ke sath tayyar ho gayi hai!")
                st.image(img_url, caption=img_prompt, use_container_width=True)

# 3. VOICE STUDIO TAB
with voice_tab:
    st.subheader("Professional Voice Studio")
    st.write("Jo text aap likhenge, ShahAI usay saaf aawaz mein convert kar dega:")
    
    voice_text = st.text_area("Yahan text likhein:", "Hello! Welcome to ShahAI Studio. Your advanced assistant is ready.")
    if st.button("Generate Voice Audio"):
        if voice_text:
            with st.spinner("Aawaz tayyar ho rahi hai..."):
                encoded_v = requests.utils.quote(voice_text)
                audio_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={encoded_v}&tl=en&client=tw-ob"
                st.success("Aawaz kamyabi ke sath tayyar ho gayi hai!")
                st.audio(audio_url, format='audio/mp3')
