import os
import streamlit as st
from huggingface_hub import InferenceClient

# Get your Hugging Face API key from the environment variable
HUGGING_FACE_API_KEY = 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
HUGGING_FACE_API_KEY = os.getenv("HUGGING_FACE_API_KEY")

if HUGGING_FACE_API_KEY is None:
    st.error("Please set the HUGGING_FACE_API_KEY environment variable.")
    st.stop()  # Stop execution if API key is missing

client = InferenceClient(api_key=HUGGING_FACE_API_KEY)

def healthcare_chatbot(user_input):
    try:
        response = client.text_generation(user_input)
        return response
    except Exception as e:  # Catch potential errors during API call
        st.error(f"Error communicating with the model: {e}") # Display error in Streamlit
        return "Sorry, I couldn't generate a response due to an error."

def main():
    st.set_page_config(page_title="Healthcare Assistant Chatbot", page_icon=":hospital:")
    
    # Sidebar Information
    st.sidebar.title("About")
    st.sidebar.info("""
        This Healthcare Assistant Chatbot is designed to assist with basic health inquiries.
        Please note that it is not a substitute for professional medical advice.
    """)

    st.sidebar.title("Health Parameters")
    st.sidebar.markdown("""
        <div style="text-align: justify; color: #444444;">
        <span style="color: #ff6f61;"><strong>**Normal Blood Pressure:**</strong></span> <span style="font-weight: bold;">Between 90/60 mmHg and 120/80 mmHg</span><br>
        <span style="color: #6b5b95;"><strong>**Normal Blood Sugar Level:**</strong></span> <span style="font-weight: bold;">70-99 mg/dL (fasting)</span><br>
        <span style="color: #88b04b;"><strong>**Normal Body Temperature:**</strong></span> <span style="font-weight: bold;">98.6°F (37°C)</span><br>
        <span style="color: #ffcc5c;"><strong>**Breathing:**</strong></span> <span style="font-weight: bold;">12 to 18 breaths per minute</span><br>
        <span style="color: #f7cac9;"><strong>**Pulse:**</strong></span> <span style="font-weight: bold;">60 to 100 beats per minute</span>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.title("Emergency")
    st.sidebar.markdown("""
        **National Healthcare Ambulance Number (India):** 108 
        <br>
        **104 Medical Helpline**
    """)

    st.sidebar.title("Chatbot Developer Information")
    st.sidebar.info("""
        Created by [Prikshit Gautam](https://www.linkedin.com/in/prikshit-gautam-76b1a9308/)
    """)

    st.title("Healthcare Assistant Chatbot")
    
    st.markdown("""
        Welcome to the Healthcare Assistant Chatbot. Please type your query in the text box below.
        This chatbot uses advanced AI to generate responses to healthcare-related questions.
    """)

    user_input = st.text_input("How can I assist you today?")
    if st.button("Submit"):
        if user_input:
            st.write("**User:** ", user_input)
            with st.spinner("Processing your query..."):
                response = healthcare_chatbot(user_input)
            st.write("**Healthcare Assistant:** ", response)
        else:
            st.warning("Please enter a message to get a response.")

if __name__ == "__main__":
    main()
