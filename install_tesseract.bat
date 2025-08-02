@echo off
echo Installing Tesseract OCR...
echo.

echo Method 1: Trying winget installation...
winget install UB-Mannheim.TesseractOCR --accept-source-agreements --accept-package-agreements

echo.
echo Method 2: If winget fails, please download manually:
echo 1. Go to: https://github.com/UB-Mannheim/tesseract/wiki
echo 2. Download: tesseract-ocr-w64-setup-5.4.0.20240606.exe
echo 3. Run the installer as Administrator
echo 4. Make sure to check "Add to PATH" during installation
echo 5. Restart your terminal after installation

echo.
echo After installation, test with: tesseract --version
pause 