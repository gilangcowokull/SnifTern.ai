import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import joblib
import re
import os
from preprocessing import preprocess_text

def load_and_preprocess_data(file_path):
    """Load and preprocess the dataset"""
    print("Loading dataset...")
    df = pd.read_csv(file_path)
    
    print("Combining text columns...")
    # Combine text columns (only use available columns)
    text_columns = ['title', 'company_profile', 'description']
    
    # Check which columns exist in the dataset
    available_columns = [col for col in text_columns if col in df.columns]
    print(f"Using columns: {available_columns}")
    
    # Combine available text columns
    df['full_text'] = ''
    for col in available_columns:
        df['full_text'] += df[col].fillna('') + ' '
    
    print("Cleaning text...")
    # Clean the combined text (process in batches for memory efficiency)
    batch_size = 1000
    cleaned_texts = []
    
    for i in range(0, len(df), batch_size):
        batch = df['full_text'].iloc[i:i+batch_size]
        cleaned_batch = batch.apply(preprocess_text)
        cleaned_texts.extend(cleaned_batch.tolist())
        print(f"Processed batch {i//batch_size + 1}/{(len(df)-1)//batch_size + 1}")
    
    df['full_text'] = cleaned_texts
    
    # Drop rows where full_text is empty
    df = df[df['full_text'].str.strip() != '']
    
    print(f"Dataset shape after preprocessing: {df.shape}")
    return df

def train_model(df):
    """Train the machine learning model"""
    print("Vectorizing text...")
    # Initialize TF-IDF vectorizer with optimized parameters
    vectorizer = TfidfVectorizer(
        max_features=3000,  # Reduced for faster processing
        stop_words='english',
        ngram_range=(1, 1),  # Only unigrams for speed
        min_df=2,  # Minimum document frequency
        max_df=0.95  # Maximum document frequency
    )
    
    # Fit and transform the text data
    X = vectorizer.fit_transform(df['full_text'])
    y = df['fraudulent']
    
    print(f"Feature matrix shape: {X.shape}")
    print("Splitting data...")
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print("Training Logistic Regression model...")
    # Train the model
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Print results
    print("\n" + "="*50)
    print("MODEL PERFORMANCE")
    print("="*50)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Real', 'Fake']))
    
    return model, vectorizer, X_test, y_test

def save_model(model, vectorizer, model_dir='model'):
    """Save the trained model and vectorizer"""
    # Create model directory if it doesn't exist
    os.makedirs(model_dir, exist_ok=True)
    
    print(f"Saving model and vectorizer to {model_dir}/...")
    joblib.dump(model, f'{model_dir}/fake_job_model.pkl')
    joblib.dump(vectorizer, f'{model_dir}/tfidf_vectorizer.pkl')
    print("Model and vectorizer saved successfully!")

def main():
    """Main function to run the training pipeline"""
    # Load and preprocess data
    df = load_and_preprocess_data('fake_job_postings.csv')
    
    # Train model
    model, vectorizer, X_test, y_test = train_model(df)
    
    # Save model
    save_model(model, vectorizer)
    
    print("\nTraining completed successfully!")
    print("Model and vectorizer saved in the 'model' folder.")

if __name__ == "__main__":
    main() 