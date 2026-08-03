import fitz
from PIL import Image
import os
import io

pdf_path = "TST Website logo.pdf"
output_dir = "logos"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Clear existing logos
for f in os.listdir(output_dir):
    if f.endswith('.png'):
        os.remove(os.path.join(output_dir, f))

def remove_bg_and_crop(img_path):
    img = Image.open(img_path).convert("RGBA")
    bg_color = img.getpixel((0, 0))
    
    # If transparent, skip
    if bg_color[3] == 0:
        return
        
    datas = img.getdata()
    newData = []
    
    tolerance = 25
    for item in datas:
        # Check if pixel is close to bg_color
        if (abs(item[0] - bg_color[0]) <= tolerance and
            abs(item[1] - bg_color[1]) <= tolerance and
            abs(item[2] - bg_color[2]) <= tolerance):
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
            
    img.putdata(newData)
    
    # Crop to bounding box
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
        
    img.save(img_path, "PNG")

doc = fitz.open(pdf_path)
for page_num in range(len(doc)):
    page = doc[page_num]
    mat = fitz.Matrix(4, 4) # equivalent to about 288 DPI
    pix = page.get_pixmap(matrix=mat)
    
    img_data = pix.tobytes("png")
    img = Image.open(io.BytesIO(img_data))
    
    out_filename = f"logo_{page_num+1:03d}.png"
    out_path = os.path.join(output_dir, out_filename)
    
    img.save(out_path)
    remove_bg_and_crop(out_path)
    print(f"Processed page {page_num+1}/{len(doc)}")

print("All logos processed!")
