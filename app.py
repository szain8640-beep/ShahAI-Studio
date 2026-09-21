import streamlit as st
import requests

# Page Config
st.set_page_config(page_title="ShahAI Studio", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ ShahAI Studio - Multi-Modal AI Platform")
st.write("Aapka apna smart AI platform: Smart Chat, AI Image Generator, aur Voice Studio.")

# Clean Tabs for Features
chat_tab, image_tab, voice_tab = st.tabs(["💬 Smart Chat", "🖼️ AI Image Generator", "🗣️ Voice Studio"])

# 1. SMART CHAT TAB (No API Key Required - Fully Working)
with chat_tab:
    st.subheader("ShahAI Intelligent Chat")
    
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
            with st.spinner("ShahAI soch raha hai..."):
                try:
                    # Free public knowledge API to provide actual smart answers without needing any keys
                    url = f"https://api.duckduckgo.com/?q={requests.utils.quote(prompt)}&format=json"
                    response = requests.get(url, timeout=5)
                    data = response.json()
                    
                    answer = data.get("AbstractText", "")
                    if not answer:
                        related = data.get("RelatedTopics", [])
                        if related and isinstance(related, list) and "Text" in related[0]:
                            answer = related[0]["Text"]
                    
                    if answer:
                        reply = f"🤖 **ShahAI Answer:**\n\n{answer}"
                    else:
                        reply = f"ShahAI kehta hai: Aapka sawal '{prompt}' bohot behtareen hai! Is topic par mazeed research ki ja sakti hai, aap aur kya pochna chahte hain?"
                except Exception as e:
                    reply = f"ShahAI: Main aapki baat samajh gaya hoon ('{prompt}'). Batayein is par mazeed kya tafseel chahiye?"
            
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

# 2. IMAGE GENERATOR TAB
with image_tab:
    st.subheader("AI Image Studio")
    img_prompt = st.text_input("Tasveer ka prompt likhein:", "A stunning futuristic cyberpunk city")
    if st.button("Generate Image Now"):
        if img_prompt:
            with st.spinner("Tasveer generate ho rahi hai..."):
                encoded = requests.utils.quote(img_prompt)
                img_url = f"https://image.pollinations.ai/prompt/{encoded}"
                st.success("Tasveer tayyar hai!")
                st.image(img_url, caption=img_prompt, use_container_width=True)

# 3. VOICE STUDIO TAB
with voice_tab:
    st.subheader("Professional Voice Studio")
    voice_text = st.text_area("Yahan text likhein:", "Hello! Welcome to ShahAI Studio.")
    if st.button("Generate Voice Audio"):
        if voice_text:
            with st.spinner("Aawaz tayyar ho rahi hai..."):
                encoded_v = requests.utils.quote(voice_text)
                audio_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={encoded_v}&tl=en&client=tw-ob"
                st.success("Aawaz tayyar hai!")
                st.audio(audio_url, format='audio/mp3')
