# Suicide Ideation Detection Using GRU, Logistic Regression, and Angular Frontend with Large Language Models Integration
https://suicideideationdetector.streamlit.app/

This project aims to detect suicide ideation from textual data using machine learning techniques and an interactive Angular-based frontend. Two models—GRU (Gated Recurrent Unit) and Logistic Regression—were used for backend predictions. The project also integrates large language models (LLMs) like **Gemini** for advanced sentiment analysis and contextual understanding.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Dataset](#dataset)
- [Preprocessing](#preprocessing)
- [Models Used](#models-used)
  - [Logistic Regression](#logistic-regression)
  - [GRU Model](#gru-model)
  - [Gemini Integration](#gemini-integration)
- [Frontend](#frontend)
- [Evaluation](#evaluation)
- [Results](#results)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Future Work](#future-work)

---

## Overview

This project provides an end-to-end pipeline for detecting suicide ideation from textual data, leveraging state-of-the-art machine learning models and a responsive Angular frontend for user interaction. It also incorporates **Gemini**, a large language model, for enhancing sentiment and contextual analysis.

---

## Features

### Sentiment Analysis
- Analyzes text polarity using `TextBlob` and Gemini for advanced sentiment classification.
- Sentiment polarity values are categorized into `positive`, `neutral`, and `negative`.

### Personality-Like Features
- Includes text-level features such as text length, average word length, and number of words.
- Enhances models with additional contextual information for better predictions.

### Angular Frontend
- A responsive and user-friendly interface developed with **Angular**.
- Features:
  - **Real-Time Prediction**: Users can input text and receive predictions instantly.
  - **Sentiment Visualization**: Displays sentiment analysis and polarity scores.
  - **Model Comparison**: Compares predictions from GRU, Logistic Regression, and Gemini models.
  - **Interactive Charts**: Visualizes performance metrics like accuracy, precision, and loss over epochs.

---

## Dataset

- **Source**: Text samples labeled as `suicide` or `non-suicide`.
- **Preprocessing**:
  - Sentiment polarity values calculated using `TextBlob`.
  - Personality-like features such as text length and word counts.
  - Categorized sentiment polarity (`low`, `mid`, `high`) using thresholds.

---

## Preprocessing

1. **Text Cleaning**:
   - Lowercasing
   - Removing special characters
2. **Feature Engineering**:
   - Sentiment polarity scores
   - Personality features (text length, word count, etc.)
3. **Gemini Integration**:
   - Gemini provides context-aware embeddings for text analysis.

---

## Models Used

### Logistic Regression

- **Input**: TF-IDF features combined with sentiment and personality features.
- **Output**: Binary classification (`suicide` or `non-suicide`).
- **Performance**:
  - **Accuracy**: 94%
  - **Classification Report**: Detailed performance metrics for each class.

---

### GRU Model

- **Input**: Text embeddings, sentiment features, and personality features.
- **Architecture**:
  - Embedding Layer
  - GRU Layer
  - Fully Connected Layers
- **Performance**:
  - Before Adding Personality Features:
    - **Accuracy**: ~92%
  - After Adding Personality Features:
    - **Accuracy**: ~95%

---

### Gemini Integration

- **Purpose**: Enhances contextual understanding of the text.
- **Role**:
  - Analyzes text semantics.
  - Improves sentiment classification accuracy.
- **Output**: Context-aware sentiment scores used alongside GRU and Logistic Regression models.

---

## Frontend

### Angular Application

- Built with **Angular 16** for a responsive and dynamic user interface.
- Key Features:
  - **Real-Time Input**: Accepts user text for classification.
  - **Visualization**: Displays predictions, sentiment scores, and personality metrics.
  - **Model Comparison**: Allows users to compare predictions across GRU, Logistic Regression, and Gemini.

### Backend Integration

- RESTful API developed in **Flask**.
- API endpoints:
  - `/predict`: Returns predictions from GRU and Logistic Regression.
  - `/analyze`: Provides sentiment and personality analysis for the input text.
  - `/gemini`: Integrates Gemini’s predictions for advanced insights.

---

## Evaluation

### Metrics

- **Accuracy**: Measures overall performance.
- **Precision, Recall, F1-Score**: Evaluates per-class performance.
- **Loss and Accuracy Curves**: Visualize training and validation progress over epochs.

### Visualizations

- **Frontend Charts**:
  - Real-time performance metrics displayed using Angular charts.
- **Training Visualizations**:
  - Loss and accuracy trends plotted for GRU fine-tuning.

---

## Results

| Model                 | Features                        | Accuracy |
|-----------------------|---------------------------------|----------|
| Logistic Regression   | Sentiment + Personality         | 94%      |
| GRU Model             | Sentiment Only                  | 92%      |
| GRU Model             | Sentiment + Personality         | 95%      |
| Gemini                | Contextual Sentiment            | ~96%     |

---

## Usage

### Running the Backend Models

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/suicide-ideation-detection.git
   cd suicide-ideation-detection
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the Flask backend:
   ```bash
   python app.py
   ```

---

### Running the Angular Frontend

1. Navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   ng serve
   ```

4. Access the application at:
   ```bash
   http://localhost:4200
   ```

---

## Dependencies

### Backend

- Python 3.7+
- TensorFlow 2.x
- scikit-learn
- TextBlob
- Flask

### Frontend

- Angular 16
- Bootstrap 5
- Chart.js

---

## Future Work

- Deploy the project on cloud platforms for real-time usage.
- Integrate more personality models for deeper insights.
- Explore transformer-based architectures (e.g., BERT, GPT) for text analysis.
- Enhance Gemini integration with more fine-tuning for suicide ideation detection.

---

Feel free to fork this repository and contribute! 🎉
