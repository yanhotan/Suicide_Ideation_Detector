import re
import streamlit as st
import requests

# Ngrok URL (use dynamic retrieval if preferred)
api_url = 'https://74e2-35-194-144-131.ngrok-free.app/chat'

st.title("Web App Predictor")

# Input field
user_input = st.text_input("Enter your input text:")

# Dropdown for model selection
model = st.selectbox("Select Model", ["GRU", "LR"])

if st.button("Get Prediction"):
    if not api_url:
        st.error("API URL not available. Check your setup.")
    else:
        # Construct payload
        payload = {"model": model.lower(), "message": user_input}

        try:
            # Send POST request to the backend
            response = requests.post(api_url, json=payload)

            if response.status_code == 200:
                response_data = response.json()
                st.write("Prediction:", response_data.get("response", "No response received."))
            else:
                st.error(f"Error in API call: {response.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
