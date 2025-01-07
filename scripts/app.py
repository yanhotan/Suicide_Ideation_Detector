import re
import streamlit as st
import requests

# Ngrok URL
api_url = 'https://a186-104-196-249-146.ngrok-free.app/chat'

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
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# We'll use a radio button or selectbox for navigation between pages
st.markdown("""
<style>
/* Overall black background (main area + sidebar) */
html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stToolbar"] {
    background-color: black !important;
    color: white !important;
}

/* Sidebar container styling */
[data-testid="stSidebar"] {
    background-color: #111111 !important; /* Very dark gray */
    color: #D4D4D4 !important; /* Light gray text */
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; /* Modern font */
    padding: 20px !important; /* Inner padding */
}

/* Sidebar heading */
.sidebar-menu-heading {
    font-size: 2rem !important; /* Larger font for heading */
    font-weight: bold !important; /* Bold heading */
    color: #00d08e !important; /* White color */
    margin-bottom: 20px; /* Spacing below heading */
}

/* Sidebar button styles (with reduced gap and no border) */
[data-testid="stSidebar"] div.stButton > button {
    background-color: black !important; /* Black background */
    color: white !important; /* White text */
    font-size: 1.2rem !important; /* Larger font size */
    font-weight: bold !important; /* Bold text */
    border: none !important; /* Remove border */
    border-radius: 10px !important; /* Rounded corners */
    padding: 10px 20px !important; /* Add padding for click area */
    margin-bottom: 8px !important; /* Reduced spacing between buttons */
    transition: all 0.3s ease-in-out; /* Smooth hover effect */
}

/* Hover effect for sidebar buttons */
[data-testid="stSidebar"] div.stButton > button:hover {
    background-color: white !important; /* White background on hover */
    color: black !important; /* Black text on hover */
    transform: scale(1.03); /* Slight scaling effect on hover */
}
</style>
""", unsafe_allow_html=True)

# Sidebar Menu Header
st.sidebar.markdown("<div class='sidebar-menu-heading'>Menu</div>", unsafe_allow_html=True)

# Sidebar Navigation Buttons
if "page" not in st.session_state:
    st.session_state.page = "detector"  # Default page

if st.sidebar.button("Suicide Ideation Detector", key="detector_button"):
    st.session_state.page = "detector"

if st.sidebar.button("About", key="about_button"):
    st.session_state.page = "about"

# Display Content Based on Navigation
if st.session_state.page == "detector":
    st.markdown('<div class="main-title">Suicide Ideation Predictor</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">Predict text with selected models: GRU or LR</div>', unsafe_allow_html=True)

    st.write("### Input Section")
    user_input = st.text_input("Enter your input text:", placeholder="Type something here...")
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
                    
                    # Choose color based on "Suicide" presence
                    # e.g., if "Suicide Ideation" is in the text => RED, else GREEN
                    if "non-suicide" in prediction.lower():
                        color = "#00d08e"  # green
                    else:
                        color = "#FF0000"  # red

                    st.markdown(
                        f"""
                        <div class="prediction-box" style="color:{color};">
                            <strong>Prediction:</strong> {prediction}
                        </div>
                        """,
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
elif st.session_state.page == "about":
    st.markdown("""
    <style>
    /* Overall background */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: black !important;
        color: white !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Sidebar container styling */
    [data-testid="stSidebar"] {
        background-color: #11111 !important;
        color: #D4D4D4 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        padding: 20px !important;
    }

    /* Sidebar buttons */
    [data-testid="stSidebar"] div.stButton > button {
        background-color: black !important;
        color: white !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        margin-bottom: 8px !important;
        transition: all 0.3s ease-in-out;
    }

    [data-testid="stSidebar"] div.stButton > button:hover {
        background-color: white !important;
        color: black !important; /* Ensure text is black on hover */
        transform: scale(1.03);
    }

    /* About page headings */
    h1.about-heading {
        color: #00d08e !important; /* Green for main heading */
        font-weight: bold !important;
        margin-top: 20px !important;
        margin-bottom: 10px !important;
    }

    h2.about-subheading, h3.about-subheading {
        color: white !important; /* White for smaller headings */
        font-weight: bold !important;
        margin-top: 15px !important;
        margin-bottom: 8px !important;
    }

    /* Green and bold */
    .about-content em {
        font-style: normal !important;
        color: #00d08e !important; /* Green color */
        font-weight: bold !important; /* Bold for emphasis */
    }

    /* Hyperlinks */
    div[data-testid="stAppViewContainer"] a {
        color: #00d08e !important;
        text-decoration: none !important;
    }
    div[data-testid="stAppViewContainer"] a:hover {
        text-decoration: underline !important;
    }
    .about-content.hotline-highlight {
    color: #00d08e !important; /* Green text */
    font-weight: bold !important; /* Bold text */
    font-style: normal !important; /* Normal style (not italic) */
    }
    </style>
    """, unsafe_allow_html=True)

    # About Page Content
    st.markdown('<h1 class="about-heading">About This App</h1>', unsafe_allow_html=True)
    st.markdown("""
    <span class="about-content">
    <em>Suicide Ideation Predictor</em> is a Streamlit application that uses two models (<em>GRU</em> and <em>LR</em>) 
    to classify text inputs into either <em>Suicide Ideation</em> or <em>Non-Suicide</em>.
    </span>
    """, unsafe_allow_html=True)

    st.markdown('<h2 class="about-subheading">How to Use</h2>', unsafe_allow_html=True)
    st.markdown("""
    1. Go to <span class="about-content"><em>Suicide Ideation Detector</em></span> (in the navigation sidebar).  
    2. Type in the text you want to analyze.  
    3. Select a model (<span class="about-content"><em>GRU</em></span> or <span class="about-content"><em>LR</em></span>).  
    4. Click <span class="about-content"><em>Get Prediction</em></span> to see the result.
    """, unsafe_allow_html=True)

    st.markdown('<h2 class="about-subheading">Disclaimer</h2>', unsafe_allow_html=True)
    st.markdown("""
    This application is intended for demonstration and educational purposes.  
    It is not a substitute for professional mental health evaluation.
    """, unsafe_allow_html=True)

    st.markdown('<h2 class="about-subheading">Contact / More Info</h2>', unsafe_allow_html=True)
    st.markdown("""
    - **Repository**: [GitHub](https://github.com/yanhotan)  
    - **Author**: TAN YAN HO  
    - <span class="about-content hotline-highlight">Hotline Information</span>: If you or someone you know needs support, please contact a suicide prevention hotline in your area:
        - Malaysia 15999 (Talian Kasih) or <span class="about-content hotline-highlight">Befrienders KL</span>: +603-7627 2929
        - International: [Visit Befrienders Worldwide](https://www.befrienders.org)
    """, unsafe_allow_html=True)

