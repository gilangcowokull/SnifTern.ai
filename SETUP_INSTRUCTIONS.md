# Setup Instructions for Fake Job Posting Detector

## Quick Start Guide

### 1. Prerequisites Installation

**For Windows:**
1. Install Tesseract OCR:
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Install to default location (usually `C:\Program Files\Tesseract-OCR`)
   - Add to PATH: `C:\Program Files\Tesseract-OCR`

**For macOS:**
```bash
brew install tesseract
```

**For Linux:**
```bash
sudo apt-get install tesseract-ocr
```

### 2. Python Dependencies

All dependencies are already installed! The system includes:
- pandas, numpy, scikit-learn for ML
- streamlit for web interface
- pytesseract for OCR
- beautifulsoup4 for web scraping
- requests for HTTP requests

### 3. Model Training (Already Done!)

The model has been trained successfully with:
- **Accuracy: 97.51%**
- **Model files saved in `model/` folder**
- **Ready to use immediately**

### 4. Running the Application

**Start the Streamlit app:**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## How to Use the App

### Option 1: Upload Screenshot
1. Select "📷 Upload Screenshot" in the sidebar
2. Upload a JPG/PNG image of a job posting
3. Click "Extract Text from Image"
4. Review the extracted text
5. Click "🔍 Detect Fake Job" for analysis

### Option 2: Paste Job Link
1. Select "🔗 Paste Job Link" in the sidebar
2. Enter the job posting URL
3. Click "Extract Text from URL"
4. Review the extracted text
5. Click "🔍 Detect Fake Job" for analysis

## Project Files Overview

- `app.py` - Main Streamlit web application
- `train_model.py` - Model training script (already executed)
- `preprocessing.py` - Text cleaning utilities
- `ocr_utils.py` - Image text extraction
- `scraping_utils.py` - Web scraping utilities
- `prediction_utils.py` - Model prediction functions
- `model/` - Trained model files
- `fake_job_postings.csv` - Training dataset

## Model Performance

- **Algorithm**: Logistic Regression with TF-IDF vectorization
- **Features**: 3000 most important words/phrases
- **Accuracy**: 97.51% on test set
- **Threshold**: 40% confidence for fake job detection

## Troubleshooting

### Common Issues:

1. **Tesseract not found**:
   - Ensure Tesseract is installed and in PATH
   - Restart terminal after installation

2. **Model files missing**:
   - Model is already trained and saved
   - Files are in `model/` folder

3. **OCR not working**:
   - Use clear, high-quality images
   - Ensure text is readable in the image

4. **Web scraping issues**:
   - Check if URL is accessible
   - Some websites may block scraping

## Test the System

Run the test script to verify everything works:
```bash
python test_model.py
```

## Features

✅ **OCR Text Extraction** - Extract text from job posting screenshots
✅ **Web Scraping** - Extract text from job posting URLs  
✅ **ML-Powered Detection** - 97.51% accuracy in detecting fake jobs
✅ **Confidence Scoring** - Percentage-based confidence levels
✅ **Modern UI** - Beautiful Streamlit interface
✅ **Modular Code** - Well-organized, maintainable codebase

## Security Note

⚠️ **This tool is for educational purposes only.** Always verify job postings through official channels. The model's predictions should not be the sole basis for decision-making.

## Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Ensure all prerequisites are installed
3. Verify the model files exist in the `model/` folder
4. Check that Tesseract OCR is properly installed

The system is ready to use! 🚀 