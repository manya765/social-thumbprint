from PIL import Image
import os
import glob

logos = glob.glob('logos/*.png')

for path in logos:
    try:
        img = Image.open(path)
        bbox = img.getbbox()
        if bbox:
            cropped = img.crop(bbox)
            cropped.save(path)
            print(f"Cropped {path}")
        else:
            print(f"Empty {path}")
    except Exception as e:
        print(f"Error on {path}: {e}")
