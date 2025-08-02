import requests
from bs4 import BeautifulSoup
from preprocessing import clean_extracted_text
import time

def extract_text_from_url(url):
    """
    Extract text from a webpage URL
    """
    try:
        # Add headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Make the request
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Extract text from body
        text = soup.get_text()
        
        # Clean the extracted text
        cleaned_text = clean_extracted_text(text)
        
        return cleaned_text
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {str(e)}")
        return ""
    except Exception as e:
        print(f"Error extracting text from URL: {str(e)}")
        return ""

def is_valid_url(url):
    """
    Basic URL validation
    """
    try:
        if not url.startswith(('http://', 'https://')):
            return False
        return True
    except:
        return False 