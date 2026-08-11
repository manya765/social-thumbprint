import os
import re

ordered_logos = [
    # Row 1 (9 logos)
    "logo_015.png", "logo_034.png", "logo_016.png", "logo_017.png", "logo_002.png",
    "logo_018.png", "logo_021.png", "logo_010.png", "logo_001.png",
    # Row 2 (8 logos)
    "logo_004.png", "logo_008.png", "logo_022.png", "logo_023.png", "logo_024.png",
    "logo_005.png", "logo_014.png", "logo_025.png",
    # Row 3 (9 logos)
    # logo_013 (dup of logo_015, Aarambh Interiors) -> logo_028 (unused, unique)
    # logo_004 (already placed in Row 2) -> logo_035 (unused, JVD Properties variant)
    # logo_012 (byte-identical dup of logo_033, Boutiqo) -> logo_037 (unused, unique)
    "logo_003.png", "logo_033.png", "logo_028.png", "logo_026.png", "logo_042.png",
    "logo_035.png", "logo_007.png", "logo_011.png", "logo_037.png",
    # Row 4 (8 logos)
    # logo_029 (dup of logo_031, Serenity) -> logo_009 (unused, unique)
    "logo_027.png", "logo_006.png", "logo_020.png", "logo_019.png", "logo_009.png",
    "logo_030.png", "logo_031.png", "logo_032.png"
]

# Logos that should preserve their exact background color without blend modes
# Format: "logo_filename": "rgb(R, G, B)"
preserve_bgs = {
    "logo_042.png": "rgb(255, 255, 255)",  # Inaara
    "logo_020.png": "rgb(255, 255, 255)",  # Sattva Yoga
    "logo_023.png": "rgb(13, 103, 181)",   # JVD Properties
    "logo_025.png": "rgb(214, 149, 72)"    # L2 Luxury Hospitality
}

# Generate dynamic CSS for the preserved backgrounds
dynamic_css = '<style id="dynamic-hex-styles">\n'
img_selectors = []
for logo_file, color in preserve_bgs.items():
    class_name = logo_file.replace('.png', '')
    dynamic_css += f'  .hex-{class_name} {{ background-color: {color}; }}\n'
    img_selectors.append(f'.hex-{class_name} img')

if img_selectors:
    dynamic_css += f'  {", ".join(img_selectors)} {{ mix-blend-mode: normal !important; }}\n'
dynamic_css += '</style>\n'

html = dynamic_css + '<div class="container hex-container">\n'

slots_per_row = [9, 8, 9, 8]
logo_idx = 0

for row_len in slots_per_row:
    html += '      <div class="hex-row">\n'
    for _ in range(row_len):
        if logo_idx < len(ordered_logos):
            logo_file = ordered_logos[logo_idx]
            class_name = logo_file.replace('.png', '')
            extra_class = f" hex-{class_name}" if logo_file in preserve_bgs else ""
            
            html += f'        <div class="hex reveal-hex{extra_class}"><img src="logos/{logo_file}" alt="Logo"></div>\n'
            logo_idx += 1
        else:
            html += '        <div class="hex" style="visibility: hidden;"></div>\n'
    html += '      </div>\n'
html += '    </div>\n  </section>'

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove old dynamic styles if they exist
content = re.sub(r'<style id="dynamic-hex-styles">.*?</style>\n', '', content, flags=re.DOTALL)

html_pattern = re.compile(r'<div class="container hex-container">.*?</div>\s*</section>', re.DOTALL)
content = html_pattern.sub(html, content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated index.html with preserved backgrounds for specific logos.")
