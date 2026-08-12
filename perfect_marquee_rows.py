import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update hex-container CSS
css_target = '''    @keyframes driftGrid {
      from {
        transform: translateX(300px);
      }

      to {
        transform: translateX(-300px);
      }
    }

    .hex-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      overflow: visible;
      width: 100vw;
      margin-left: calc(-50vw + 50%);
      /* Full bleed horizontal */
      animation: driftGrid 20s linear infinite;
      will-change: transform;
    }'''

css_replace = '''    @keyframes honeycombMarquee {
      from { transform: translateX(0); }
      to { transform: translateX(-12096px); } /* 72 hexes * 168px */
    }

    .hex-container {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      overflow: hidden;
      width: 100vw;
      max-width: none !important;
      margin-left: calc(-50vw + 50%);
    }

    .hex-track {
      display: flex;
      flex-direction: column;
      width: max-content;
    }

    .hex-track:hover .hex-row {
      animation-play-state: paused;
    }'''
content = content.replace(css_target, css_replace)

# 2. Update .hex-row CSS
hex_row_target = '''    .hex-row {
      display: flex;
      justify-content: center;
      margin-bottom: -46px;
      width: 100%;
      flex-wrap: nowrap;
    }'''

hex_row_replace = '''    .hex-row {
      display: flex;
      justify-content: flex-start;
      margin-bottom: -46px;
      width: max-content;
      flex-wrap: nowrap;
      animation: honeycombMarquee 150s linear infinite;
      will-change: transform;
    }

    .hex-row:nth-child(even) {
      margin-left: 84px;
    }'''
content = content.replace(hex_row_target, hex_row_replace)

# 3. Duplicate row inner HTML to build 144 hexes per row
# Row 1 and 3 have 9 hexes -> duplicate 16 times (16 * 9 = 144 hexes)
# Row 2 and 4 have 8 hexes -> duplicate 18 times (18 * 8 = 144 hexes)

hex_row_blocks = re.findall(r'(<div class="hex-row">)(.*?)(</div>\s*<div class="hex-row">|</div>\s*</div>\s*</section>)', content, flags=re.DOTALL)

for i, match in enumerate(hex_row_blocks):
    inner_html = match[1]
    
    if i == 0 or i == 2: # Rows 1 and 3 (9 hexes)
        new_inner = inner_html * 16
    else: # Rows 2 and 4 (8 hexes)
        new_inner = inner_html * 18
        
    old_full = match[0] + inner_html + match[2]
    new_full = match[0] + new_inner + match[2]
    content = content.replace(old_full, new_full)

# Wrap the rows in .hex-track
content = content.replace('<div class="hex-row">', '<div class="hex-track">\n      <div class="hex-row">', 1)
content = content.replace('      </div>\n    </div>\n  </section>', '      </div>\n    </div>\n    </div>\n  </section>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied perfect row-based marquee!")
