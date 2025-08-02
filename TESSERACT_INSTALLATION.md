# Tesseract OCR Installation Guide for Windows

## Quick Installation Steps

### Option 1: Download and Install Manually

1. **Download Tesseract for Windows:**
   - Go to: https://github.com/UB-Mannheim/tesseract/wiki
   - Download the latest version (e.g., `tesseract-ocr-w64-setup-5.3.3.20231005.exe`)

2. **Install Tesseract:**
   - Run the downloaded `.exe` file
   - **Important**: Install to default location: `C:\Program Files\Tesseract-OCR`
   - Make sure to check "Add to PATH" during installation

3. **Verify Installation:**
   - Open a new Command Prompt or PowerShell
   - Run: `tesseract --version`
   - You should see version information

### Option 2: Using Chocolatey (if you have it)

```powershell
choco install tesseract
```

### Option 3: Using Winget (Windows Package Manager)

```powershell
winget install UB-Mannheim.TesseractOCR
```

## Adding to PATH Manually (if needed)

If Tesseract is installed but not in PATH:

1. **Find Tesseract installation:**
   - Usually in `C:\Program Files\Tesseract-OCR\`
   - Or `C:\Program Files (x86)\Tesseract-OCR\`

2. **Add to PATH:**
   - Press `Win + R`, type `sysdm.cpl`, press Enter
   - Click "Environment Variables"
   - Under "System Variables", find "Path", click "Edit"
   - Click "New", add: `C:\Program Files\Tesseract-OCR`
   - Click "OK" on all dialogs

3. **Restart your terminal/command prompt**

## Verify Installation

After installation, test with:

```powershell
tesseract --version
```

You should see output like:
```
tesseract 5.3.3
 leptonica-1.83.1
  libgif 5.2.1 : libjpeg 8d (libjpeg-turbo 3.0.1) : libpng 1.6.39 : libtiff 4.5.1 : zlib 1.3 : libwebp 1.3.2 : libopenjp2 2.4.0
```

## Troubleshooting

### Common Issues:

1. **"tesseract is not recognized"**
   - Tesseract is not in PATH
   - Restart your terminal after adding to PATH
   - Check installation location

2. **Permission errors**
   - Run installer as Administrator
   - Check antivirus software

3. **Missing DLL errors**
   - Install Visual C++ Redistributable
   - Download from Microsoft's website

## Alternative: Use URL Input Only

If you can't install Tesseract, you can still use the app by:
1. Taking a screenshot of the job posting
2. Uploading it to an image hosting service
3. Using the URL input method instead

## Support

If you continue having issues:
1. Check the installation path
2. Restart your computer after installation
3. Try running the app with administrator privileges 