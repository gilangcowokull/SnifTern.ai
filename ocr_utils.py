import pytesseract
from PIL import Image
import io
from preprocessing import clean_extracted_text
import os

def check_tesseract_installation():
    """
    Check if Tesseract is properly installed
    """
    try:
        # Try to get Tesseract version
        version = pytesseract.get_tesseract_version()
        return True, f"Tesseract {version} is installed"
    except Exception as e:
        return False, str(e)

def extract_text_from_image(image):
    """
    Extract text from an uploaded image using OCR
    """
    try:
        # First check if Tesseract is installed
        tesseract_installed, message = check_tesseract_installation()
        
        if not tesseract_installed:
            print(f"❌ Tesseract OCR is not installed: {message}")
            print("""
            **To fix this issue:**
            
            1. **Download Tesseract**: Go to https://github.com/UB-Mannheim/tesseract/wiki
            2. **Install**: Run the installer and make sure to check "Add to PATH"
            3. **Restart**: Restart your terminal/command prompt
            4. **Alternative**: Use the URL input method instead
            
            See `TESSERACT_INSTALLATION.md` for detailed instructions.
            """)
            return ""
        
        # Convert streamlit uploaded file to PIL Image
        if hasattr(image, 'read'):
            img = Image.open(io.BytesIO(image.read()))
        else:
            img = Image.open(image)
        
        # Extract text using pytesseract
        text = pytesseract.image_to_string(img)
        
        # Clean the extracted text
        cleaned_text = clean_extracted_text(text)
        
        if not cleaned_text.strip():
            print("⚠️ No text could be extracted from the image. Please ensure the image contains clear, readable text.")
        
        return cleaned_text
    
    except Exception as e:
        print(f"Error extracting text from image: {str(e)}")
        print("""
        **Troubleshooting tips:**
        
        - Make sure the image contains clear, readable text
        - Try a different image format (JPG, PNG)
        - Ensure Tesseract is properly installed
        - Use the URL input method as an alternative
        """)
        return ""

def is_valid_image(image):
    """
    Check if the uploaded file is a valid image
    """
    try:
        if hasattr(image, 'read'):
            img = Image.open(io.BytesIO(image.read()))
        else:
            img = Image.open(image)
        
        # Reset file pointer
        if hasattr(image, 'seek'):
            image.seek(0)
        
        return True
    except Exception:
        return False

def get_ocr_status():
    """
    Get the current OCR status and provide helpful information
    """
    installed, message = check_tesseract_installation()
    
    if installed:
        return True, f"✅ {message}"
    else:
        return False, f"❌ {message}" 