import re
import streamlit as st
import requests

import streamlit as st
import re
import numpy as np
import pickle
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
import nltk
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.feature_extraction.text import TfidfVectorizer

# Make sure these downloads happen at least once in your environment
nltk.download('wordnet')
nltk.download('omw-1.4')  # for extended WordNet support

# ---------------------
# Load Models & Assets
# ---------------------

# 1) Load GRU Model & Tokenizer
GRU_MODEL_PATH = "gru_model.keras"  # adjust path if needed
TOKENIZER_PATH = "tokenizer.pkl"    # adjust path if needed

gru_model = load_model(GRU_MODEL_PATH)
with open(TOKENIZER_PATH, "rb") as f:
    tokenizer = pickle.load(f)

# 2) Load Logistic Regression Model & TF-IDF Vectorizer
LR_MODEL_PATH = "logistic_regression_sentiment_fine_tuned.pkl"
VECTORIZER_PATH = "tfidf_vectorizer_sentiment.pkl"

with open(LR_MODEL_PATH, "rb") as f:
    lr_model = pickle.load(f)
with open(VECTORIZER_PATH, "rb") as f:
    tfidf_vectorizer = pickle.load(f)

# ---------------------
# Helper Functions
# ---------------------

def preprocess_text_for_gru(text: str) -> str:
    # Similar to 'preprocess_text' in your Colab snippet
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    return text

def calculate_polarity_category(polarity_score: float):
    # same logic from snippet
    if polarity_score < -0.5:
        return [1, 0, 0]
    elif -0.5 <= polarity_score <= 0.5:
        return [0, 1, 0]
    else:
        return [0, 0, 1]

def predict_with_gru(text: str) -> str:
    try:
        processed_text = preprocess_text_for_gru(text)
        sequence = tokenizer.texts_to_sequences([processed_text])
        padded_sequence = pad_sequences(sequence, maxlen=200, padding="post")

        # Add sentiment-based features
        polarity_score = TextBlob(text).sentiment.polarity
        polarity_category = calculate_polarity_category(polarity_score)
        polarity_features = np.array([polarity_category])
        input_combined = np.hstack([padded_sequence, polarity_features])

        # GRU Model Prediction
        prediction = gru_model.predict(input_combined)
        suicide_prob = prediction[0][1] * 100

        if suicide_prob >= 50:
            return f"Suicide Ideation ({suicide_prob:.2f}%)"
        else:
            return f"Non-Suicide ({100 - suicide_prob:.2f}%)"
    except Exception as e:
        return f"Error processing GRU model: {str(e)}"

# ---------------

def preprocess_input_for_lr(text: str) -> str:
    # lower, remove special chars, lemmatize
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    tokens = text.split()
    lemmatized_tokens = [WordNetLemmatizer().lemmatize(t) for t in tokens]
    return " ".join(lemmatized_tokens)

def predict_with_lr(text: str) -> str:
    try:
        processed_text = preprocess_input_for_lr(text)
        tfidf_features = tfidf_vectorizer.transform([processed_text])

        # Calculate sentiment
        polarity_score = TextBlob(text).sentiment.polarity
        sentiment_feature = np.array([[polarity_score]])

        # Combine features
        input_combined = np.hstack([tfidf_features.toarray(), sentiment_feature])

        # Match feature size
        expected_size = lr_model.coef_.shape[1]
        current_size = input_combined.shape[1]

        if current_size < expected_size:
            padding = np.zeros((1, expected_size - current_size))
            input_combined = np.hstack([input_combined, padding])
        elif current_size > expected_size:
            input_combined = input_combined[:, :expected_size]

        # Predict
        prediction_probs = lr_model.predict_proba(input_combined)[0]
        suicide_prob = prediction_probs[1] * 100
        non_suicide_prob = prediction_probs[0] * 100

        if suicide_prob >= 50:
            return f"Suicide Ideation ({suicide_prob:.2f}%)"
        else:
            return f"Non-Suicide Ideation ({non_suicide_prob:.2f}%)"
    except Exception as e:
        return f"Error processing LR model: {str(e)}"

# Ngrok URL
api_url = 'https://25d1-34-125-119-166.ngrok-free.app/chat'
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

st.set_page_config(page_title="Suicide Ideation Predictor", page_icon="🧠", layout="centered")

st.title("Suicide Ideation Predictor")
st.markdown("This application uses **two** models (GRU and LR) to classify whether input text suggests Suicide Ideation or Non-Suicidal Ideation.")

# User Input
user_text = st.text_area("Enter your text below:")

# Model Selector
model_choices = ["GRU", "LR"]
selected_model = st.selectbox("Select Model:", model_choices)

# Prediction
if st.button("Get Prediction"):
    if not user_text.strip():
        st.warning("Please enter some text before predicting.")
    else:
        if selected_model == "GRU":
            result = predict_with_gru(user_text)
        else:
            result = predict_with_lr(user_text)

        st.subheader("Prediction Result")
        st.write(result)


# # Main Title
# st.markdown('<div class="main-title">Suicide Ideation Predictor</div>', unsafe_allow_html=True)
# st.markdown('<div class="sub-text">Predict text with selected models: GRU or LR</div>', unsafe_allow_html=True)

# # Input Section
# st.write("### Input Section")
# user_input = st.text_input("Enter your input text:", placeholder="Type something here...")

# # Model Selection Dropdown
# st.write("### Model Selection")
# model = st.selectbox("Select Model:", ["GRU", "LR"])

# # Prediction Button and Output Section
# if st.button("Get Prediction", key="predict", help="Click to make a prediction"):
#     if not api_url:
#         st.error("API URL not available. Check your setup.")
#     elif not user_input.strip():
#         st.warning("Please enter a valid input text.")
#     else:
#         # Construct payload
#         payload = {"model": model.lower(), "message": user_input}

#         try:
#             # Send POST request to the backend
#             response = requests.post(api_url, json=payload)

#             if response.status_code == 200:
#                 response_data = response.json()
#                 prediction = response_data.get("response", "No response received.")
#                 st.markdown(
#                     f'<div class="prediction-box"><strong>Prediction:</strong> {prediction}</div>',
#                     unsafe_allow_html=True,
#                 )
#             else:
#                 st.error(f"Error in API call: {response.text}")

#         except requests.exceptions.RequestException as e:
#             st.error(f"Request failed: {e}")