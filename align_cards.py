import os
import glob
import re

def align_cards():
    base_dir = r"d:\social thumbrint"
    videos_dir = os.path.join(base_dir, "videos")
    
    mp4_files = glob.glob(os.path.join(videos_dir, "*.mp4"))
    
    import re as regex
    def natural_keys(text):
        return [ int(c) if c.isdigit() else c for c in regex.split(r'(\d+)', text) ]
    
    mp4_files.sort(key=natural_keys)
    
    # Generate descriptions based on filenames
    def get_description(filename):
        lower_name = filename.lower()
        if "adorne" in lower_name:
            return "Showcasing the elegance and timeless beauty of the exclusive jewellery collection."
        elif "arctic star" in lower_name:
            return "A dynamic and refreshing visual campaign crafted for Arctic Star."
        elif "baggit" in lower_name:
            return "Highlighting modern fashion and durable aesthetics for Baggit's latest line."
        elif "baulkline" in lower_name:
            return "A bold and premium brand identity presentation for Baulkline."
        elif "kira" in lower_name:
            return "High-energy, fast-paced commercial production for Kira's television campaign."
        elif "luzo" in lower_name:
            if "hair" in lower_name:
                return "Vibrant and stylish hair color transformations for Luzo."
            elif "app" in lower_name:
                return "Sleek and intuitive app walkthrough highlighting Luzo's digital experience."
            else:
                return "Engaging influencer-driven content crafted for Luzo's social platforms."
        elif "meena bazaar" in lower_name:
            if "saree" in lower_name:
                return "An elegant display of traditional and modern sarees by Meena Bazaar."
            elif "ad" in lower_name:
                return "A cinematic advertisement campaign highlighting Meena Bazaar's heritage."
            else:
                return "Curated influencer collaborations showcasing Meena Bazaar's ethnic wear."
        elif "riwaaj" in lower_name:
            return "Capturing the essence of tradition and modern grace in the Riwaaj collection."
        elif "cappacino" in lower_name:
            return "A sophisticated and warm lifestyle campaign for The Cappacino Collection."
        elif "velvet" in lower_name:
            return "A luxurious and dreamy aesthetic experience crafted for Velvet Reverie."
        else:
            return "Engaging and high-quality visual content production."

    def format_title(filename):
        title = filename.replace(".mp4", "")
        # Remove numbers like " 2" or "final2" for a cleaner look if we want, but let's just capitalize
        return title.title()

    cuberto_css = """
  <!-- CUBERTO STAGGERED STYLES -->
  <style>
    /* Remove card background and shadow, make transparent */
    .work-card {
        background: transparent !important;
        box-shadow: none !important;
        backdrop-filter: none !important;
        -webkit-backdrop-filter: none !important;
        border-radius: 0 !important;
        padding: 0 !important;
        overflow: visible !important;
        display: block;
        text-decoration: none;
    }
    
    /* 2-Column Staggered Grid like Cuberto */
    .work-grid {
        display: grid !important;
        grid-template-columns: 1fr 1fr !important;
        gap: 6rem 4rem !important;
        align-items: start;
    }
    
    @media (min-width: 992px) {
        .work-card:nth-child(even) {
            margin-top: 12rem !important; /* The massive stagger effect */
        }
    }
    @media (max-width: 991px) {
        .work-grid {
            grid-template-columns: 1fr !important; /* Stack on mobile */
            gap: 4rem !important;
        }
        .work-card:nth-child(even) {
            margin-top: 0 !important;
        }
    }

    /* The media container */
    .work-img {
        border-radius: 24px !important; 
        overflow: hidden !important;
        transform: translateZ(0); /* Force GPU */
        position: relative;
        padding-bottom: 125% !important; /* Very tall Cuberto portrait format */
        background: #111 !important;
        margin-bottom: 2rem;
    }

    /* The video scales on hover */
    .work-img video {
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        object-fit: cover;
        transform: scale(1);
        transition: transform 1.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    .work-card:hover .work-img video {
        transform: scale(1.08); /* Smooth scale */
    }

    .work-overlay {
        display: none !important;
    }

    /* Typography Beneath (Descriptive Text) */
    .work-info {
        padding: 0 1rem !important;
        display: flex;
        flex-direction: column !important;
        align-items: flex-start !important;
        justify-content: flex-start !important;
    }
    .work-info h4 {
        font-size: 2rem !important;
        color: var(--white) !important;
        font-family: var(--font-body) !important;
        font-weight: 500 !important;
        letter-spacing: -0.02em !important;
        margin: 0 0 1rem 0 !important;
        line-height: 1.2;
    }
    .work-info p {
        font-size: 1.2rem !important;
        color: rgba(255,255,255,0.7) !important;
        font-weight: 400 !important;
        margin: 0 !important;
        line-height: 1.6;
        max-width: 90%;
    }

    /* Custom Cursor Morphing to "PLAY" */
    .cursor-fingerprint {
        transition: transform 0.3s ease, width 0.3s ease, height 0.3s ease, background 0.3s ease, border-radius 0.3s ease;
    }
    .cursor-fingerprint.view-mode {
        width: 100px; height: 100px;
        transform: translate(-50%, -50%) !important;
        background: rgba(0, 176, 185, 0.8) !important; /* Teal play button */
        border: none !important;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        opacity: 1 !important;
    }
    .cursor-fingerprint.view-mode svg {
        display: none; 
    }
    .cursor-fingerprint.view-mode::after {
        content: 'PLAY';
        color: var(--white);
        font-size: 15px;
        font-weight: 700;
        letter-spacing: 2px;
    }
  </style>
  <script>
    window.addEventListener('DOMContentLoaded', () => {
        const cursor = document.getElementById('customCursor');
        if(!cursor) return;
        
        setTimeout(() => {
            document.querySelectorAll('.brand-card').forEach(card => {
                card.addEventListener('mouseenter', () => cursor.classList.add('view-mode'));
                card.addEventListener('mouseleave', () => cursor.classList.remove('view-mode'));
            });
        }, 1000);
    });
  </script>
"""

    def generate_card_html(filename):
        desc = get_description(filename)
        title = format_title(filename)
        
        # We will make the cards just trigger the modal with ONLY their specific video
        # since we are displaying all 23 individually.
        videos_json = f"['{filename}']"
        
        # Adding 'brand-card' class so the modal and cursor logic picks it up
        return f"""
        <div class="work-card reveal-heading in-view brand-card" data-brand="{title}" data-videos="{videos_json}" style="cursor: pointer;">
          <div class="work-img">
             <video src="videos/{filename}" muted loop playsinline onmouseover="this.play()" onmouseout="this.pause()"></video>
          </div>
          <div class="work-info">
            <p>{desc}</p>
          </div>
        </div>
"""

    # 1. Update portfolio.html (all 23 videos)
    portfolio_path = os.path.join(base_dir, "portfolio.html")
    with open(portfolio_path, "r", encoding="utf-8") as f:
        content = f.read()

    all_cards = ""
    for video in mp4_files:
        all_cards += generate_card_html(os.path.basename(video))

    # Replace grid
    pattern = r'(<div class="work-grid" style="grid-template-columns: repeat\(auto-fit, minmax\(320px, 1fr\)\); gap: 2rem;">).*?(</section>)'
    
    # We might have injected cuberto css before, so the pattern might be just <div class="work-grid">
    if '<div class="work-grid" style=' in content:
        new_grid = f'\\1\n{all_cards}\n      </div>\n    </div>\n  \\2'
        content = re.sub(pattern, new_grid, content, flags=re.DOTALL)
    else:
        # It was already modified by cuberto_style.py, so we look for <div class="work-grid">
        pattern = r'(<div class="work-grid">).*?(</section>)'
        new_grid = f'\\1\n{all_cards}\n      </div>\n    </div>\n  \\2'
        content = re.sub(pattern, new_grid, content, flags=re.DOTALL)
        
    # Replace old cuberto styles if they exist
    if '<!-- CUBERTO STYLES -->' in content:
        content = re.sub(r'<!-- CUBERTO STYLES -->.*?</script>', cuberto_css, content, flags=re.DOTALL)
    elif '<!-- CUBERTO STAGGERED STYLES -->' in content:
        content = re.sub(r'<!-- CUBERTO STAGGERED STYLES -->.*?</script>', cuberto_css, content, flags=re.DOTALL)
    else:
        content = content.replace('</head>', cuberto_css + '\n</head>')

    with open(portfolio_path, "w", encoding="utf-8") as f:
        f.write(content)

    # 2. Update index.html (Maybe just show 4 featured videos to keep staggered grid looking good)
    index_path = os.path.join(base_dir, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        idx_content = f.read()

    # Pick 4 specific videos for the homepage
    featured_files = [
        "Meena Bazaar ad video.mp4", 
        "kira new TV video final2.mp4", 
        "Luzo hair color video.mp4", 
        "Baulkline video.mp4"
    ]
    featured_cards = ""
    for v in featured_files:
        # Check if they exist in mp4_files
        if any(v == os.path.basename(f) for f in mp4_files):
            featured_cards += generate_card_html(v)

    idx_pattern = r'(<div class="work-grid">).*?(</section>)'
    idx_new_grid = f'\\1\n{featured_cards}\n      </div>\n    </div>\n  \\2'
    idx_content = re.sub(idx_pattern, idx_new_grid, idx_content, flags=re.DOTALL)

    if '<!-- CUBERTO STYLES -->' in idx_content:
        idx_content = re.sub(r'<!-- CUBERTO STYLES -->.*?</script>', cuberto_css, idx_content, flags=re.DOTALL)
    elif '<!-- CUBERTO STAGGERED STYLES -->' in idx_content:
        idx_content = re.sub(r'<!-- CUBERTO STAGGERED STYLES -->.*?</script>', cuberto_css, idx_content, flags=re.DOTALL)
    else:
        idx_content = idx_content.replace('</head>', cuberto_css + '\n</head>')

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(idx_content)

    print("Staggered layout and descriptions applied successfully.")

if __name__ == "__main__":
    align_cards()
