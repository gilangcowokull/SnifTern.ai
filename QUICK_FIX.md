# Quick Fix for Tesseract OCR Issue

## 🚨 Current Issue
The app shows: "tesseract is not installed or it's not in your PATH"

## 🔧 Solution Options

### Option 1: Manual Installation (Recommended)

1. **Download Tesseract:**
   - Go to: https://github.com/UB-Mannheim/tesseract/wiki
   - Click on the latest version: `tesseract-ocr-w64-setup-5.4.0.20240606.exe`

2. **Install:**
   - Run the downloaded `.exe` file **as Administrator**
   - Install to default location: `C:\Program Files\Tesseract-OCR`
   - **IMPORTANT**: Check "Add to PATH" during installation

3. **Restart:**
   - Close all terminal windows
   - Open a new terminal
   - Test: `tesseract --version`

### Option 2: Use URL Input Only (No Installation Needed)

If you can't install Tesseract, you can still use the app:

1. **Take a screenshot** of the job posting
2. **Upload to image hosting** (like imgur.com, postimages.org)
3. **Use the URL input method** in the app
4. **Paste the image URL** instead of uploading directly

### Option 3: Alternative OCR Services

You can also:
1. Use online OCR tools (like Google Lens, OCR.space)
2. Copy the text manually
3. Use the URL input method

## 🎯 Quick Test

After installation, test in PowerShell:
```powershell
tesseract --version
```

You should see:
```
tesseract 5.4.0
 leptonica-1.83.1
  libgif 5.2.1 : libjpeg 8d (libjpeg-turbo 3.0.1) : libpng 1.6.39 : libtiff 4.5.1 : zlib 1.3 : libwebp 1.3.2 : libopenjp2 2.4.0
```

## 🚀 After Installation

1. **Restart the app:**
   ```powershell
   streamlit run app.py
   ```

2. **Test OCR:**
   - Upload a screenshot
   - Should work without errors

## 📞 Still Having Issues?

1. Check if Tesseract is in PATH:
   - Press `Win + R`, type `sysdm.cpl`
   - Environment Variables → System Variables → Path
   - Should contain: `C:\Program Files\Tesseract-OCR`

2. Try running as Administrator:
   - Right-click PowerShell → Run as Administrator
   - Install Tesseract again

3. Check antivirus software:
   - Some antivirus may block the installation
   - Temporarily disable and try again 