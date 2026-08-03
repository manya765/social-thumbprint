import fitz
import os

pdf_path = "TST Website logo.pdf"
output_dir = "logos"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

doc = fitz.open(pdf_path)

img_count = 0
for page_num in range(len(doc)):
    page = doc[page_num]
    image_list = page.get_images(full=True)
    
    for img_index, img in enumerate(image_list):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        
        img_filename = f"image{page_num+1}_{img_index+1}.{image_ext}"
        img_filepath = os.path.join(output_dir, img_filename)
        
        with open(img_filepath, "wb") as f:
            f.write(image_bytes)
            
        print(f"Extracted {img_filename}")
        img_count += 1

print(f"Total images extracted: {img_count}")

# If no images found, maybe render the page as a single image
if img_count == 0:
    print("No embedded images found. Rendering the entire page as a PNG...")
    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap(dpi=300)
        output_file = os.path.join(output_dir, f"rendered_page_{page_num+1}.png")
        pix.save(output_file)
        print(f"Rendered {output_file}")
