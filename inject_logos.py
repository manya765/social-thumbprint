import os
import re

html_path = "index.html"
logos_dir = "logos"

images = [f for f in os.listdir(logos_dir) if f.startswith('logo_') and f.endswith('.png')]
images.sort()

total_images = len(images)

if total_images == 0:
    print("No images found.")
    exit()

# Distribute over 3 rows ensuring staggered pattern (odd/even/odd or even/odd/even)
base = total_images // 3
row1_count = base
row2_count = base
row3_count = base

rem = total_images % 3
if rem == 1:
    row2_count += 1
elif rem == 2:
    row1_count += 1
    row3_count += 1

row_counts = [row1_count, row2_count, row3_count]

html_content = '<div class="container hex-container">\n'

img_idx = 0
for count in row_counts:
    html_content += '    <div class="hex-row">\n'
    for _ in range(count):
        if img_idx < len(images):
            img_name = images[img_idx]
            html_content += f'      <div class="hex reveal-hex"><img src="logos/{img_name}" alt="Logo"></div>\n'
            img_idx += 1
    html_content += '    </div>\n'

html_content += '  </div>'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = re.compile(r'<div class="container hex-container">.*?</section>', re.DOTALL)
new_content = pattern.sub(html_content + '\n</section>', content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Injected {total_images} logos into {html_path} across {row_counts} hexagons.")
