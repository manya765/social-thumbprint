import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update driftGrid animation to hexMarquee in CSS
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

css_replace = '''    @keyframes hexMarquee {
      from { transform: translateX(0); }
      to { transform: translateX(-1512px); }
    }

    .hex-container {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      overflow: hidden;
      width: 100vw;
      margin-left: calc(-50vw + 50%);
      will-change: transform;
    }'''
content = content.replace(css_target, css_replace)

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
      animation: hexMarquee 25s linear infinite;
    }
    
    .hex-row:nth-child(even) {
      margin-left: 84px;
    }
    
    .hex-row:hover {
      animation-play-state: paused;
    }'''
content = content.replace(hex_row_target, hex_row_replace)

# 2. Duplicate the contents of `.hex-row` 5 times (total 6 copies) to make it super wide
hex_row_blocks = re.findall(r'(<div class="hex-row">)(.*?)(</div>\s*<div class="hex-row">|</div>\s*</div>\s*</section>)', content, flags=re.DOTALL)
for match in hex_row_blocks:
    inner_html = match[1]
    # Repeat the inner_html 5 more times
    new_inner_html = inner_html * 6
    old_full = match[0] + inner_html + match[2]
    new_full = match[0] + new_inner_html + match[2]
    content = content.replace(old_full, new_full)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied perfect hex marquee!")
