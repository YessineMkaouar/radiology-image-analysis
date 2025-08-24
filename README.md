
# AI Radiology Analysis Assistant

> An intelligent assistant for radiological image analysis using Gemini 2.5 Pro and a modern Gradio interface.

## 🎯 Features

- **Automated analysis** of radiological images (X-rays, mammograms, 2D scans)
- **Intuitive user interface** developed with Gradio
- **Structured reports** in French following medical standards
- **Multi-format support**: JPEG, PNG, TIFF, BMP, DICOM
- **Advanced clinico-radiological correlation**

## ⚠️ Medical Disclaimer

**This tool is intended for educational and assistance purposes only.**

- Results do NOT replace professional medical diagnosis
- Always consult a qualified radiologist for definitive diagnosis
- Do not use for critical medical decisions

## 🚀 Quick Installation

### Prerequisites

- Python 3.8 or higher
- Google Gemini API Key ([Get here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone or download the project**

   ```bash
   git clone <repository-url>
   cd radiology-image-analysis
   ```
2. **Run the startup script**

   ```bash
   python start.py
   ```

   The script will automatically:

   - Check Python version
   - Install all dependencies
   - Create configuration file
   - Launch the application
3. **Configure API key**

   - Open the created `.env` file
   - Replace `your_gemini_api_key_here` with your actual Gemini API key
   - Restart the application
4. **Access the interface**

   - Open your browser to: http://localhost:7860

## 🛠️ Manual Installation

If you prefer manual installation:

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API key

# Launch application
python app.py
```

## 📋 Usage

### 1. Web Interface

1. **Upload a radiological image** (supported formats: JPEG, PNG, TIFF, BMP, DICOM)
2. **Enter clinical information** (required)
3. **Complete patient information** (optional)
4. **Click "Analyze Radiological Image"**
5. **Review the generated report**

### 2. Report Structure

The generated report follows a standardized medical structure:

- **Header**: Patient and examination information
- **Clinical information**: Provided medical context
- **Analytical description**: Objective observation of radiological signs
- **Synthesis and differential diagnosis**: Clinico-radiological correlation
- **Impression/Conclusion**: Probable diagnosis and recommendations

### 3. Clinical Information Examples

```
53-year-old male patient, smoker, referred for worsening C8-T1 
cervicobrachial neuralgia. Presents with left upper limb pain and 
slight muscular atrophy of the shoulder.
```

```
45-year-old female patient, non-smoker, consulting for persistent 
cough for 3 weeks with mild exertional dyspnea. Family history 
of lung cancer.
```

## 🔧 Advanced Configuration

### Environment Variables

`.env` file:

```
GOOGLE_API_KEY=your_actual_gemini_api_key
```

### Prompt Customization

The analysis prompt can be customized in `radiology_analyzer.py` in the `create_analysis_prompt()` method.

## 📁 Project Structure

```
radiology-image-analysis/
├── app.py                 # Main Gradio application
├── radiology_analyzer.py  # Gemini analysis engine
├── start.py              # Automatic startup script
├── requirements.txt      # Python dependencies
├── .env                  # Configuration (created automatically)
├── README.md            # Documentation
└── examples/            # Example images (optional)
```

## 🐛 Troubleshooting

### Error: "Import could not be resolved"

This is normal before dependency installation. Run `python start.py` to automatically install all required packages.

### Error: "API key not configured"

1. Check that the `.env` file exists
2. Ensure your Gemini API key is correctly configured
3. Restart the application

### Error: "Invalid image"

- Check that the image format is supported (JPEG, PNG, TIFF, BMP, DICOM)
- Ensure the image is not corrupted
- Check that the image size is sufficient (minimum 100x100 pixels)

### Performance Issues

- Use reasonable resolution images (max 1024x1024)
- Check your internet connection for API calls
- DICOM images may take longer to process

## 🔐 Security and Privacy

- **Local data**: Images are processed locally before sending to API
- **No storage**: No images are saved on our servers
- **Gemini API**: Data transits through Google servers according to their terms
- **Responsibility**: User is responsible for GDPR/HIPAA compliance

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the project
2. Create a branch for your feature
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is under MIT license. See the `LICENSE` file for more details.

## 🆘 Support

For help:

1. Consult this documentation
2. Check [GitHub Issues](issues)
3. Create a new issue if necessary

## 🔮 Roadmap

- [ ] Advanced DICOM image support
- [ ] Integration of specialized models by examination type
- [ ] PDF report export
- [ ] REST API for integration
- [ ] Batch mode for processing multiple images
- [ ] Multilingual support (English, Spanish)

---

**Developed with ❤️ for the medical community**

*Last updated: August 2025*
