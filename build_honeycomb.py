import re
import os

slots_per_row = [9, 8, 9, 8]
total_slots = sum(slots_per_row)

logos_dir = 'logos'

HEX_PITCH_PX = 168  # 160px hex width + 4px margin on each side
MARQUEE_SPEED_PX_PER_SEC = 30  # constant scroll speed across all rows
ROW_STAGGER_PX = HEX_PITCH_PX / 2  # honeycomb brick-offset between rows

html = f'<div class="container hex-container" data-marquee-speed="{MARQUEE_SPEED_PX_PER_SEC}">\n'
logo_idx = 1

max_row_len = max(slots_per_row)

for row_num, row_len in enumerate(slots_per_row):
    row_logos = []
    for _ in range(row_len):
        logo_file = f"logo_page_{logo_idx:02d}.png"
        logo_path = os.path.join(logos_dir, logo_file)
        row_logos.append(logo_file if os.path.exists(logo_path) else None)
        logo_idx += 1

    # Pad every row to the same slot count (max_row_len) with invisible
    # filler hexes so every row's one-copy loop width - and therefore its
    # animation duration - is identical. Rows with different loop lengths
    # would drift out of sync over time (they'd each wrap at a different
    # moment), breaking the honeycomb's brick-offset alignment between
    # rows. Keeping loop widths equal keeps every row's relative stagger
    # constant forever, not just at t=0.
    padded_logos = row_logos + [None] * (max_row_len - len(row_logos))

    one_copy_width = max_row_len * HEX_PITCH_PX
    stagger = ROW_STAGGER_PX if row_num % 2 == 1 else 0

    # data-loop-width drives a single shared requestAnimationFrame loop (see
    # the script near the end of the file) that positions every row from one
    # common timestamp, instead of independent CSS animations - CSS
    # animations on separate elements aren't guaranteed to start on the same
    # frame, which caused a few px of drift between rows even with identical
    # duration/loop-width.
    row_style = f"margin-left: {stagger}px;"
    html += f'      <div class="hex-row" data-loop-width="{one_copy_width}" style="{row_style}">\n'
    for logo_file in padded_logos * 2:
        if logo_file:
            html += f'        <div class="hex reveal-hex"><img src="logos/{logo_file}" alt="Logo"></div>\n'
        else:
            html += '        <div class="hex reveal-hex" style="visibility: hidden;"></div>\n'
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

print(f"Updated index.html: {total_slots} logos across {len(slots_per_row)} rows, each row duplicated for a seamless marquee loop.")
