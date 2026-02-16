import streamlit as st
import requests
import json
import numpy as np

st.set_page_config(page_title="Iris Classifier UI", layout="wide")

st.title(" Iris Flower Classifier")
st.markdown("**Predict iris flower species using machine learning**")

# Sidebar configuration
st.sidebar.header("API Configuration")
api_url = st.sidebar.text_input("API URL", value="http://127.0.0.1:8000")

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("Input Measurements")
    
    sepal_length = st.slider(
        "Sepal Length (cm)",
        min_value=0.1,
        max_value=10.0,
        value=5.1,
        step=0.1,
        help="Length of the sepal in centimeters"
    )
    
    sepal_width = st.slider(
        "Sepal Width (cm)",
        min_value=0.1,
        max_value=10.0,
        value=3.5,
        step=0.1,
        help="Width of the sepal in centimeters"
    )
    
    petal_length = st.slider(
        "Petal Length (cm)",
        min_value=0.1,
        max_value=10.0,
        value=1.4,
        step=0.1,
        help="Length of the petal in centimeters"
    )
    
    petal_width = st.slider(
        "Petal Width (cm)",
        min_value=0.0,
        max_value=5.0,
        value=0.2,
        step=0.1,
        help="Width of the petal in centimeters"
    )
    
    # Button to make prediction
    if st.button(" Predict", use_container_width=True):
        payload = {
            "sepal_length": sepal_length,
            "sepal_width": sepal_width,
            "petal_length": petal_length,
            "petal_width": petal_width
        }
        
        try:
            response = requests.post(f"{api_url}/predict", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                
                with col2:
                    st.subheader("Prediction Result")
                    st.success(f"**Predicted Class: {result['prediction']}**")
                    
                    st.metric(
                        "Confidence",
                        f"{result['confidence']*100:.2f}%",
                        delta=f"Index: {result['prediction_index']}"
                    )
                    
                    # Probability chart
                    st.subheader("Class Probabilities")
                    proba_data = {
                        "setosa": result['probabilities'][0],
                        "versicolor": result['probabilities'][1],
                        "virginica": result['probabilities'][2]
                    }
                    st.bar_chart(proba_data)
                    
                    st.caption(f"Timestamp: {result['timestamp']}")
            else:
                st.error(f"Error: {response.status_code} - {response.json().get('detail', 'Unknown error')}")
                
        except requests.exceptions.ConnectionError:
            st.error(f" Cannot connect to API at {api_url}. Is the server running?")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Information section
with st.expander("ℹ About This App"):
    st.write("""
    This app uses a **Random Forest classifier** trained on the famous Iris dataset.
    
    **Features:**
    - Sepal Length: Length of the sepal
    - Sepal Width: Width of the sepal
    - Petal Length: Length of the petal
    - Petal Width: Width of the petal
    
    **Classes:**
    - Setosa
    - Versicolor
    - Virginica
    
    **Model Performance:** 100% accuracy on test set
    """)

# API Health Check
with st.sidebar.expander(" API Status"):
    try:
        health = requests.get(f"{api_url}/health")
        if health.status_code == 200:
            st.success(" API is running")
            st.json(health.json())
        else:
            st.error(" API returned error")
    except:
        st.error(" Cannot reach API")
