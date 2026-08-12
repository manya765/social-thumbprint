import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update both marquee animations from -50% to -25%
content = content.replace("to { transform: translateX(-50%); }", "to { transform: translateX(-25%); }")

# 2. Duplicate the contents of `.hex-row` again to make 4 copies total.
# To safely get the inner content of each hex-row:
# We know the inner content consists of <div class="hex reveal-hex">...</div> elements.
# Let's find all hex-rows
hex_row_blocks = re.findall(r'(<div class="hex-row">)(.*?)(</div>\s*<div class="hex-row">|</div>\s*</div>\s*</section>)', content, flags=re.DOTALL)
for match in hex_row_blocks:
    inner_html = match[1]
    # Currently inner_html contains 2 copies of the logos. We want 4 copies.
    # So we just duplicate inner_html once.
    new_inner_html = inner_html + inner_html
    old_full = match[0] + inner_html + match[2]
    new_full = match[0] + new_inner_html + match[2]
    content = content.replace(old_full, new_full)

# 3. Duplicate the contents of `.testimonials-track` again to make 4 copies total.
testi_track_match = re.search(r'(<div class="testimonials-track"[^>]*>)(.*?)(</div>\s*</div>\s*</section>)', content, flags=re.DOTALL)
if testi_track_match:
    inner_html = testi_track_match.group(2)
    new_inner_html = inner_html + inner_html
    old_full = testi_track_match.group(0)
    new_full = testi_track_match.group(1) + new_inner_html + testi_track_match.group(3)
    content = content.replace(old_full, new_full)

# 4. Remove inline overflow and scroll-snap from .testimonials-track
content = content.replace(
    'style="display: flex; gap: 2rem; overflow-x: auto; padding: 4rem 5vw 6rem; scroll-snap-type: x mandatory; scrollbar-width: none; -ms-overflow-style: none; align-items: center;"',
    'style="display: flex; gap: 2rem; padding: 4rem 5vw 6rem; align-items: center;"'
)

# Also ensure .testimonials-track-container has overflow: hidden
content = content.replace(
    'style="width: 100vw; position: relative; left: 50%; right: 50%; margin-left: -50vw; margin-right: -50vw;"',
    'style="width: 100vw; position: relative; left: 50%; right: 50%; margin-left: -50vw; margin-right: -50vw; overflow: hidden;"'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed marquee gaps!")
