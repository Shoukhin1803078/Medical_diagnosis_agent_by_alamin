

import streamlit as st
import google.generativeai as genai
from PIL import Image
import base64

if "messages" not in st.session_state:
    st.session_state.messages = []
if "model" not in st.session_state:
    st.session_state.model = None

def initialize_gemini(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name="gemini-2.0-flash-exp")

st.title("Medical Image Diagnosis Agent 🩺")
st.caption("Upload medical images for professional AI-powered analysis by Al Amin. 🌟")

# Sidebar with API configuration
with st.sidebar:
    st.header("Configuration")
    gemini_key = st.text_input("Enter Gemini API Key", type="password")
    if st.button("Activate Gemini"):
        if gemini_key:
            try:
                st.session_state.model = initialize_gemini(gemini_key)
                st.success("Gemini API activated!")
            except Exception as e:
                st.error(f"Error activating API: {str(e)}")
        else:
            st.error("Please enter an API key")
            
    st.divider()
    uploaded_file = st.file_uploader("Upload Medical Image (X-ray, MRI, CT scan)", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Medical Image", use_container_width=True)
        if st.button("Analyze Image"):
            st.session_state.start_analysis = True
            
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask about the image...")

if prompt or (uploaded_file and st.session_state.get("start_analysis")):
    if not st.session_state.model:
        st.error("Please activate Gemini API first")
        st.stop()

    if not prompt and uploaded_file:
        prompt = "Analyze the uploaded medical image."
        
    inputs = [prompt]
    if uploaded_file:
        inputs.append(image)

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

    with st.spinner("Analyzing..."):
        try:
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                full_response = ""
                response = st.session_state.model.generate_content(inputs, stream=True)
                
                for chunk in response:
                    if chunk.text:
                        full_response += chunk.text
                        response_placeholder.markdown(full_response + "▌")
                response_placeholder.markdown(full_response)

            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Analysis error: {str(e)}")

st.markdown("---")
