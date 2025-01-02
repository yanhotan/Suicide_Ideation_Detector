import re
import streamlit as st
import requests

# Ngrok URL
api_url = 'https://8c36-35-237-177-226.ngrok-free.app/chat'
# def get_ngrok_url_from_environment(file_path):
#     with open(file_path, 'r') as file:
#         content = file.read()
#         match = re.search(r"apiUrl: '(https?://.*?)'", content)
#         if match:
#             return match.group(1)
#     return None

# environment_file = "../src/environments/environment.ts"
# api_url = get_ngrok_url_from_environment(environment_file)

# Set Page Configuration
st.set_page_config(page_title="Suicide Ideation Predictor", page_icon="💭", layout="centered")

# Page Title with Styling
st.markdown("""
<style>
/* Force full black background */
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

/* Title styling */
.main-title {
    font-size: 3rem;
    font-weight: bold;
    color: #00d08e; /* Green for main title */
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

/* ---------- COMBINED SELECTBOX STYLING FOR EXPANDED MENU ---------- */
/* The following classes typically appear when the dropdown is expanded */

/* Overall container for selected value, placeholder, etc. */

            /* Target the main select container and its children */
    [data-baseweb="select"] {
        background-color: #1c1c1c !important; /* Dark gray background */
        color: #00d08e !important;           /* Green text */
    }
    [data-baseweb="select"] * {
        background-color: #1c1c1c !important;
        color: #00d08e !important;
    }

    /* Separator and indicators (the dropdown arrow, etc.) */
    [data-baseweb="select"] .css-1okebmr-indicatorSeparator {
        background-color: #00d08e !important;
    }
    [data-baseweb="select"] .css-1hb7zxy-IndicatorsContainer,
    [data-baseweb="select"] .css-1fps5q1 {
        color: #00d08e !important;
    }

    /* Expanded dropdown menu */
    [data-baseweb="select"] .css-26l3qy-menu {
        background-color: #1c1c1c !important;
        color: #00d08e !important;
        border: 1px solid #00d08e !important;
    }

    /* Individual dropdown options */
    [data-baseweb="select"] .css-yt9ioa-option {
        background-color: #1c1c1c !important;
        color: #00d08e !important;
    }
    [data-baseweb="select"] .css-yt9ioa-option:hover {
        background-color: #2a2a2a !important; /* Lighter gray on hover */
        color: #00ffbe !important;           /* Brighter green text on hover */
    }
/* ---------- END SELECTBOX STYLING ---------- */

/* Button styling */
div.stButton button {
    background-color: #00d08e !important; /* Green background */
    color: black !important;             /* Black text for contrast */
    font-weight: bold !important;        /* Make text stand out */
    border-radius: 8px !important;
    padding: 10px 20px !important;
    font-size: 1rem !important;
    border: none !important;
}
div.stButton button:hover {
    background-color: #02f1a3 !important; /* Lighter green on hover */
    color: black !important;
}

/* Prediction box styling */
.prediction-box {
    background-color: #1c1c1c;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.5);
    color: #00d08e; /* Green text for prediction */
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

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
        # Construct payload
        payload = {"model": model.lower(), "message": user_input}

        try:
            # Send POST request to the backend
            response = requests.post(api_url, json=payload)

            if response.status_code == 200:
                response_data = response.json()
                prediction = response_data.get("response", "No response received.")
                st.markdown(
                    f'<div class="prediction-box"><strong>Prediction:</strong> {prediction}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.error(f"Error in API call: {response.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")