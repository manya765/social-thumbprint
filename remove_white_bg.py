import os
from PIL import Image

output_dir = "logos"

preserve_bgs = [
    "logo_042.png",  # Inaara
    "logo_020.png",  # Sattva Yoga
    "logo_023.png",  # JVD Properties
    "logo_025.png"   # L2 Luxury Hospitality
]

for filename in os.listdir(output_dir):
    if filename.startswith('logo_') and filename.endswith('.png'):
        if filename in preserve_bgs:
            continue
            
        img_path = os.path.join(output_dir, filename)
        img = Image.open(img_path).convert("RGBA")
        datas = img.getdata()
        
        newData = []
        tolerance = 25
        # We assume white background for these
        bg_color = (255, 255, 255)
        
        # Check the top-left pixel to see if it's white. If it's not white, 
        # it might have a colored background (e.g. black). 
        # But wait, Boutiqo is black! If we remove white, Boutiqo's black background stays!
        # If we want to remove black background from Boutiqo too, we should use its edge color.
        edge_color = img.getpixel((0,0))
        
        for item in datas:
            # If the pixel matches the edge color, make it transparent
            if (abs(item[0] - edge_color[0]) <= tolerance and
                abs(item[1] - edge_color[1]) <= tolerance and
                abs(item[2] - edge_color[2]) <= tolerance):
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
                
        img.putdata(newData)
        img.save(img_path, "PNG")
        print(f"Processed {filename} (Removed {edge_color} background)")

print("Backgrounds removed!")
