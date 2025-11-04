# 🎨 Background Remover - Streamlit Web App

A modern, browser-based application for removing backgrounds from images using AI-powered vectorization.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## ✨ Features

- 🖼️ **Modern Web Interface** - Clean, intuitive UI built with Streamlit
- 🎯 **Smart Corner Detection** - Automatically detects background colors from image corners
- 🔄 **Real-time Processing** - Upload and process images instantly
- 📐 **Customizable Output** - Adjust output dimensions to your needs
- 💾 **One-Click Download** - Download processed images with transparent backgrounds
- 🎨 **Color Preview** - See the detected background color before processing
- ⚙️ **Flexible Settings** - Configure sample size, padding, and more

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Vectorizer.ai API credentials

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd /Users/jaha/work/python/background-remover
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API credentials:**
   
   Create a `.env` file in the project root:
   ```env
   VECTORIZER_API_KEY=your_api_key_here
   VECTORIZER_SECRET=your_api_secret_here
   ```

### Running the App

**Start the Streamlit app:**
```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## 📖 How to Use

1. **Upload an Image** - Click "Browse files" or drag & drop an image
2. **Adjust Settings** (Optional) - Configure output dimensions and detection parameters in the sidebar
3. **Review Detection** - Check the detected corner color preview
4. **Process Image** - Click "🚀 Remove Background" button
5. **Download Result** - Click "📥 Download Processed Image" to save your file

## ⚙️ Configuration Options

### Sidebar Settings

- **Output Dimensions**: Set custom width and height (default: 4500 × 5400 px)
- **Sample Size**: Number of pixels to sample per corner (1-10, default: 3)
- **Add Padding**: Optionally add background padding before removal

## 📁 Project Structure

```
background-remover/
├── app.py              # Streamlit web application
├── utils.py            # Core image processing functions
├── main.py             # Original batch processing script
├── requirements.txt    # Python dependencies
├── .env               # API credentials (create this)
├── img/               # Input images (for batch processing)
├── imgFix/            # Pre-processed images
└── bgone-img/         # Output images with removed backgrounds
```

## 🛠️ Technical Details

### Technologies Used

- **Streamlit** - Web application framework
- **PIL/Pillow** - Image processing
- **Vectorizer.ai API** - AI-powered background removal
- **Python-dotenv** - Environment variable management

### How It Works

1. **Corner Detection**: Samples pixels from all four corners of the image
2. **Color Analysis**: Identifies the most common color among sampled pixels
3. **API Processing**: Sends image to Vectorizer.ai with color-to-transparent mapping
4. **Result Delivery**: Returns processed PNG with transparent background

## 🎯 Use Cases

- E-commerce product photography
- Profile picture creation
- Graphic design projects
- Social media content
- Presentation materials
- Marketing collateral

## 🐛 Troubleshooting

### API Credentials Error
- Ensure your `.env` file exists and contains valid credentials
- Check that `VECTORIZER_API_KEY` and `VECTORIZER_SECRET` are set correctly

### Image Upload Issues
- Supported formats: JPG, JPEG, PNG
- Check file size limits (API dependent)

### Processing Errors
- Verify internet connection
- Check API quota/limits
- Try reducing output dimensions

## 📝 Original Batch Processing

The original `main.py` script is still available for batch processing multiple images:

```bash
python main.py
```

## 🔒 Privacy & Security

- Images are processed via Vectorizer.ai API
- Set `policy.retention_days: '0'` for immediate deletion after processing
- Store API credentials securely in `.env` file (never commit to version control)

## 📄 License

See LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## 💡 Tips

- Use consistent lighting for better corner detection
- Higher sample sizes provide more accurate color detection
- Test mode is free but adds watermark - upgrade API plan for production use

---

Made with ❤️ using Streamlit
