#!/usr/bin/env python3
"""
Crop portrait for circular display on jayspudvilas.com and glasscase.org
Creates a square crop focused on face/upper body for circular presentation
"""
from PIL import Image
import sys

def crop_portrait_for_circle(input_path, output_path, size=800):
    """
    Crop portrait to square format optimized for circular display
    Focus on center where head/shoulders are positioned
    """
    img = Image.open(input_path)
    width, height = img.size
    
    print(f"Original size: {width}x{height}")
    
    # For circular avatars, the crop must be centered on the face.
    # The previous crop drifted too far SW (arm/knee dominated), especially on mobile.
    # Strategy: slightly larger crop + shift NE so head/shoulders sit near center.

    crop_size = int(height * 0.8)

    left = int(width * 0.11)
    top = int(height * 0.0)
    right = left + crop_size
    bottom = top + crop_size
    
    # Ensure we don't exceed image bounds
    if right > width:
        right = width
        left = right - crop_size
    
    if bottom > height:
        bottom = height
        top = bottom - crop_size
    
    print(f"Crop box: left={left}, top={top}, right={right}, bottom={bottom}")
    
    # Crop the image
    cropped = img.crop((left, top, right, bottom))
    
    # Resize to target size for web optimization
    cropped_resized = cropped.resize((size, size), Image.Resampling.LANCZOS)
    
    # Save with optimization
    cropped_resized.save(output_path, 'PNG', optimize=True, quality=95)
    
    print(f"Saved cropped portrait: {size}x{size} to {output_path}")
    return cropped_resized.size

if __name__ == "__main__":
    input_file = "/Users/jsp/jayspudvilas/jsp-portrait.JPEG"
    
    # Create optimized versions for both sites
    jayspudvilas_output = "/Users/jsp/jayspudvilas/portrait.png"
    glasscase_output = "/Users/jsp/glasscase/portrait.png"
    
    # Create 800x800 version (high quality for retina displays)
    crop_portrait_for_circle(input_file, jayspudvilas_output, size=800)
    crop_portrait_for_circle(input_file, glasscase_output, size=800)
    
    print("\n✓ Portrait updated for both websites")
    print(f"  - jayspudvilas.com: {jayspudvilas_output}")
    print(f"  - glasscase.org: {glasscase_output}")
