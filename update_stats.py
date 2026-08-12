import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Increase bento-grid size
content = re.sub(r'(\.bento-grid\s*\{[^}]*?max-width:\s*)1400px', r'\g<1>1800px', content)

# Change .bento-card width to give it more space
content = re.sub(r'(\.bento-card\s*\{[^}]*?width:\s*calc\()20%', r'\g<1>22%', content)

new_stats = '''
        <div class="stat">
          <h3 data-target="100" data-prefix="" data-suffix="+">0+</h3>
          <p>Clients Served</p>
        </div>
        <div class="stat">
          <h3 data-target="30" data-prefix="" data-suffix="k+">0k+</h3>
          <p>Hours of Making Content</p>
        </div>
        <div class="stat">
          <h3 data-target="1000" data-prefix="" data-suffix="+">0+</h3>
          <p>Days of Content Calendars</p>
        </div>
        <div class="stat">
          <h3 data-target="120" data-prefix="" data-suffix="+">0+</h3>
          <p>Campaigns Produced</p>
        </div>
'''

content = re.sub(r'<div class="stats-float" id="statsFloat">[\s\S]*?</div>\s*</div>\s*</section>', f'<div class="stats-float" id="statsFloat">{new_stats}      </div>\n    </div>\n  </section>', content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated stats and bento-grid size successfully.")
