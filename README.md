# 🎨 Background Remover

An intelligent Python tool that automatically removes backgrounds from images using AI-powered vectorization. The tool detects the background color from image corners and replaces it with transparency, perfect for product photography and image editing workflows.

## ✨ Features

- **Smart Background Detection**: Automatically analyzes corner pixels to determine the most common background color
- **Batch Processing**: Process multiple images at once
- **Flexible Output**: Customize output dimensions (default: 4500x5400px)
- **Pre-processing Support**: Add colored backgrounds before removing them
- **High-Quality Results**: Uses vectorizer.ai API for professional-grade background removal
- **Progress Tracking**: Detailed console output with emoji indicators for easy monitoring

## 📋 Prerequisites

- Python 3.7 or higher
- Vectorizer.ai API credentials ([Get them here](https://vectorizer.ai))
- pip (Python package manager)

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/Jahataa/background-remover.git
cd background-remover
```

### 2. Create a virtual environment (recommended)
```bash
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your environment variables
```bash
cp .env.example .env
```

Edit `.env` and add your Vectorizer.ai credentials:
```bash
VECTORIZER_API_KEY=your_api_key_here
VECTORIZER_SECRET=your_secret_here
```

## 📁 Project Structure

```
background-remover/
├── main.py              # Main script
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── .env                # Your API credentials (create this)
├── imgFix/             # Place original images here for pre-processing
├── img/                # Intermediate images (after adding background)
├── bgone-img/          # Final output (background removed)
└── README.md           # This file
```

## 🎯 Usage

### Basic Workflow

The tool works in two stages:

#### **Stage 1: Add Background (Optional)**
If your images need a uniform background added first:

1. Place your original images in the `imgFix/` folder
   - Supported formats: `.jpg`, `.jpeg`, `.png` (case-insensitive)

2. Run the script:
```bash
python main.py
```

3. The script will:
   - Analyze corner colors
   - Add a background based on detected color
   - Save processed images to `img/` folder

#### **Stage 2: Remove Background**
1. Ensure images are in the `img/` folder
   - Either from Stage 1 or place them manually

2. Run the script:
```bash
python main.py
```

3. When prompted, enter output dimensions:
```
📏 Enter output width (px): 4500
📏 Enter output height (px): 5400
```
   - Press Enter to use defaults (4500x5400)

4. The script will:
   - Detect background color from corners
   - Upload to vectorizer.ai
   - Remove background
   - Save transparent PNG to `bgone-img/`

### Example Output

```
🖼️  OUTPUT SIZE CONFIGURATION
================================================
Please enter the desired output dimensions:
(Press Enter to use defaults: 4500x5400)

📏 Enter output width (px): 
   ℹ️  Using default width: 4500px
📏 Enter output height (px): 
   ℹ️  Using default height: 5400px
================================================

📁 Found 3 JPEG image(s) to process:
   - ./img/product1.jpg
   - ./img/product2.jpg
   - ./img/product3.jpg

============================================================
🔄 Processing: ./img/product1.jpg
============================================================
  🔍 Analyzing corners in image...
  📐 Image dimensions: 3000x3600 pixels
  🎯 Sampling 3x3 pixels from each corner
  🎨 Top 3 colors found:
     1. #FFFFFF RGB(255, 255, 255) - 30 pixels (83.3%)

🎨 Final detected corner color: #FFFFFF RGB(255, 255, 255)

📤 Uploading to vectorizer.ai...
📡 API Response: 200
✅ Success! Saved to: ./bgone-img/product1.png
📁 Output file size: 245.3 KB

============================================================
📊 PROCESSING SUMMARY
============================================================
   ✅ Successful: 3
   ❌ Failed: 0
   📝 Total processed: 3
   📈 Success rate: 100.0%
============================================================
```

## 🔧 Configuration

### Customize Output Size
Edit the default dimensions in the script or enter them when prompted:
```python
output_width = "4500"   # pixels
output_height = "5400"  # pixels
```

### Adjust Corner Sampling
Change the `sample_size` parameter to sample more/fewer pixels:
```python
corner_color = get_most_common_corner_color(file, sample_size=5)  # default is 3
```

### Background Positioning
Modify the centering parameters in `add_background_bottom()`:
```python
centering=(0.5, 0.05)  # x=0.5 (center), y=0.05 (5% from top)
```

## 📦 Dependencies

- **Pillow** (12.0.0): Image processing
- **python-dotenv** (1.1.1): Environment variable management
- **requests** (2.32.5): API communication
- See `requirements.txt` for complete list

## 🔑 API Credentials

Get your free API credentials from [vectorizer.ai](https://vectorizer.ai):
1. Sign up for an account
2. Navigate to API settings
3. Generate API key and secret
4. Add them to your `.env` file

**Note**: The script uses `test_preview` mode which is free for testing.

## 🐛 Troubleshooting

### No images found
- Ensure images are in the correct folder (`imgFix/` or `img/`)
- Check file extensions are supported (jpg, jpeg, png)

### API errors
- Verify your API credentials in `.env`
- Check your internet connection
- Ensure you haven't exceeded API rate limits

### Import errors
- Make sure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Permission errors
- Ensure folders have write permissions
- Run with appropriate user permissions

## 📝 License

This project is licensed under the terms specified in the LICENSE file.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🔗 Resources

- [Vectorizer.ai Documentation](https://vectorizer.ai/api/v1/docs)
- [Pillow Documentation](https://pillow.readthedocs.io/)
- [Python dotenv](https://pypi.org/project/python-dotenv/)

## 💡 Tips

- For best results, use images with uniform backgrounds
- Higher sample sizes provide more accurate color detection but slower processing
- Test mode is free but adds a watermark - upgrade to production mode for clean outputs
- Keep original images as backups in case you need to reprocess

## 📧 Support

For issues or questions, please open an issue on the GitHub repository.

---

Made with ❤️ for effortless background removal
