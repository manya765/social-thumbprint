import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace CSS
css_pattern = re.compile(r'\.hex-row \{.*?\n    \.hex img \{.*?\}', re.DOTALL)
new_css = r'''\.hex-row {
      display: flex;
      justify-content: center;
      margin-bottom: -46px;
      width: 100%;
      flex-wrap: nowrap;
    }

    .hex {
      flex-shrink: 0;
      width: 160px;
      height: 184px;
      background: rgba(255, 255, 255, 0.15);
      clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
      margin: 0 4px;
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
    }

    .hex img {
      max-width: 90%;
      max-height: 90%;
      object-fit: contain;
      pointer-events: none;
    }'''

# Manually replacing to avoid regex dotall failing if there are slight differences
content = re.sub(r'\.hex-row\s*\{.*?\n    \.hex img\s*\{.*?\}', new_css, content, flags=re.DOTALL)

# Replace HTML
html_pattern = re.compile(r'<div class="container hex-container">.*?</div>\s*</section>', re.DOTALL)
new_html = '<div class="container hex-container">\n'
count = 1
for row_len in [12, 13, 12, 13]:
    new_html += '      <div class="hex-row">\n'
    for _ in range(row_len):
        # We extracted up to 50 logos in the previous step
        # If the pdf had 50 logos, we loop from 1 to 50
        if count <= 50:
            new_html += f'        <div class="hex reveal-hex"><img src="logos/logo_{count:03d}.png" alt="Logo"></div>\n'
        count += 1
    new_html += '      </div>\n'
new_html += '    </div>\n  </section>'

content = html_pattern.sub(new_html, content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated index.html')
