import joblib
import streamlit as st
from preprocessing import preprocess_text
import os

class FakeJobPredictor:
    def __init__(self, model_dir='model'):
        """
        Initialize the predictor with trained model and vectorizer
        """
        self.model_path = os.path.join(model_dir, 'fake_job_model.pkl')
        self.vectorizer_path = os.path.join(model_dir, 'tfidf_vectorizer.pkl')
        
        # Load model and vectorizer
        try:
            self.model = joblib.load(self.model_path)
            self.vectorizer = joblib.load(self.vectorizer_path)
            st.success("Model loaded successfully!")
        except FileNotFoundError:
            st.error("Model files not found. Please run train_model.py first.")
            self.model = None
            self.vectorizer = None
    
    def predict(self, text, threshold=0.6):
        """
        Predict if a job posting is fake or real
        Returns: (prediction, confidence_score, is_fake)
        """
        if self.model is None or self.vectorizer is None:
            return None, 0, False
        
        try:
            # Preprocess the text
            processed_text = preprocess_text(text)
            
            if not processed_text.strip():
                return "No text to analyze", 0, False
            
            # Vectorize the text
            text_vector = self.vectorizer.transform([processed_text])
            
            # Get prediction probability
            proba = self.model.predict_proba(text_vector)[0]
            
            # Get prediction (0 = real, 1 = fake)
            prediction = self.model.predict(text_vector)[0]
            
            # Calculate confidence score (how real the job is)
            if prediction == 0:  # Real
                confidence_score = proba[0] * 100
                is_fake = False
            else:  # Fake
                confidence_score = proba[1] * 100
                is_fake = True
            
            return prediction, confidence_score, is_fake
            
        except Exception as e:
            st.error(f"Error making prediction: {str(e)}")
            return None, 0, False
    
    def get_prediction_result(self, text, threshold=0.4):
        """
        Get formatted prediction result
        """
        prediction, confidence_score, is_fake = self.predict(text, threshold)
        
        if prediction is None:
            return "Error", 0, "❌"
        
        # Determine if it's likely fake based on threshold
        # Lower threshold for better sensitivity to fake jobs
        if is_fake and confidence_score > (threshold * 100):
            result = "Likely FAKE ❌"
        else:
            result = "Likely REAL ✅"
        
        return result, confidence_score, "❌" if is_fake else "✅" 