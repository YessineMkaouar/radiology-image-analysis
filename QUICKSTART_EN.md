# 🚀 Quick Start Guide - AI Radiology Analysis Assistant

## For Windows Users

1. **Run the automated setup:**
   ```bash
   start_en.bat
   ```

2. **Or manually:**
   ```bash
   python start_en.py
   ```

## For Linux/Mac Users

1. **Make the script executable:**
   ```bash
   chmod +x start_en.sh
   ```

2. **Run the automated setup:**
   ```bash
   ./start_en.sh
   ```

3. **Or manually:**
   ```bash
   python3 start_en.py
   ```

## 🔑 API Configuration

1. Get your Gemini API key from: https://makersuite.google.com/app/apikey
2. Open the `.env` file and replace `your_gemini_api_key_here` with your actual key

## 🏥 Using the Application

1. Open your browser to http://localhost:7860
2. Upload a radiology image (DICOM, PNG, JPG, etc.)
3. Click "Analyze Image"
4. View the detailed medical report

## ⚠️ Important Notes

- This is an AI assistant tool, NOT a medical diagnosis device
- Always consult qualified medical professionals
- Keep your API key secure and never share it publicly

## 🆘 Troubleshooting

- **Port already in use:** The application will automatically find an available port
- **API errors:** Check your internet connection and API key
- **Image format issues:** Try converting to PNG or JPG format
- **Installation problems:** Run `diagnostic.py` to check your environment

For more details, see the complete `README_EN.md` file.
