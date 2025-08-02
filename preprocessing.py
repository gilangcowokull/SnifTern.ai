import re
import html
import pandas as pd
from bs4 import BeautifulSoup

def preprocess_text(text):
    """
    Clean and preprocess text by removing HTML tags, punctuation, 
    special characters, and converting to lowercase
    """
    if pd.isna(text) or text == '':
        return ''
    
    # Convert to string if not already
    text = str(text)
    
    # Decode HTML entities
    text = html.unescape(text)
    
    # Remove HTML tags using BeautifulSoup
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text()
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and punctuation (keep alphanumeric and spaces)
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading and trailing whitespace
    text = text.strip()
    
    return text

def clean_extracted_text(text):
    """
    Clean text extracted from OCR or web scraping
    """
    if not text or text.strip() == '':
        return ''
    
    # Basic cleaning
    text = text.strip()
    
    # Remove excessive newlines and spaces
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip() 