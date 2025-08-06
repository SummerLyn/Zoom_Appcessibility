#!/usr/bin/env python3
"""
Image optimization script for the Zoom Accessibility app.
This script compresses and resizes images to improve load times.
"""

import os
from PIL import Image
import glob

def optimize_image(image_path, max_width=800, max_height=600, quality=85):
    """
    Optimize an image by resizing and compressing it.
    
    Args:
        image_path: Path to the image file
        max_width: Maximum width in pixels
        max_height: Maximum height in pixels
        quality: JPEG quality (1-100)
    """
    try:
        with Image.open(image_path) as img:
            # Get original size
            original_size = os.path.getsize(image_path)
            
            # Convert to RGB if necessary (for JPEG compatibility)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Calculate new dimensions while maintaining aspect ratio
            width, height = img.size
            if width > max_width or height > max_height:
                img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Create optimized filename
            base, ext = os.path.splitext(image_path)
            optimized_path = f"{base}_optimized{ext}"
            
            # Save optimized image
            img.save(optimized_path, 'JPEG', quality=quality, optimize=True)
            
            # Get new size
            new_size = os.path.getsize(optimized_path)
            reduction = ((original_size - new_size) / original_size) * 100
            
            print(f"Optimized {os.path.basename(image_path)}")
            print(f"  Original: {original_size // 1024}KB -> Optimized: {new_size // 1024}KB")
            print(f"  Size reduction: {reduction:.1f}%")
            
            return optimized_path
            
    except Exception as e:
        print(f"Error optimizing {image_path}: {e}")
        return None

def main():
    """Main function to optimize all images in the static directory."""
    
    # Find all image files
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(glob.glob(f"static/images/{ext}"))
    
    if not image_files:
        print("No images found in static/images/")
        return
    
    print(f"Found {len(image_files)} images to optimize...")
    
    total_original = 0
    total_optimized = 0
    
    for image_path in image_files:
        original_size = os.path.getsize(image_path)
        total_original += original_size
        
        optimized_path = optimize_image(image_path)
        if optimized_path:
            optimized_size = os.path.getsize(optimized_path)
            total_optimized += optimized_size
        
        print("-" * 50)
    
    if total_optimized > 0:
        total_reduction = ((total_original - total_optimized) / total_original) * 100
        print(f"\nTotal optimization results:")
        print(f"Original total size: {total_original // 1024}KB")
        print(f"Optimized total size: {total_optimized // 1024}KB")
        print(f"Total size reduction: {total_reduction:.1f}%")
    
    print("\nImage optimization complete!")
    print("\nTo use optimized images:")
    print("1. Review the optimized images")
    print("2. Replace original files with optimized versions if satisfied")
    print("3. Update your templates to use the optimized images")

if __name__ == "__main__":
    main()