"""
Utility functions for background removal and image processing
"""
import os
import requests
from collections import Counter
from PIL import Image, ImageOps
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_most_common_corner_color(image, sample_size=3):
    """
    Sample pixels from each corner and return the most common color.
    
    Args:
        image: PIL Image object
        sample_size: Number of pixels to sample from each corner (default: 3)
    
    Returns:
        Tuple of RGB values (r, g, b) of the most common color
    """
    try:
        image = image.convert('RGB')
        width, height = image.size
        
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
            coordinates = corner_samplers[corner]()
            for x, y in coordinates:
                pixel_color = image.getpixel((x, y))
                corner_pixels.append(pixel_color)
        
        # Count color occurrences
        color_counter = Counter(corner_pixels)
        
        # Get the most common color
        most_common_color = color_counter.most_common(1)[0][0]
        
        return most_common_color
        
    except Exception as e:
        # Fallback to white if there's an error
        return (255, 255, 255)

def rgb_to_hex(rgb_tuple):
    """Convert RGB tuple to hex color string"""
    r, g, b = rgb_tuple
    return f"#{r:02x}{g:02x}{b:02x}".upper()

def add_background_padding(image, color, width, height):
    """
    Add a background color padding to the image
    
    Args:
        image: PIL Image object
        color: RGB tuple for background color
        width: Target width
        height: Target height
    
    Returns:
        PIL Image with padding
    """
    target_size = (width, height)
    
    padded = ImageOps.pad(
        image,
        target_size,
        color=color,
        centering=(0.5, 0.05),  # x=0.5 → center horizontally, y=0.05 → 5% from top
    )
    
    return padded

def remove_background_api(image_bytes, corner_hex, output_width=4500, output_height=5400):
    """
    Remove background using vectorizer.ai API
    
    Args:
        image_bytes: Image data as bytes
        corner_hex: Hex color to remove (e.g., '#FFFFFF')
        output_width: Output image width
        output_height: Output image height
    
    Returns:
        Tuple of (success: bool, result_bytes: bytes or error_message: str)
    """
    api_key = os.getenv('VECTORIZER_API_KEY')
    api_secret = os.getenv('VECTORIZER_SECRET')
    
    if not api_key or not api_secret:
        return False, "API credentials not found. Please set VECTORIZER_API_KEY and VECTORIZER_SECRET in .env file"
    
    try:
        response = requests.post(
            'https://vectorizer.ai/api/v1/vectorize',
            files={'image': image_bytes},
            data={
                'mode': 'test_preview',
                'policy.retention_days': '0',
                'processing.palette': f'{corner_hex} -> #00000000 ~ 0.05;',
                'output.file_format': 'png',
                'output.size.width': str(output_width),
                'output.size.height': str(output_height),
                'processing.shapes.min_area_px': '1.0',
            },
            auth=(api_key, api_secret)
        )
        
        if response.status_code == 200:
            return True, response.content
        else:
            return False, f"API Error: {response.status_code} - {response.text}"
            
    except Exception as e:
        return False, f"Exception: {str(e)}"
