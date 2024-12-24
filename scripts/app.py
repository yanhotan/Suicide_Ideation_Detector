import re
import streamlit as st
import requests

def get_ngrok_url_from_environment(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        match = re.search(r"apiUrl: '(https?://.*?)'", content)
        if match:
            return match.group(1)
    return None

# Retrieve Ngrok URL dynamically
environment_file = "src/environments/environment.ts"
api_url = get_ngrok_url_from_environment(environment_file)

st.title("Web App Predictor")

# Input field
user_input = st.text_input("Enter your input text:")

# Dropdown for model selection
model = st.selectbox("Select Model", ["gru", "gemini"])

if st.button("Get Prediction"):
    if model == "gru":
        response = requests.post(f"{api_url}/chat", json={"model": model, "message": user_input})
    elif model == "gemini":
        gemini_api_url = "http://localhost:5000/api/generate"
        response = requests.post(gemini_api_url, json={"prompt": user_input})

    if response.status_code == 200:
        st.write("Prediction:", response.json().get("response", "No response received."))
    else:
        st.error("Error in API call:", response.text)
