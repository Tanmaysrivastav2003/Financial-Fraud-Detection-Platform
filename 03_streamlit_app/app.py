# ======================================================================================
# 0. LIBRARIES AND SETTINGS
# ======================================================================================
import streamlit as st
import pandas as pd
import joblib
import shap
import streamlit.components.v1 as components
import os
from sklearn.preprocessing import LabelEncoder
import numpy as np

st.set_page_config(page_title="Fraud Detection App", layout="wide")

# ======================================================================================
# 1. LOAD THE SAVED ARTIFACTS
# ======================================================================================
@st.cache_resource
def load_artifacts():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    artifacts_path = os.path.join(project_root, "models", "fraud_detection_artifacts.pkl")
    
    if not os.path.exists(artifacts_path):
        st.error("Model artifacts not found! Please run the 'final-model.ipynb' notebook.")
        return None
    
    return joblib.load(artifacts_path)

artifacts = load_artifacts()

if artifacts:
    model = artifacts['model']
    scaler = artifacts['scaler']
    explainer = artifacts['explainer']
    features = artifacts['features']
    st.success("Model and artifacts loaded successfully!")
else:
    st.stop()

# ======================================================================================
# 2. DEFINE THE USER INTERFACE (UI)
# ======================================================================================
st.title("Simplified Fraud Detection App")
st.sidebar.header("Input Transaction Details")

def user_input_features():
    data = {
        'age': st.sidebar.slider('Age', 18, 100, 35),
        'kyc_status': st.sidebar.selectbox('KYC Status', ('complete', 'incomplete')),
        'days_since_kyc_incomplete': st.sidebar.number_input('Days Since KYC Incomplete', 0, 365, 0),
        'transaction_amount': st.sidebar.number_input('Transaction Amount ($)', 10.0, 200000.0, 5000.0),
        'transaction_method': st.sidebar.selectbox('Transaction Method', ('card', 'online', 'cash', 'upi')),
        'transaction_category': st.sidebar.selectbox('Transaction Category', ('food', 'travel', 'loan', 'recreation')),
        'transaction_time': st.sidebar.slider('Transaction Time (0-23h)', 0, 23, 14),
        'average_expenditure': st.sidebar.number_input('Average Expenditure ($)', 100.0, 100000.0, 1500.0),
        'comparison_with_avg_expenditure': st.sidebar.number_input('Transaction vs. Avg Exp.', -50000.0, 190000.0, 3500.0),
        'transaction_count_7_days': st.sidebar.slider('Transactions in Last 7 Days', 1, 50, 10),
        'suspicion_indicator': st.sidebar.selectbox('Manual Suspicion Flag', (0, 1)),
    }
    feature_df = pd.DataFrame(data, index=[0])
    return feature_df

input_df = user_input_features()

# ======================================================================================
# 3. PREDICT AND EXPLAIN
# ======================================================================================
st.subheader("User Input")
st.write(input_df)

if st.button("Predict Fraud Status"):
    processed_df = input_df.copy()
    
    for col in processed_df.select_dtypes(include=['object']).columns:
        processed_df[col] = LabelEncoder().fit_transform(processed_df[col])
        
    processed_df = processed_df[features]
    scaled_input = scaler.transform(processed_df)
    prediction = model.predict(scaled_input)[0]
    prediction_proba = model.predict_proba(scaled_input)[0]

    st.subheader("Prediction")
    if prediction == 1:
        st.error(f"FRAUD DETECTED (Probability: {prediction_proba[1]*100:.2f}%)")
    else:
        st.success(f"Transaction is likely NOT FRAUDULENT (Probability: {prediction_proba[0]*100:.2f}%)")

    st.subheader("Prediction Explanation")
    
    # ================================================================================
    # The Final, Modern, Correct Plotting Method
    # ================================================================================
    
    # Define a function to render the SHAP plot using Streamlit Components
    def st_shap(plot, height=None):
        shap_html = f"<head>{shap.getjs()}</head><body>{plot.html()}</body>"
        components.html(shap_html, height=height)

    # Calculate SHAP explanation object for the single prediction
    explanation = explainer(scaled_input)
    
    # Create the force plot object for the fraud class (class 1)
    force_plot = shap.force_plot(
        explanation.base_values[0][1], # Base value for class 1
        explanation.values[0][:,1],    # SHAP values for class 1
        processed_df.iloc[0]           # User input features for labeling
    )
    
    # Display the plot
    st_shap(force_plot, 400)

    st.markdown("""
    **How to read this chart:** Red features push the prediction score higher (towards fraud), while blue features push it lower.
    """)