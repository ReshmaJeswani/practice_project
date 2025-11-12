import rasterio
import numpy as np
import json
import sys

def load_image_with_four_bands(filepath):
    """
    Loads an image with four bands (Red, Green, Blue, NIR) using rasterio.
    Returns a dictionary with band arrays. 
    """
    with rasterio.open(filepath) as src:
        red = src.read(1)
        green = src.read(2)
        blue = src.read(3)
        nir = src.read(4)
    return {'red': red, 'green': green, 'blue': blue, 'nir': nir}

def calculate_ndvi(red, nir):
    """
    Calculates NDVI index from Red and NIR bands.
    NDVI = (NIR - Red) / (NIR + Red)
    """
    np.seterr(divide='ignore', invalid='ignore')
    ndvi = (nir.astype(float) - red.astype(float)) / (nir + red)
    return ndvi

def main(json_path):
    # Load input JSON
    with open(json_path, 'r') as f:
        config = json.load(f)
    image_path = config.get('input_file')
    if not image_path:
        print("Error: 'input_file' not found in JSON.")
        return

    bands = load_image_with_four_bands(image_path)
    ndvi = calculate_ndvi(bands['red'], bands['nir'])
    print("NDVI calculated. Shape:", ndvi.shape)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ndvi.py <input_json>")
    else:
        main(sys.argv[1])