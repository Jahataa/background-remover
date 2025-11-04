# Either use the sample code below, or this SDK: https://pypi.org/project/vectorizer-ai/
# Requires "requests" and "python-dotenv" to be installed
import os
import glob
import requests
from dotenv import load_dotenv
from pathlib import Path
from collections import Counter
from PIL import Image, ImageOps

# Load environment variables from .env file
load_dotenv()

def get_most_common_corner_color(image_path, sample_size=3):
    """
    Sample pixels from each corner and return the most common color.
    
    Args:
        image_path: Path to the image file
        sample_size: Number of pixels to sample from each corner (default: 3)
    
    Returns:
        Tuple of RGB values (r, g, b) of the most common color
    """
    try:
        print(f"  🔍 Analyzing corners in image...")
        image = Image.open(image_path)
        image = image.convert('RGB')
        width, height = image.size
        print(f"  📐 Image dimensions: {width}x{height} pixels")
        print(f"  🎯 Sampling {sample_size}x{sample_size} pixels from each corner")
        
        corner_pixels = []
        
        # Define corner sampling functions
        def sample_top_left():
            return [(i, j) for i in range(min(sample_size, width)) for j in range(min(sample_size, height))]
        
        def sample_top_right():
            start_x = max(0, width - sample_size)
            return [(start_x + i, j) for i in range(min(sample_size, width)) for j in range(min(sample_size, height))]
        
        def sample_bottom_left():
            start_y = max(0, height - sample_size)
            return [(i, start_y + j) for i in range(min(sample_size, width)) for j in range(min(sample_size, height))]
        
        def sample_bottom_right():
            start_x = max(0, width - sample_size)
            start_y = max(0, height - sample_size)
            return [(start_x + i, start_y + j) for i in range(min(sample_size, width)) for j in range(min(sample_size, height))]
        
        # Dictionary mapping (like a switch statement)
        corner_samplers = {
            'top-left': sample_top_left,
            'top-right': sample_top_right,
            'bottom-left': sample_bottom_left,
            'bottom-right': sample_bottom_right
        }
        
        # Sample from each corner using the mapping
        for corner in corner_samplers:
            print(f"  📍 Sampling {corner} corner...")
            coordinates = corner_samplers[corner]()
            corner_pixel_count = 0
            for x, y in coordinates:
                pixel_color = image.getpixel((x, y))
                corner_pixels.append(pixel_color)
                corner_pixel_count += 1
            print(f"     ➤ Collected {corner_pixel_count} pixels from {corner}")
        
        print(f"  📊 Total pixels collected: {len(corner_pixels)}")
        
        # Count color occurrences
        color_counter = Counter(corner_pixels)
        
        # Get the most common color
        most_common_color = color_counter.most_common(1)[0][0]
        most_common_count = color_counter.most_common(1)[0][1]
        
        print(f"  🏆 Most common color appears {most_common_count}/{len(corner_pixels)} times")
        print(f"  🎨 Top 3 colors found:")
        for i, (color, count) in enumerate(color_counter.most_common(3), 1):
            hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}".upper()
            percentage = (count / len(corner_pixels)) * 100
            print(f"     {i}. {hex_color} RGB{color} - {count} pixels ({percentage:.1f}%)")
        
        return most_common_color
        
    except Exception as e:
        print(f"⚠️  Error analyzing corners for {image_path}: {str(e)}")
        # Fallback to white if there's an error
        return (255, 255, 255)

def rgb_to_hex(rgb_tuple):
    """Convert RGB tuple to hex color string"""
    r, g, b = rgb_tuple
    return f"#{r:02x}{g:02x}{b:02x}".upper()

# Load environment variables from .env file
load_dotenv()

# Get API credentials from environment variables
api_key = os.getenv('VECTORIZER_API_KEY')
api_secret = os.getenv('VECTORIZER_SECRET')

def get_background_color_from_corner(image_path):
    """Get background color from top-right corner and format for vectorizer API"""
    image = Image.open(image_path)
    image = image.convert('RGB')
    width, height = image.size
    
    # Get top-right pixel
    r, g, b = image.getpixel((width - 1, 0))
    
    # Convert to hex format for the API
    hex_color = f"#{r:02x}{g:02x}{b:02x}".upper()
    
    return hex_color

if not api_key or not api_secret:
    raise ValueError("Please set VECTORIZER_API_KEY and VECTORIZER_SECRET in your .env file")


# Prompt user for output dimensions
print("\n" + "="*60)
print("🖼️  OUTPUT SIZE CONFIGURATION")
print("="*60)
print("Please enter the desired output dimensions:")
print("(Press Enter to use defaults: 4500x5400)")

output_width = input("\n📏 Enter output width (px): ").strip()
output_height = input("📏 Enter output height (px): ").strip()

# Use defaults if user doesn't provide values
if not output_width:
    output_width = "4500"
    print(f"   ℹ️  Using default width: {output_width}px")
else:
    print(f"   ✓ Width set to: {output_width}px")

if not output_height:
    output_height = "5400"
    print(f"   ℹ️  Using default height: {output_height}px")
else:
    print(f"   ✓ Height set to: {output_height}px")

print("="*60)

# Prompt user for padding preference
print("\n" + "="*60)
print("🎨 BACKGROUND PADDING CONFIGURATION")
print("="*60)
print("Do you want to add background padding to images before processing?")
print("(This adds a colored background to match corner colors)")
print()
print("Options:")
print("  1. Yes - Add background padding")
print("  2. No - Skip padding (process original images)")

padding_choice = input("\n👉 Enter your choice (1 or 2): ").strip()

if padding_choice == "1":
    use_padding = True
    print("   ✓ Background padding ENABLED")
elif padding_choice == "2":
    use_padding = False
    print("   ✓ Background padding DISABLED")
else:
    use_padding = True
    print(f"   ℹ️  Invalid choice '{padding_choice}', defaulting to YES (padding enabled)")

print("="*60)

def add_background_bottom(image_path: str, color: tuple, width: int, height: int) -> None:
    """Add a background color to the bottom of the image"""

    target_size = (width, height)
    image_name = Path(image_path).stem
    image = Image.open(image_path)
    
    padded = ImageOps.pad(
        image,
        target_size,
        color=color,
        centering=(0.5, 0.01),  # x=0.5 → center horizontally, y=0.01 → 1% from top
    )

    return padded.save(f"./img/{image_name}.png")
img_patterns = ['./imgFix/*.jpg', './imgFix/*.jpeg', './imgFix/*.JPG', './imgFix/*.JPEG', './imgFix/*.png', './imgFix/*.PNG'] 

files = []

if use_padding:
    print(f"\n{'='*60}")
    print("🎨 APPLYING BACKGROUND PADDING")
    print(f"{'='*60}")
    for img in img_patterns:
        files.extend(glob.glob(img))
    
    if not files:
        print("❌ No images found in ./imgFix/ directory for padding")
    else:
        print(f"📁 Found {len(files)} image(s) to pad:")
        for file in files:
            print(f"   - {file}")
        
        for file in files:
            print(f"\n{'─'*40}")
            print(f"🖼️  Processing: {file}")
            corner_color = get_most_common_corner_color(file)
            print(f"  ➕ Adding background padding...")
            add_background_bottom(file, corner_color, int(output_width), int(output_height))
            print(f"  ✅ Padding applied!")
    print(f"{'='*60}\n")
else:
    print(f"\n{'='*60}")
    print("⏭️  SKIPPING BACKGROUND PADDING")
    print(f"{'='*60}\n")

# Choose source directory based on padding choice
if use_padding:
    # If padding was applied, use the ./img directory (padded images)
    source_patterns = ['./img/*.jpg', './img/*.jpeg', './img/*.JPG', './img/*.JPEG', './img/*.png', './img/*.PNG']
    source_dir = "./img/"
else:
    # If padding was skipped, use the ./imgFix directory (original images)
    source_patterns = ['./imgFix/*.jpg', './imgFix/*.jpeg', './imgFix/*.JPG', './imgFix/*.JPEG', './imgFix/*.png', './imgFix/*.PNG']
    source_dir = "./imgFix/"

# Find all image files in the chosen source directory
image_files = []
for pattern in source_patterns:
    image_files.extend(glob.glob(pattern))

if not image_files:
    print(f"❌ No images found in {source_dir} directory")
    exit(1)

print(f"📁 Found {len(image_files)} image(s) to process from {source_dir}:")
for img in image_files:
    print(f"   - {img}")

# Process each image
successful = 0
failed = 0

for image_path in image_files:
    print(f"\n{'='*60}")
    print(f"🔄 Processing: {image_path}")
    print(f"{'='*60}")
    image_name = Path(image_path).stem
    
    # Detect most common corner color for background removal
    corner_color = get_most_common_corner_color(image_path)
    corner_hex = rgb_to_hex(corner_color)
    print(f"\n🎨 Final detected corner color: {corner_hex} RGB{corner_color}")
    
    print(f"\n📤 Uploading to vectorizer.ai...")
    try:
        with open(image_path, 'rb') as image_file:
            print(f"  📝 API settings:")
            print(f"     • Mode: test_preview")
            print(f"     • Background removal: {corner_hex} -> transparent")
            print(f"     • Output format: PNG")
            print(f"     • Min shape area: 1.0px")
            
            response = requests.post(
                'https://vectorizer.ai/api/v1/vectorize',
                files={'image': image_file},
                data={
                    # Enable test mode for free testing
                    'mode': 'test_preview',

                    'policy.retention_days': '0',  # Optional: Set retention policy
                    
                    # Remove detected corner color by mapping it to transparent
                    'processing.palette': f'{corner_hex} -> #00000000 ~ 0.05;',
                    
                    # Output format options
                    'output.file_format': 'png',  # Fixed parameter name
                    'output.size.width': output_width,    # User-specified width
                    'output.size.height': output_height,   # User-specified height

                    # Optional: Reduce small artifacts
                    'processing.shapes.min_area_px': '1.0',
                    
                    # TODO: Add more upload options here
                },
                auth=(api_key, api_secret)
            )
        
        print(f'\n📡 API Response: {response.status_code}')
        
        if response.status_code == requests.codes.ok:
            # Save result with unique filename based on original image name
            output_path = f'./bgone-img/{image_name}.png'
            with open(output_path, 'wb') as out:
                out.write(response.content)
            file_size = len(response.content) / 1024  # KB
            print(f"✅ Success! Saved to: {output_path}")
            print(f"📁 Output file size: {file_size:.1f} KB")
            successful += 1
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            failed += 1
            
    except Exception as e:
        print(f"❌ Exception processing {image_path}: {str(e)}")
        failed += 1

# Summary
print(f"\n{'='*60}")
print(f"📊 PROCESSING SUMMARY")
print(f"{'='*60}")
print(f"   ✅ Successful: {successful}")
print(f"   ❌ Failed: {failed}")
print(f"   📝 Total processed: {len(image_files)}")
if successful > 0:
    success_rate = (successful / len(image_files)) * 100
    print(f"   📈 Success rate: {success_rate:.1f}%")
print(f"{'='*60}")