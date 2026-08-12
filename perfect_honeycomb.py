import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace the hex-container CSS
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
      to { transform: translateX(-1512px); }
    }

    .hex-marquee-container {
      overflow: hidden;
      width: 100vw;
      max-width: none !important;
      margin-left: calc(-50vw + 50%);
    }

    .hex-marquee-track {
      display: flex;
      width: max-content;
      animation: honeycombMarquee 30s linear infinite;
      will-change: transform;
    }
    .hex-marquee-track:hover {
      animation-play-state: paused;
    }

    .hex-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      overflow: visible;
      width: 1512px;
      margin: 0;
    }'''
content = content.replace(css_target, css_replace)

# 2. Find the whole `.hex-container` block and wrap/duplicate it
hex_container_pattern = re.compile(r'(<div class="container hex-container">)(.*?)(</div>\s*</section>)', re.DOTALL)
match = hex_container_pattern.search(content)

if match:
    # We change the class of the container block slightly to avoid confusion, or keep it.
    # The original is `<div class="container hex-container">`.
    # Let's remove `container` from it so it doesn't get max-width constraints by itself,
    # though it shouldn't matter since we set width: 1512px.
    # Actually, let's keep it just `hex-container`.
    single_block = '<div class="hex-container">' + match.group(2) + '</div>'
    
    # We duplicate it 6 times
    tiled_blocks = single_block * 6
    
    # Wrap it in track and container
    new_html = '<div class="hex-marquee-container"><div class="hex-marquee-track">\n' + tiled_blocks + '\n</div></div>\n</section>'
    
    old_full = match.group(0)
    content = content.replace(old_full, new_html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied flawless honeycomb marquee!")
