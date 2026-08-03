from PIL import Image
import os

input_dir = 'logos'
output_dir = 'logos'

def remove_bg(img_path, out_path):
    img = Image.open(img_path).convert("RGBA")
    
    # Get the background color from the top-left pixel
    bg_color = img.getpixel((0, 0))
    
    # If the image is completely transparent already, skip
    if bg_color[3] == 0:
        if img_path != out_path:
            img.save(out_path, "PNG")
        return

    datas = img.getdata()
    newData = []
    
    tolerance = 15
    for item in datas:
        # Check if pixel is close to bg_color
        if (abs(item[0] - bg_color[0]) <= tolerance and
            abs(item[1] - bg_color[1]) <= tolerance and
            abs(item[2] - bg_color[2]) <= tolerance):
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(out_path, "PNG")

for filename in os.listdir(input_dir):
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        input_path = os.path.join(input_dir, filename)
        name, ext = os.path.splitext(filename)
        output_filename = name + ".png"
        output_path = os.path.join(output_dir, output_filename)
        
        try:
            remove_bg(input_path, output_path)
            print(f"Processed {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

print("Background removal complete.")
