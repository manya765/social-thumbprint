import re
import math

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the rows. Each row has exactly 9 logos so that 9 * 160 = 1440px loop width.
row1_images = [f"logos/logo_page_{str(i).zfill(2)}.png" for i in range(1, 10)]
row2_images = [f"logos/logo_page_{str(i).zfill(2)}.png" for i in range(10, 18)] + ["logos/new_logo_page_1.png"]
row3_images = [f"logos/logo_page_{str(i).zfill(2)}.png" for i in range(18, 27)]
row4_images = [f"logos/logo_page_{str(i).zfill(2)}.png" for i in range(27, 35)] + ["logos/new_logo_page_2.png"]

rows = [row1_images, row2_images, row3_images, row4_images]
loop_width = 1440
NUM_DUPLICATES = 3

new_html_rows = []
for idx, row_images in enumerate(rows):
    is_even = (idx % 2 == 1)
    margin_left = "80px" if is_even else "0px"
    
    row_html = f'      <div class="hex-row" data-loop-width="{loop_width}" style="margin-left: {margin_left};">\n'
    
    for dup in range(NUM_DUPLICATES):
        for img in row_images:
            row_html += f'        <div class="hex reveal-hex"><img src="{img}" alt="Logo"></div>\n'
    
    row_html += '      </div>'
    new_html_rows.append(row_html)

new_honeycomb_content = '<div class="hex-container" data-marquee-speed="30">\n' + '\n'.join(new_html_rows) + '\n    </div>'

# Find existing hex-container and replace
container_pattern = re.compile(r'<div class="[^"]*hex-container"[^>]*>[\s\S]*?(?=</section>)')
if container_pattern.search(content):
    content = container_pattern.sub(new_honeycomb_content + '\n  ', content)
else:
    print("Could not find hex-container to replace!")

# CSS modifications for .hex, .hex-row, .hex-container
css_target_row = re.search(r'\.hex-row\s*\{[^\}]+\}', content).group(0)
css_replace_row = '''    .hex-row {
      display: flex;
      justify-content: flex-start;
      margin-bottom: -46px;
      width: max-content;
      flex-wrap: nowrap;
      will-change: transform;
    }'''
content = content.replace(css_target_row, css_replace_row)

css_target_hex = re.search(r'\.hex\s*\{[^\}]+\}', content).group(0)
css_replace_hex = '''    .hex {
      flex: 0 0 160px;
      width: 160px;
      height: 184px;
      background: rgba(255, 255, 255, 0.15);
      clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
      margin: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      text-align: center;
      font-family: var(--font-heading);
      font-size: 0.95rem;
      font-weight: 700;
      color: var(--white);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      opacity: 0;
      transform: scale(0.3);
      transition: all 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }'''
content = content.replace(css_target_hex, css_replace_hex)

container_match = re.search(r'\.hex-container\s*\{[^\}]+\}', content)
if container_match:
    container_target = container_match.group(0)
    container_replace = '''    .hex-container {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      overflow: hidden;
      width: 100vw;
      max-width: 100vw !important;
      margin-left: calc(-50vw + 50%);
    }'''
    content = content.replace(container_target, container_replace)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Honeycomb rebuilt with 0 margin, full width, and new logos.")
