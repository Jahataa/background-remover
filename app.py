"""
Background Remover - Streamlit Web App
A modern web interface for removing backgrounds from images
"""
import streamlit as st
from PIL import Image
import io
from utils import (
    get_most_common_corner_color,
    rgb_to_hex,
    add_background_padding,
    remove_background_api
)

# Page configuration
st.set_page_config(
    page_title="Background Remover",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        font-weight: 600;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #FF6B6B;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 75, 75, 0.3);
    }
    .upload-text {
        text-align: center;
        padding: 2rem;
        border: 2px dashed #FF4B4B;
        border-radius: 10px;
        background-color: #f8f9fa;
    }
    .success-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        margin: 1rem 0;
    }
    h1 {
        color: #FF4B4B;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# App header
st.title("🎨 Background Remover")
st.markdown("### Transform your images with AI-powered background removal")
st.markdown("---")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Settings")
    
    st.subheader("📐 Output Dimensions")
    output_width = st.number_input(
        "Width (px)",
        min_value=100,
        max_value=10000,
        value=4500,
        step=100,
        help="Output image width in pixels"
    )
    
    output_height = st.number_input(
        "Height (px)",
        min_value=100,
        max_value=10000,
        value=5400,
        step=100,
        help="Output image height in pixels"
    )
    
    st.markdown("---")
    
    st.subheader("🎯 Corner Detection")
    sample_size = st.slider(
        "Sample size per corner",
        min_value=1,
        max_value=10,
        value=3,
        help="Number of pixels to sample from each corner"
    )
    
    st.markdown("---")
    
    st.subheader("🖼️ Processing Options")
    add_padding = st.checkbox(
        "Add background padding",
        value=False,
        help="Add colored padding before background removal"
    )
    
    st.markdown("---")
    
    st.info("💡 **Tip:** Upload an image to get started!")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 Upload Image")
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['jpg', 'jpeg', 'png', 'JPG', 'JPEG', 'PNG'],
        help="Supported formats: JPG, JPEG, PNG"
    )
    
    if uploaded_file is not None:
        # Display original image
        image = Image.open(uploaded_file)
        st.image(image, caption="Original Image", use_container_width=True)
        
        # Get image info
        width, height = image.size
        st.markdown(f"""
        <div class="info-box">
        📊 <strong>Image Info:</strong><br>
        • Dimensions: {width} × {height} pixels<br>
        • Format: {image.format}<br>
        • Mode: {image.mode}
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.subheader("✨ Processed Image")
    
    if uploaded_file is not None:
        # Detect corner color
        corner_color = get_most_common_corner_color(image, sample_size=sample_size)
        corner_hex = rgb_to_hex(corner_color)
        
        # Display detected color
        st.markdown(f"""
        <div class="info-box">
        🎨 <strong>Detected Corner Color:</strong><br>
        • Hex: {corner_hex}<br>
        • RGB: {corner_color}
        </div>
        """, unsafe_allow_html=True)
        
        # Color preview
        st.color_picker("Preview detected color", corner_hex, disabled=True)
        
        # Process button
        if st.button("🚀 Remove Background", type="primary"):
            with st.spinner("Processing image... This may take a few moments."):
                try:
                    # Optional: Add padding first
                    if add_padding:
                        image = add_background_padding(
                            image,
                            corner_color,
                            int(output_width),
                            int(output_height)
                        )
                    
                    # Convert image to bytes
                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format='PNG')
                    img_byte_arr.seek(0)
                    
                    # Remove background via API
                    success, result = remove_background_api(
                        img_byte_arr,
                        corner_hex,
                        int(output_width),
                        int(output_height)
                    )
                    
                    if success:
                        # Display processed image
                        processed_image = Image.open(io.BytesIO(result))
                        st.image(processed_image, caption="Background Removed", use_container_width=True)
                        
                        # Success message
                        st.markdown(f"""
                        <div class="success-box">
                        ✅ <strong>Success!</strong><br>
                        Background removed successfully!<br>
                        Output size: {len(result) / 1024:.1f} KB
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Download button
                        st.download_button(
                            label="📥 Download Processed Image",
                            data=result,
                            file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}_no_bg.png",
                            mime="image/png"
                        )
                    else:
                        st.error(f"❌ Error: {result}")
                        
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")
    else:
        st.info("👈 Upload an image to begin processing")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p><strong>Background Remover</strong> | Powered by Vectorizer.ai API</p>
    <p>Made with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)
