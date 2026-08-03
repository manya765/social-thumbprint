import os
from rembg import remove

input_dir = 'logos'
output_dir = 'logos'

for filename in os.listdir(input_dir):
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        input_path = os.path.join(input_dir, filename)
        
        try:
            with open(input_path, 'rb') as i:
                input_bytes = i.read()
            
            output_bytes = remove(input_bytes)
            
            # Save as PNG
            name, ext = os.path.splitext(filename)
            output_filename = name + ".png"
            output_path = os.path.join(output_dir, output_filename)
            
            with open(output_path, 'wb') as o:
                o.write(output_bytes)
                
            print(f"Removed background: {filename} -> {output_filename}")
        except Exception as e:
            print(f"Failed to process {filename}: {e}")

print("Background removal complete.")
