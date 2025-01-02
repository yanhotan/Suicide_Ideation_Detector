import re
import streamlit as st
import requests

# Ngrok URL
api_url = 'https://8c36-35-237-177-226.ngrok-free.app/chat'

#############################
#       PAGE CONFIG
#############################
st.set_page_config(
    page_title="Suicide Ideation Predictor",
    page_icon="💭",
    layout="centered"
)

#############################
#         CSS STYLES
#############################
st.markdown("""
<style>
/* Overall black background (main area + sidebar) */
html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stToolbar"] {
    background-color: black !important;
    color: white !important;
}

/* Make all generic Streamlit labels/headings white */
.block-container h1, .block-container h2, .block-container h3,
.block-container h4, .block-container h5, .block-container h6,
.block-container label, .block-container p,
.block-container .stMarkdown, div[role="radiogroup"] label {
    color: white !important;
}

/* Sidebar background color */
[data-testid="stSidebar"] {
    background-color: black !important;  /* Black sidebar */
}

/* Sidebar heading in green */
.sidebar-menu-heading {
    color: #00d08e !important;  /* Green color */
    font-size: 1.5rem !important;
    margin-bottom: 0.5rem;
}

/* Radio button labels default to white */
[data-baseweb="radio"] > label > div {
    color: white !important;
}

/* Highlight the selected radio option in green */
[data-baseweb="radio"] > label[data-selected="true"] > div {
    color: #00d08e !important;
    font-weight: bold;
}

/* Title styling */
.main-title {
    font-size: 3rem;
    font-weight: bold;
    color: #00d08e;
    text-align: center;
    margin-bottom: 20px;
}

/* Subtitle styling */
.sub-text {
    font-size: 1.2rem;
    text-align: center;
    margin-bottom: 30px;
    color: white;
}

/* Text input styling */
.stTextInput > div > input {
    background-color: #1c1c1c;
    color: white;
    border-radius: 5px;
    border: 1px solid #00d08e;
    padding: 10px;
}

/* Simple selectbox container styling (when not expanded) */
.stSelectbox > div {
    background-color: #1c1c1c !important;
    color: white !important;
    border-radius: 5px !important;
    border: 1px solid #00d08e !important;
}

/* SELECTBOX theming when expanded */
[data-baseweb="select"] {
    background-color: #1c1c1c !important;
    color: #00d08e !important;
}
[data-baseweb="select"] * {
    background-color: #1c1c1c !important;
    color: #00d08e !important;
}
[data-baseweb="select"] .css-1okebmr-indicatorSeparator {
    background-color: #00d08e !important;
}
[data-baseweb="select"] .css-1hb7zxy-IndicatorsContainer,
[data-baseweb="select"] .css-1fps5q1 {
    color: #00d08e !important;
}
[data-baseweb="select"] .css-26l3qy-menu {
    background-color: #1c1c1c !important;
    color: #00d08e !important;
    border: 1px solid #00d08e !important;
}
[data-baseweb="select"] .css-yt9ioa-option {
    background-color: #1c1c1c !important;
    color: #00d08e !important;
}
[data-baseweb="select"] .css-yt9ioa-option:hover {
    background-color: #2a2a2a !important;
    color: #00ffbe !important;
}

/* Button styling */
div.stButton button {
    background-color: #00d08e !important;
    color: black !important;
    font-weight: bold !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    font-size: 1rem !important;
    border: none !important;
}
div.stButton button:hover {
    background-color: #02f1a3 !important;
    color: black !important;
}

/* Prediction box styling */
.prediction-box {
    background-color: #1c1c1c;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.5);
    color: #00d08e;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# We'll use a radio button or selectbox for navigation between pages
st.sidebar.markdown("<div class='sidebar-menu-heading'>Menu</div>", unsafe_allow_html=True)
page = st.sidebar.radio("", ("Suicide Ideation Detector", "About"))

if page == "Suicide Ideation Detector":

    # Main Title
    st.markdown('<div class="main-title">Suicide Ideation Predictor</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">Predict text with selected models: GRU or LR</div>', unsafe_allow_html=True)

    # Input Section
    st.write("### Input Section")
    user_input = st.text_input("Enter your input text:", placeholder="Type something here...")

    # Model Selection Dropdown
    st.write("### Model Selection")
    model = st.selectbox("Select Model:", ["GRU", "LR"])

    # Prediction Button and Output Section
    if st.button("Get Prediction", key="predict", help="Click to make a prediction"):
        if not api_url:
            st.error("API URL not available. Check your setup.")
        elif not user_input.strip():
            st.warning("Please enter a valid input text.")
        else:
            payload = {"model": model.lower(), "message": user_input}

            try:
                response = requests.post(api_url, json=payload)
                if response.status_code == 200:
                    response_data = response.json()
                    prediction = response_data.get("response", "No response received.")
                    st.markdown(
                        f'<div class="prediction-box"><strong>Prediction:</strong> {prediction}</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    # Non-200 response => show token message
                    st.error("The token is now invalid please refresh and get the new api token")

            except requests.exceptions.RequestException:
                st.error("The token is now invalid please refresh and get the new api token")

#############################
#       ABOUT PAGE
#############################
elif page == "About":
    # Use inline HTML in Markdown to color the headings green (#00d08e).
    st.markdown("<h2 style='color:#00d08e;'>About This App</h2>", unsafe_allow_html=True)
    st.write("""
    **Suicide Ideation Predictor** is a Streamlit application that uses two models (GRU and LR)
    to classify text inputs into either *Suicide Ideation* or *Non-Suicide*.
    """)

    st.markdown("<h3 style='color:#00d08e;'>How to Use</h3>", unsafe_allow_html=True)
    st.write("""
    1. Go to **Suicide Ideation Detector** (in the navigation sidebar).
    2. Type in the text you want to analyze.
    3. Select a model (GRU or LR).
    4. Click **Get Prediction** to see the result.
    """)

    st.markdown("<h3 style='color:#00d08e;'>Disclaimer</h3>", unsafe_allow_html=True)
    st.write("""
    This application is intended for **demonstration** and **educational** purposes.
    It is **not** a substitute for professional mental health evaluation.
    """)

    st.markdown("<h3 style='color:#00d08e;'>Contact / More Info</h3>", unsafe_allow_html=True)
    st.write("""
    - **Repository**: [GitHub](https://github.com/yanhotan)
    - **Author**: TAN YAN HO
    """)
