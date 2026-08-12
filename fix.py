import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Change service-list-desc color to white
content = re.sub(r'color:\s*var\(--teal-light\);', 'color: #ffffff;', content)

# 2. Duplicate hexes in hex-row
hex_rows = re.findall(r'(<div class="hex-row">)(.*?)(</div>\s*<div class="hex-row">|</div>\s*</div>\s*</section>)', content, flags=re.DOTALL)
for match in hex_rows:
    original_hexes = match[1]
    duplicated = match[0] + original_hexes + original_hexes + match[2]
    old_full = match[0] + original_hexes + match[2]
    content = content.replace(old_full, duplicated)

# 3. Update driftGrid animation to marquee for hex-row
# Find hex-container and driftGrid css
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
      to { transform: translateX(-50%); }
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
      animation-direction: reverse;
    }
    .hex-row:hover {
      animation-play-state: paused;
    }'''
content = content.replace(hex_row_target, hex_row_replace)

# 4. Duplicate testimonials
testi_track_match = re.search(r'(<div class="testimonials-track"[^>]*>)(.*?)(</div>\s*</div>\s*</section>)', content, flags=re.DOTALL)
if testi_track_match:
    original_cards = testi_track_match.group(2)
    # duplicate cards
    new_track = testi_track_match.group(1) + original_cards + original_cards + testi_track_match.group(3)
    content = content.replace(testi_track_match.group(0), new_track)

# 5. Make testimonials-track a marquee
testi_css_target = '''    .testimonials-track {
      display: flex;
      gap: 2rem;
      transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }'''
testi_css_replace = '''    @keyframes testiMarquee {
      from { transform: translateX(0); }
      to { transform: translateX(-50%); }
    }
    .testimonials-track {
      display: flex;
      gap: 2rem;
      width: max-content;
      animation: testiMarquee 40s linear infinite;
    }
    .testimonials-track:hover {
      animation-play-state: paused;
    }'''
content = content.replace(testi_css_target, testi_css_replace)

# 6. Hide arrows for testimonials
arrows_target = '''        <button class="testi-arrow testi-prev" aria-label="Previous">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M15 18l-6-6 6-6" />
          </svg>
        </button>
        <button class="testi-arrow testi-next" aria-label="Next">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 18l6-6-6-6" />
          </svg>
        </button>'''
content = content.replace(arrows_target, '')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
